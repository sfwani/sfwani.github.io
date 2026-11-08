---
title: "GHSA-jmgj-cq6g-6hr2"
heading: "GHSA-jmgj-cq6g-6hr2"
role: "Incorrect Authorization via Base Member Removal"
seo_title: "GHSA-jmgj-cq6g-6hr2: Incorrect Authorization via Base Member Removal - Sanaan Fayaz Wani"
ghsa_id: "GHSA-jmgj-cq6g-6hr2"
cve_id: ""
published_at: "2026-11-02"
permalink: /advisories/ghsa-jmgj-cq6g-6hr2/
layout: c2
description: "Incorrect Authorization via Base Member Removal. nocodb, CVSS 2.7 Low, CWE-863 Incorrect authorization. Writeup by Sanaan Fayaz Wani, the credited reporter."
image: /assets/img/og/ghsa-jmgj-cq6g-6hr2.png
kicker_repo: "nocodb/nocodb"
comments: false
last_modified_at: 2026-11-07T21:22:25+00:00
---
<section class="sec g" id="writeup" aria-labelledby="h-writeup" data-sev="low" data-score="2.7" data-sevword="Low" data-short="Upgrade to 2026.09.1">
  <h2 id="h-writeup" class="vh">GHSA-jmgj-cq6g-6hr2</h2>
  <div class="ah" data-sev="low"><div class="ah-score"><p class="ah-num">2.7</p><p class="ah-sev">Low</p><p class="ah-of">CVSS 3.1 base</p><div class="ah-meter" aria-hidden="true"><i style="width:27%"></i></div><ol class="tlv" aria-label="Disclosure timeline"><li><b>2026-09-24</b><span>Reported privately</span></li><li><span class="tlv-d">39 days later</span><b>2026-11-02</b><span>Published by the maintainer</span></li></ol></div><div class="act"><p class="act-k">What to do</p><p class="act-v">If you run <b>nocodb</b> <b>0.253.0 to before 2026.09.1</b>, upgrade to <b>2026.09.1</b> or later.</p></div><p class="ts"><em>Anyone who can reach it over the network</em>, with <em>a high-privilege account</em> and no user interaction, can <em>change some data</em>.<span class="ts-src">Read from the CVSS 3.1 vector</span></p><div class="bx" style="--n:4"><div class="bx-head"><span class="k-lab">CVSS 3.1 metrics</span></div><div class="bx-row"><p class="bx-g">To exploit it</p><dl class="bx-grid"><div class="bx-c"><dt>Attack vector</dt><dd>Network</dd></div><div class="bx-c"><dt>Attack complexity</dt><dd>Low</dd></div><div class="bx-c"><dt>Privileges required</dt><dd>High</dd></div><div class="bx-c"><dt>User interaction</dt><dd>None</dd></div></dl></div><div class="bx-row"><p class="bx-g">What it gets</p><dl class="bx-grid"><div class="bx-c"><dt>Confidentiality</dt><dd>None</dd></div><div class="bx-c"><dt>Integrity</dt><dd>Low</dd></div><div class="bx-c"><dt>Availability</dt><dd>None</dd></div><div class="bx-c"><dt>Scope</dt><dd>Unchanged</dd></div></dl></div><p class="bx-foot"><a href="https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:N/I:L/A:N" rel="noopener">Open this vector in the FIRST calculator &#8599;</a></p></div><dl class="meta"><div class="meta-i wide"><dt class="k-lab">Weakness</dt><dd class="meta-v"><abbr title="Incorrect Authorization">CWE-863</abbr> <span class="meta-s">Incorrect Authorization</span></dd></div><div class="meta-i"><dt class="k-lab">Advisory</dt><dd class="meta-v"><a href="https://github.com/nocodb/nocodb/security/advisories/GHSA-jmgj-cq6g-6hr2">GHSA-jmgj-cq6g-6hr2</a></dd></div><div class="meta-i"><dt class="k-lab">CVE</dt><dd class="meta-v">not assigned</dd></div><div class="meta-i"><dt class="k-lab">Vector</dt><dd class="meta-v"><span class="vec">CVSS:3.1/<wbr>AV:N/<wbr>AC:L/<wbr>PR:H/<wbr>UI:N/<wbr>S:U/<wbr>C:N/<wbr>I:L/<wbr>A:N</span></dd></div><div class="meta-i wide"><dt class="k-lab">Also in nocodb</dt><dd class="meta-v"><a href="/advisories/ghsa-jcc2-3vff-7867/">GHSA-jcc2-3vff-7867</a> 6.5</dd></div></dl><div class="tl" role="group" aria-label="Disclosure timeline"><div class="tl-n"><b>2026-09-24</b><span>Reported privately</span></div><div class="tl-seg"><span>39 days</span></div><div class="tl-n"><b>2026-11-02</b><span>Published by the maintainer</span></div></div><p class="ah-note">This page reproduces the published advisory for this finding. The advisory of record is linked above.</p></div>
  <div class="col-body prose" markdown="1">

### Affected versions

<div class="vts"><div class="vt" aria-hidden="true"><div class="vt-pkg">nocodb</div><div class="vt-bar"><div class="vt-pre">Not listed as affected</div><div class="vt-bad"><b>0.253.0</b><i>Affected</i><b>before 2026.09.1</b></div><div class="vt-fix">Fixed in <b>2026.09.1</b></div></div></div></div>

| Package | Ecosystem | Vulnerable | Fixed in |
|:--|:--|:--|:--|
| `nocodb` | other | >= 0.253.0, < 2026.09.1 | 2026.09.1 |
{: .vh}

### Summary

The check meant to stop a base member from removing someone with a higher base role never took effect, so a base Creator could remove an Owner of the base.

### Details

`baseUserDelete` in `base-users.service.ts`, in both the Community and Enterprise services, compared the target's role power with the caller's through `getProjectRolePower`, which expects a user and reads its `base_roles`. The target side was given `baseUser.base_roles`, the roles themselves, so the helper found no roles on it and returned -1, and the comparison could never refuse the request. Base Creators hold the member removal permission, so a Creator could remove a member with the higher Owner role. The separate checks that keep the last Owner of a base and protect super admins were unaffected. The target user is now passed to the comparison, so removing a member whose role outranks the caller's is refused.

### Impact

An attacker needs an account with the Creator role on the base. They could remove another Owner of the base, a role above their own, as long as at least one Owner remained. Super admins and the base's last Owner could not be removed this way.

### Credit

This issue was reported by [@sfwani](https://github.com/sfwani).

<section class="fs-inline" aria-labelledby="h-record"><h2 id="h-record" class="no-idx">The record</h2><dl class="fs"><dt>Weakness</dt><dd><b>CWE-863</b> Incorrect Authorization</dd><dt>Affected</dt><dd>nocodb <b>0.253.0 to before 2026.09.1</b></dd><dt>Fixed in</dt><dd><b>2026.09.1</b></dd><dt>Disclosure</dt><dd><b>2026-09-24</b> Reported privately<br><span class="fs-gap">39 days later</span><b>2026-11-02</b> Published</dd><dt>Advisory</dt><dd><a href="https://github.com/nocodb/nocodb/security/advisories/GHSA-jmgj-cq6g-6hr2">GHSA-jmgj-cq6g-6hr2</a></dd><dt>Also in nocodb</dt><dd><a href="/advisories/ghsa-jcc2-3vff-7867/">GHSA-jcc2-3vff-7867</a> 6.5</dd></dl></section>

## About this writeup

Sanaan Fayaz Wani (GitHub [`sfwani`](https://github.com/sfwani)) reported this vulnerability to the `nocodb` maintainers under coordinated disclosure and is credited as a reporter in [GHSA-jmgj-cq6g-6hr2](https://github.com/nocodb/nocodb/security/advisories/GHSA-jmgj-cq6g-6hr2), published 2026-11-02.

All published findings: [advisory index](/advisories/).


  </div>
  <aside class="srail" aria-label="Fact sheet" data-sev="low"><div class="sr-h"><span class="sr-num">2.7</span><span class="sr-sev">Low</span></div><p class="sr-src">CVSS 3.1 base</p><dl class="fs"><dt>Weakness</dt><dd><b>CWE-863</b> Incorrect Authorization</dd><dt>Affected</dt><dd>nocodb <b>0.253.0 to before 2026.09.1</b></dd><dt>Fixed in</dt><dd><b>2026.09.1</b></dd><dt>Disclosure</dt><dd><b>2026-09-24</b> Reported privately<br><span class="fs-gap">39 days later</span><b>2026-11-02</b> Published</dd><dt>Advisory</dt><dd><a href="https://github.com/nocodb/nocodb/security/advisories/GHSA-jmgj-cq6g-6hr2">GHSA-jmgj-cq6g-6hr2</a></dd><dt>Also in nocodb</dt><dd><a href="/advisories/ghsa-jcc2-3vff-7867/">GHSA-jcc2-3vff-7867</a> 6.5</dd></dl><a class="sr-top" href="#top">Back to top</a></aside>
</section>
