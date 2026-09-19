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


HIGHLIGHT_N = 3

# One line each, written rather than lifted from the maintainer's advisory
# title. Keyed by GHSA id so a new top finding falls back to the published
# summary instead of silently showing a stale sentence.
HIGHLIGHT_BLURBS = {
    "GHSA-pqxw-g93w-hj9x":
        "The shipped Docker Compose example hardcodes the secrets that sign login links. "
        "Anyone who has read the repository can mint a session as any user, and the runner "
        "network puts the database, cache and registry one hop away.",
    "CVE-2026-57516":
        "A dataset reader trusted its default decoder, so loading a remote dataset ran "
        "pickle.loads and torch.load with weights_only off. Reading data was enough to "
        "execute code.",
    "CVE-2026-45675":
        "Two paths could claim the first-user account at once. Winning that race made an "
        "attacker an administrator on a fresh instance.",
}


def render_table(rows):
    """The home page summary: the highest findings, not the whole ledger.

    The full table lives on /advisories/ and used to be duplicated here, which
    made the landing page a data dump and repeated eleven rows verbatim one
    click apart. Rows arrive sorted by severity then score, so the first few
    are the strongest.
    """
    import html as _html

    def esc(x):
        return _html.escape(str(x), quote=True)

    picked = rows[:HIGHLIGHT_N]
    items = []
    for r in picked:
        name = r["cve_id"] or r["ghsa_id"]
        score = f'{r["score"]:.1f}' if r["score"] is not None else esc(r["severity"])
        # The maintainers' own advisory titles read as advisory titles. These
        # are written by hand so the landing page reads as prose; anything not
        # listed falls back to the published summary rather than to nothing.
        summary = HIGHLIGHT_BLURBS.get(r["ghsa_id"]) or (r.get("summary") or "")
        if len(summary) > 165:
            summary = summary[:165].rsplit(" ", 1)[0] + "\u2026"
        items.append(
            f'<li class="sel-item">'
            f'<p class="sel-head"><a href="{esc(r["url"])}">{esc(name)}</a>'
            f'<span class="sel-proj"><code>{esc(short_package(r["package"]))}</code></span>'
            f'<span class="sel-score">{score}</span></p>'
            f'<p class="sel-sum">{esc(summary)}</p></li>')

    n = len(rows)
    return (
        '<div class="sel" markdown="0">'
        f'<ol class="sel-list">{"".join(items)}</ol>'
        f'<p class="sel-more"><a href="/advisories/">All {n} advisories, with CVSS vectors and '
        'full writeups &rarr;</a></p>'
        '</div>')


def render_counters(rows):
    n = len(rows)
    cves = len({r["cve_id"] for r in rows if r["cve_id"]})
    projects = len({r["package"] for r in rows})
    word = "advisory" if n == 1 else "advisories"
    return (
        f"**{cves} CVEs assigned.** {n} published {word} across {projects} projects, "
        f"from {REPORTS_FILED} reports filed against {PROJECTS_AUDITED} open source projects."
    )


SELF_ASSESSED = {
    # GHSA-pqxw-g93w-hj9x was published High with no score and no vector, in
    # v3 or v4, so nothing upstream can supply one. This vector is derived by
    # hand from the advisory's own text: unauthenticated (the secrets ship in
    # hosting/docker/.env.example), AC:H granting the precondition that the
    # operator kept those defaults, S:C because the documented chain crosses
    # out of the webapp into Postgres, Redis, ClickHouse and the registry, and
    # three High impacts. That computes to 9.0. It is flagged everywhere it is
    # rendered: this site's claim is that its numbers resolve to a public
    # advisory, and this one does not.
    "GHSA-pqxw-g93w-hj9x": {
        "score": 9.0,
        "vector": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H",
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


AUTH_CWES = {"CWE-306", "CWE-862", "CWE-863"}


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

    foot = (f"One CVSS v3.1 base vector for each of the {n_pub + n_self} published "
            "advisories, as the coordinating database records them.")
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
