---
title: "GHSA-42mf-vpmr-gw5r"
heading: "GHSA-42mf-vpmr-gw5r"
role: "Command Filter Bypass in LocalShellEnvironment via shell=True Allows Arbitrary OS Command Execution"
seo_title: "GHSA-42mf-vpmr-gw5r: Command Filter Bypass in LocalShellEnvironment via shell=True Allows Arbitrary… - Sanaan Fayaz Wani"
ghsa_id: "GHSA-42mf-vpmr-gw5r"
cve_id: ""
published_at: "2026-10-03"
permalink: /advisories/ghsa-42mf-vpmr-gw5r/
layout: c2
description: "Command Filter Bypass in LocalShellEnvironment via shell=True Allows Arbitrary OS Command Execution. ag2, CVSS 9.9 Critical, CWE-78 Command injection. Writeup by Sanaan Fayaz Wani, the credited reporter."
image: /assets/img/og/ghsa-42mf-vpmr-gw5r.png
kicker_repo: "ag2ai/ag2"
comments: false
last_modified_at: 2026-10-24T23:51:00+00:00
---
<section class="sec g" id="writeup" aria-labelledby="h-writeup" data-sev="critical" data-score="9.9" data-sevword="Critical" data-short="Upgrade to 1.1.2">
  <h2 id="h-writeup" class="vh">GHSA-42mf-vpmr-gw5r</h2>
  <div class="ah" data-sev="critical"><div class="ah-score"><p class="ah-num">9.9</p><p class="ah-sev">Critical</p><p class="ah-of">CVSS 3.1 base</p><p class="ah-tag">My assessment</p><div class="ah-meter" aria-hidden="true"><i style="width:99%"></i></div><ol class="tlv" aria-label="Disclosure timeline"><li><b>2026-05-22</b><span>Reported privately</span></li><li><span class="tlv-d">134 days later</span><b>2026-10-03</b><span>Published by the maintainer</span></li></ol></div><div class="act"><p class="act-k">What to do</p><p class="act-v">If you run <b>ag2</b> <b>1.0.0 to before 1.1.2</b>, upgrade to <b>1.1.2</b> or later.</p></div><p class="ts"><em>Anyone who can reach it over the network</em>, with <em>a low-privilege account</em> and no user interaction, can <em>read and change sensitive data and make it unavailable</em>, and <em>the impact reaches beyond the vulnerable component</em>.<span class="ts-src">Read from the CVSS 3.1 vector</span></p><div class="bx" style="--n:4"><div class="bx-head"><span class="k-lab">CVSS 3.1 metrics</span></div><div class="bx-row"><p class="bx-g">To exploit it</p><dl class="bx-grid"><div class="bx-c"><dt>Attack vector</dt><dd>Network</dd></div><div class="bx-c"><dt>Attack complexity</dt><dd>Low</dd></div><div class="bx-c"><dt>Privileges required</dt><dd>Low</dd></div><div class="bx-c"><dt>User interaction</dt><dd>None</dd></div></dl></div><div class="bx-row"><p class="bx-g">What it gets</p><dl class="bx-grid"><div class="bx-c"><dt>Confidentiality</dt><dd>High</dd></div><div class="bx-c"><dt>Integrity</dt><dd>High</dd></div><div class="bx-c"><dt>Availability</dt><dd>High</dd></div><div class="bx-c"><dt>Scope</dt><dd>Changed</dd></div></dl></div><p class="bx-foot"><a href="https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H" rel="noopener">Open this vector in the FIRST calculator &#8599;</a></p></div><dl class="meta"><div class="meta-i wide"><dt class="k-lab">Weakness</dt><dd class="meta-v"><abbr title="Improper Neutralization of Special Elements used in an OS Command (&#x27;OS Command Injection&#x27;)">CWE-78</abbr> <span class="meta-s">Improper Neutralization of Special Elements used in an OS Command (&#x27;OS Command Injection&#x27;)</span></dd></div><div class="meta-i"><dt class="k-lab">Advisory</dt><dd class="meta-v"><a href="https://github.com/ag2ai/ag2/security/advisories/GHSA-42mf-vpmr-gw5r">GHSA-42mf-vpmr-gw5r</a></dd></div><div class="meta-i"><dt class="k-lab">CVE</dt><dd class="meta-v">not assigned</dd></div><div class="meta-i"><dt class="k-lab">Vector</dt><dd class="meta-v"><span class="vec">CVSS:3.1/<wbr>AV:N/<wbr>AC:L/<wbr>PR:L/<wbr>UI:N/<wbr>S:C/<wbr>C:H/<wbr>I:H/<wbr>A:H</span></dd></div><div class="meta-i wide"><dt class="k-lab">Also in ag2</dt><dd class="meta-v"><a href="/advisories/ghsa-qrjx-72xx-xhmh/">GHSA-qrjx-72xx-xhmh</a> 8.1</dd></div></dl><div class="tl" role="group" aria-label="Disclosure timeline"><div class="tl-n"><b>2026-05-22</b><span>Reported privately</span></div><div class="tl-seg"><span>134 days</span></div><div class="tl-n"><b>2026-10-03</b><span>Published by the maintainer</span></div></div><p class="ah-note">My analysis of this finding: root cause, the vulnerable code, the impact and the fix, in the site’s format. The official advisory of record is linked above.</p><p class="ah-note ah-note--disc">GitHub published this advisory as Critical with no CVSS score and no vector, in v3 or v4. The score and vector above are my own assessment of the finding, within the severity band GitHub published. Where GitHub publishes a numeric score, this page shows that one instead.</p></div>
  <div class="col-body prose" markdown="1">

### Affected versions

<div class="vts"><div class="vt" aria-hidden="true"><div class="vt-pkg">ag2<span class="k-lab">pip</span></div><div class="vt-bar"><div class="vt-pre">Not listed as affected</div><div class="vt-bad"><b>1.0.0</b><i>Affected</i><b>before 1.1.2</b></div><div class="vt-fix">Fixed in <b>1.1.2</b></div></div></div></div>

| Package | Ecosystem | Vulnerable | Fixed in |
|:--|:--|:--|:--|
| `ag2` | pip | >= 1.0.0, < 1.1.2 | 1.1.2 |
{: .vh}

## Summary

AG2's beta `LocalShellEnvironment` (formerly Microsoft AutoGen) advertises three ways to constrain what an agent can run in a shell: an `allowed` whitelist, a `blocked` blacklist, and a `readonly` mode backed by a curated `READONLY_COMMANDS` list. Every one of them is a prefix check applied to the raw command string, and the command is then handed to `subprocess.run(..., shell=True)`. Because the OS shell, not the filter, decides where one command ends and the next begins, any allowed prefix can be followed by `;`, `&&`, `|`, or `$(...)` to run arbitrary commands. The restriction is cosmetic.

## Where it lives

The filter, in `autogen/beta/tools/shell/environment/base.py`, only looks at how the string begins:

<pre class="has-mark"><code class="language-python"><span class="ln">def matches(pattern: str, command: str) -&gt; bool:</span><span class="ln">    stripped = command.strip()</span><span class="ln bug">    if not stripped.startswith(pattern):</span><span class="ln">        return False</span><span class="ln">    rest = stripped[len(pattern):]</span><span class="ln">    return rest == &quot;&quot; or rest[0] == &quot; &quot;</span></code></pre>

<p class="mark-cap"><span><span class="mark-k">The bug</span>only checks how the command string begins</span></p>

`LocalShellEnvironment.run()` in `environment/local.py` runs whatever passes that check through a full shell:

<pre class="has-mark"><code class="language-python"><span class="ln">if self._allowed is not None and not any(matches(p, command) for p in self._allowed):</span><span class="ln">    return f&quot;Command not allowed: {command!r}&quot;</span><span class="ln">...</span><span class="ln">result = subprocess.run(</span><span class="ln">    command,</span><span class="ln bug">    shell=True,</span><span class="ln">    cwd=self._workdir,</span><span class="ln">    ...</span><span class="ln">)</span></code></pre>

<p class="mark-cap"><span><span class="mark-k">The bug</span>runs the filtered string through a full shell</span></p>

The code already knows. The comment above `READONLY_COMMANDS` in `base.py` calls the list "best-effort" and notes that "`echo` can still redirect output (`echo x > file`), because `shell=True` processing happens inside the OS shell after our prefix check." That caveat understates it: the same mechanism allows arbitrary execution, not just redirection.

## Impact

The security boundary the API promises does not exist. A caller who trusts `readonly=True`, or an allow list, to pen in an LLM-driven or otherwise untrusted command string gets full OS command execution under the process's privileges instead.

**readonly / allow list bypass.** `echo x; id` begins with the allowed `echo`, so it passes, and the shell then runs `id`. `git --version && id` passes an `allowed=["git"]` gate the same way. `cat /dev/null | id` passes `readonly=True` and pipes into an arbitrary program.

**blocklist bypass.** `blocked=["rm", "curl"]` is evaded by `echo $(rm -rf /)`, which never starts with a blocked prefix yet executes `rm` inside a subshell.

I confirmed each of these against a faithful copy of `matches()` and `READONLY_COMMANDS` driving a real `subprocess.run(..., shell=True)`: in every case the filter returned "allowed" and the injected `id` produced `uid=` output.

## Fix

Stop treating a prefix of a shell string as a security boundary. Either tokenize with `shlex.split()` and execute argv-style with `shell=False`, validating the resolved program against the allow list, or run inside a real sandbox. If `shell=True` must stay, reject any command containing shell metacharacters (`;`, `&`, `|`, `$`, backticks, redirections, newlines) before it reaches `subprocess.run`, and document that the prefix lists are not a privilege boundary.

<section class="fs-inline" aria-labelledby="h-record"><h2 id="h-record" class="no-idx">The record</h2><dl class="fs"><dt>Weakness</dt><dd><b>CWE-78</b> Improper Neutralization of Special Elements used in an OS Command (&#x27;OS Command Injection&#x27;)</dd><dt>Affected</dt><dd>ag2 <b>1.0.0 to before 1.1.2</b></dd><dt>Fixed in</dt><dd><b>1.1.2</b></dd><dt>Disclosure</dt><dd><b>2026-05-22</b> Reported privately<br><span class="fs-gap">134 days later</span><b>2026-10-03</b> Published</dd><dt>Advisory</dt><dd><a href="https://github.com/ag2ai/ag2/security/advisories/GHSA-42mf-vpmr-gw5r">GHSA-42mf-vpmr-gw5r</a></dd><dt>Also in ag2</dt><dd><a href="/advisories/ghsa-qrjx-72xx-xhmh/">GHSA-qrjx-72xx-xhmh</a> 8.1</dd></dl></section>

## About this writeup

Sanaan Fayaz Wani (GitHub [`sfwani`](https://github.com/sfwani)) reported this vulnerability to the `ag2` maintainers under coordinated disclosure and is credited as a reporter in [GHSA-42mf-vpmr-gw5r](https://github.com/ag2ai/ag2/security/advisories/GHSA-42mf-vpmr-gw5r), published 2026-10-03.

All published findings: [advisory index](/advisories/).


  </div>
  <aside class="srail" aria-label="Fact sheet" data-sev="critical"><div class="sr-h"><span class="sr-num">9.9</span><span class="sr-sev">Critical</span></div><p class="sr-src">CVSS 3.1 base · my assessment</p><dl class="fs"><dt>Weakness</dt><dd><b>CWE-78</b> Improper Neutralization of Special Elements used in an OS Command (&#x27;OS Command Injection&#x27;)</dd><dt>Affected</dt><dd>ag2 <b>1.0.0 to before 1.1.2</b></dd><dt>Fixed in</dt><dd><b>1.1.2</b></dd><dt>Disclosure</dt><dd><b>2026-05-22</b> Reported privately<br><span class="fs-gap">134 days later</span><b>2026-10-03</b> Published</dd><dt>Advisory</dt><dd><a href="https://github.com/ag2ai/ag2/security/advisories/GHSA-42mf-vpmr-gw5r">GHSA-42mf-vpmr-gw5r</a></dd><dt>Also in ag2</dt><dd><a href="/advisories/ghsa-qrjx-72xx-xhmh/">GHSA-qrjx-72xx-xhmh</a> 8.1</dd></dl><a class="sr-top" href="#top">Back to top</a></aside>
</section>
