#!/usr/bin/env python3
"""Generate one page per published advisory, plus the /advisories/ index.

Source of truth is the same as update_advisories.py: the public credit search
plus advisories.txt for repo level advisories the global database never got.
Nothing unpublished can appear here, because both paths gate on state ==
published and on this user's credit being accepted.

Run: python3 scripts/build_writeups.py
"""

import pathlib
import re
import sys
from datetime import datetime, timezone

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from update_advisories import (  # noqa: E402
    API, USER, session, credited_ghsa_ids, extra_repo_advisories, CWE_LABELS,
    short_package,
    render_chart,
    # The derived score for the one advisory published without one lives in
    # the sibling generator, so the two pages this repo builds cannot
    # disagree about it.
    cvss_of,
)

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "advisories"
SITE = "https://sfwani.github.io"


def raw_global(s, ghsa_id):
    r = s.get(f"{API}/advisories/{ghsa_id}", timeout=30)
    if r.status_code != 200:
        print(f"skip {ghsa_id}: HTTP {r.status_code}", file=sys.stderr)
        return None
    a = r.json()
    return None if a.get("withdrawn_at") else a


def raw_repo_level(s, repo, ghsa_id):
    """Only an advisory that is published and where USER credit is accepted."""
    r = s.get(f"{API}/repos/{repo}/security-advisories/{ghsa_id}", timeout=30)
    if r.status_code != 200:
        print(f"skip {ghsa_id}: HTTP {r.status_code}", file=sys.stderr)
        return None
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


def body(a):
    score, vector, self_assessed = cvss_of(a)
    cwes = ", ".join(f"{c['cwe_id']} ({c['name']})" for c in a.get("cwes") or []) or "n/a"
    sev = (a.get("severity") or "").capitalize()
    if score is None:
        sev += " (no CVSS score published)"
        vec_cell = "`not published`"
    elif self_assessed:
        sev += f" ({score:.1f}, self-assessed)"
        vec_cell = f"`{vector}` (self-assessed)"
    else:
        sev += f" ({score})"
        vec_cell = f"`{vector}`"
    out = [
        "| | |",
        "|:--|:--|",
        f"| Advisory | [{a['ghsa_id']}]({a.get('html_url')}) |",
        f"| CVE | {a.get('cve_id') or 'not assigned'} |",
        f"| Severity | {sev} |",
        f"| CVSS vector | {vec_cell} |",
        f"| CWE | {cwes} |",
        f"| Published | {(a.get('published_at') or '')[:10]} |",
        "",
    ]
    vulns = a.get("vulnerabilities") or []
    if vulns:
        out += ["### Affected versions", "",
                "| Package | Ecosystem | Vulnerable | Fixed in |", "|:--|:--|:--|:--|"]
        for v in vulns:
            pkg = v.get("package") or {}
            out.append(
                f"| `{pkg.get('name','n/a')}` | {pkg.get('ecosystem','n/a')} | "
                f"{v.get('vulnerable_version_range') or 'n/a'} | "
                f"{v.get('first_patched_version') or 'n/a'} |"
            )
        out.append("")
    desc = (a.get("description") or "").replace("\r\n", "\n").replace("\r", "\n")
    out += [desc.strip(), ""]
    refs = [r for r in (a.get("references") or []) if r != a.get("html_url")]
    if refs:
        heading = "## Advisory references" if "## References" in desc else "## References"
        out += [heading, ""] + [f"* <{r}>" for r in refs] + [""]

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
        "All published findings: [advisory index](/advisories/). "
        "About the researcher: [about](/about/) and [experience](/experience/).",
        "",
    ]
    return "\n".join(out)


def yaml_q(v):
    return '"' + str(v).replace('\\', '\\\\').replace('"', '\\"') + '"'


def write_page(a, stamp):
    name = a.get("cve_id") or a["ghsa_id"]
    summary = re.sub(r"\s+", " ", (a.get("summary") or "").strip())
    desc = summary[:200]
    fm = "\n".join([
        "---",
        f"title: {yaml_q(name)}",
        f"heading: {yaml_q(f'{name}: {summary}')}",
        f"seo_title: {yaml_q(f'{name}: {clip(summary, 80)} - Sanaan Fayaz Wani')}",
        f"ghsa_id: {yaml_q(a['ghsa_id'])}",
        f"cve_id: {yaml_q(a.get('cve_id') or '')}",
        f"published_at: {yaml_q((a.get('published_at') or '')[:10])}",
        f"permalink: /advisories/{slug(a)}/",
        "layout: page",
        f"description: {yaml_q(desc)}",
        "comments: false",
        f"last_modified_at: {stamp}",
        "---",
        "",
    ])
    p = OUT / f"{slug(a)}.md"
    new = fm + body(a)
    old = p.read_text(encoding="utf-8") if p.exists() else None
    if old is not None:
        # Keep the existing stamp when only the stamp would change.
        if re.sub(r"^last_modified_at:.*$", "", old, flags=re.M) == \
           re.sub(r"^last_modified_at:.*$", "", new, flags=re.M):
            return False
    p.write_text(new, encoding="utf-8")
    return True


def write_index(rows, stamp):
    rows.sort(key=lambda a: (a.get("published_at") or ""), reverse=True)
    lines = [
        "---",
        "title: Advisories",
        "permalink: /advisories/",
        "layout: page",
        'description: "Full writeups for every published security advisory credited to '
        'Sanaan Wani: root cause, vulnerable code, reproduction and fix."',
        "comments: false",
        f"last_modified_at: {stamp}",
        "---",
        "",
        "Every advisory below is published, fixed and credited. Each page carries the root "
        "cause, the vulnerable code, reproduction steps and the fix, as published in the "
        "advisory itself. Reports still in coordinated disclosure are not listed, named or "
        "hinted at until the maintainer ships a fix.",
        "",
        "Five of these are in the global GitHub Advisory Database and are returned by the "
        "[public credit search](https://github.com/advisories?query=credit%3Asfwani). The "
        "others are repository level advisories that the maintainer published and credited "
        "but never forwarded to the global database, so that search cannot see them. Each "
        "row links to its own advisory, where the credit is visible.",
        "",
    ]
    # Same T1 ledger table as the home page: five columns do not fit the prose
    # measure, so it breaks out where there is room and scrolls in a labelled
    # region where there is not, instead of silently wrapping or silently
    # clipping. Markup is built here rather than as a markdown table because
    # kramdown cannot express the wrapper or the scoped column classes.
    import html as _html

    def esc(x):
        return _html.escape(str(x), quote=True)

    body = []
    any_self = False
    for a in rows:
        name = a.get("cve_id") or a["ghsa_id"]
        score, _v, self_assessed = cvss_of(a)
        any_self = any_self or self_assessed
        sev = (a.get("severity") or "").capitalize()
        if score is None:
            cvss = '<span class="adv-none">not scored</span>'
        else:
            mark = ('<abbr title="Scored by me, not by the coordinating database">&dagger;</abbr>'
                    if self_assessed else "")
            cvss = f"{score:.1f}{mark}"
        pkgs = sorted({v["package"]["name"] for v in a.get("vulnerabilities") or []
                       if v.get("package")})
        pkg = short_package(pkgs[0]) if pkgs else "n/a"
        cwe = (a.get("cwes") or [{}])[0].get("cwe_id")
        cls = CWE_LABELS.get(cwe, cwe or "n/a")
        if cwe and cls != cwe:
            cls = f"{cls} ({cwe})"
        pub = (a.get("published_at") or "")[:10]
        body.append(
            f'<tr><th scope="row"><a href="/advisories/{slug(a)}/">{esc(name)}</a></th>'
            f"<td><code>{esc(pkg)}</code></td>"
            f'<td class="adv-num">{cvss}</td>'
            f"<td>{esc(sev)}</td>"
            f"<td>{esc(cls)}</td>"
            f'<td><time datetime="{esc(pub)}">{esc(pub)}</time></td></tr>')

    n = len(rows)
    foot = ""
    if any_self:
        foot = ('<p class="adv-ledgertable__foot">&dagger; Scored by me, not by the coordinating '
                "database. That advisory was published with a severity but no CVSS score and no "
                "vector, in v3 or v4; the score shown is my own CVSS v3.1 base score derived from "
                "the published finding, and its vector is on its page.</p>")
    lines += [
        '<div class="adv-ledgertable" markdown="0">'
        f'<p class="adv-ledgertable__note">{n} published '
        f"{'advisory' if n == 1 else 'advisories'}."
        '<span class="adv-ledgertable__hint"> The table scrolls sideways.</span></p>'
        '<div class="adv-ledgertable__scroll" role="region" tabindex="0" '
        'aria-label="Published advisories">'
        '<table><thead><tr><th scope="col">Advisory</th><th scope="col">Project</th>'
        '<th scope="col">CVSS</th><th scope="col">Severity</th>'
        '<th scope="col">Weakness</th><th scope="col">Published</th></tr></thead>'
        f'<tbody>{"".join(body)}</tbody></table></div>{foot}</div>',
        "",
        # No markdown heading here: the specimen carries its own, and an h2 at
        # the prose measure above a figure at the breakout width reads as a
        # misalignment.
        # The specimen lives here rather than on the home page: it is the same
        # eleven advisories as the table directly above it, so this is where a
        # reader already has the context for it, and here it can use the full
        # breakout width instead of being squeezed into the prose measure.
        render_chart([{
            "vector": cvss_of(a)[1],
            "score": cvss_of(a)[0],
            "self_assessed": cvss_of(a)[2],
            "severity": (a.get("severity") or "").capitalize(),
            "cve_id": a.get("cve_id"),
            "ghsa_id": a["ghsa_id"],
            "package": (sorted({v["package"]["name"] for v in a.get("vulnerabilities") or []
                                if v.get("package")}) or ["n/a"])[0],
            "url": f"/advisories/{slug(a)}/",
        } for a in rows]),
        "",
    ]
    (ROOT / "advisories.md").write_text("\n".join(lines), encoding="utf-8")


def write_llms_txt(rows):
    """Generate /llms.txt from the same advisory rows as everything else.

    Generated rather than hand written so it cannot drift from the site. See
    the note in the repo README about how much weight to put on this file.
    """
    rows = sorted(rows, key=lambda a: (a.get("published_at") or ""), reverse=True)
    out = [
        "# Sanaan Fayaz Wani",
        "",
        "> Security Engineer at Amazon working in IAM security and agentic AI, and an "
        "independent vulnerability researcher. Seven assigned CVEs and eleven published, "
        "credited security advisories against AI agent frameworks and the infrastructure "
        "that runs large language models, from 167 advisories filed across 59 open source "
        "projects.",
        "",
        "Every advisory below is published, fixed and credited to Sanaan Fayaz Wani "
        "(GitHub: sfwani). Each page carries the root cause, the vulnerable code, "
        "reproduction steps and the fix.",
        "",
        "## Pages",
        "",
        f"- [Home]({SITE}/): bio, the advisory table and the weakness class breakdown.",
        f"- [About]({SITE}/about/): research focus, method and coordinated disclosure practice.",
        f"- [Experience]({SITE}/experience/): roles at Amazon and Cyber Florida, University of "
        "South Florida degree, certifications and competition record.",
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
            rating = f"{score:.1f} {sev}" + (", score self-assessed" if self_assessed else "")
        pkgs = sorted({v["package"]["name"] for v in a.get("vulnerabilities") or [] if v.get("package")})
        pkg = short_package(pkgs[0]) if pkgs else "n/a"
        cwe = (a.get("cwes") or [{}])[0].get("cwe_id") or "n/a"
        out.append(f"- [{name}]({SITE}/advisories/{slug(a)}/): {pkg}, {rating}, {cwe}. "
                   f"Published {(a.get('published_at') or '')[:10]}. "
                   f"Advisory of record: {a.get('html_url')}")
    out.append("")
    (ROOT / "llms.txt").write_text("\n".join(out), encoding="utf-8")


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
            rows.append(a)
            seen.add(gid)
    if not rows:
        raise SystemExit("no advisories resolved, refusing to write empty pages")
    changed = sum(write_page(a, stamp) for a in rows)
    write_index(list(rows), stamp)
    write_llms_txt(rows)
    print(f"{len(rows)} advisories, {changed} pages written or updated", file=sys.stderr)


if __name__ == "__main__":
    main()
