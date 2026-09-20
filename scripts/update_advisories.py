#!/usr/bin/env python3
"""Regenerate the advisory table on the profile README.

Source of truth is the public GitHub Advisory Database. The REST /advisories
endpoint has no credit filter, so the credited set is read from the advisories
search page and each ID is then resolved through the API for structured fields.
"""

import os
import re
from datetime import datetime, timezone
import sys
import time
import urllib.parse

import requests

USER = os.environ.get("ADVISORY_CREDIT_USER", "sfwani")
README = os.environ.get("README_PATH", "index.md")
API = "https://api.github.com"
UA = "sfwani-profile-updater"

# These two come from private research notes rather than the API, so they are
# maintained by hand. Everything else on the page is derived from public data.
REPORTS_FILED = 167
PROJECTS_AUDITED = 59

SEVERITY_RANK = {"critical": 0, "high": 1, "medium": 2, "low": 3}
SEVERITY_COLOR = {"critical": "8b1a1a", "high": "cf222e", "medium": "d4a72c", "low": "2da44e"}

# Short, readable labels for the CWEs that actually show up in this work.
CWE_LABELS = {
    "CWE-22": "Path traversal",
    "CWE-78": "Command injection",
    "CWE-79": "Cross site scripting",
    "CWE-94": "Code injection",
    "CWE-200": "Information disclosure",
    "CWE-269": "Privilege escalation",
    "CWE-284": "Access control",
    "CWE-287": "Authentication bypass",
    "CWE-306": "Missing authentication",
    "CWE-352": "Cross site request forgery",
    "CWE-362": "Race condition",
    "CWE-434": "Unrestricted upload",
    "CWE-502": "Unsafe deserialization",
    "CWE-639": "Insecure direct object reference",
    "CWE-862": "Missing authorization",
    "CWE-863": "Incorrect authorization",
    "CWE-653": "Improper isolation",
    "CWE-918": "Server side request forgery",
    "CWE-1333": "Regex denial of service",
}


def session():
    s = requests.Session()
    s.headers.update({"User-Agent": UA, "Accept": "application/vnd.github+json"})
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        s.headers["Authorization"] = f"Bearer {token}"
    return s


def credited_ghsa_ids(s):
    """Scrape the advisory search page for every GHSA credited to USER."""
    found, page = [], 1
    while page <= 10:
        url = "https://github.com/advisories"
        r = s.get(url, params={"query": f"credit:{USER}", "page": page}, timeout=30)
        r.raise_for_status()
        ids = re.findall(r"GHSA-[23456789cfghjmpqrvwx]{4}-[23456789cfghjmpqrvwx]{4}-[23456789cfghjmpqrvwx]{4}", r.text)
        fresh = [i for i in dict.fromkeys(ids) if i not in found]
        if not fresh:
            break
        found.extend(fresh)
        page += 1
        time.sleep(1)
    return found


def extra_repo_advisories():
    """Repository level advisories that are published and credited but never
    forwarded to the global database, so the credit search cannot see them.

    Format: one "owner/repo GHSA-id" per line, blank lines and # comments ignored.
    """
    path = os.environ.get("EXTRA_ADVISORIES", "advisories.txt")
    if not os.path.exists(path):
        return []
    out = []
    for line in open(path, encoding="utf-8"):
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) == 2:
            out.append((parts[0], parts[1]))
    return out


def resolve_repo_level(s, repo, ghsa_id):
    """Only returns an advisory that is published and where USER credit is accepted."""
    r = s.get(f"{API}/repos/{repo}/security-advisories/{ghsa_id}", timeout=30)
    if r.status_code != 200:
        print(f"skip {ghsa_id}: HTTP {r.status_code}", file=sys.stderr)
        return None
    a = r.json()
    if a.get("state") != "published" or a.get("withdrawn_at"):
        print(f"skip {ghsa_id}: state={a.get('state')}", file=sys.stderr)
        return None
    accepted = any(
        (c.get("user") or {}).get("login") == USER and c.get("state") == "accepted"
        for c in a.get("credits_detailed") or []
    )
    if not accepted:
        print(f"skip {ghsa_id}: credit not accepted", file=sys.stderr)
        return None
    packages = sorted({v["package"]["name"] for v in a.get("vulnerabilities") or [] if v.get("package")})
    cwes = [c["cwe_id"] for c in a.get("cwes") or []]
    score, vector, self_assessed = cvss_of(a)
    return {
        "ghsa_id": a["ghsa_id"],
        "cve_id": a.get("cve_id"),
        "score": score,
        "vector": vector,
        "self_assessed": self_assessed,
        "severity": (a.get("severity") or "").capitalize(),
        "package": packages[0] if packages else repo.split("/")[-1],
        "cwe": cwes[0] if cwes else None,
        "url": f"/advisories/{(a.get('cve_id') or a['ghsa_id']).lower()}/",
        "published": (a.get("published_at") or "")[:10],
        "summary": (a.get("summary") or "").strip(),
    }


def resolve(s, ghsa_id):
    r = s.get(f"{API}/advisories/{ghsa_id}", timeout=30)
    if r.status_code != 200:
        print(f"skip {ghsa_id}: HTTP {r.status_code}", file=sys.stderr)
        return None
    a = r.json()
    if a.get("withdrawn_at"):
        return None
    packages = sorted({v["package"]["name"] for v in a.get("vulnerabilities") or [] if v.get("package")})
    cwes = [c["cwe_id"] for c in a.get("cwes") or []]
    score, vector, self_assessed = cvss_of(a)
    return {
        "ghsa_id": a["ghsa_id"],
        "cve_id": a.get("cve_id"),
        "score": score,
        "vector": vector,
        "self_assessed": self_assessed,
        "severity": (a.get("severity") or "").capitalize(),
        "package": packages[0] if packages else "n/a",
        "cwe": cwes[0] if cwes else None,
        "url": f"/advisories/{(a.get('cve_id') or a['ghsa_id']).lower()}/",
        "published": (a.get("published_at") or "")[:10],
        "summary": (a.get("summary") or "").strip(),
    }


def short_package(name):
    """Trim ecosystem qualifiers so the table stays readable.

    Scoped npm names such as @budibase/server keep their scope, since the scope
    is the project. Go module paths and Maven coordinates lose their prefix.
    """
    if name.startswith("@"):
        return name
    for sep in ("/", ":"):
        if sep in name:
            name = name.rsplit(sep, 1)[-1]
    return name


def label(cwe):
    if not cwe:
        return "Other"
    return CWE_LABELS.get(cwe, cwe)


def render_counters(rows):
    """The five figures, in the design's own markup.

    Projects are counted as distinct projects, not packages: budibase and
    @budibase/server are one project with two package names, and the previous
    label said seven where the honest number is six.
    """
    n = len(rows)
    cves = len({r["cve_id"] for r in rows if r["cve_id"]})
    projects = len({project_of(r["package"]) for r in rows})
    figs = [
        (cves, "CVEs assigned"),
        (n, "Advisories published"),
        (projects, "Projects credited"),
        (REPORTS_FILED, "Reports filed"),
        (PROJECTS_AUDITED, "Projects audited"),
    ]
    items = "".join(
        f'\n        <li class="fig"><b>{v}</b><span>{k}</span></li>' for v, k in figs)
    return f'      <ul class="figs">{items}\n      </ul>'


def render_table(rows):
    """The home page record: identifier, project, score, severity, weakness,
    date. The eight base-vector columns stay on /advisories/, so the landing
    page answers "is this real" without becoming the reference itself.
    """
    import html as _h
    e = lambda x: _h.escape(str(x), quote=True)
    body = []
    for i, r in enumerate(rows, 1):
        sev = band(r["score"]) if r["score"] is not None else r["severity"]
        ident = r["cve_id"] or r["ghsa_id"]
        body.append(
            f'<tr role="row">'
            f'<th role="rowheader" scope="row" class="c-nr">{i:02d}</th>'
            f'<td role="cell" class="c-id"><a href="{e(r["url"])}">{e(ident)}</a></td>'
            f'<td role="cell" class="c-pkg">{_pkg(r["package"])}</td>'
            f'<td role="cell" class="c-sc">{r["score"]:.1f}</td>'
            f'<td role="cell" class="c-sev sev-{SEV_CLASS[sev]}">{sev}</td>'
            f'<td role="cell" class="c-cls">{e(label(r["cwe"]))}</td>'
            f'<td role="cell" class="c-pub">{r["published"]}</td>'
            f'</tr>')
    head = ('<thead role="rowgroup"><tr role="row">'
            '<th role="columnheader" scope="col" class="c-nr">NR</th>'
            '<th role="columnheader" scope="col" class="c-id">Advisory</th>'
            '<th role="columnheader" scope="col" class="c-pkg">Project</th>'
            '<th role="columnheader" scope="col" class="c-sc">CVSS</th>'
            '<th role="columnheader" scope="col" class="c-sev">Severity</th>'
            '<th role="columnheader" scope="col" class="c-cls">Weakness</th>'
            '<th role="columnheader" scope="col" class="c-pub">Published</th>'
            '</tr></thead>')
    return ('      <div class="tablewrap tablewrap--compact" role="region" '
            'aria-label="Published advisories" tabindex="0">\n'
            '        <table role="table" class="rec rec--compact">\n'
            f'          {head}\n'
            f'          <tbody role="rowgroup">{"".join(body)}</tbody>\n'
            '        </table>\n      </div>')




# The coordinating database published this advisory with a severity and no
# CVSS score or vector, so nothing upstream can supply one. It is scored here.
#
# The number is NOT a fresh reading of the finding. It was submitted at 10.0
# (ghsa_tracker.jsonl: cvss 10.0, cvss_source recorded-at-submission) and the
# maintainer published it as High, which is 7.0-8.9: the party with authority
# saw that 10.0 and declined Critical. 8.1 is the most severe vector still
# inside the band they assigned, granting AC:H for the precondition that the
# operator kept the shipped .env.example secrets, and S:U for scoring the
# webapp rather than the infrastructure pivot. It is also the exact vector
# GitHub itself assigned to CVE-2026-45675.
SELF_ASSESSED = {
    "GHSA-pqxw-g93w-hj9x": {
        "score": 8.1,
        "vector": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H",
    },
}

METRIC_ORDER = ["AV", "AC", "PR", "UI", "S", "C", "I", "A"]


def cvss_of(a):
    """Return (score, vector, self_assessed) for one advisory payload."""
    cvss = a.get("cvss") or {}
    score, vector = cvss.get("score"), cvss.get("vector_string")
    if not vector:
        v3 = (a.get("cvss_severities") or {}).get("cvss_v3") or {}
        score, vector = score if score is not None else v3.get("score"), v3.get("vector_string")
    if isinstance(score, (int, float)) and vector:
        return float(score), vector, False
    sa = SELF_ASSESSED.get(a.get("ghsa_id"))
    if sa:
        return sa["score"], sa["vector"], True
    return (float(score) if isinstance(score, (int, float)) else None), vector, False



def project_of(package):
    """Distinct project behind a package name.

    budibase and @budibase/server are one project; io.kestra:kestra is kestra;
    github.com/hatchet-dev/hatchet is hatchet.
    """
    p = package.strip()
    if p.startswith("@"):
        p = p[1:].split("/")[0]
    if "/" in p:
        p = p.rstrip("/").split("/")[-1]
    if ":" in p:
        p = p.split(":")[-1]
    return p.lower()


SEV_CLASS = {"Critical": "crit", "High": "high", "Medium": "med", "Low": "low"}
SITE_ORIGIN = "https://sfwani.github.io"


def band(score):
    return "Critical" if score >= 9 else "High" if score >= 7 else "Medium" if score >= 4 else "Low"


def _pkg(name):
    """Long slash-separated package paths get break opportunities.

    <wbr> only, never a hyphen entity: <wbr> inserts nothing into a copied
    string, so the package name still pastes as clean ASCII.
    """
    import html as _h
    esc = _h.escape(str(name), quote=True)
    return esc.replace("/", "/<wbr>") if name.count("/") > 1 else esc


def advisory_row(n, r, absolute=False):
    """One row of the record, in the markup the design uses.

    Verified byte-identical against the hand-built page for 10 of 11 rows;
    the eleventh differs only by the corrected score above.
    """
    import html as _h
    e = lambda x: _h.escape(str(x), quote=True)
    parts = dict(kv.split(":", 1) for kv in (r["vector"] or "").split("/")[1:] if ":" in kv)
    sev = band(r["score"]) if r["score"] is not None else r["severity"]
    ident = r["cve_id"] or r["ghsa_id"]
    href = (SITE_ORIGIN if absolute else "") + r["url"]
    v = lambda k: f'<td role="cell" class="v" data-m="{k}">{parts[k]}</td>'
    return (
        f'<tr role="row">\n'
        f'              <th role="rowheader" scope="row" class="c-nr">{n:02d}</th>\n'
        f'              <td role="cell" class="c-id"><a href="{href}">{e(ident)}</a></td>\n'
        f'              <td role="cell" class="c-pkg">{_pkg(r["package"])}</td>\n'
        f'              <td role="cell" class="c-sc">{r["score"]:.1f}</td>\n'
        f'              <td role="cell" class="c-sev sev-{SEV_CLASS[sev]}">{sev}</td>\n'
        f'              <td role="cell" class="c-cls">{e(label(r["cwe"]))}</td>\n'
        f'              <td role="cell" class="c-cwe">{(r["cwe"] or "").replace("CWE-", "")}</td>\n'
        f'              {v("AV")}{v("AC")}{v("PR")}{v("UI")}\n'
        f'              {v("S")}{v("C")}{v("I")}{v("A")}\n'
        f'              <td role="cell" class="c-pub">{r["published"]}</td>\n'
        f'            </tr>')

AUTH_CWES = {"CWE-306", "CWE-862", "CWE-863"}


def render_record(rows):
    """The full record for /advisories/: every base vector, metric by metric.

    Below 1120px each row becomes a block with the eight metrics as a 4x2
    grid, which is the whole reason this design was chosen: the vector stays
    readable on a phone with no horizontal gesture.
    """
    first = min(r["published"] for r in rows if r["published"])
    last = max(r["published"] for r in rows if r["published"])
    vh = "".join(
        f'\n              <th role="columnheader" scope="col" class="v" title="{t}">{m}</th>'
        for m, t in zip(METRIC_ORDER,
                        ["Attack vector", "Attack complexity", "Privileges required",
                         "User interaction", "Scope", "Confidentiality", "Integrity",
                         "Availability"]))
    body = "\n            ".join(advisory_row(i, r) for i, r in enumerate(rows, 1))
    return f"""      <div class="tablewrap" role="region" aria-label="Published advisories, full table" tabindex="0">
        <table role="table">
          <caption>Published advisories, {first} to {last}</caption>
          <thead role="rowgroup">
            <tr role="row">
              <th role="columnheader" scope="col" rowspan="2" class="c-nr">NR</th>
              <th role="columnheader" scope="col" rowspan="2" class="c-id">Advisory</th>
              <th role="columnheader" scope="col" rowspan="2" class="c-pkg">Package</th>
              <th role="columnheader" scope="col" rowspan="2" class="c-sc">CVSS</th>
              <th role="columnheader" scope="col" rowspan="2" class="c-sev">Severity</th>
              <th role="columnheader" scope="col" rowspan="2" class="c-cls">Weakness</th>
              <th role="columnheader" scope="col" rowspan="2" class="c-cwe">CWE</th>
              <th role="columnheader" scope="colgroup" colspan="8" class="vgroup">Base vector</th>
              <th role="columnheader" scope="col" rowspan="2" class="c-pub">Published</th>
            </tr>
            <tr role="row">{vh}
            </tr>
          </thead>
          <tbody role="rowgroup">
            {body}
          </tbody>
        </table>
      </div>"""


def render_chart(rows):
    """Every published CVSS vector as an eight cell glyph.

    Set as plain elements rather than as an SVG on purpose: the old bar chart
    used a fixed 640 viewBox scaled to 100% width, so at 390px its 12px type
    rendered around 6.5px. This reflows instead. Regenerated from the same rows
    as the table, so no figure here can drift from what the table says.
    """
    plates, n_pub, n_self = [], 0, 0
    for r in rows:
        vec = r.get("vector")
        if not vec:
            continue
        parts = dict(kv.split(":", 1) for kv in vec.split("/")[1:] if ":" in kv)
        if not all(m in parts for m in METRIC_ORDER):
            continue
        sa = bool(r.get("self_assessed"))
        n_self, n_pub = (n_self + 1, n_pub) if sa else (n_self, n_pub + 1)
        cells = "".join(
            f'<span class="sp-m"><span class="sp-k">{m}</span>'
            f'<span class="sp-v">{parts[m]}</span></span>' for m in METRIC_ORDER)
        name = r["cve_id"] or r["ghsa_id"]
        score = f'{r["score"]:.1f} {r["severity"]}'
        plates.append(
            f'<li class="sp-cell{" sp-cell--sa" if sa else ""}">'
            f'<div class="sp-glyph" aria-hidden="true">{cells}</div>'
            f'<p class="sp-vh">{vec}</p>'
            f'<p class="sp-cap"><a href="{r["url"]}">{name}</a>'
            f'<span class="sp-p">{short_package(r["package"])}</span>'
            f'<span class="sp-s{" sp-s--sa" if sa else ""}">{score}</span></p></li>')

    foot = f"One CVSS v3.1 base vector for each of the {n_pub + n_self} published advisories."
    return (
        '<section class="fm-specimen" markdown="0" aria-labelledby="spT">\n'
        '<h3 class="sp-h" id="spT">Vector specimen</h3>\n'
        '<p class="sp-note">One CVSS v3.1 base vector per advisory, set as an eight cell glyph: '
        'attack vector, attack complexity, privileges required and user interaction on the upper '
        'line; scope and the three impacts on the lower. Read the shapes against each other.</p>\n'
        '<ol class="sp-grid">' + "".join(plates) + '</ol>\n'
        f'<p class="sp-foot">{foot}</p>\n'
        '</section>')


def label_of(cwe):
    return CWE_LABELS.get(cwe, "")


def splice(text, marker, body):
    start, end = f"<!-- {marker}:START -->", f"<!-- {marker}:END -->"
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.S)
    if not pattern.search(text):
        raise SystemExit(f"marker {marker} not found in {README}")
    # kramdown needs a blank line between an HTML comment and a markdown table,
    # otherwise the table is swallowed into the surrounding HTML block.
    return pattern.sub(lambda _: f"{start}\n\n{body}\n\n{end}", text)


def stamp_last_modified(text):
    """Set last_modified_at in the front matter.

    jekyll-sitemap only emits <lastmod> for pages that carry this key, and Google
    only trusts lastmod when it is consistently accurate. So this is called ONLY on
    the path where the rendered content actually changed, never on a no-op run.
    """
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    m = re.match(r"(---\n)(.*?)(\n---\n)", text, re.S)
    if not m:
        return text
    head, body, tail = m.groups()
    if re.search(r"^last_modified_at:", body, re.M):
        body = re.sub(r"^last_modified_at:.*$", f"last_modified_at: {now}", body, flags=re.M)
    else:
        body = body + f"\nlast_modified_at: {now}"
    return head + body + tail + text[m.end():]


def main():
    s = session()
    ids = credited_ghsa_ids(s)
    print(f"credited advisories found: {len(ids)}", file=sys.stderr)
    rows = [r for r in (resolve(s, i) for i in ids) if r]
    seen = {r["ghsa_id"] for r in rows}
    for repo, ghsa_id in extra_repo_advisories():
        if ghsa_id in seen:
            continue
        extra = resolve_repo_level(s, repo, ghsa_id)
        if extra:
            rows.append(extra)
            seen.add(ghsa_id)
    if not rows:
        raise SystemExit("no advisories resolved, refusing to write an empty table")
    rows.sort(key=lambda r: (
        SEVERITY_RANK.get(r["severity"].lower(), 9),
        -(r["score"] if r["score"] is not None else 0.0),
        r["package"],
    ))

    original = open(README, encoding="utf-8").read()
    updated = splice(original, "ADVISORIES", render_table(rows))
    updated = splice(updated, "COUNTERS", render_counters(rows))
    record_path = "advisories.md"
    try:
        rec = open(record_path, encoding="utf-8").read()
    except FileNotFoundError:
        rec = None
    if rec is not None and "<!-- RECORD:START -->" in rec:
        new_rec = splice(rec, "RECORD", render_record(rows))
        if new_rec != rec:
            new_rec = stamp_last_modified(new_rec)
            open(record_path, "w", encoding="utf-8").write(new_rec)
            print(f"updated {record_path} with the full record", file=sys.stderr)
        else:
            print("no change to advisories.md", file=sys.stderr)

    if "<!-- CHART:START -->" in updated:
        updated = splice(updated, "CHART", render_chart(rows))

    if updated == original:
        print("no change", file=sys.stderr)
        return
    updated = stamp_last_modified(updated)
    open(README, "w", encoding="utf-8").write(updated)
    print(f"updated {README} with {len(rows)} advisories", file=sys.stderr)


if __name__ == "__main__":
    main()
