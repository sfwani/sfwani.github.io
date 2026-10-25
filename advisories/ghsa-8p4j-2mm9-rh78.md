---
title: "GHSA-8p4j-2mm9-rh78"
heading: "GHSA-8p4j-2mm9-rh78"
role: "Registry HTTP actions could reach private network destinations before nsjail egress filtering"
seo_title: "GHSA-8p4j-2mm9-rh78: Registry HTTP actions could reach private network destinations before nsjail… - Sanaan Fayaz Wani"
ghsa_id: "GHSA-8p4j-2mm9-rh78"
cve_id: ""
published_at: "2026-09-20"
permalink: /advisories/ghsa-8p4j-2mm9-rh78/
layout: c2
description: "Registry HTTP actions could reach private network destinations before nsjail egress filtering. Tracecat, CVSS 6.5 Medium, CWE-918 Server side request forgery. Writeup by Sanaan Fayaz Wani, the credited reporter."
image: /assets/img/og/ghsa-8p4j-2mm9-rh78.png
kicker_repo: "TracecatHQ/tracecat"
comments: false
last_modified_at: 2026-10-24T23:51:00+00:00
---
<section class="sec g" id="writeup" aria-labelledby="h-writeup" data-sev="medium" data-score="6.5" data-sevword="Medium" data-short="Upgrade to 1.0.0-beta.52-rc.3">
  <h2 id="h-writeup" class="vh">GHSA-8p4j-2mm9-rh78</h2>
  <div class="ah" data-sev="medium"><div class="ah-score"><p class="ah-num">6.5</p><p class="ah-sev">Medium</p><p class="ah-of">CVSS 3.1 base</p><div class="ah-meter" aria-hidden="true"><i style="width:65%"></i></div><ol class="tlv" aria-label="Disclosure timeline"><li><b>2026-05-28</b><span>Reported privately</span></li><li><span class="tlv-d">115 days later</span><b>2026-09-20</b><span>Published by the maintainer</span></li></ol></div><div class="act"><p class="act-k">What to do</p><p class="act-v">If you run <b>Tracecat</b> <b>0.41.0 to before 1.0.0-beta.52-rc.3</b>, upgrade to <b>1.0.0-beta.52-rc.3</b> or later.</p></div><p class="ts"><em>Anyone who can reach it over the network</em>, with <em>a low-privilege account</em> and no user interaction, can <em>read sensitive data</em>.<span class="ts-src">Read from the CVSS 3.1 vector</span></p><div class="bx" style="--n:4"><div class="bx-head"><span class="k-lab">CVSS 3.1 metrics</span></div><div class="bx-row"><p class="bx-g">To exploit it</p><dl class="bx-grid"><div class="bx-c"><dt>Attack vector</dt><dd>Network</dd></div><div class="bx-c"><dt>Attack complexity</dt><dd>Low</dd></div><div class="bx-c"><dt>Privileges required</dt><dd>Low</dd></div><div class="bx-c"><dt>User interaction</dt><dd>None</dd></div></dl></div><div class="bx-row"><p class="bx-g">What it gets</p><dl class="bx-grid"><div class="bx-c"><dt>Confidentiality</dt><dd>High</dd></div><div class="bx-c"><dt>Integrity</dt><dd>None</dd></div><div class="bx-c"><dt>Availability</dt><dd>None</dd></div><div class="bx-c"><dt>Scope</dt><dd>Unchanged</dd></div></dl></div><p class="bx-foot"><a href="https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N" rel="noopener">Open this vector in the FIRST calculator &#8599;</a></p></div><dl class="meta"><div class="meta-i wide"><dt class="k-lab">Weakness</dt><dd class="meta-v"><abbr title="Server-Side Request Forgery (SSRF)">CWE-918</abbr> <span class="meta-s">Server-Side Request Forgery (SSRF)</span></dd></div><div class="meta-i"><dt class="k-lab">Advisory</dt><dd class="meta-v"><a href="https://github.com/TracecatHQ/tracecat/security/advisories/GHSA-8p4j-2mm9-rh78">GHSA-8p4j-2mm9-rh78</a></dd></div><div class="meta-i"><dt class="k-lab">CVE</dt><dd class="meta-v">not assigned</dd></div><div class="meta-i"><dt class="k-lab">Vector</dt><dd class="meta-v"><span class="vec">CVSS:3.1/<wbr>AV:N/<wbr>AC:L/<wbr>PR:L/<wbr>UI:N/<wbr>S:U/<wbr>C:H/<wbr>I:N/<wbr>A:N</span></dd></div></dl><div class="tl" role="group" aria-label="Disclosure timeline"><div class="tl-n"><b>2026-05-28</b><span>Reported privately</span></div><div class="tl-seg"><span>115 days</span></div><div class="tl-n"><b>2026-09-20</b><span>Published by the maintainer</span></div></div><p class="ah-note">My analysis of this finding: root cause, the vulnerable code, the impact and the fix, in the site’s format. The official advisory of record is linked above.</p></div>
  <div class="col-body prose" markdown="1">

### Affected versions

<div class="vts"><div class="vt" aria-hidden="true"><div class="vt-pkg">Tracecat</div><div class="vt-bar"><div class="vt-pre">Not listed as affected</div><div class="vt-bad"><b>0.41.0</b><i>Affected</i><b>before 1.0.0-beta.52-rc.3</b></div><div class="vt-fix">Fixed in <b>1.0.0-beta.52-rc.3</b></div></div></div></div>

| Package | Ecosystem | Vulnerable | Fixed in |
|:--|:--|:--|:--|
| `Tracecat` | other | >= 0.41.0, < 1.0.0-beta.52-rc.3 | >= 1.0.0-beta.52-rc.3 |
{: .vh}

## Summary

Tracecat's `core.cases.upload_attachment_from_url` registry action takes a URL from an authenticated workflow author, fetches it with `httpx`, and stores the full response body as a case attachment the author can read back. There is no URL validation of any kind: no scheme allowlist, no private or link local IP blocking, no DNS rebinding guard. That makes it a clean full read SSRF, where the response is handed straight back to the attacker rather than merely triggered blind.

## Where it lives

The action is defined in `packages/tracecat-registry/tracecat_registry/core/cases.py`. The `url` parameter is a plain `str`, and the fetch runs with no checks between input and request:

<pre class="has-mark"><code class="language-python"><span class="ln">async def upload_attachment_from_url(</span><span class="ln">    case_id: Annotated[str, Doc(&quot;The ID of the case to attach the file to.&quot;)],</span><span class="ln">    url: Annotated[str, Doc(&quot;The URL of the file to upload.&quot;)],</span><span class="ln">    headers: Annotated[dict[str, str] | None, Doc(&quot;The headers to use when downloading the file.&quot;)] = None,</span><span class="ln">    file_name: Annotated[str | None, Doc(&quot;...&quot;)] = None,</span><span class="ln">) -&gt; types.CaseAttachmentRead:</span><span class="ln">    &quot;&quot;&quot;Upload a file attachment to a case from a URL.&quot;&quot;&quot;</span><span class="ln">    async with httpx.AsyncClient() as client:</span><span class="ln bug">        response = await client.get(url, headers=headers)</span><span class="ln">        response.raise_for_status()</span><span class="ln">        content = response.content</span><span class="ln">        content_type = response.headers.get(&quot;Content-Type&quot;)</span><span class="ln">    ...</span><span class="ln bug">    return await _upload_attachment(case_id, file_name, content, content_type)</span></code></pre>

<p class="mark-cap"><span><span class="mark-k">The bug</span>fetches the author supplied url with no validation</span><span><span class="mark-k">The bug</span>stores the full response body as a readable attachment</span></p>

Two details sharpen it. The `headers` parameter is attacker controlled, so a request can carry the `X-aws-ec2-metadata-token` header needed for IMDSv2 token based metadata access. And `content` is persisted through `_upload_attachment`, so whatever the internal service returns becomes a downloadable attachment on the case. The same gap in reflected form sits in the `core.http_request` family in `core/http.py`, where Pydantic `HttpUrl` validates URL shape but never rejects private ranges.

## Impact

My own findings pair this with Tracecat's default of `TRACECAT__DISABLE_NSJAIL=true`, which ships across `.env.example`, both executor services in `docker-compose.yml`, and `tracecat/config.py`. With the sandbox off the executor has no network isolation, so the SSRF reaches everything on the Docker network. I live validated reachability from the executor to Redis (received `+PONG`), PostgreSQL (TCP connect on 5432), and MinIO (HTTP 200). On a cloud deployment the same action reaches `169.254.169.254` for IAM credential theft, with the custom `headers` covering IMDSv2. Because the full body is stored and retrievable, this is exfiltration, not a pingback. One mitigating note: `httpx` does not follow redirects by default, so redirect based pivots do not work out of the box.

## Fix

Validate before the request, not just the format. Resolve the hostname, reject any resolved address inside `127.0.0.0/8`, `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`, `169.254.0.0/16`, `::1/128`, `fc00::/7` and `fe80::/10`, and restrict the scheme to `http` and `https`. Apply that same check in `upload_attachment_from_url` and across the `core.http_request` and `core.http_paginate` actions, since the paginator can emit arbitrary follow up URLs that skip even the `HttpUrl` format check.

<section class="fs-inline" aria-labelledby="h-record"><h2 id="h-record" class="no-idx">The record</h2><dl class="fs"><dt>Weakness</dt><dd><b>CWE-918</b> Server-Side Request Forgery (SSRF)</dd><dt>Affected</dt><dd>Tracecat <b>0.41.0 to before 1.0.0-beta.52-rc.3</b></dd><dt>Fixed in</dt><dd><b>1.0.0-beta.52-rc.3</b></dd><dt>Disclosure</dt><dd><b>2026-05-28</b> Reported privately<br><span class="fs-gap">115 days later</span><b>2026-09-20</b> Published</dd><dt>Advisory</dt><dd><a href="https://github.com/TracecatHQ/tracecat/security/advisories/GHSA-8p4j-2mm9-rh78">GHSA-8p4j-2mm9-rh78</a></dd></dl></section>

## About this writeup

Sanaan Fayaz Wani (GitHub [`sfwani`](https://github.com/sfwani)) reported this vulnerability to the `Tracecat` maintainers under coordinated disclosure and is credited as a reporter in [GHSA-8p4j-2mm9-rh78](https://github.com/TracecatHQ/tracecat/security/advisories/GHSA-8p4j-2mm9-rh78), published 2026-09-20.

All published findings: [advisory index](/advisories/).


  </div>
  <aside class="srail" aria-label="Fact sheet" data-sev="medium"><div class="sr-h"><span class="sr-num">6.5</span><span class="sr-sev">Medium</span></div><p class="sr-src">CVSS 3.1 base</p><dl class="fs"><dt>Weakness</dt><dd><b>CWE-918</b> Server-Side Request Forgery (SSRF)</dd><dt>Affected</dt><dd>Tracecat <b>0.41.0 to before 1.0.0-beta.52-rc.3</b></dd><dt>Fixed in</dt><dd><b>1.0.0-beta.52-rc.3</b></dd><dt>Disclosure</dt><dd><b>2026-05-28</b> Reported privately<br><span class="fs-gap">115 days later</span><b>2026-09-20</b> Published</dd><dt>Advisory</dt><dd><a href="https://github.com/TracecatHQ/tracecat/security/advisories/GHSA-8p4j-2mm9-rh78">GHSA-8p4j-2mm9-rh78</a></dd></dl><a class="sr-top" href="#top">Back to top</a></aside>
</section>
