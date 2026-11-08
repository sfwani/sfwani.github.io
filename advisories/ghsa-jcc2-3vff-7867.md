---
title: "GHSA-jcc2-3vff-7867"
heading: "GHSA-jcc2-3vff-7867"
role: "Database Credential Exposure via Connection Test Endpoint"
seo_title: "GHSA-jcc2-3vff-7867: Database Credential Exposure via Connection Test Endpoint - Sanaan Fayaz Wani"
ghsa_id: "GHSA-jcc2-3vff-7867"
cve_id: ""
published_at: "2026-11-02"
permalink: /advisories/ghsa-jcc2-3vff-7867/
layout: c2
description: "Database Credential Exposure via Connection Test Endpoint. nocodb, CVSS 6.5 Medium, CWE-522. Writeup by Sanaan Fayaz Wani, the credited reporter."
image: /assets/img/og/ghsa-jcc2-3vff-7867.png
kicker_repo: "nocodb/nocodb"
comments: false
last_modified_at: 2026-11-07T21:22:25+00:00
---
<section class="sec g" id="writeup" aria-labelledby="h-writeup" data-sev="medium" data-score="6.5" data-sevword="Medium" data-short="Upgrade to 2026.10.1">
  <h2 id="h-writeup" class="vh">GHSA-jcc2-3vff-7867</h2>
  <div class="ah" data-sev="medium"><div class="ah-score"><p class="ah-num">6.5</p><p class="ah-sev">Medium</p><p class="ah-of">CVSS 3.1 base</p><div class="ah-meter" aria-hidden="true"><i style="width:65%"></i></div><ol class="tlv" aria-label="Disclosure timeline"><li><b>2026-11-02</b><span>Published by the maintainer</span></li></ol></div><div class="act"><p class="act-k">What to do</p><p class="act-v">If you run <b>nocodb</b> <b>before 2026.10.1</b>, upgrade to <b>2026.10.1</b> or later.</p></div><p class="ts"><em>Anyone who can reach it over the network</em>, with <em>a low-privilege account</em> and no user interaction, can <em>read sensitive data</em>.<span class="ts-src">Read from the CVSS 3.1 vector</span></p><div class="bx" style="--n:4"><div class="bx-head"><span class="k-lab">CVSS 3.1 metrics</span></div><div class="bx-row"><p class="bx-g">To exploit it</p><dl class="bx-grid"><div class="bx-c"><dt>Attack vector</dt><dd>Network</dd></div><div class="bx-c"><dt>Attack complexity</dt><dd>Low</dd></div><div class="bx-c"><dt>Privileges required</dt><dd>Low</dd></div><div class="bx-c"><dt>User interaction</dt><dd>None</dd></div></dl></div><div class="bx-row"><p class="bx-g">What it gets</p><dl class="bx-grid"><div class="bx-c"><dt>Confidentiality</dt><dd>High</dd></div><div class="bx-c"><dt>Integrity</dt><dd>None</dd></div><div class="bx-c"><dt>Availability</dt><dd>None</dd></div><div class="bx-c"><dt>Scope</dt><dd>Unchanged</dd></div></dl></div><p class="bx-foot"><a href="https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N" rel="noopener">Open this vector in the FIRST calculator &#8599;</a></p></div><dl class="meta"><div class="meta-i wide"><dt class="k-lab">Weakness</dt><dd class="meta-v"><abbr title="Insufficiently Protected Credentials">CWE-522</abbr>, <abbr title="Incorrect Authorization">CWE-863</abbr> <span class="meta-s">Insufficiently Protected Credentials · Incorrect Authorization</span></dd></div><div class="meta-i"><dt class="k-lab">Advisory</dt><dd class="meta-v"><a href="https://github.com/nocodb/nocodb/security/advisories/GHSA-jcc2-3vff-7867">GHSA-jcc2-3vff-7867</a></dd></div><div class="meta-i"><dt class="k-lab">CVE</dt><dd class="meta-v">not assigned</dd></div><div class="meta-i"><dt class="k-lab">Vector</dt><dd class="meta-v"><span class="vec">CVSS:3.1/<wbr>AV:N/<wbr>AC:L/<wbr>PR:L/<wbr>UI:N/<wbr>S:U/<wbr>C:H/<wbr>I:N/<wbr>A:N</span></dd></div><div class="meta-i wide"><dt class="k-lab">Also in nocodb</dt><dd class="meta-v"><a href="/advisories/ghsa-jmgj-cq6g-6hr2/">GHSA-jmgj-cq6g-6hr2</a> 2.7</dd></div></dl><p class="ah-note">This page reproduces the published advisory for this finding. The advisory of record is linked above.</p></div>
  <div class="col-body prose" markdown="1">

### Affected versions

<div class="vts"><div class="vt" aria-hidden="true"><div class="vt-pkg">nocodb</div><div class="vt-bar nolo"><div class="vt-bad"><b>No lower bound</b><i>Affected</i><b>before 2026.10.1</b></div><div class="vt-fix">Fixed in <b>2026.10.1</b></div></div></div></div>

| Package | Ecosystem | Vulnerable | Fixed in |
|:--|:--|:--|:--|
| `nocodb` | other | < 2026.10.1 | 2026.10.1 |
{: .vh}

### Summary

The connection-test endpoint merged caller-supplied connection fields over a stored integration's configuration, so a caller could redirect the connection attempt to a host they control while inheriting the stored database password. A workspace-ownership guard added to the same route for CVE-2026-47381 was also unreachable.

### Details

The handler in `utils.controller.ts` deep-merged the request body over `integration.getConfig()`, so `connection.host`, `port` and `user` were overridden by the caller while unstated fields, including the stored password, were inherited. Both editions behaved this way, apart from vault-backed configurations in the Enterprise edition. PostgreSQL md5 and MySQL challenge-response handshakes are offline-crackable, so a connectivity check became credential extraction, although NocoDB masks stored connection secrets on read elsewhere.

Separately, the workspace-mismatch check added by the CVE-2026-47381 fix was conditioned on a request property the extract-ids middleware never populates on this route: the ACL is declared at organization scope, and the default-workspace fallback applies only to workspace- and base-scope ACLs. The membership fallback beneath it was skipped outright for organization-level creators. The Enterprise controller overrides this method and enforces workspace membership, and the community edition has no second workspace, so the dead guard was latent. The private-integration check is unaffected by either issue.

A test that names a saved connection now takes only the database and schema from the request and refuses any other client or target field, so stored credentials only go to the stored host. The unreachable workspace check has been removed.

### Impact

A caller already authorized on an integration could point its stored credentials at a server they control and capture the database password, escalating NocoDB-mediated access into raw credentials for the connected database. The unreachable ownership guard left CVE-2026-47381 unmitigated on this route and would have failed open had the community edition gained multi-workspace support.

### Credit

This issue was reported by uu K. It was independently reported by [@sfwani](https://github.com/sfwani).

<section class="fs-inline" aria-labelledby="h-record"><h2 id="h-record" class="no-idx">The record</h2><dl class="fs"><dt>Weakness</dt><dd><b>CWE-522</b> Insufficiently Protected Credentials<br><b>CWE-863</b> Incorrect Authorization</dd><dt>Affected</dt><dd>nocodb <b>before 2026.10.1</b></dd><dt>Fixed in</dt><dd><b>2026.10.1</b></dd><dt>Disclosure</dt><dd><b>2026-11-02</b> Published</dd><dt>Advisory</dt><dd><a href="https://github.com/nocodb/nocodb/security/advisories/GHSA-jcc2-3vff-7867">GHSA-jcc2-3vff-7867</a></dd><dt>Also in nocodb</dt><dd><a href="/advisories/ghsa-jmgj-cq6g-6hr2/">GHSA-jmgj-cq6g-6hr2</a> 2.7</dd></dl></section>

## About this writeup

Sanaan Fayaz Wani (GitHub [`sfwani`](https://github.com/sfwani)) reported this vulnerability to the `nocodb` maintainers under coordinated disclosure and is credited as a reporter in [GHSA-jcc2-3vff-7867](https://github.com/nocodb/nocodb/security/advisories/GHSA-jcc2-3vff-7867), published 2026-11-02.

All published findings: [advisory index](/advisories/).


  </div>
  <aside class="srail" aria-label="Fact sheet" data-sev="medium"><div class="sr-h"><span class="sr-num">6.5</span><span class="sr-sev">Medium</span></div><p class="sr-src">CVSS 3.1 base</p><dl class="fs"><dt>Weakness</dt><dd><b>CWE-522</b> Insufficiently Protected Credentials<br><b>CWE-863</b> Incorrect Authorization</dd><dt>Affected</dt><dd>nocodb <b>before 2026.10.1</b></dd><dt>Fixed in</dt><dd><b>2026.10.1</b></dd><dt>Disclosure</dt><dd><b>2026-11-02</b> Published</dd><dt>Advisory</dt><dd><a href="https://github.com/nocodb/nocodb/security/advisories/GHSA-jcc2-3vff-7867">GHSA-jcc2-3vff-7867</a></dd><dt>Also in nocodb</dt><dd><a href="/advisories/ghsa-jmgj-cq6g-6hr2/">GHSA-jmgj-cq6g-6hr2</a> 2.7</dd></dl><a class="sr-top" href="#top">Back to top</a></aside>
</section>
