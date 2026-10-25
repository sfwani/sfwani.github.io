---
title: "GHSA-jvm6-86c5-f8j8"
heading: "GHSA-jvm6-86c5-f8j8"
role: "SSRF via AI provider baseUrl bypasses safeFetch, reachable by any space owner"
seo_title: "GHSA-jvm6-86c5-f8j8: SSRF via AI provider baseUrl bypasses safeFetch, reachable by any space owner - Sanaan Fayaz Wani"
ghsa_id: "GHSA-jvm6-86c5-f8j8"
cve_id: ""
published_at: "2026-10-13"
permalink: /advisories/ghsa-jvm6-86c5-f8j8/
layout: c2
description: "SSRF via AI provider baseUrl bypasses safeFetch, reachable by any space owner. teable, CVSS 6.5 Medium, CWE-918 Server side request forgery. Writeup by Sanaan Fayaz Wani, the credited reporter."
image: /assets/img/og/ghsa-jvm6-86c5-f8j8.png
kicker_repo: "teableio/teable"
comments: false
last_modified_at: 2026-10-24T23:51:00+00:00
---
<section class="sec g" id="writeup" aria-labelledby="h-writeup" data-sev="medium" data-score="6.5" data-sevword="Medium" data-short="Upgrade to release.2026-10-12T12-45-53Z.3331">
  <h2 id="h-writeup" class="vh">GHSA-jvm6-86c5-f8j8</h2>
  <div class="ah" data-sev="medium"><div class="ah-score"><p class="ah-num">6.5</p><p class="ah-sev">Medium</p><p class="ah-of">CVSS 3.1 base</p><div class="ah-meter" aria-hidden="true"><i style="width:65%"></i></div><ol class="tlv" aria-label="Disclosure timeline"><li><b>2026-09-04</b><span>Reported privately</span></li><li><span class="tlv-d">39 days later</span><b>2026-10-13</b><span>Published by the maintainer</span></li></ol></div><div class="act"><p class="act-k">What to do</p><p class="act-v">If you run <b>teable</b> <b>before release.2026-10-12T12-45-53Z.3331</b>, upgrade to <b>release.2026-10-12T12-45-53Z.3331</b> or later.</p></div><p class="ts"><em>Anyone who can reach it over the network</em>, with <em>a low-privilege account</em> and no user interaction, can <em>read sensitive data</em>.<span class="ts-src">Read from the CVSS 3.1 vector</span></p><div class="bx" style="--n:4"><div class="bx-head"><span class="k-lab">CVSS 3.1 metrics</span></div><div class="bx-row"><p class="bx-g">To exploit it</p><dl class="bx-grid"><div class="bx-c"><dt>Attack vector</dt><dd>Network</dd></div><div class="bx-c"><dt>Attack complexity</dt><dd>Low</dd></div><div class="bx-c"><dt>Privileges required</dt><dd>Low</dd></div><div class="bx-c"><dt>User interaction</dt><dd>None</dd></div></dl></div><div class="bx-row"><p class="bx-g">What it gets</p><dl class="bx-grid"><div class="bx-c"><dt>Confidentiality</dt><dd>High</dd></div><div class="bx-c"><dt>Integrity</dt><dd>None</dd></div><div class="bx-c"><dt>Availability</dt><dd>None</dd></div><div class="bx-c"><dt>Scope</dt><dd>Unchanged</dd></div></dl></div><p class="bx-foot"><a href="https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N" rel="noopener">Open this vector in the FIRST calculator &#8599;</a></p></div><dl class="meta"><div class="meta-i wide"><dt class="k-lab">Weakness</dt><dd class="meta-v"><abbr title="Server-Side Request Forgery (SSRF)">CWE-918</abbr> <span class="meta-s">Server-Side Request Forgery (SSRF)</span></dd></div><div class="meta-i"><dt class="k-lab">Advisory</dt><dd class="meta-v"><a href="https://github.com/teableio/teable/security/advisories/GHSA-jvm6-86c5-f8j8">GHSA-jvm6-86c5-f8j8</a></dd></div><div class="meta-i"><dt class="k-lab">CVE</dt><dd class="meta-v">not assigned</dd></div><div class="meta-i"><dt class="k-lab">Vector</dt><dd class="meta-v"><span class="vec">CVSS:3.1/<wbr>AV:N/<wbr>AC:L/<wbr>PR:L/<wbr>UI:N/<wbr>S:U/<wbr>C:H/<wbr>I:N/<wbr>A:N</span></dd></div><div class="meta-i wide"><dt class="k-lab">Also in teable</dt><dd class="meta-v"><a href="/advisories/ghsa-w677-p6hx-85vw/">GHSA-w677-p6hx-85vw</a> 7.1</dd></div></dl><div class="tl" role="group" aria-label="Disclosure timeline"><div class="tl-n"><b>2026-09-04</b><span>Reported privately</span></div><div class="tl-seg"><span>39 days</span></div><div class="tl-n"><b>2026-10-13</b><span>Published by the maintainer</span></div></div><p class="ah-note">My analysis of this finding: root cause, the vulnerable code, the impact and the fix, in the site’s format. The official advisory of record is linked above.</p></div>
  <div class="col-body prose" markdown="1">

### Affected versions

<div class="vts"><div class="vt" aria-hidden="true"><div class="vt-pkg">teableio/teable</div><div class="vt-bar nolo"><div class="vt-bad"><b>No lower bound</b><i>Affected</i><b>before release.2026-10-12T12-45-53Z.3331</b></div><div class="vt-fix">Fixed in <b>release.2026-10-12T12-45-53Z.3331</b></div></div></div></div>

| Package | Ecosystem | Vulnerable | Fixed in |
|:--|:--|:--|:--|
| `teableio/teable` | other | < release.2026-10-12T12-45-53Z.3331 | release.2026-10-12T12-45-53Z.3331 |
{: .vh}

## Summary

Teable ships its own SSRF guard (`createSsrfSafeFetch` / `safeFetch`) and wires it into the import and attachment paths. The AI provider path does not use it. `POST /api/space/:spaceId/test-llm` builds an LLM provider from a fully user-controlled `baseUrl` and makes the server issue an outbound request to it, through a plain global `fetch` with no host or scheme allowlist. Any authenticated user can reach the endpoint, and the error responses distinguish open ports from closed ones, giving a server-side internal port-scan and reachability oracle against hosts the attacker cannot reach directly. This is a server-side request forgery (CWE-918).

## Where it lives

The route carries `@Permissions('space|update')`, which sounds privileged but is held by every user on a space they create: `POST /api/space` needs only `space|create` (a default capability), and the creator becomes `Role.Owner`, which has `space|update`. The handler ignores the path `spaceId` entirely and acts on the request body, so an attacker's own throwaway space satisfies the gate. `baseUrl` is validated only as `z.url()`, with no host or scheme restriction.

`testLLM` in `apps/nestjs-backend/src/features/setting/open-api/setting-open-api.service.ts` takes `baseUrl` straight from the request body, builds the provider, and calls `generateText`, which performs the outbound request:

<pre class="has-mark"><code class="language-ts"><span class="ln">async testLLM(testLLMRo: ITestLLMRo): Promise&lt;ITestLLMVo&gt; {</span><span class="ln">  const { type, baseUrl, apiKey, models, ... } = testLLMRo;</span><span class="ln">  ...</span><span class="ln bug">  const providerOptions = getAdaptedProviderOptions(type, { name: model, baseURL: baseUrl, apiKey });</span><span class="ln">  const modelProvider = provider({ ...providerOptions } as never) as OpenAIProvider;</span></code></pre>

<p class="mark-cap"><span><span class="mark-k">The bug</span>user supplied baseUrl becomes the provider endpoint</span></p>

The provider fetch is defined in `apps/nestjs-backend/src/features/ai/util.ts`, and it is the unguarded global `fetch`, not `safeFetch`:

<pre class="has-mark"><code class="language-ts"><span class="ln">const createFixingFetch = (): typeof fetch =&gt; {</span><span class="ln">  return async (input, init) =&gt; {</span><span class="ln bug">    const response = await fetch(input, init);   // plain global fetch, no SSRF guard</span><span class="ln">    ...</span></code></pre>

<p class="mark-cap"><span><span class="mark-k">The bug</span>plain global fetch with no SSRF guard</span></p>

The other provider factories in `modelProviders` use the AI SDK's own default fetch, also unfiltered. None of them route through the `safeFetch` that imports and external-DB connections already enforce.

## Impact

I confirmed the oracle live against `ghcr.io/teableio/teable:latest` as a non-admin user, probing docker-network services the attacker has no direct route to:

```
baseUrl teable-db:5432    (internal Postgres, OPEN) -> "Cannot connect to API: other side closed"  (connected)
baseUrl teable-db:1       (CLOSED port)             -> "Cannot connect to API: bad port"
baseUrl teable-cache:6379 (internal Redis, OPEN)    -> "other side closed"                         (connected)
```

The distinct error per target proves the server performed the attacker-directed outbound connection and reflected the result. An unprivileged tenant in a multi-tenant deployment can enumerate and fingerprint internal services, databases, caches and cloud metadata endpoints that are otherwise unreachable from its network position, and an endpoint returning OpenAI-shaped JSON reflects its body back to the caller.

## Fix

Route the AI provider path through the existing guard: pass a `createSsrfSafeFetch()`-based fetch into every entry of `modelProviders` (not only the OpenAI-compatible wrapper) and into `createGateway`, or install it as a global undici dispatcher. Restrict `baseUrl` to public https hosts via an allowlist, and return a generic failure message instead of the raw connection error so the port oracle disappears.

<section class="fs-inline" aria-labelledby="h-record"><h2 id="h-record" class="no-idx">The record</h2><dl class="fs"><dt>Weakness</dt><dd><b>CWE-918</b> Server-Side Request Forgery (SSRF)</dd><dt>Affected</dt><dd>teable <b>before release.2026-10-12T12-45-53Z.3331</b></dd><dt>Fixed in</dt><dd><b>release.2026-10-12T12-45-53Z.3331</b></dd><dt>Disclosure</dt><dd><b>2026-09-04</b> Reported privately<br><span class="fs-gap">39 days later</span><b>2026-10-13</b> Published</dd><dt>Advisory</dt><dd><a href="https://github.com/teableio/teable/security/advisories/GHSA-jvm6-86c5-f8j8">GHSA-jvm6-86c5-f8j8</a></dd><dt>Also in teable</dt><dd><a href="/advisories/ghsa-w677-p6hx-85vw/">GHSA-w677-p6hx-85vw</a> 7.1</dd></dl></section>

## About this writeup

Sanaan Fayaz Wani (GitHub [`sfwani`](https://github.com/sfwani)) reported this vulnerability to the `teable` maintainers under coordinated disclosure and is credited as a reporter in [GHSA-jvm6-86c5-f8j8](https://github.com/teableio/teable/security/advisories/GHSA-jvm6-86c5-f8j8), published 2026-10-13.

All published findings: [advisory index](/advisories/).


  </div>
  <aside class="srail" aria-label="Fact sheet" data-sev="medium"><div class="sr-h"><span class="sr-num">6.5</span><span class="sr-sev">Medium</span></div><p class="sr-src">CVSS 3.1 base</p><dl class="fs"><dt>Weakness</dt><dd><b>CWE-918</b> Server-Side Request Forgery (SSRF)</dd><dt>Affected</dt><dd>teable <b>before release.2026-10-12T12-45-53Z.3331</b></dd><dt>Fixed in</dt><dd><b>release.2026-10-12T12-45-53Z.3331</b></dd><dt>Disclosure</dt><dd><b>2026-09-04</b> Reported privately<br><span class="fs-gap">39 days later</span><b>2026-10-13</b> Published</dd><dt>Advisory</dt><dd><a href="https://github.com/teableio/teable/security/advisories/GHSA-jvm6-86c5-f8j8">GHSA-jvm6-86c5-f8j8</a></dd><dt>Also in teable</dt><dd><a href="/advisories/ghsa-w677-p6hx-85vw/">GHSA-w677-p6hx-85vw</a> 7.1</dd></dl><a class="sr-top" href="#top">Back to top</a></aside>
</section>
