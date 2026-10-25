"""What an advisory page and the homepage table say about one advisory, in words.

Shared by build_writeups.py (the pages) and update_advisories.py (the homepage
record), so the two can never word the same advisory differently. Everything
here is read from the published record: the CVSS vector, the affected ranges,
the fixed versions and the disclosure dates. Nothing may claim more than the
record does, so a missing fix, a per-branch fix or a fix that sits inside its
own affected range is said plainly rather than smoothed over.
"""

import html
import json
import pathlib
import re
from datetime import date

API = "https://api.github.com"


def esc(s):
    return html.escape("" if s is None else str(s), quote=True)


def join(items):
    items = list(items)
    if len(items) < 2:
        return items[0] if items else ""
    return ", ".join(items[:-1]) + " and " + items[-1]


def days(a, b):
    return (date.fromisoformat(b) - date.fromisoformat(a)).days


# ── CVSS ──────────────────────────────────────────────────────────────
_CIA = [("N", "None"), ("L", "Low"), ("H", "High")]
SCALE = {
    "AV": [("P", "Physical"), ("L", "Local"), ("A", "Adjacent"), ("N", "Network")],
    "AC": [("H", "High"), ("L", "Low")], "AT": [("P", "Present"), ("N", "None")],
    "PR": [("H", "High"), ("L", "Low"), ("N", "None")],
    "UI3": [("R", "Required"), ("N", "None")], "UI4": [("A", "Active"), ("P", "Passive"), ("N", "None")],
    "S": [("U", "Unchanged"), ("C", "Changed")],
    "C": _CIA, "I": _CIA, "A": _CIA, "VC": _CIA, "VI": _CIA, "VA": _CIA, "SC": _CIA, "SI": _CIA, "SA": _CIA,
    "E": [("U", "Unreported"), ("P", "Proof of concept"), ("A", "Attacked")],
}
NAME = {
    "AV": "Attack vector", "AC": "Attack complexity", "AT": "Attack requirements", "PR": "Privileges required",
    "UI": "User interaction", "S": "Scope", "C": "Confidentiality", "I": "Integrity", "A": "Availability",
    "VC": "Confidentiality", "VI": "Integrity", "VA": "Availability", "SC": "Confidentiality",
    "SI": "Integrity", "SA": "Availability", "E": "Exploit maturity",
}


def parse_vec(vector):
    """{"ver": "3.1", "m": {"AV": "N", ...}} from a vector string."""
    parts = str(vector).split("/")
    out = {"ver": parts[0].split(":")[1] if ":" in parts[0] else "", "m": {}}
    for p in parts[1:]:
        kv = p.split(":")
        if len(kv) == 2:
            out["m"][kv[0]] = kv[1]
    return out


def is_v4(p):
    return p["ver"] == "4.0"


def rank(k, v, v4):
    """Where value v sits on metric k's own scale, mildest first."""
    sc = SCALE.get(("UI4" if v4 else "UI3") if k == "UI" else k)
    if not sc:
        return None
    for i, (code, word) in enumerate(sc):
        if code == v:
            return {"i": i, "n": len(sc), "frac": i / (len(sc) - 1), "word": word}
    return None


def sentence(p):
    """Plain-English reading of the vector, worded per CVSS version so no phrase
    claims more than the metric's definition allows. Returns HTML."""
    m, v4 = p["m"], is_v4(p)
    C, I, A = (m.get("VC"), m.get("VI"), m.get("VA")) if v4 else (m.get("C"), m.get("I"), m.get("A"))
    who = {"N": "Anyone who can reach it over the network", "A": "Anyone on an adjacent network",
           "L": "Someone with local access", "P": "Someone with physical access"}.get(m.get("AV"), "An attacker")
    acct = {"N": "no account", "L": "a low-privilege account", "H": "a high-privilege account"}.get(m.get("PR"), "some access")
    s = f"<em>{who}</em>, with <em>{acct}</em>"
    if m.get("UI") == "N":
        s += " and no user interaction"
    else:
        s += ", " + {"R": "if a user takes some action", "P": "if a user is passively involved",
                     "A": "if a user actively takes part"}.get(m.get("UI"), "with user interaction")
    cond = []
    if v4:
        if m.get("AC") == "H":
            cond.append("if they can defeat a protection or obtain a target-specific secret")
        if m.get("AT") == "P":
            cond.append("given conditions on the target they do not control")
    elif m.get("AC") == "H":
        cond.append("given conditions outside the attacker's control")
    if cond:
        s += ", " + ", ".join(cond)
    parts = []
    if C == "H" and I == "H":
        parts.append("read and change sensitive data")
    elif C != "N" and C == I:
        parts.append("read and change some data")
    else:
        if C == "H":
            parts.append("read sensitive data")
        if C == "L":
            parts.append("read some data")
        if I == "H":
            parts.append("change data with serious effect")
        if I == "L":
            parts.append("change some data")
    if A == "H":
        parts.append("make it unavailable")
    if A == "L":
        parts.append("degrade its availability")
    beyond = any(m.get(k) not in (None, "N") for k in ("SC", "SI", "SA")) if v4 else m.get("S") == "C"
    if parts:
        s += f", can <em>{join(parts)}</em>"
        if beyond:
            s += ", and <em>" + ("other systems are affected too" if v4 else
                                 "the impact reaches beyond the vulnerable component") + "</em>"
    elif beyond:
        s += ", can <em>affect other systems</em>, though not the vulnerable system itself"
    else:
        s += ", with no direct impact"
    return s + "."


def metric_groups(p):
    """The Simple boxes' rows: (heading, [metric keys]) with unset metrics dropped."""
    v4, m = is_v4(p), p["m"]
    rows = [("To exploit it", ["AV", "AC", "AT", "PR", "UI"] if v4 else ["AV", "AC", "PR", "UI"]),
            ("What it gets", ["VC", "VI", "VA"] if v4 else ["C", "I", "A", "S"])]
    if v4:
        rows.append(("Other systems", ["SC", "SI", "SA"]))
    out = []
    for head, keys in rows:
        keys = [k for k in keys if m.get(k) and m[k] != "X"]
        if keys:
            out.append((head, keys))
    return out


def first_calc(vector):
    ver = vector.split("/")[0].replace("CVSS:", "")
    return f"https://www.first.org/cvss/calculator/{'4.0' if ver == '4.0' else '3.1'}#{vector}"


# ── versions ──────────────────────────────────────────────────────────
def vcmp(a, b):
    A, B = re.split(r"[^0-9A-Za-z]+", str(a)), re.split(r"[^0-9A-Za-z]+", str(b))
    for i in range(max(len(A), len(B))):
        if i >= len(A):
            return -1
        if i >= len(B):
            return 1
        x, y = A[i], B[i]
        if x.isdigit() and y.isdigit():
            if int(x) != int(y):
                return -1 if int(x) < int(y) else 1
        elif x != y:
            return -1 if x < y else 1
    return 0


def parse_range(r):
    o = {"lo": None, "lo_inc": True, "hi": None, "hi_inc": True, "eq": None}
    for t in str(r or "").split(","):
        t = t.strip()
        mm = re.match(r"^(>=|<=|>|<|=)?\s*(.+)$", t)
        if not mm:
            continue
        op, v = mm.group(1) or "=", mm.group(2)
        if op in (">=", ">"):
            o["lo"], o["lo_inc"] = v, op == ">="
        elif op in ("<=", "<"):
            o["hi"], o["hi_inc"] = v, op == "<="
        else:
            o["eq"] = v
    return o


def range_text(r):
    o = parse_range(r)
    if o["eq"]:
        return o["eq"] + " only"
    if o["lo"] and o["hi"]:
        return o["lo"] + (" to " if o["hi_inc"] else " to before ") + o["hi"]
    if o["hi"]:
        return o["hi"] + " and earlier" if o["hi_inc"] else "before " + o["hi"]
    if o["lo"]:
        return o["lo"] + " and later"
    return r or "Not listed"


def short_pkg(n):
    n = str(n or "")
    return n if n.startswith("@") else re.split(r"[/:]", n)[-1]


def vulns_of(a):
    """Affected records from either API shape: the global database calls the
    fix first_patched_version, the repository endpoint patched_versions."""
    out = []
    for v in a.get("vulnerabilities") or []:
        pkg = v.get("package") or {}
        out.append({
            "package": pkg.get("name"), "ecosystem": pkg.get("ecosystem"),
            "range": v.get("vulnerable_version_range"),
            "fixed": v.get("first_patched_version") or v.get("patched_versions") or None,
        })
    return out


def vuln_info(v):
    o = parse_range(v["range"])
    f = str(v["fixed"]).strip() if v.get("fixed") else None
    fx = None
    if f:
        parts = re.split(r"\s*,\s*", f)
        if len(parts) > 1:
            fx = {"branches": [re.sub(r"^(>=|>)\s*", "", x) for x in parts]}
        else:
            mm = re.match(r"^(>=|>)?\s*(.+)$", f)
            fx = {"op": mm.group(1) or ">=", "v": mm.group(2)}
    conflict = False
    if fx and "branches" not in fx and o["hi"]:
        c = vcmp(fx["v"], o["hi"])
        conflict = c < 0 if fx["op"] == ">" else (c <= 0 if o["hi_inc"] else c < 0)
    label = None
    if fx:
        label = " or ".join(fx["branches"]) if "branches" in fx else ("after " + fx["v"] if fx["op"] == ">" else fx["v"])
    eco = v.get("ecosystem")
    return {"pkg": v.get("package") or "", "eco": eco if eco and eco != "other" else "",
            "range": v["range"], "o": o, "fx": fx, "conflict": conflict, "label": label}


def action(vulns):
    """What a defender should do, from the affected records. HTML plus a short form."""
    infos = [vuln_info(v) for v in vulns]
    if not infos:
        return {"html": "No affected versions are listed in the advisory.", "short": "Affected versions not listed", "warn": False, "multi": False}

    def one(i, with_pkg):
        who = (f"<b>{esc(short_pkg(i['pkg']))}</b> " if with_pkg else "") + f"<b>{esc(range_text(i['range']))}</b>"
        fx = i["fx"]
        if not fx:
            return {"html": f"If you run {who}, no fixed version is listed in the advisory.", "short": "No fix listed", "warn": True}
        if "branches" in fx:
            return {"html": f"If you run {who}, upgrade to the fixed release in your line: <b>" +
                    "</b> or <b>".join(esc(b) for b in fx["branches"]) + "</b>.", "short": "Fixed in " + i["label"], "warn": False}
        if i["conflict"]:
            return {"html": f"If you run {who}, the advisory lists <b>{esc(fx['v'])}</b> as both affected and fixed, "
                    "so confirm the fixed release with the maintainer.", "short": "Fix unclear", "warn": True}
        if fx["op"] == ">":
            return {"html": f"If you run {who}, upgrade to a release after <b>{esc(fx['v'])}</b>.", "short": "Upgrade past " + fx["v"], "warn": False}
        return {"html": f"If you run {who}, upgrade to <b>{esc(fx['v'])}</b> or later.", "short": "Upgrade to " + fx["v"], "warn": False}

    if len(infos) == 1:
        r = one(infos[0], True)
        r["multi"] = False
        return r
    same = all(x["pkg"] == infos[0]["pkg"] for x in infos)
    lines = [one(x, not same) for x in infos]
    return {"html": "<br>".join(l["html"] for l in lines), "short": "Fix differs by range",
            "warn": any(l["warn"] for l in lines), "multi": True}


# ── disclosure ────────────────────────────────────────────────────────
def repo_of(a):
    loc = a.get("source_code_location") or ""
    m = (re.search(r"github\.com/([^/]+/[^/#?]+)", loc)
         or re.search(r"github\.com/([^/]+/[^/]+)/security/advisories", a.get("html_url") or ""))
    return m.group(1) if m else None


def disclosure_facts(s, a, repo=None):
    """When the report was filed, whether it began as a private report, and when
    the maintainer published it. The repository advisory carries these; the
    global database's own published_at is the later date GitHub reviewed it."""
    repo = repo or repo_of(a)
    reported, repo_published, private = a.get("created_at"), None, False
    if repo:
        if "state" in a:
            j = a  # already the repository advisory; the global one has no state
        else:
            r = s.get(f"{API}/repos/{repo}/security-advisories/{a['ghsa_id']}", timeout=30)
            if r.status_code != 200:
                raise SystemExit(f"{a['ghsa_id']}: repository advisory HTTP {r.status_code}, nothing written")
            j = r.json()
        reported = reported or j.get("created_at")
        repo_published = j.get("published_at")
        # Present only when the advisory began as a private vulnerability
        # report; otherwise created_at is just when the maintainer opened it.
        private = bool(j.get("submission"))
    out = {"repo": repo, "reported": (reported or "")[:10] or None,
           "repo_published": (repo_published or "")[:10] or None, "private_report": private}
    # When the report was filed is shown only to the advisory's collaborators,
    # which includes its reporter but not the workflow's token. A local build
    # run as the reporter records it here; the daily job falls back on it so
    # it does not quietly drop the date every morning.
    known = _disclosure_cache().get(a["ghsa_id"])
    if not out["reported"] and known:
        out["reported"], out["private_report"] = known["reported"], known["private_report"]
    return out


DISCLOSURE_CACHE = pathlib.Path(__file__).resolve().parent / "disclosure.json"


def _disclosure_cache():
    try:
        return json.loads(DISCLOSURE_CACHE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def save_disclosure(facts):
    """facts: {ghsa_id: disclosure_facts(...)}. Keeps only what a reporter's
    view adds, and never forgets a date it already had."""
    cache = _disclosure_cache()
    for gid, d in facts.items():
        if d.get("reported"):
            cache[gid] = {"reported": d["reported"], "private_report": d["private_report"]}
    DISCLOSURE_CACHE.write_text(json.dumps(cache, indent=1, sort_keys=True) + "\n", encoding="utf-8")


def disclosure(d, published):
    """[(date, label)] in order: reported, published by the maintainer, and
    the database date where GitHub's review came later."""
    nodes = []
    if d.get("reported"):
        nodes.append((d["reported"], "Reported privately" if d.get("private_report") else "Advisory opened"))
    rp = d.get("repo_published") or published
    if rp:
        nodes.append((rp, "Published by the maintainer"))
    if published and published != rp:
        nodes.append((published, "Added to GitHub's advisory database"))
    return nodes
