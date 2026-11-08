---
title: "GHSA-5mc6-2qfj-59cg"
heading: "GHSA-5mc6-2qfj-59cg"
role: "Opik SDKs render Jinja2/Nunjucks prompt templates without a sandbox, allowing code execution"
seo_title: "GHSA-5mc6-2qfj-59cg: Opik SDKs render Jinja2/Nunjucks prompt templates without a sandbox, allowing… - Sanaan Fayaz Wani"
ghsa_id: "GHSA-5mc6-2qfj-59cg"
cve_id: ""
published_at: "2026-11-05"
permalink: /advisories/ghsa-5mc6-2qfj-59cg/
layout: c2
description: "Opik SDKs render Jinja2/Nunjucks prompt templates without a sandbox, allowing code execution. opik, CVSS 8.8 High, CWE-94 Code injection. Writeup by Sanaan Fayaz Wani, the credited reporter."
image: /assets/img/og/ghsa-5mc6-2qfj-59cg.png
kicker_repo: "comet-ml/opik"
comments: false
last_modified_at: 2026-11-07T21:22:25+00:00
---
<section class="sec g" id="writeup" aria-labelledby="h-writeup" data-sev="high" data-score="8.8" data-sevword="High" data-short="Fix differs by range">
  <h2 id="h-writeup" class="vh">GHSA-5mc6-2qfj-59cg</h2>
  <div class="ah" data-sev="high"><div class="ah-score"><p class="ah-num">8.8</p><p class="ah-sev">High</p><p class="ah-of">CVSS 3.1 base</p><div class="ah-meter" aria-hidden="true"><i style="width:88%"></i></div><ol class="tlv" aria-label="Disclosure timeline"><li><b>2026-10-25</b><span>Reported privately</span></li><li><span class="tlv-d">11 days later</span><b>2026-11-05</b><span>Published by the maintainer</span></li></ol></div><div class="act"><p class="act-k">What to do</p><p class="act-v multi">If you run <b>before 2.2.123</b>, upgrade to <b>2.2.123</b> or later.<br>If you run <b>before 2.2.123</b>, upgrade to <b>2.2.123</b> or later.</p></div><p class="ts"><em>Anyone who can reach it over the network</em>, with <em>no account</em>, if a user takes some action, can <em>read and change sensitive data and make it unavailable</em>.<span class="ts-src">Read from the CVSS 3.1 vector</span></p><div class="bx" style="--n:4"><div class="bx-head"><span class="k-lab">CVSS 3.1 metrics</span></div><div class="bx-row"><p class="bx-g">To exploit it</p><dl class="bx-grid"><div class="bx-c"><dt>Attack vector</dt><dd>Network</dd></div><div class="bx-c"><dt>Attack complexity</dt><dd>Low</dd></div><div class="bx-c"><dt>Privileges required</dt><dd>None</dd></div><div class="bx-c"><dt>User interaction</dt><dd>Required</dd></div></dl></div><div class="bx-row"><p class="bx-g">What it gets</p><dl class="bx-grid"><div class="bx-c"><dt>Confidentiality</dt><dd>High</dd></div><div class="bx-c"><dt>Integrity</dt><dd>High</dd></div><div class="bx-c"><dt>Availability</dt><dd>High</dd></div><div class="bx-c"><dt>Scope</dt><dd>Unchanged</dd></div></dl></div><p class="bx-foot"><a href="https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H" rel="noopener">Open this vector in the FIRST calculator &#8599;</a></p></div><dl class="meta"><div class="meta-i wide"><dt class="k-lab">Weakness</dt><dd class="meta-v"><abbr title="Improper Control of Generation of Code">CWE-94</abbr>, <abbr title="Improper Neutralization of Special Elements Used in a Template Engine">CWE-1336</abbr> <span class="meta-s">Improper Control of Generation of Code · Improper Neutralization of Special Elements Used in a Template Engine</span></dd></div><div class="meta-i"><dt class="k-lab">Advisory</dt><dd class="meta-v"><a href="https://github.com/comet-ml/opik/security/advisories/GHSA-5mc6-2qfj-59cg">GHSA-5mc6-2qfj-59cg</a></dd></div><div class="meta-i"><dt class="k-lab">CVE</dt><dd class="meta-v">not assigned</dd></div><div class="meta-i"><dt class="k-lab">Vector</dt><dd class="meta-v"><span class="vec">CVSS:3.1/<wbr>AV:N/<wbr>AC:L/<wbr>PR:N/<wbr>UI:R/<wbr>S:U/<wbr>C:H/<wbr>I:H/<wbr>A:H</span></dd></div></dl><div class="tl" role="group" aria-label="Disclosure timeline"><div class="tl-n"><b>2026-10-25</b><span>Reported privately</span></div><div class="tl-seg"><span>11 days</span></div><div class="tl-n"><b>2026-11-05</b><span>Published by the maintainer</span></div></div><p class="ah-note">This page reproduces the published advisory for this finding. The advisory of record is linked above.</p></div>
  <div class="col-body prose" markdown="1">

### Affected versions

<div class="vts"><div class="vt" aria-hidden="true"><div class="vt-pkg">opik<span class="k-lab">pip</span></div><div class="vt-bar nolo"><div class="vt-bad"><b>No lower bound</b><i>Affected</i><b>before 2.2.123</b></div><div class="vt-fix">Fixed in <b>2.2.123</b></div></div></div><div class="vt" aria-hidden="true"><div class="vt-pkg">opik<span class="k-lab">npm</span></div><div class="vt-bar nolo"><div class="vt-bad"><b>No lower bound</b><i>Affected</i><b>before 2.2.123</b></div><div class="vt-fix">Fixed in <b>2.2.123</b></div></div></div></div>

| Package | Ecosystem | Vulnerable | Fixed in |
|:--|:--|:--|:--|
| `opik` | pip | < 2.2.123 | 2.2.123 |
| `opik` | npm | < 2.2.123 | 2.2.123 |
{: .vh}

#### Summary
Before 2.2.123, the Opik Python and TypeScript SDKs rendered prompts of type `jinja2` with an unsandboxed template engine (Jinja2 in Python, Nunjucks in TypeScript). A template containing crafted template expressions could execute arbitrary code in the process that formats the prompt.

#### Impact
An application is affected if it formats a `jinja2` prompt whose template text can be written by someone the application does not fully trust. One example is a prompt fetched from a shared Opik workspace fetched from a shared Opik workspace (`get_prompt()` in Python, `getPrompt()` in TypeScript) and then rendered with `format()`. The code runs with the privileges of the application process, including its environment variables, credentials and network access. On self-hosted Opik deployments running without authentication, anyone who can reach the Opik API can create or edit prompts.

Prompts of the default `mustache` type are not affected.

#### Patches
Fixed in `opik` 2.2.123 (PyPI and npm). The Python SDK now renders Jinja2 templates in Jinja2's `SandboxedEnvironment`, and the TypeScript SDK renders with a restricted Nunjucks environment. Upgrade to 2.2.123 or later.

#### Workarounds
If you cannot upgrade:
- Do not format `jinja2` prompts whose template text comes from sources you do not control.
- Use `mustache` prompts instead.
- Restrict who can create or edit prompts in your workspace.

#### Credits
Reported by `sfwani`.

<section class="fs-inline" aria-labelledby="h-record"><h2 id="h-record" class="no-idx">The record</h2><dl class="fs"><dt>Weakness</dt><dd><b>CWE-94</b> Improper Control of Generation of Code<br><b>CWE-1336</b> Improper Neutralization of Special Elements Used in a Template Engine</dd><dt>Affected</dt><dd><span class="fs-v">opik <b>before 2.2.123</b><span class="fs-gap">fixed in 2.2.123</span></span><span class="fs-v">opik <b>before 2.2.123</b><span class="fs-gap">fixed in 2.2.123</span></span></dd><dt>Disclosure</dt><dd><b>2026-10-25</b> Reported privately<br><span class="fs-gap">11 days later</span><b>2026-11-05</b> Published</dd><dt>Advisory</dt><dd><a href="https://github.com/comet-ml/opik/security/advisories/GHSA-5mc6-2qfj-59cg">GHSA-5mc6-2qfj-59cg</a></dd></dl></section>

## About this writeup

Sanaan Fayaz Wani (GitHub [`sfwani`](https://github.com/sfwani)) reported this vulnerability to the `opik` maintainers under coordinated disclosure and is credited as a reporter in [GHSA-5mc6-2qfj-59cg](https://github.com/comet-ml/opik/security/advisories/GHSA-5mc6-2qfj-59cg), published 2026-11-05.

All published findings: [advisory index](/advisories/).


  </div>
  <aside class="srail" aria-label="Fact sheet" data-sev="high"><div class="sr-h"><span class="sr-num">8.8</span><span class="sr-sev">High</span></div><p class="sr-src">CVSS 3.1 base</p><dl class="fs"><dt>Weakness</dt><dd><b>CWE-94</b> Improper Control of Generation of Code<br><b>CWE-1336</b> Improper Neutralization of Special Elements Used in a Template Engine</dd><dt>Affected</dt><dd><span class="fs-v">opik <b>before 2.2.123</b><span class="fs-gap">fixed in 2.2.123</span></span><span class="fs-v">opik <b>before 2.2.123</b><span class="fs-gap">fixed in 2.2.123</span></span></dd><dt>Disclosure</dt><dd><b>2026-10-25</b> Reported privately<br><span class="fs-gap">11 days later</span><b>2026-11-05</b> Published</dd><dt>Advisory</dt><dd><a href="https://github.com/comet-ml/opik/security/advisories/GHSA-5mc6-2qfj-59cg">GHSA-5mc6-2qfj-59cg</a></dd></dl><a class="sr-top" href="#top">Back to top</a></aside>
</section>
