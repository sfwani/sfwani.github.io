#!/usr/bin/env python3
"""Generate one page per published advisory, plus the /advisories/ index.

Source of truth is the same as update_advisories.py: the public credit search
plus advisories.txt for repo level advisories the global database never got.
Nothing unpublished can appear here, because both paths gate on state ==
published and on this user's credit being accepted.

Run: python3 scripts/build_writeups.py
"""

import html
import os
import pathlib
import re
import sys
from datetime import datetime, timezone

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from update_advisories import (  # noqa: E402
    API, USER, session, credited_ghsa_ids, extra_repo_advisories, CWE_LABELS,
    maintainer_published,
    short_package,
    render_chart,
    # The derived score for the one advisory published without one lives in
    # the sibling generator, so the two pages this repo builds cannot
    # disagree about it.
    cvss_of,
    project_of,
)
import og_cards  # noqa: E402
import advisory_facts as F  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
# The shared helper reads advisories.txt relative to the working directory, so
# run from anywhere else it quietly saw none and the pages, feed and llms.txt
# were rewritten short. Pin it to this repo.
os.environ.setdefault("EXTRA_ADVISORIES", str(ROOT / "advisories.txt"))
OUT = ROOT / "advisories"
SITE = "https://sfwani.github.io"


def raw_global(s, ghsa_id):
    r = s.get(f"{API}/advisories/{ghsa_id}", timeout=30)
    if r.status_code != 200:
        # A failed fetch is not a withdrawn advisory. Skipping it would publish
        # a shorter record, so stop and leave every file as it was.
        raise SystemExit(f"{ghsa_id}: HTTP {r.status_code}, nothing written")
    a = r.json()
    if a.get("withdrawn_at"):
        return None
    # Everything downstream reads published_at, so it carries the maintainer's
    # disclosure date; GitHub's own review date is kept beside it.
    a["github_published_at"] = a.get("published_at")
    a["published_at"] = maintainer_published(s, a)
    return a


def raw_repo_level(s, repo, ghsa_id):
    """Only an advisory that is published and where USER credit is accepted."""
    r = s.get(f"{API}/repos/{repo}/security-advisories/{ghsa_id}", timeout=30)
    if r.status_code != 200:
        # A failed fetch is not a withdrawn advisory. Skipping it would publish
        # a shorter record, so stop and leave every file as it was.
        raise SystemExit(f"{ghsa_id}: HTTP {r.status_code}, nothing written")
    a = r.json()
    if a.get("state") != "published" or a.get("withdrawn_at"):
        print(f"skip {ghsa_id}: state={a.get('state')}", file=sys.stderr)
        return None
    ok = any(
        (c.get("user") or {}).get("login") == USER and c.get("state") == "accepted"
        for c in a.get("credits_detailed") or []
    )
    if not ok:
        print(f"skip {ghsa_id}: credit not accepted", file=sys.stderr)
        return None
    return a


def clip(s, n):
    """Truncate on a word boundary so a <title> never ends mid-token."""
    s = s.strip()
    if len(s) <= n:
        return s
    cut = s[:n]
    sp = cut.rfind(" ")
    return (cut[:sp] if sp > n * 0.6 else cut).rstrip(" ,.:;-") + "\u2026"


def slug(a):
    return (a.get("cve_id") or a["ghsa_id"]).lower()


# Maintainer summaries are used as page titles, and a few arrive unfit for one:
# cut off mid-word, or carrying punctuation the site does not use. An entry here
# replaces the title on this site only; the advisory of record is untouched.
SUMMARY_OVERRIDES = {
    "GHSA-jvm6-86c5-f8j8": "SSRF via AI provider baseUrl bypasses safeFetch, reachable by any space owner",
}


def summary_of(a):
    s = SUMMARY_OVERRIDES.get(a["ghsa_id"]) or (a.get("summary") or "")
    s = re.sub(r"\s+", " ", s.strip())
    return re.sub(r"\s*[—–]\s*", ", ", s)


def facts_of(a):
    """(project, score, severity, scheme, cwe) as the page and its card state them."""
    pkgs = sorted({v["package"]["name"] for v in a.get("vulnerabilities") or [] if v.get("package")})
    project = short_package(pkgs[0]) if pkgs else a["ghsa_id"]
    score, vector, self_assessed = cvss_of(a)
    scheme = ("CVSS 4.0" if (vector or "").startswith("CVSS:4") else "CVSS 3.1") + (" · my assessment" if self_assessed else "")
    cwe = (a.get("cwes") or [{}])[0].get("cwe_id")
    if cwe and CWE_LABELS.get(cwe):
        cwe = f"{cwe} {CWE_LABELS[cwe]}"
    return project, score, (a.get("severity") or "").capitalize(), scheme, cwe


def describe(a, summary):
    """The search and link-preview snippet: what it is, how bad, whose writeup.
    The title already carries the summary, so this adds what the title lacks."""
    project, score, sev, _scheme, cwe = facts_of(a)
    rating = f"CVSS {score:.1f} {sev}" if score is not None else sev
    lead = summary if summary.endswith((".", "!", "?")) else summary + "."
    return f"{lead} {project}, {rating}{', ' + cwe if cwe else ''}. Writeup by Sanaan Fayaz Wani, the credited reporter."


def own_writeup(a):
    """Path to my own writeup for this advisory, or None. Keyed by the same slug
    the page uses, so _writeups/<slug>.md opts one advisory into my own text."""
    p = ROOT / "_writeups" / f"{slug(a)}.md"
    return p if p.exists() else None


def _esc(s):
    return html.escape("" if s is None else str(s), quote=True)


# ── The advisory header ────────────────────────────────────────────
# Answer first: how bad it is and what to do, then the vector read as one
# sentence, then the metrics as plain boxes, then the record identifiers.
# Built as raw HTML because the panel is a grid citizen of the section rather
# than prose: the score hangs in the numeral gutter where a section number
# would sit, and everything else aligns to the body column beside it.

def score_label(vector):
    """CVSS 4.0 names a score by the metric groups in its vector: with a threat
    metric (E) set it is CVSS-BT, not a base score."""
    if not vector:
        return "CVSS base"
    ver = vector.split("/")[0].replace("CVSS:", "")
    threat = ver.startswith("4") and any(p.startswith("E:") and p != "E:X" for p in vector.split("/"))
    return f"CVSS-BT {ver}" if threat else f"CVSS {ver} base"


def cwe_list(a):
    return [(c["cwe_id"], c.get("name") or "") for c in a.get("cwes") or []]


def timeline_html(nodes):
    """The disclosure dates stood upright under the score, and the same dates
    across for a phone, where the score column stacks above everything."""
    if not nodes:
        return "", ""
    lis = []
    for i, (d, lab) in enumerate(nodes):
        gap = f'<span class="tlv-d">{F.days(nodes[i - 1][0], d)} days later</span>' if i else ""
        lis.append(f"<li>{gap}<b>{_esc(d)}</b><span>{_esc(lab)}</span></li>")
    upright = '<ol class="tlv" aria-label="Disclosure timeline">' + "".join(lis) + "</ol>"
    if len(nodes) < 2:
        return upright, ""
    across = []
    for i, (d, lab) in enumerate(nodes):
        if i:
            across.append(f'<div class="tl-seg"><span>{F.days(nodes[i - 1][0], d)} days</span></div>')
        across.append(f'<div class="tl-n"><b>{_esc(d)}</b><span>{_esc(lab)}</span></div>')
    return upright, '<div class="tl" role="group" aria-label="Disclosure timeline">' + "".join(across) + "</div>"


def boxes_html(p, vector):
    """One plain box per metric, its name and its value. The sentence above
    already says what they mean, so the boxes only have to state them."""
    groups = F.metric_groups(p)
    n = max(len(keys) for _h, keys in groups)
    rows = []
    for head, keys in groups:
        cells = "".join(
            f'<div class="bx-c"><dt>{_esc(F.NAME[k])}</dt>'
            f'<dd>{_esc((F.rank(k, p["m"][k], F.is_v4(p)) or {"word": p["m"][k]})["word"])}</dd></div>'
            for k in keys)
        rows.append(f'<div class="bx-row"><p class="bx-g">{_esc(head)}</p><dl class="bx-grid">{cells}</dl></div>')
    threat = ""
    e = p["m"].get("E")
    if F.is_v4(p) and e and e != "X":
        word = (F.rank("E", e, True) or {"word": e})["word"]
        threat = (f'<p class="bx-threat"><span class="k-lab">Threat</span>Exploit maturity: <b>{_esc(word)}</b>. '
                  "Because this is set, the score is CVSS-BT.</p>")
    return (f'<div class="bx" style="--n:{n}"><div class="bx-head"><span class="k-lab">CVSS {_esc(p["ver"])} metrics</span></div>'
            + "".join(rows) + threat +
            f'<p class="bx-foot"><a href="{_esc(F.first_calc(vector))}" rel="noopener">Open this vector in the FIRST calculator &#8599;</a></p></div>')


def siblings_html(ctx, sep):
    return sep.join(f'<a href="/advisories/{_esc(s)}/">{_esc(name)}</a> {_esc(sc)}' for s, name, sc in ctx["siblings"])


def advisory_header_html(a, ctx):
    score, vector, self_assessed = cvss_of(a)
    sev_word = (a.get("severity") or "").capitalize()
    sev_key = (a.get("severity") or "none").lower()
    p = F.parse_vec(vector) if vector else None
    upright, across = timeline_html(ctx["nodes"])

    # Score column, with the disclosure dates under it.
    bits = []
    if score is None:
        bits.append(f'<p class="ah-sev ah-sev--lg">{_esc(sev_word) or "Unrated"}</p>')
        bits.append('<p class="ah-of">No published CVSS score</p>')
    else:
        pct = max(0, min(100, round(score * 10)))
        bits.append(f'<p class="ah-num">{score:.1f}</p>')
        bits.append(f'<p class="ah-sev">{_esc(sev_word)}</p>')
        bits.append(f'<p class="ah-of">{_esc(score_label(vector))}</p>')
        if self_assessed:
            bits.append('<p class="ah-tag">My assessment</p>')
        bits.append(f'<div class="ah-meter" aria-hidden="true"><i style="width:{pct}%"></i></div>')
    out = ['<div class="ah-score">' + "".join(bits) + upright + "</div>"]

    act = ctx["action"]
    out.append(f'<div class="act{" warn" if act["warn"] else ""}"><p class="act-k">What to do</p>'
               f'<p class="act-v{" multi" if act["multi"] else ""}">{act["html"]}</p></div>')
    if p:
        out.append(f'<p class="ts">{F.sentence(p)}<span class="ts-src">Read from the CVSS {_esc(p["ver"])} vector</span></p>')
        out.append(boxes_html(p, vector))

    # Record identifiers.
    items = []
    cw = cwe_list(a)
    if cw:
        names = " · ".join(n for _c, n in cw if n)
        items.append(("Weakness", ", ".join(f'<abbr title="{_esc(n)}">{_esc(c)}</abbr>' for c, n in cw)
                      + (f' <span class="meta-s">{_esc(names)}</span>' if names else ""), True))
    items.append(("Advisory", f'<a href="{_esc(a.get("html_url"))}">{_esc(a["ghsa_id"])}</a>', False))
    items.append(("CVE", _esc(a.get("cve_id") or "not assigned"), False))
    if vector:
        items.append(("Vector", '<span class="vec">' + _esc(vector).replace("/", "/<wbr>") + "</span>", False))
    if ctx["siblings"]:
        items.append((f"Also in {_esc(ctx['project'])}", siblings_html(ctx, " · "), True))
    out.append('<dl class="meta">' + "".join(
        f'<div class="meta-i{" wide" if wide else ""}"><dt class="k-lab">{k}</dt><dd class="meta-v">{v}</dd></div>'
        for k, v, wide in items) + "</dl>")
    out.append(across)

    # The note frames whose words follow. Only say "my analysis" where a
    # _writeups/ file actually replaces the published text; an advisory without
    # one falls back to the maintainer's own writeup, and claiming it as my
    # analysis would misstate authorship.
    if own_writeup(a):
        out.append('<p class="ah-note">My analysis of this finding: root cause, the vulnerable '
                   'code, the impact and the fix, in the site’s format. The official advisory '
                   'of record is linked above.</p>')
    else:
        out.append('<p class="ah-note">This page reproduces the published advisory for this '
                   'finding. The advisory of record is linked above.</p>')
    if self_assessed:
        out.append('<p class="ah-note ah-note--disc">GitHub published this advisory as '
                   f'{_esc(sev_word)} with no CVSS score and no vector, in v3 or v4. The score '
                   'and vector above are my own assessment of the finding, within the severity '
                   'band GitHub published. Where GitHub publishes a numeric score, this page '
                   'shows that one instead.</p>')
    return f'<div class="ah" data-sev="{_esc(sev_key)}">' + "".join(out) + "</div>"


# ── The fact sheet ─────────────────────────────────────────────────
# The reference facts a reader looks back for while reading the writeup: the
# weakness, the versions involved, the disclosure dates and the IDs. Stated as
# record, not advice; "what to do" already led the page. Set in the right
# margin on a wide screen and at the foot of the writeup on anything narrower.

def fact_rows(a, ctx):
    rows = []
    cw = cwe_list(a)
    if cw:
        rows.append(("Weakness", "<br>".join(f"<b>{_esc(c)}</b>" + (f" {_esc(n)}" if n else "") for c, n in cw)))
    infos = [F.vuln_info(v) for v in ctx["vulns"]]
    if len(infos) == 1:
        i = infos[0]
        fixed = "Not listed" if not i["fx"] else "Unclear in the record" if i["conflict"] else i["label"]
        rows.append(("Affected", f'{_esc(F.short_pkg(i["pkg"]))} <b>{_esc(F.range_text(i["range"]))}</b>'))
        rows.append(("Fixed in", f"<b>{_esc(fixed)}</b>"))
    elif infos:
        # Several ranges: each one beside its own fix, so they cannot be misread.
        rows.append(("Affected", "".join(
            f'<span class="fs-v">{_esc(F.short_pkg(i["pkg"]))} <b>{_esc(F.range_text(i["range"]))}</b>'
            f'<span class="fs-gap">' + ("no fix listed" if not i["fx"] else "fix unclear in the record" if i["conflict"]
                                         else "fixed in " + _esc(i["label"])) + "</span></span>"
            for i in infos)))
    nodes = ctx["nodes"]
    if nodes:
        rows.append(("Disclosure", "<br>".join(
            (f'<span class="fs-gap">{F.days(nodes[i - 1][0], d)} days later</span>' if i else "")
            + f"<b>{_esc(d)}</b> " + _esc("Published" if lab == "Published by the maintainer" else lab)
            for i, (d, lab) in enumerate(nodes))))
    rows.append(("Advisory", f'<a href="{_esc(a.get("html_url"))}">{_esc(a["ghsa_id"])}</a>'
                 + (f"<br>{_esc(a['cve_id'])}" if a.get("cve_id") else "")))
    if ctx["siblings"]:
        rows.append((f"Also in {_esc(ctx['project'])}", siblings_html(ctx, "<br>")))
    return '<dl class="fs">' + "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in rows) + "</dl>"


def rail_html(a, ctx):
    score, vector, self_assessed = cvss_of(a)
    head = ""
    if score is not None:
        head = (f'<div class="sr-h"><span class="sr-num">{score:.1f}</span>'
                f'<span class="sr-sev">{_esc((a.get("severity") or "").capitalize())}</span></div>'
                f'<p class="sr-src">{_esc(score_label(vector))}{" · my assessment" if self_assessed else ""}</p>')
    return (f'<aside class="srail" aria-label="Fact sheet" data-sev="{_esc((a.get("severity") or "none").lower())}">'
            + head + fact_rows(a, ctx) + '<a class="sr-top" href="#top">Back to top</a></aside>')


def record_html(a, ctx):
    # The heading is left out of the running index: on a wide screen this
    # section is hidden in favour of the margin, and the link would go nowhere.
    return ('<section class="fs-inline" aria-labelledby="h-record">'
            '<h2 id="h-record" class="no-idx">The record</h2>' + fact_rows(a, ctx) + "</section>")


# ── Affected versions, drawn ───────────────────────────────────────
def version_tracks_html(ctx):
    out = []
    for i in (F.vuln_info(v) for v in ctx["vulns"]):
        o = i["o"]
        pkg = _esc(i["pkg"]) + (f'<span class="k-lab">{_esc(i["eco"])}</span>' if i["eco"] else "")
        left = o["eq"] or ((o["lo"] if o["lo_inc"] else "after " + o["lo"]) if o["lo"] else "No lower bound")
        right = "" if o["eq"] else ((o["hi"] if o["hi_inc"] else "before " + o["hi"]) if o["hi"] else "No upper bound")
        lo = bool(o["lo"] or o["eq"])
        bar = ('<div class="vt-pre">Not listed as affected</div>' if lo else "") + \
              f'<div class="vt-bad"><b>{_esc(left)}</b><i>Affected</i><b>{_esc(right)}</b></div>' + \
              (f'<div class="vt-fix">Fixed in <b>{_esc(i["label"])}</b></div>' if i["fx"]
               else '<div class="vt-fix none">No fixed version listed</div>')
        note = ""
        if i["conflict"]:
            note = f'<p class="vt-note"><b>Data conflict</b> The advisory lists {_esc(i["fx"]["v"])} as both affected and fixed.</p>'
        elif i["fx"] and "branches" in i["fx"]:
            note = '<p class="vt-note">One fix per release line. Upgrade within the line you run.</p>'
        out.append(f'<div class="vt" aria-hidden="true"><div class="vt-pkg">{pkg}</div>'
                   f'<div class="vt-bar{"" if lo else " nolo"}">{bar}</div>{note}</div>')
    return "".join(out)


# ── Marked lines in code ───────────────────────────────────────────
# A writeup marks the lines it names as the bug, or as the fix, with a comment
# right above the code fence:  <!-- bug: <text on that line> :: <caption> -->
# The generator finds the one line containing that text and tints it, and sets
# the captions under the block. A ```diff fence is coloured by its own + and -.
_MARK = re.compile(r"^<!-- (bug|fix): (.+?) :: (.+?) -->$")


def _code_block(lang, code, marks):
    lines = code.split("\n")
    indent = min((len(l) - len(l.lstrip(" ")) for l in lines if l.strip()), default=0)
    lines = [l[min(indent, len(l) - len(l.lstrip(" "))):] for l in lines]
    spans, used = [], []
    for line in lines:
        cls = ""
        if lang == "diff" and line.startswith("+") and not line.startswith("+++"):
            cls = " add"
        elif lang == "diff" and line.startswith("-") and not line.startswith("---"):
            cls = " del"
        for kind, text, cap in marks:
            if text in line:
                cls = " " + kind
                used.append((kind, cap))
                break
        spans.append(f'<span class="ln{cls}">{_esc(line) or " "}</span>')
    missing = [t for _k, t, _c in marks if not any(t in l for l in lines)]
    if missing:
        raise SystemExit(f"marked text not found in its code block: {missing}")
    lc = f' class="language-{_esc(lang)}"' if lang else ""
    out = f'<pre class="{"has-mark" if used else "plain"}"><code{lc}>' + "".join(spans) + "</code></pre>"
    if used:
        out += '\n\n<p class="mark-cap">' + "".join(
            f'<span><span class="mark-k{" fix" if k == "fix" else ""}">{"The fix" if k == "fix" else "The bug"}</span>{_esc(c)}</span>'
            for k, c in used) + "</p>"
    return out


def mark_code(text):
    """Rewrite marked and diff fences as pre-rendered blocks; leave the rest."""
    lines, out, i = text.split("\n"), [], 0
    while i < len(lines):
        marks = []
        while i < len(lines) and _MARK.match(lines[i]):
            marks.append(_MARK.match(lines[i]).groups())
            i += 1
        if i < len(lines) and lines[i].startswith("```") and (marks or lines[i].strip() == "```diff"):
            lang = lines[i][3:].strip()
            j = i + 1
            while not lines[j].startswith("```"):
                j += 1
            out.append(_code_block(lang, "\n".join(lines[i + 1:j]), marks))
            i = j + 1
            continue
        if marks:
            raise SystemExit(f"mark comment not directly above a code fence: {marks}")
        out.append(lines[i])
        i += 1
    return "\n".join(out)


def body(a, ctx):
    out = []
    vulns = a.get("vulnerabilities") or []
    if vulns:
        # The drawn tracks are for the eye; the table stays for anything that
        # reads the page as text, hidden from view but not from the tree.
        out += ["### Affected versions", "", f'<div class="vts">{version_tracks_html(ctx)}</div>', "",
                "| Package | Ecosystem | Vulnerable | Fixed in |", "|:--|:--|:--|:--|"]
        for v in vulns:
            pkg = v.get("package") or {}
            # The global advisory DB calls it first_patched_version; the repo
            # endpoint, which serves every advisory listed in advisories.txt,
            # calls it patched_versions. Reading only the first showed "n/a"
            # for fixes that had shipped.
            fixed = v.get("first_patched_version") or v.get("patched_versions")
            out.append(
                f"| `{pkg.get('name','n/a')}` | {pkg.get('ecosystem','n/a')} | "
                f"{v.get('vulnerable_version_range') or 'n/a'} | "
                f"{fixed or 'n/a'} |"
            )
        out += ["{: .vh}", ""]
    # A hand-built figure for this advisory, if one exists. Kept in _figures/
    # rather than spliced into the maintainer's own markdown: that text is
    # theirs and its headings vary, so anchoring to them would be brittle.
    # Sitting here it gives the reader the shape of the chain before the code.
    figure = ROOT / "_figures" / f"{slug(a)}.html"
    if figure.exists():
        out += ['<div markdown="0">', figure.read_text(encoding="utf-8").strip(), "</div>", ""]

    # My own writeup, if one exists for this advisory, replaces the maintainer's
    # published text. The official advisory stays linked in the table above as
    # the record; this page is then my analysis of the finding, in my words and
    # in the site's format. Advisories without a file here fall back to the
    # published text, so the switch is opt in, one advisory at a time.
    own = own_writeup(a)
    if own:
        desc = mark_code(own.read_text(encoding="utf-8").strip())
    else:
        desc = (a.get("description") or "").replace("\r\n", "\n").replace("\r", "\n").strip()
    out += [desc, ""]
    refs = [r for r in (a.get("references") or []) if r != a.get("html_url")]
    if refs:
        heading = "## Advisory references" if "## References" in desc else "## References"
        out += [heading, ""] + [f"* <{r}>" for r in refs] + [""]

    out += [record_html(a, ctx), ""]

    # Attribution and backlinks. Without this the writeups say who the page belongs
    # to only in <title>, so a retrieval pipeline correctly refuses to credit the
    # discovery, and every writeup is a dead end for internal linking.
    pkgs = sorted({v["package"]["name"] for v in a.get("vulnerabilities") or [] if v.get("package")})
    proj = short_package(pkgs[0]) if pkgs else "the"
    out += [
        "## About this writeup",
        "",
        f"Sanaan Fayaz Wani (GitHub [`sfwani`](https://github.com/sfwani)) reported this "
        f"vulnerability to the `{proj}` maintainers under coordinated disclosure and is "
        f"credited as a reporter in [{a['ghsa_id']}]({a.get('html_url')}), published "
        f"{(a.get('published_at') or '')[:10]}.",
        "",
        "All published findings: [advisory index](/advisories/).",
        "",
    ]
    return "\n".join(out)


def yaml_q(v):
    return '"' + str(v).replace('\\', '\\\\').replace('"', '\\"') + '"'


def write_page(a, ctx, stamp):
    name = a.get("cve_id") or a["ghsa_id"]
    summary = summary_of(a)
    desc = describe(a, summary)
    fm = "\n".join([
        "---",
        f"title: {yaml_q(name)}",
        f"heading: {yaml_q(name)}",
        f"role: {yaml_q(summary)}",
        f"seo_title: {yaml_q(f'{name}: {clip(summary, 80)} - Sanaan Fayaz Wani')}",
        f"ghsa_id: {yaml_q(a['ghsa_id'])}",
        f"cve_id: {yaml_q(a.get('cve_id') or '')}",
        f"published_at: {yaml_q((a.get('published_at') or '')[:10])}",
        f"permalink: /advisories/{slug(a)}/",
        "layout: c2",
        f"description: {yaml_q(desc)}",
        f"image: /assets/img/og/{slug(a)}.png",
        f"kicker_repo: {yaml_q(ctx['repo'] or '')}",
        "comments: false",
        f"last_modified_at: {stamp}",
        "---",
        "",
    ])
    p = OUT / f"{slug(a)}.md"
    # Wrapped as a C2 section so the page inherits the grid, the section rule and
    # the measure. The section head that C2 gives every section (a numeral, a
    # heading, a note) is dropped here: a writeup has one section whose heading
    # only ever repeated the advisory id already in the title, the numeral slot
    # fell back to a meaningless dash, and the note floated off the grid beside
    # them. The advisory-header panel takes its place, and the id is kept as a
    # visually hidden h2 so the section still has an accessible name. The h2
    # sits outside .prose on purpose: the running index is built from the prose
    # subheadings, and an h2 inside it would show up as a phantom first entry.
    # markdown="1" keeps kramdown processing the inner text.
    name = _esc(a.get("cve_id") or a["ghsa_id"])
    score = cvss_of(a)[0]
    sev = _esc((a.get("severity") or "none").lower())
    new = fm + (
        # The data attributes feed the score and short advice that ride in the
        # index band once the header has scrolled away.
        f'<section class="sec g" id="writeup" aria-labelledby="h-writeup" data-sev="{sev}"'
        f' data-score="{"" if score is None else f"{score:.1f}"}" data-sevword="{_esc(sev.capitalize())}"'
        f' data-short="{_esc(ctx["action"]["short"])}">\n'
        f'  <h2 id="h-writeup" class="vh">{name}</h2>\n'
        '  ' + advisory_header_html(a, ctx) + '\n'
        '  <div class="col-body prose" markdown="1">\n\n'
        + body(a, ctx) +
        '\n\n  </div>\n  ' + rail_html(a, ctx) + '\n</section>\n')
    old = p.read_text(encoding="utf-8") if p.exists() else None
    if old is not None:
        # Keep the existing stamp when only the stamp would change.
        if re.sub(r"^last_modified_at:.*$", "", old, flags=re.M) == \
           re.sub(r"^last_modified_at:.*$", "", new, flags=re.M):
            return False
    p.write_text(new, encoding="utf-8")
    return True


def write_index(rows, stamp):
    """Disabled: /advisories/ is now a C2 page in the repo, and its record is
    spliced by update_advisories.py between the RECORD markers. Two writers for
    one file is exactly how the three-surface drift used to happen."""
    return

def write_llms_txt(rows):
    """Generate /llms.txt from the same advisory rows as everything else.

    Generated rather than hand written so it cannot drift from the site. See
    the note in the repo README about how much weight to put on this file.
    """
    rows = sorted(rows, key=lambda a: (a.get("published_at") or ""), reverse=True)
    # Derived from the same rows as everything else, so the counts cannot drift
    # from the table the way a hand-written number did.
    n_pub = len(rows)
    n_cve = len({a.get("cve_id") for a in rows if a.get("cve_id")})
    out = [
        "# Sanaan Fayaz Wani",
        "",
        "> Security Engineer at Amazon working in IAM security and agentic AI, and an "
        f"independent vulnerability researcher. {n_cve} assigned CVEs and {n_pub} published, "
        "credited security advisories against AI agent frameworks and the infrastructure "
        "that runs large language models, from 167 advisories filed across 59 open source "
        "projects.",
        "",
        "Every advisory below is published and credited to Sanaan Fayaz Wani "
        "(GitHub: sfwani). Each page carries the root cause, the vulnerable code, "
        "reproduction steps and the fix.",
        "",
        "## Pages",
        "",
        f"- [Home]({SITE}/): bio, the advisory table, the weakness class breakdown, "
        "roles, certifications and competition record.",
        f"- [Advisories]({SITE}/advisories/): index of all published advisories.",
        "",
        "## Published advisories",
        "",
    ]
    for a in rows:
        name = a.get("cve_id") or a["ghsa_id"]
        score, _v, self_assessed = cvss_of(a)
        sev = (a.get("severity") or "").capitalize()
        if score is None:
            rating = f"{sev}, no published score"
        else:
            rating = f"{score:.1f} {sev}"
        pkgs = sorted({v["package"]["name"] for v in a.get("vulnerabilities") or [] if v.get("package")})
        pkg = short_package(pkgs[0]) if pkgs else "n/a"
        cwe = (a.get("cwes") or [{}])[0].get("cwe_id") or "n/a"
        out.append(f"- [{name}]({SITE}/advisories/{slug(a)}/): {pkg}, {rating}, {cwe}. "
                   f"Published {(a.get('published_at') or '')[:10]}. "
                   f"Advisory of record: {a.get('html_url')}")
    out.append("")
    (ROOT / "llms.txt").write_text("\n".join(out), encoding="utf-8")


def contexts(s, rows):
    """Per advisory: the repository, the disclosure dates, the affected records,
    what to do, and the other advisories on the same project."""
    out = {}
    for a in rows:
        d = F.disclosure_facts(s, a, a.get("_repo"))
        vulns = F.vulns_of(a)
        out[a["ghsa_id"]] = dict(d, vulns=vulns, action=F.action(vulns),
                                 nodes=F.disclosure(d, (a.get("published_at") or "")[:10] or None),
                                 project=(d["repo"] or "").split("/")[-1] or facts_of(a)[0])
    for a in rows:
        c = out[a["ghsa_id"]]
        sib = [b for b in rows if b is not a and c["repo"] and out[b["ghsa_id"]]["repo"] == c["repo"]]
        sib.sort(key=lambda b: (b.get("published_at") or ""), reverse=True)
        c["siblings"] = [(slug(b), b.get("cve_id") or b["ghsa_id"],
                          "" if cvss_of(b)[0] is None else f"{cvss_of(b)[0]:.1f}") for b in sib]
    return out


def write_cards(rows):
    """A link preview per advisory, plus the homepage's, from the same rows."""
    og = ROOT / "assets" / "img" / "og"
    og.mkdir(parents=True, exist_ok=True)
    for a in rows:
        project, score, sev, scheme, cwe = facts_of(a)
        og_cards.advisory_card(og / f"{slug(a)}.png", a.get("cve_id") or a["ghsa_id"],
                               project, summary_of(a), score, sev, scheme, cwe)
    figs = [
        (len({a.get("cve_id") for a in rows if a.get("cve_id")}), "CVEs assigned"),
        (len(rows), "Advisories published"),
        # Counted exactly as the homepage counter counts them.
        (len({project_of(min(v["package"]["name"] for v in a["vulnerabilities"] if v.get("package")))
              for a in rows if any(v.get("package") for v in a.get("vulnerabilities") or [])}),
         "Projects credited"),
    ]
    og_cards.home_card(ROOT / "assets" / "img" / "ogp.png", figs)


def write_feed(rows):
    """/feed.xml, an Atom feed of the published advisories, newest first.
    Dated by publication, never by build, so a rebuild does not re-announce."""
    rows = sorted(rows, key=lambda a: (a.get("published_at") or ""), reverse=True)
    x = html.escape

    def when(a):
        return f"{(a.get('published_at') or '')[:10]}T00:00:00Z"

    out = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<feed xmlns="http://www.w3.org/2005/Atom">',
        "  <title>Sanaan Fayaz Wani: published advisories</title>",
        "  <subtitle>Credited security advisories in AI agent frameworks and LLM infrastructure.</subtitle>",
        f'  <link href="{SITE}/feed.xml" rel="self"/>',
        f'  <link href="{SITE}/advisories/"/>',
        f"  <id>{SITE}/advisories/</id>",
        f"  <updated>{when(rows[0])}</updated>",
        "  <author><name>Sanaan Fayaz Wani</name><uri>https://github.com/sfwani</uri></author>",
    ]
    for a in rows:
        name = a.get("cve_id") or a["ghsa_id"]
        url = f"{SITE}/advisories/{slug(a)}/"
        s = summary_of(a)
        out += [
            "  <entry>",
            f"    <title>{x(name)}: {x(s)}</title>",
            f'    <link href="{url}"/>',
            f"    <id>{url}</id>",
            f"    <published>{when(a)}</published>",
            f"    <updated>{when(a)}</updated>",
            f"    <summary>{x(describe(a, s))}</summary>",
            "  </entry>",
        ]
    out += ["</feed>", ""]
    (ROOT / "feed.xml").write_text("\n".join(out), encoding="utf-8")


def main():
    OUT.mkdir(exist_ok=True)
    s = session()
    stamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    rows, seen = [], set()
    for gid in credited_ghsa_ids(s):
        a = raw_global(s, gid)
        if a:
            rows.append(a)
            seen.add(a["ghsa_id"])
    for repo, gid in extra_repo_advisories():
        if gid in seen:
            continue
        a = raw_repo_level(s, repo, gid)
        if a:
            a["_repo"] = repo
            rows.append(a)
            seen.add(gid)
    if not rows:
        raise SystemExit("no advisories resolved, refusing to write empty pages")
    ctxs = contexts(s, rows)
    changed = sum(write_page(a, ctxs[a["ghsa_id"]], stamp) for a in rows)
    write_index(list(rows), stamp)
    write_llms_txt(rows)
    write_feed(rows)
    write_cards(rows)
    print(f"{len(rows)} advisories, {changed} pages written or updated", file=sys.stderr)


if __name__ == "__main__":
    main()
