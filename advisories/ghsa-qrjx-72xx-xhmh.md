---
title: "GHSA-qrjx-72xx-xhmh"
heading: "GHSA-qrjx-72xx-xhmh"
role: "Path Traversal in DiskKnowledgeStore via Incorrect startswith Path Containment Check"
seo_title: "GHSA-qrjx-72xx-xhmh: Path Traversal in DiskKnowledgeStore via Incorrect startswith Path Containment… - Sanaan Fayaz Wani"
ghsa_id: "GHSA-qrjx-72xx-xhmh"
cve_id: ""
published_at: "2026-09-25"
permalink: /advisories/ghsa-qrjx-72xx-xhmh/
layout: c2
description: "Path Traversal in DiskKnowledgeStore via Incorrect startswith Path Containment Check. ag2, CVSS 8.1 High, CWE-22 Path traversal. Writeup by Sanaan Fayaz Wani, the credited reporter."
image: /assets/img/og/ghsa-qrjx-72xx-xhmh.png
kicker_repo: "ag2ai/ag2"
comments: false
last_modified_at: 2026-10-24T23:51:00+00:00
---
<section class="sec g" id="writeup" aria-labelledby="h-writeup" data-sev="high" data-score="8.1" data-sevword="High" data-short="Fix differs by range">
  <h2 id="h-writeup" class="vh">GHSA-qrjx-72xx-xhmh</h2>
  <div class="ah" data-sev="high"><div class="ah-score"><p class="ah-num">8.1</p><p class="ah-sev">High</p><p class="ah-of">CVSS 3.1 base</p><p class="ah-tag">My assessment</p><div class="ah-meter" aria-hidden="true"><i style="width:81%"></i></div><ol class="tlv" aria-label="Disclosure timeline"><li><b>2026-05-22</b><span>Reported privately</span></li><li><span class="tlv-d">126 days later</span><b>2026-09-25</b><span>Published by the maintainer</span></li></ol></div><div class="act warn"><p class="act-k">What to do</p><p class="act-v multi">If you run <b>ag2</b> <b>0.12.2 to before 1.1.0</b>, upgrade to <b>1.1.0</b> or later.<br>If you run <b>autogen</b> <b>0.12.2 to 0.14.1</b>, no fixed version is listed in the advisory.</p></div><p class="ts"><em>Anyone who can reach it over the network</em>, with <em>a low-privilege account</em> and no user interaction, can <em>read and change sensitive data</em>.<span class="ts-src">Read from the CVSS 3.1 vector</span></p><div class="bx" style="--n:4"><div class="bx-head"><span class="k-lab">CVSS 3.1 metrics</span></div><div class="bx-row"><p class="bx-g">To exploit it</p><dl class="bx-grid"><div class="bx-c"><dt>Attack vector</dt><dd>Network</dd></div><div class="bx-c"><dt>Attack complexity</dt><dd>Low</dd></div><div class="bx-c"><dt>Privileges required</dt><dd>Low</dd></div><div class="bx-c"><dt>User interaction</dt><dd>None</dd></div></dl></div><div class="bx-row"><p class="bx-g">What it gets</p><dl class="bx-grid"><div class="bx-c"><dt>Confidentiality</dt><dd>High</dd></div><div class="bx-c"><dt>Integrity</dt><dd>High</dd></div><div class="bx-c"><dt>Availability</dt><dd>None</dd></div><div class="bx-c"><dt>Scope</dt><dd>Unchanged</dd></div></dl></div><p class="bx-foot"><a href="https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N" rel="noopener">Open this vector in the FIRST calculator &#8599;</a></p></div><dl class="meta"><div class="meta-i wide"><dt class="k-lab">Weakness</dt><dd class="meta-v"><abbr title="Improper Limitation of a Pathname to a Restricted Directory (&#x27;Path Traversal&#x27;)">CWE-22</abbr> <span class="meta-s">Improper Limitation of a Pathname to a Restricted Directory (&#x27;Path Traversal&#x27;)</span></dd></div><div class="meta-i"><dt class="k-lab">Advisory</dt><dd class="meta-v"><a href="https://github.com/ag2ai/ag2/security/advisories/GHSA-qrjx-72xx-xhmh">GHSA-qrjx-72xx-xhmh</a></dd></div><div class="meta-i"><dt class="k-lab">CVE</dt><dd class="meta-v">not assigned</dd></div><div class="meta-i"><dt class="k-lab">Vector</dt><dd class="meta-v"><span class="vec">CVSS:3.1/<wbr>AV:N/<wbr>AC:L/<wbr>PR:L/<wbr>UI:N/<wbr>S:U/<wbr>C:H/<wbr>I:H/<wbr>A:N</span></dd></div><div class="meta-i wide"><dt class="k-lab">Also in ag2</dt><dd class="meta-v"><a href="/advisories/ghsa-42mf-vpmr-gw5r/">GHSA-42mf-vpmr-gw5r</a> 9.9</dd></div></dl><div class="tl" role="group" aria-label="Disclosure timeline"><div class="tl-n"><b>2026-05-22</b><span>Reported privately</span></div><div class="tl-seg"><span>126 days</span></div><div class="tl-n"><b>2026-09-25</b><span>Published by the maintainer</span></div></div><p class="ah-note">My analysis of this finding: root cause, the vulnerable code, the impact and the fix, in the site’s format. The official advisory of record is linked above.</p><p class="ah-note ah-note--disc">GitHub published this advisory as High with no CVSS score and no vector, in v3 or v4. The score and vector above are my own assessment of the finding, within the severity band GitHub published. Where GitHub publishes a numeric score, this page shows that one instead.</p></div>
  <div class="col-body prose" markdown="1">

### Affected versions

<div class="vts"><div class="vt" aria-hidden="true"><div class="vt-pkg">ag2<span class="k-lab">pip</span></div><div class="vt-bar"><div class="vt-pre">Not listed as affected</div><div class="vt-bad"><b>0.12.2</b><i>Affected</i><b>before 1.1.0</b></div><div class="vt-fix">Fixed in <b>1.1.0</b></div></div></div><div class="vt" aria-hidden="true"><div class="vt-pkg">autogen<span class="k-lab">pip</span></div><div class="vt-bar"><div class="vt-pre">Not listed as affected</div><div class="vt-bad"><b>0.12.2</b><i>Affected</i><b>0.14.1</b></div><div class="vt-fix none">No fixed version listed</div></div></div></div>

| Package | Ecosystem | Vulnerable | Fixed in |
|:--|:--|:--|:--|
| `ag2` | pip | >= 0.12.2, < 1.1.0 | 1.1.0 |
| `autogen` | pip | >= 0.12.2, <= 0.14.1 | n/a |
{: .vh}

## Summary

AG2's beta `DiskKnowledgeStore` maps agent-supplied virtual paths onto real files under a root directory, and tries to keep every operation inside that root with a single containment check. The check compares the resolved path against the root with `str.startswith`, which is a classic path-confinement anti-pattern: a sibling directory whose name merely shares a prefix with the root satisfies the test. So a path like `../store_evil/secret.txt` resolves outside the intended root yet passes validation, and every read, write, list, delete, and append in the store inherits the hole.

## Where it lives

The containment logic is one line in `autogen/beta/knowledge/disk.py`, inside `_resolve()`:

<pre class="has-mark"><code class="language-python"><span class="ln">def _resolve(self, path: str) -&gt; Path:</span><span class="ln">    &quot;&quot;&quot;Map virtual path to real filesystem path.&quot;&quot;&quot;</span><span class="ln">    normalized = _normalize(path).lstrip(&quot;/&quot;)</span><span class="ln">    resolved = (self._root / normalized).resolve() if normalized else self._root.resolve()</span><span class="ln bug">    if not str(resolved).startswith(str(self._root.resolve())):</span><span class="ln">        raise ValueError(f&quot;Path traversal blocked: {path}&quot;)</span><span class="ln">    return resolved</span></code></pre>

<p class="mark-cap"><span><span class="mark-k">The bug</span>string prefix check lets prefix-sharing sibling directories through</span></p>

`_resolve()` is the single gate for the whole store: `read`, `write`, `list`, `delete`, `exists`, `append`, `read_range`, and `on_change` all route their path argument through it. Whatever `_resolve()` lets out, those methods will operate on.

The rest of the codebase already knows the right way to do this. `is_relative_to()` is the correct, prefix-safe containment check, and it is used elsewhere for exactly this purpose (for example `filesystem.py:246` and `apply_patch_tool.py:245`), making `disk.py` the outlier.

## Impact

With `root="/data/store"`, the virtual path `../store_evil/secret.txt` resolves to `/data/store_evil/secret.txt`. The guard asks whether `"/data/store_evil/secret.txt".startswith("/data/store")`, which is `True`, so the traversal is "blocked" only in name. The caller then reads, overwrites, or deletes a file in a directory that was never meant to be reachable.

Because `_resolve()` backs every operation, the primitive is read and write and delete, not read alone. An attacker who influences the path an agent passes to the knowledge store can exfiltrate files from, or clobber files in, any sibling directory sharing the root's name prefix, escaping the sandbox the store is supposed to provide.

I verified this against a faithful copy of the vulnerable `_resolve()`: the traversal path was accepted, resolved into a sibling directory, and read back a planted secret file, while the `is_relative_to()` version rejected the same path.

## Fix

Replace the `startswith` test with a true ancestor check:

<pre class="has-mark"><code class="language-python"><span class="ln fix">if not resolved.is_relative_to(self._root.resolve()):</span><span class="ln">    raise ValueError(f&quot;Path traversal blocked: {path}&quot;)</span></code></pre>

<p class="mark-cap"><span><span class="mark-k fix">The fix</span>compares path components instead of string prefixes</span></p>

`Path.is_relative_to` compares path components rather than string prefixes, so `/data/store_evil` is correctly recognized as outside `/data/store`. This matches what the project already does in `filesystem.py` and `apply_patch_tool.py`.

<section class="fs-inline" aria-labelledby="h-record"><h2 id="h-record" class="no-idx">The record</h2><dl class="fs"><dt>Weakness</dt><dd><b>CWE-22</b> Improper Limitation of a Pathname to a Restricted Directory (&#x27;Path Traversal&#x27;)</dd><dt>Affected</dt><dd><span class="fs-v">ag2 <b>0.12.2 to before 1.1.0</b><span class="fs-gap">fixed in 1.1.0</span></span><span class="fs-v">autogen <b>0.12.2 to 0.14.1</b><span class="fs-gap">no fix listed</span></span></dd><dt>Disclosure</dt><dd><b>2026-05-22</b> Reported privately<br><span class="fs-gap">126 days later</span><b>2026-09-25</b> Published</dd><dt>Advisory</dt><dd><a href="https://github.com/ag2ai/ag2/security/advisories/GHSA-qrjx-72xx-xhmh">GHSA-qrjx-72xx-xhmh</a></dd><dt>Also in ag2</dt><dd><a href="/advisories/ghsa-42mf-vpmr-gw5r/">GHSA-42mf-vpmr-gw5r</a> 9.9</dd></dl></section>

## About this writeup

Sanaan Fayaz Wani (GitHub [`sfwani`](https://github.com/sfwani)) reported this vulnerability to the `ag2` maintainers under coordinated disclosure and is credited as a reporter in [GHSA-qrjx-72xx-xhmh](https://github.com/ag2ai/ag2/security/advisories/GHSA-qrjx-72xx-xhmh), published 2026-09-25.

All published findings: [advisory index](/advisories/).


  </div>
  <aside class="srail" aria-label="Fact sheet" data-sev="high"><div class="sr-h"><span class="sr-num">8.1</span><span class="sr-sev">High</span></div><p class="sr-src">CVSS 3.1 base · my assessment</p><dl class="fs"><dt>Weakness</dt><dd><b>CWE-22</b> Improper Limitation of a Pathname to a Restricted Directory (&#x27;Path Traversal&#x27;)</dd><dt>Affected</dt><dd><span class="fs-v">ag2 <b>0.12.2 to before 1.1.0</b><span class="fs-gap">fixed in 1.1.0</span></span><span class="fs-v">autogen <b>0.12.2 to 0.14.1</b><span class="fs-gap">no fix listed</span></span></dd><dt>Disclosure</dt><dd><b>2026-05-22</b> Reported privately<br><span class="fs-gap">126 days later</span><b>2026-09-25</b> Published</dd><dt>Advisory</dt><dd><a href="https://github.com/ag2ai/ag2/security/advisories/GHSA-qrjx-72xx-xhmh">GHSA-qrjx-72xx-xhmh</a></dd><dt>Also in ag2</dt><dd><a href="/advisories/ghsa-42mf-vpmr-gw5r/">GHSA-42mf-vpmr-gw5r</a> 9.9</dd></dl><a class="sr-top" href="#top">Back to top</a></aside>
</section>
