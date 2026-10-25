---
title: "GHSA-v3vj-mch3-x6c2"
heading: "GHSA-v3vj-mch3-x6c2"
role: "Sandbox launcher isolation failure permits host-level code execution"
seo_title: "GHSA-v3vj-mch3-x6c2: Sandbox launcher isolation failure permits host-level code execution - Sanaan Fayaz Wani"
ghsa_id: "GHSA-v3vj-mch3-x6c2"
cve_id: ""
published_at: "2026-10-13"
permalink: /advisories/ghsa-v3vj-mch3-x6c2/
layout: c2
description: "Sandbox launcher isolation failure permits host-level code execution. omnigent, CVSS 8.8 High, CWE-668 Resource exposure. Writeup by Sanaan Fayaz Wani, the credited reporter."
image: /assets/img/og/ghsa-v3vj-mch3-x6c2.png
kicker_repo: "omnigent-ai/omnigent"
comments: false
last_modified_at: 2026-10-24T23:51:00+00:00
---
<section class="sec g" id="writeup" aria-labelledby="h-writeup" data-sev="high" data-score="8.8" data-sevword="High" data-short="Upgrade to 0.18.0">
  <h2 id="h-writeup" class="vh">GHSA-v3vj-mch3-x6c2</h2>
  <div class="ah" data-sev="high"><div class="ah-score"><p class="ah-num">8.8</p><p class="ah-sev">High</p><p class="ah-of">CVSS 3.1 base</p><div class="ah-meter" aria-hidden="true"><i style="width:88%"></i></div><ol class="tlv" aria-label="Disclosure timeline"><li><b>2026-08-15</b><span>Reported privately</span></li><li><span class="tlv-d">59 days later</span><b>2026-10-13</b><span>Published by the maintainer</span></li></ol></div><div class="act"><p class="act-k">What to do</p><p class="act-v">If you run <b>omnigent</b> <b>before 0.18.0</b>, upgrade to <b>0.18.0</b> or later.</p></div><p class="ts"><em>Someone with local access</em>, with <em>a low-privilege account</em> and no user interaction, can <em>read and change sensitive data and make it unavailable</em>, and <em>the impact reaches beyond the vulnerable component</em>.<span class="ts-src">Read from the CVSS 3.1 vector</span></p><div class="bx" style="--n:4"><div class="bx-head"><span class="k-lab">CVSS 3.1 metrics</span></div><div class="bx-row"><p class="bx-g">To exploit it</p><dl class="bx-grid"><div class="bx-c"><dt>Attack vector</dt><dd>Local</dd></div><div class="bx-c"><dt>Attack complexity</dt><dd>Low</dd></div><div class="bx-c"><dt>Privileges required</dt><dd>Low</dd></div><div class="bx-c"><dt>User interaction</dt><dd>None</dd></div></dl></div><div class="bx-row"><p class="bx-g">What it gets</p><dl class="bx-grid"><div class="bx-c"><dt>Confidentiality</dt><dd>High</dd></div><div class="bx-c"><dt>Integrity</dt><dd>High</dd></div><div class="bx-c"><dt>Availability</dt><dd>High</dd></div><div class="bx-c"><dt>Scope</dt><dd>Changed</dd></div></dl></div><p class="bx-foot"><a href="https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H" rel="noopener">Open this vector in the FIRST calculator &#8599;</a></p></div><dl class="meta"><div class="meta-i wide"><dt class="k-lab">Weakness</dt><dd class="meta-v"><abbr title="Exposure of Resource to Wrong Sphere">CWE-668</abbr>, <abbr title="Incorrect Permission Assignment for Critical Resource">CWE-732</abbr> <span class="meta-s">Exposure of Resource to Wrong Sphere · Incorrect Permission Assignment for Critical Resource</span></dd></div><div class="meta-i"><dt class="k-lab">Advisory</dt><dd class="meta-v"><a href="https://github.com/omnigent-ai/omnigent/security/advisories/GHSA-v3vj-mch3-x6c2">GHSA-v3vj-mch3-x6c2</a></dd></div><div class="meta-i"><dt class="k-lab">CVE</dt><dd class="meta-v">not assigned</dd></div><div class="meta-i"><dt class="k-lab">Vector</dt><dd class="meta-v"><span class="vec">CVSS:3.1/<wbr>AV:L/<wbr>AC:L/<wbr>PR:L/<wbr>UI:N/<wbr>S:C/<wbr>C:H/<wbr>I:H/<wbr>A:H</span></dd></div></dl><div class="tl" role="group" aria-label="Disclosure timeline"><div class="tl-n"><b>2026-08-15</b><span>Reported privately</span></div><div class="tl-seg"><span>59 days</span></div><div class="tl-n"><b>2026-10-13</b><span>Published by the maintainer</span></div></div><p class="ah-note">My analysis of this finding: root cause, the vulnerable code, the impact and the fix, in the site’s format. The official advisory of record is linked above.</p></div>
  <div class="col-body prose" markdown="1">

### Affected versions

<div class="vts"><div class="vt" aria-hidden="true"><div class="vt-pkg">omnigent<span class="k-lab">pip</span></div><div class="vt-bar nolo"><div class="vt-bad"><b>No lower bound</b><i>Affected</i><b>before 0.18.0</b></div><div class="vt-fix">Fixed in <b>0.18.0</b></div></div></div></div>

| Package | Ecosystem | Vulnerable | Fixed in |
|:--|:--|:--|:--|
| `omnigent` | pip | < 0.18.0 | 0.18.0 |
{: .vh}

## Summary

Omnigent (Databricks) runs agent tool calls inside a bubblewrap jail, and its own policies present that jail as the real security boundary. I found that five shipped executors grant the host `/tmp` directory as a sandbox write root. Because the bubblewrap backend mounts a private `--tmpfs /tmp` first and only then binds the write roots, the later bind of the host `/tmp` overmounts the private tmpfs and makes the real host `/tmp` writable from inside the sandbox. The host executed launcher script that omnigent writes into that same directory then becomes an overwrite target, which hands a sandboxed agent code execution on the host. Verified live against `omnigent==0.9.0` from PyPI.

## Where it lives

The `/tmp` grant sits right next to the launcher creation in each executor. From `omnigent/inner/goose_executor.py` (the same pattern appears in `pi_executor.py`, `qwen_executor.py`, `kimi_executor.py` and `acp_executor.py`):

<pre class="has-mark"><code class="language-python"><span class="ln">sandbox = with_additional_write_roots(</span><span class="ln">    sandbox,</span><span class="ln">    [</span><span class="ln">        Path.home() / &quot;.config&quot; / &quot;goose&quot;,</span><span class="ln">        Path.home() / &quot;.local&quot; / &quot;share&quot; / &quot;goose&quot;,</span><span class="ln bug">        Path(&quot;/tmp&quot;),</span><span class="ln">    ],</span><span class="ln">)</span><span class="ln">...</span><span class="ln">return create_exec_launcher(self._goose_path, sandbox)</span></code></pre>

<p class="mark-cap"><span><span class="mark-k">The bug</span>grants the host /tmp as a sandbox write root</span></p>

`create_exec_launcher` in `omnigent/inner/sandbox.py` mints that launcher world executable:

<pre class="has-mark"><code class="language-python"><span class="ln bug">fd, path = tempfile.mkstemp(prefix=&quot;omnigent-sandbox-&quot;, suffix=&quot;.py&quot;)  # :1112</span><span class="ln">...</span><span class="ln bug">os.chmod(path, 0o755)                                                  # :1129</span></code></pre>

<p class="mark-cap"><span><span class="mark-k">The bug</span>writes the host launcher into the shared /tmp</span><span><span class="mark-k">The bug</span>launcher is 0755, owned by the uid the sandbox shares</span></p>

The launcher runs on the host and only then re-execs into the wrap. The code comment at `sandbox.py:1006` states the exact assumption the `/tmp` grant breaks:

<pre class="has-mark"><code class="language-python"><span class="ln bug"># bwrap mounts ``/tmp`` as a fresh tmpfs, so the host&#x27;s</span><span class="ln"># ``/tmp/omnigent-sandbox-*.py`` written by</span><span class="ln"># ``create_exec_launcher`` is invisible inside the wrap.</span></code></pre>

<p class="mark-cap"><span><span class="mark-k">The bug</span>the assumption the /tmp grant breaks</span></p>

`bwrap_sandbox.py` emits `--tmpfs /tmp` and then `--bind-try /tmp /tmp`; later bwrap ops win, so the host `/tmp` replaces the tmpfs. It also emits no `--unshare-user` and no `--uid`, so the sandboxed process shares the uid that owns the 0755 launcher and may overwrite it. Root is not required.

## Impact

This crosses the sandbox to host boundary, the one control omnigent names as its security boundary (`policies/builtins/safety.py` ships `enforce_sandbox`; the `blast_radius` docstring disclaims itself and points at sandboxing). The default is not narrowly opt in: `OSEnvSandboxSpec.type` defaults to `"linux_bwrap"`, so any agent whose `os_env` does not explicitly set `type: none` gets the affected sandbox.

My controlled PoC isolated the grant as the cause. With cwd write root `/work` and no `/tmp` grant, a sandboxed write failed and the host saw nothing. With `/tmp` granted the identical write succeeded and the host file appeared:

```
CONTROL  (no /tmp grant): sandboxed write rc=2   HOST sees file: False
AFFECTED (/tmp granted):  sandboxed write rc=0   HOST sees file: True
```

End to end, driven by the real executor, I enumerated the launcher from inside the sandbox, overwrote it, and the host side launcher then ran my content (`ATTACKER_CODE_ON_HOST`) as the host user, reproduced even with an unprivileged `--uid 65534`. `pi_executor` is deterministic: it mints the path once in `__init__` and re-execs it for every session and RPC restart, so no race is needed. The agent gains the host's filesystem, environment and credentials.

## Fix

Stop writing the host executed launcher into a directory the sandbox can reach. Place it under a `0700` directory outside every write root and chmod it `0700` rather than `0755`:

<pre class="has-mark"><code class="language-python"><span class="ln fix">launcher_dir = _private_launcher_dir()   # 0700, outside every write root</span><span class="ln">fd, path = tempfile.mkstemp(prefix=&quot;omnigent-sandbox-&quot;, suffix=&quot;.py&quot;, dir=launcher_dir)</span><span class="ln">...</span><span class="ln fix">os.chmod(path, 0o700)</span></code></pre>

<p class="mark-cap"><span><span class="mark-k fix">The fix</span>places the launcher in a private 0700 directory</span><span><span class="mark-k fix">The fix</span>sets the launcher mode to 0700 instead of 0755</span></p>

Then narrow the `/tmp` grants to a per session subdirectory such as `/tmp/omnigent-<uuid>`, and have `with_additional_write_roots` reject or warn on any root that is an ancestor of the launcher directory so this class of mistake fails loudly. CWE-668 with CWE-732.

<section class="fs-inline" aria-labelledby="h-record"><h2 id="h-record" class="no-idx">The record</h2><dl class="fs"><dt>Weakness</dt><dd><b>CWE-668</b> Exposure of Resource to Wrong Sphere<br><b>CWE-732</b> Incorrect Permission Assignment for Critical Resource</dd><dt>Affected</dt><dd>omnigent <b>before 0.18.0</b></dd><dt>Fixed in</dt><dd><b>0.18.0</b></dd><dt>Disclosure</dt><dd><b>2026-08-15</b> Reported privately<br><span class="fs-gap">59 days later</span><b>2026-10-13</b> Published</dd><dt>Advisory</dt><dd><a href="https://github.com/omnigent-ai/omnigent/security/advisories/GHSA-v3vj-mch3-x6c2">GHSA-v3vj-mch3-x6c2</a></dd></dl></section>

## About this writeup

Sanaan Fayaz Wani (GitHub [`sfwani`](https://github.com/sfwani)) reported this vulnerability to the `omnigent` maintainers under coordinated disclosure and is credited as a reporter in [GHSA-v3vj-mch3-x6c2](https://github.com/omnigent-ai/omnigent/security/advisories/GHSA-v3vj-mch3-x6c2), published 2026-10-13.

All published findings: [advisory index](/advisories/).


  </div>
  <aside class="srail" aria-label="Fact sheet" data-sev="high"><div class="sr-h"><span class="sr-num">8.8</span><span class="sr-sev">High</span></div><p class="sr-src">CVSS 3.1 base</p><dl class="fs"><dt>Weakness</dt><dd><b>CWE-668</b> Exposure of Resource to Wrong Sphere<br><b>CWE-732</b> Incorrect Permission Assignment for Critical Resource</dd><dt>Affected</dt><dd>omnigent <b>before 0.18.0</b></dd><dt>Fixed in</dt><dd><b>0.18.0</b></dd><dt>Disclosure</dt><dd><b>2026-08-15</b> Reported privately<br><span class="fs-gap">59 days later</span><b>2026-10-13</b> Published</dd><dt>Advisory</dt><dd><a href="https://github.com/omnigent-ai/omnigent/security/advisories/GHSA-v3vj-mch3-x6c2">GHSA-v3vj-mch3-x6c2</a></dd></dl><a class="sr-top" href="#top">Back to top</a></aside>
</section>
