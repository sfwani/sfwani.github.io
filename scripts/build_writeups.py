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
        sev += f" ({score:.1f})"
        vec_cell = f"`{vector}`"
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
        # Where the score is not GitHub's, say so once, here, in plain prose.
        # It is off every index and every figure because repeating it read as
        # a disclaimer, but the number still has to be attributable somewhere
        # and this is the page a reader checking it would open.
        *([] if not self_assessed else [
            f"GitHub published this advisory as {(a.get('severity') or '').capitalize()} "
            "with no CVSS score and no vector, in v3 or v4. The score and vector above are "
            "my own assessment of the finding as published.",
            "",
        ]),
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
    # A hand-built figure for this advisory, if one exists. Kept in _figures/
    # rather than spliced into the maintainer's own markdown: that text is
    # theirs and its headings vary, so anchoring to them would be brittle.
    # Sitting here it gives the reader the shape of the chain before the code.
    figure = ROOT / "_figures" / f"{slug(a)}.html"
    if figure.exists():
        out += ['<div markdown="0">', figure.read_text(encoding="utf-8").strip(), "</div>", ""]

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
        "All published findings: [advisory index](/advisories/).",
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
        f"heading: {yaml_q(name)}",
        f"role: {yaml_q(summary)}",
        f"seo_title: {yaml_q(f'{name}: {clip(summary, 80)} - Sanaan Fayaz Wani')}",
        f"ghsa_id: {yaml_q(a['ghsa_id'])}",
        f"cve_id: {yaml_q(a.get('cve_id') or '')}",
        f"published_at: {yaml_q((a.get('published_at') or '')[:10])}",
        f"permalink: /advisories/{slug(a)}/",
        "layout: c2",
        f"description: {yaml_q(desc)}",
        "comments: false",
        f"last_modified_at: {stamp}",
        "---",
        "",
    ])
    p = OUT / f"{slug(a)}.md"
    # Wrapped as a C2 section so the page inherits the grid, the section rule
    # and the measure. markdown="1" keeps kramdown processing the inner text.
    new = fm + (
        '<section class="sec g" id="writeup" aria-labelledby="h-writeup">\n'
        '  <div class="sec-head">\n'
        '    <p class="idx idx--none">\u2014</p>\n'
        f'    <h2 id="h-writeup">{a["ghsa_id"]}</h2>\n'
        '    <p class="sec-sub">Published, fixed and credited. Root cause, the vulnerable code, '
        'reproduction and the fix, as published in the advisory itself.</p>\n'
        '  </div>\n'
        '  <div class="col-body prose" markdown="1">\n\n'
        + body(a) +
        '\n\n  </div>\n</section>\n')
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
