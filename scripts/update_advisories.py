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

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import advisory_facts as F  # noqa: E402

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
    "CWE-321": "Hard-coded crypto key",
    "CWE-352": "Cross site request forgery",
    "CWE-362": "Race condition",
    "CWE-434": "Unrestricted upload",
    "CWE-502": "Unsafe deserialization",
    "CWE-639": "Insecure direct object reference",
    "CWE-862": "Missing authorization",
    "CWE-863": "Incorrect authorization",
    "CWE-653": "Improper isolation",
    "CWE-668": "Resource exposure",
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


def maintainer_published(s, a):
    """The date the maintainer published the advisory.

    The global database's published_at is when GitHub reviewed the advisory
    in, which trailed the maintainer's own publication by up to three months
    on eight of these. The repo advisory carries the disclosure date; the
    global one is the fallback when the repo cannot be reached.
    """
    m = re.search(r"github\.com/([^/]+/[^/#?]+)", a.get("source_code_location") or "")
    if m:
        r = s.get(f"{API}/repos/{m.group(1)}/security-advisories/{a['ghsa_id']}", timeout=30)
        if r.status_code == 200 and r.json().get("published_at"):
            return r.json()["published_at"]
    return a.get("published_at")


def row_facts(s, a, repo):
    """What the homepage row opens to: the affected records and the disclosure
    dates. If the repository advisory cannot be read, the row simply says less
    rather than stopping the daily refresh."""
    try:
        disc = F.disclosure_facts(s, a, repo)
    except SystemExit as e:
        print(f"{a['ghsa_id']}: no disclosure dates ({e})", file=sys.stderr)
        disc = None
    return {"vulns": F.vulns_of(a), "disc": disc}


def resolve_repo_level(s, repo, ghsa_id):
    """Only returns an advisory that is published and where USER credit is accepted."""
    r = s.get(f"{API}/repos/{repo}/security-advisories/{ghsa_id}", timeout=30)
    if r.status_code != 200:
        # A failed fetch is not a withdrawn advisory. Skipping it would commit
        # a shorter record, so stop and leave the page as it was.
        raise SystemExit(f"{ghsa_id}: HTTP {r.status_code}, nothing written")
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
        **row_facts(s, a, repo),
    }


def resolve(s, ghsa_id):
    r = s.get(f"{API}/advisories/{ghsa_id}", timeout=30)
    if r.status_code != 200:
        # A failed fetch is not a withdrawn advisory. Skipping it would commit
        # a shorter record, so stop and leave the page as it was.
        raise SystemExit(f"{ghsa_id}: HTTP {r.status_code}, nothing written")
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
        "published": (maintainer_published(s, a) or "")[:10],
        "summary": (a.get("summary") or "").strip(),
        **row_facts(s, a, None),
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


def peek_row(i, r, sev, cols=9):
    """The short reading a row opens to: the vector as a sentence, what to do,
    and how long disclosure took. Hidden until the reader asks for it.

    cols spans the peek cell across the whole row; the record ledger has 9
    columns, so that is the default."""
    import html as _h
    e = lambda x: _h.escape(str(x), quote=True)
    act = F.action(r["vulns"])
    nodes = F.disclosure(r["disc"] or {}, r["published"] or None)
    if len(nodes) > 1:
        disc = (f'<b>{F.days(nodes[0][0], nodes[1][0])} days</b><small>{e(nodes[0][1])} {e(nodes[0][0])}, '
                f'published {e(nodes[1][0])}</small>')
        disc_k = "Report to publication"
    else:
        disc = f'<b>{e(r["published"])}</b><small>Published by the maintainer</small>'
        disc_k = "Published"
    sent = F.sentence(F.parse_vec(r["vector"])) if r["vector"] else ""
    note = ('<div class="pk-f"><small>Score is my assessment; GitHub published no CVSS for this advisory.</small></div>'
            if r["self_assessed"] else "")
    return (f'<tr role="row" class="peek" id="peek-{i:02d}" data-sev="{e(sev.lower())}" hidden>'
            f'<td role="cell" colspan="{cols}"><div class="pk">'
            f'<div><p class="pk-s">{sent}</p>{note}</div>'
            f'<div class="pk-f"><span class="k-lab">What to do</span><b{" class=\"quiet\"" if act["warn"] else ""}>{e(act["short"])}</b></div>'
            f'<div class="pk-f"><span class="k-lab">{disc_k}</span>{disc}</div>'
            f'<a class="pk-a" href="{e(r["url"])}">Read the writeup &rarr;</a>'
            f'</div></td></tr>')


# The home page "Advisories" section shows a curated grid of finding cards,
# chosen for technical depth and severity, plus a quieter card that opens the
# full record. The complete ledger (every row, every base vector) is /advisories/.
CURATED = [
    "GHSA-24q6-6h89-f9p7",  # AutoGPT 10.0 auth bypass
    "GHSA-42mf-vpmr-gw5r",  # ag2 9.9 command injection
    "GHSA-jmr9-98g4-2phv",  # portainer 9.4 access control (v4)
    "CVE-2026-49950",       # xinference 9.3 missing auth (v4, CVE)
    "CVE-2026-57516",       # ray 8.8 code injection (CVE)
    "GHSA-5mc6-2qfj-59cg",  # opik 8.8 template injection -> RCE
    "CVE-2026-45675",       # open-webui 8.1 privilege escalation (CVE)
    "GHSA-hxvp-ff3g-qcj7",  # vendure 8.8 information disclosure
]


def _norm(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


def _card_hook(url, package):
    """The card's one-line hook: the advisory file's description, first sentence,
    with a leading 'Project: ' prefix dropped when it only echoes the package
    name already shown as the card title (e.g. 'Ray: Arbitrary code...')."""
    slug = url.strip("/").split("/")[-1]
    path = os.path.join(os.path.dirname(README) or ".", "advisories", slug + ".md")
    try:
        fm = open(path, encoding="utf-8").read()
    except FileNotFoundError:
        return ""
    m = re.search(r'^description:\s*"(.*?)"', fm, re.M | re.S)
    if not m:
        return ""
    desc = m.group(1)
    hm = re.match(r"(.*?)\.\s+[^.]*,\s+CVSS", desc, re.S)
    hook = (hm.group(1) if hm else desc.split(". ")[0]).strip()
    pm = re.match(r"^([A-Za-z0-9 .&/_-]{1,28}?):\s+(.*)$", hook, re.S)
    if pm:
        lead, pkgtoks = _norm(pm.group(1)), _norm(re.sub(r"^.*/", "", package))
        if lead and (lead in pkgtoks or pkgtoks in lead):
            rest = pm.group(2)
            hook = rest[:1].upper() + rest[1:]
    return hook


def render_cards(rows):
    """The home page "Advisories" grid: the curated finding cards plus the
    quieter card that opens the full record."""
    import html as _h
    e = lambda x: _h.escape(str(x), quote=True)
    by_id = {}
    for r in rows:
        for key in (r.get("cve_id"), r.get("ghsa_id")):
            if key:
                by_id[key] = r
    cards = []
    for ident in CURATED:
        r = by_id.get(ident)
        if not r:
            continue
        sev = band(r["score"]) if r["score"] is not None else r["severity"]
        name = r["cve_id"] or r["ghsa_id"]
        badge = ('<span class="k-cve">CVE</span>' if name.startswith("CVE-")
                 else '<span class="k-ghsa">GHSA</span>')
        hook = _card_hook(r["url"], r["package"])
        cards.append(
            f'<a class="card" data-sev="{e(sev.lower())}" href="{e(r["url"])}">'
            f'<div class="card-top"><span class="card-score">{r["score"]:.1f}</span>'
            f'<span class="card-sev">{e(sev)}</span></div>'
            f'<div class="card-proj">{e(r["package"])}</div>'
            f'<p class="card-hook">{e(hook)}</p>'
            f'<div class="card-foot"><span class="card-cls">{e(label(r["cwe"]))}</span>'
            f'<span class="card-cwe">CWE-{(r["cwe"] or "").replace("CWE-", "")}</span>'
            f'{badge}</div></a>')
    n = len(rows)
    all_card = (
        f'<a class="card card--all" href="/advisories/">'
        f'<div class="all-top"><span class="all-n">{n}</span>'
        f'<span class="all-tag">Record</span></div>'
        f'<div class="all-title">The full record</div>'
        f'<div class="all-s">Every published advisory, each with its CVSS base vector, '
        f'weakness class and writeup.</div>'
        f'<span class="all-go">Browse all advisories &rarr;</span></a>')
    return ('      <div class="cards">\n        '
            + "\n        ".join(cards)
            + '\n        ' + all_card + '\n      </div>')




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
    # ag2ai/ag2: published Critical with no CVSS vector. shell=True with
    # prefix-only command filtering is bypassed by shell metacharacters for
    # arbitrary OS command execution. Score and vector are the exact CVSS
    # line stated in the advisory I published: PR:L for the agent/developer
    # context the shell tool runs in, S:C because the filter boundary is crossed
    # to host OS execution. Computes to 9.9, inside the maintainer Critical band.
    "GHSA-42mf-vpmr-gw5r": {
        "score": 9.9,
        "vector": "CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H",
    },
    # ag2ai/ag2: a second advisory, published High with no CVSS vector. Path
    # traversal in DiskKnowledgeStore from a startswith containment check that a
    # prefix-sharing sibling directory bypasses, giving read, write and delete
    # outside the root to an agent that drives the knowledge tool. The vector
    # is taken verbatim from the advisory's own CVSS line. That line states
    # 7.5, but the vector computes to 8.1 under CVSS 3.1 (exploitability 2.835
    # + impact 5.177, rounded up), so the score is the computed one, still
    # inside the maintainer's High band.
    "GHSA-qrjx-72xx-xhmh": {
        "score": 8.1,
        "vector": "CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N",
    },
}

METRIC_ORDER = ["AV", "AC", "PR", "UI", "S", "C", "I", "A"]


def _cvss_pick(obj, prefix):
    """A (score, vector) from one CVSS node, only if it is a real base score on
    the requested version. Guards against the 0.0 placeholder GitHub sometimes
    stores next to a vector it has not fully computed."""
    o = obj or {}
    s, v = o.get("score"), o.get("vector_string")
    if isinstance(s, (int, float)) and s > 0 and v and v.startswith(prefix):
        return float(s), v
    return None, None


def cvss_of(a):
    """Return (score, vector, self_assessed) for one advisory payload.

    GitHub's published base score is authoritative: a CVSS v3.1 score if present,
    otherwise a v4.0 score (GitHub increasingly scores on v4). This is on purpose.
    These pages are a public record, so the number a reader sees is the maintainer
    and CNA's own, never ours, wherever they published one. Only when GitHub
    published a severity band with no numeric score at all do we fall back to a
    deliberate self assessment, which the page then labels plainly as ours and
    inside the band GitHub published. The 0.0 placeholder GitHub sometimes stores
    next to an uncomputed vector is rejected by _cvss_pick (it requires score > 0),
    so it never masquerades as a real score. The top level `cvss` node can hold
    either version, so it is checked under both prefixes. Callers that lay a vector
    out metric by metric detect v4 from its "CVSS:4" prefix.
    """
    cvss = a.get("cvss") or {}
    sev = a.get("cvss_severities") or {}
    for obj in (cvss, sev.get("cvss_v3")):
        s, v = _cvss_pick(obj, "CVSS:3")
        if s:
            return s, v, False
    for obj in (cvss, sev.get("cvss_v4")):
        s, v = _cvss_pick(obj, "CVSS:4")
        if s:
            return s, v, False
    sa = SELF_ASSESSED.get(a.get("ghsa_id"))
    if sa:
        return sa["score"], sa["vector"], True
    return None, None, False



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
    sev = band(r["score"]) if r["score"] is not None else r["severity"]
    ident = r["cve_id"] or r["ghsa_id"]
    href = (SITE_ORIGIN if absolute else "") + r["url"]
    # One base-vector column, rendered identically for every row: a muted scale
    # tag (v3.1 / v4.0) then one self-labeled chip per metric. A v3.1 vector is
    # eight chips and sits on one line; a v4.0 vector is eleven (plus any threat
    # metric) and wraps to a second line in the same style, so the two scales
    # read as one consistent column instead of breaking the grid with a spanning
    # cell. The chip carries its own metric key, so no shared header is needed.
    pairs = [kv.split(":", 1) for kv in (r["vector"] or "").split("/")[1:] if ":" in kv]
    scale = e((r["vector"] or "CVSS:4.0").split("/", 1)[0].replace("CVSS:", "v"))
    chips = "".join(f'<span class="vm"><i>{e(k)}</i><b>{e(val)}</b></span>' for k, val in pairs)
    vector_cell = (f'<td role="cell" class="c-vec">'
                   f'<span class="vm-s">{scale}</span>{chips}</td>')
    return (
        f'<tr role="row" data-sev="{e(sev.lower())}">\n'
        f'              <th role="rowheader" scope="row" class="c-nr">{n:02d}</th>\n'
        f'              <td role="cell" class="c-id"><a href="{href}">{e(ident)}</a></td>\n'
        f'              <td role="cell" class="c-pkg">{_pkg(r["package"])}</td>\n'
        f'              <td role="cell" class="c-sc">{r["score"]:.1f}</td>\n'
        f'              <td role="cell" class="c-sev sev-{SEV_CLASS[sev]}">{sev}</td>\n'
        f'              <td role="cell" class="c-cls">{e(label(r["cwe"]))}</td>\n'
        f'              <td role="cell" class="c-cwe">{(r["cwe"] or "").replace("CWE-", "")}</td>\n'
        f'              {vector_cell}\n'
        f'              <td role="cell" class="c-pub">{r["published"]}</td>\n'
        f'            </tr>')

AUTH_CWES = {"CWE-306", "CWE-862", "CWE-863"}


def render_record(rows):
    """The full record for /advisories/: every base vector in one column.

    Each row shows its CVSS base vector as a muted scale tag and one self-labeled
    chip per metric, the same way for v3.1 and v4.0. Below 1120px each row becomes
    a block and the vector chips wrap as their own band, so the vector stays
    readable on a phone with no horizontal gesture.
    """
    def _pair(i, r):
        sev = band(r["score"]) if r["score"] is not None else r["severity"]
        return advisory_row(i, r) + "\n            " + peek_row(i, r, sev, 9)
    body = "\n            ".join(_pair(i, r) for i, r in enumerate(rows, 1))
    return f"""      <div class="tablewrap" role="region" aria-label="Published advisories, full table" tabindex="0">
        <table role="table">
          <thead role="rowgroup">
            <tr role="row">
              <th role="columnheader" scope="col" class="c-nr">NR</th>
              <th role="columnheader" scope="col" class="c-id">Advisory</th>
              <th role="columnheader" scope="col" class="c-pkg">Package</th>
              <th role="columnheader" scope="col" class="c-sc">CVSS</th>
              <th role="columnheader" scope="col" class="c-sev">Severity</th>
              <th role="columnheader" scope="col" class="c-cls">Weakness</th>
              <th role="columnheader" scope="col" class="c-cwe">CWE</th>
              <th role="columnheader" scope="col" class="c-vec">Base vector</th>
              <th role="columnheader" scope="col" class="c-pub">Published</th>
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

    foot = f"One CVSS v3.1 base vector for each of the {n_pub + n_self} advisories scored on that scale."
    return (
        '<section class="fm-specimen" markdown="0" aria-labelledby="spT">\n'
        '<h3 class="sp-h" id="spT">Vector specimen</h3>\n'
        '<p class="sp-note">One CVSS v3.1 base vector per v3.1 scored advisory, set as an eight cell glyph: '
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
    # The home page shows a curated grid of finding cards (render_cards); the
    # full base-vector ledger lives on /advisories/ (render_record).
    updated = splice(original, "ADVISORIES", render_cards(rows))
    updated = splice(updated, "COUNTERS", render_counters(rows))
    record_path = "advisories.md"
    try:
        rec = open(record_path, encoding="utf-8").read()
    except FileNotFoundError:
        rec = None
    if rec is not None and "<!-- RECORD:START -->" in rec:
        # Keep the section-head count (the "29" index beside "Full record") in
        # sync with the record, so it never drifts from the number of rows.
        rec = re.sub(r'(<p class="idx">)\d+(</p>)', rf'\g<1>{len(rows)}\g<2>', rec, count=1)
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
