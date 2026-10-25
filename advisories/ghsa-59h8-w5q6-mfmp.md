---
title: "GHSA-59h8-w5q6-mfmp"
heading: "GHSA-59h8-w5q6-mfmp"
role: "Trigger.dev: Unauthenticated Realtime Stream Data Injection via Run FriendlyId"
seo_title: "GHSA-59h8-w5q6-mfmp: Trigger.dev: Unauthenticated Realtime Stream Data Injection via Run FriendlyId - Sanaan Fayaz Wani"
ghsa_id: "GHSA-59h8-w5q6-mfmp"
cve_id: ""
published_at: "2026-07-21"
permalink: /advisories/ghsa-59h8-w5q6-mfmp/
layout: c2
description: "Trigger.dev: Unauthenticated Realtime Stream Data Injection via Run FriendlyId. trigger.dev, CVSS 5.3 Medium, CWE-306 Missing authentication. Writeup by Sanaan Fayaz Wani, the credited reporter."
image: /assets/img/og/ghsa-59h8-w5q6-mfmp.png
kicker_repo: "triggerdotdev/trigger.dev"
comments: false
last_modified_at: 2026-10-24T23:51:00+00:00
---
<section class="sec g" id="writeup" aria-labelledby="h-writeup" data-sev="medium" data-score="5.3" data-sevword="Medium" data-short="Upgrade to 4.5.5">
  <h2 id="h-writeup" class="vh">GHSA-59h8-w5q6-mfmp</h2>
  <div class="ah" data-sev="medium"><div class="ah-score"><p class="ah-num">5.3</p><p class="ah-sev">Medium</p><p class="ah-of">CVSS 3.1 base</p><div class="ah-meter" aria-hidden="true"><i style="width:53%"></i></div><ol class="tlv" aria-label="Disclosure timeline"><li><b>2026-05-22</b><span>Reported privately</span></li><li><span class="tlv-d">60 days later</span><b>2026-07-21</b><span>Published by the maintainer</span></li></ol></div><div class="act"><p class="act-k">What to do</p><p class="act-v">If you run <b>trigger.dev</b> <b>4.5.4 and earlier</b>, upgrade to <b>4.5.5</b> or later.</p></div><p class="ts"><em>Anyone who can reach it over the network</em>, with <em>no account</em> and no user interaction, can <em>change some data</em>.<span class="ts-src">Read from the CVSS 3.1 vector</span></p><div class="bx" style="--n:4"><div class="bx-head"><span class="k-lab">CVSS 3.1 metrics</span></div><div class="bx-row"><p class="bx-g">To exploit it</p><dl class="bx-grid"><div class="bx-c"><dt>Attack vector</dt><dd>Network</dd></div><div class="bx-c"><dt>Attack complexity</dt><dd>Low</dd></div><div class="bx-c"><dt>Privileges required</dt><dd>None</dd></div><div class="bx-c"><dt>User interaction</dt><dd>None</dd></div></dl></div><div class="bx-row"><p class="bx-g">What it gets</p><dl class="bx-grid"><div class="bx-c"><dt>Confidentiality</dt><dd>None</dd></div><div class="bx-c"><dt>Integrity</dt><dd>Low</dd></div><div class="bx-c"><dt>Availability</dt><dd>None</dd></div><div class="bx-c"><dt>Scope</dt><dd>Unchanged</dd></div></dl></div><p class="bx-foot"><a href="https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:N" rel="noopener">Open this vector in the FIRST calculator &#8599;</a></p></div><dl class="meta"><div class="meta-i wide"><dt class="k-lab">Weakness</dt><dd class="meta-v"><abbr title="Missing Authentication for Critical Function">CWE-306</abbr> <span class="meta-s">Missing Authentication for Critical Function</span></dd></div><div class="meta-i"><dt class="k-lab">Advisory</dt><dd class="meta-v"><a href="https://github.com/advisories/GHSA-59h8-w5q6-mfmp">GHSA-59h8-w5q6-mfmp</a></dd></div><div class="meta-i"><dt class="k-lab">CVE</dt><dd class="meta-v">not assigned</dd></div><div class="meta-i"><dt class="k-lab">Vector</dt><dd class="meta-v"><span class="vec">CVSS:3.1/<wbr>AV:N/<wbr>AC:L/<wbr>PR:N/<wbr>UI:N/<wbr>S:U/<wbr>C:N/<wbr>I:L/<wbr>A:N</span></dd></div><div class="meta-i wide"><dt class="k-lab">Also in trigger.dev</dt><dd class="meta-v"><a href="/advisories/ghsa-jc26-22qp-cgqj/">GHSA-jc26-22qp-cgqj</a> 7.9 · <a href="/advisories/ghsa-pqxw-g93w-hj9x/">GHSA-pqxw-g93w-hj9x</a> 8.1</dd></div></dl><div class="tl" role="group" aria-label="Disclosure timeline"><div class="tl-n"><b>2026-05-22</b><span>Reported privately</span></div><div class="tl-seg"><span>60 days</span></div><div class="tl-n"><b>2026-07-21</b><span>Published by the maintainer</span></div></div><p class="ah-note">My analysis of this finding: root cause, the vulnerable code, the impact and the fix, in the site’s format. The official advisory of record is linked above.</p></div>
  <div class="col-body prose" markdown="1">

### Affected versions

<div class="vts"><div class="vt" aria-hidden="true"><div class="vt-pkg">trigger.dev<span class="k-lab">npm</span></div><div class="vt-bar nolo"><div class="vt-bad"><b>No lower bound</b><i>Affected</i><b>4.5.4</b></div><div class="vt-fix">Fixed in <b>4.5.5</b></div></div></div></div>

| Package | Ecosystem | Vulnerable | Fixed in |
|:--|:--|:--|:--|
| `trigger.dev` | npm | <= 4.5.4 | 4.5.5 |
{: .vh}

## Summary

trigger.dev's realtime streams let a running task push data (logs, AI token chunks, progress) to clients subscribed to a run. The POST ingest handler at `apps/webapp/app/routes/realtime.v1.streams.$runId.$streamId.ts` carries no authentication at all. Anyone who can reach the webapp and knows a run's `friendlyId` can inject arbitrary bytes into that run's realtime stream, and those bytes are delivered to every subscriber as if they came from the task itself.

## Where it lives

The `action` handler is explicitly a plain Remix action with no auth wrapper. The comment on the function says the quiet part out loud:

<pre class="has-mark"><code class="language-typescript"><span class="ln">// Plain action for backwards compatibility with older clients that don&#x27;t send auth headers</span><span class="ln bug">export async function action({ request, params }: ActionFunctionArgs) {</span><span class="ln">  const parsedParams = ParamsSchema.safeParse(params);</span><span class="ln">  ...</span><span class="ln">  const { runId, streamId } = parsedParams.data;</span><span class="ln"> </span><span class="ln">  // Look up the run without environment scoping for backwards compatibility</span><span class="ln">  const run = await $replica.taskRun.findFirst({</span><span class="ln">    where: {</span><span class="ln bug">      friendlyId: runId,</span><span class="ln">    },</span><span class="ln">    ...</span><span class="ln">  });</span></code></pre>

<p class="mark-cap"><span><span class="mark-k">The bug</span>plain action with no authentication wrapper</span><span><span class="mark-k">The bug</span>looks up the run by id with no environment scoping</span></p>

Compare this with the GET `loader` in the same file, which is built through `createLoaderApiRoute` with `allowJWT`, a `findResource` that scopes on `runtimeEnvironmentId: auth.environment.id`, and an `authorization` block. The read path is authenticated and tenant scoped. The write path is not. The lookup deliberately drops environment scoping, so the only thing standing between an attacker and a stream is knowledge of the `friendlyId`. The handler then feeds the raw request body straight into the stream:

<pre class="has-mark"><code class="language-typescript"><span class="ln">return realtimeStream.ingestData(</span><span class="ln bug">  request.body,</span><span class="ln">  run.friendlyId,</span><span class="ln">  streamId,</span><span class="ln">  clientId,</span><span class="ln">  resumeFromChunkNumber</span><span class="ln">);</span></code></pre>

<p class="mark-cap"><span><span class="mark-k">The bug</span>raw request body goes straight into the stream</span></p>

The `friendlyId` is not a secret. It is a `run_` prefix plus a nanoid (`packages/core/src/v3/isomorphic/friendlyId.ts`), and it surfaces in dashboard URLs, API responses, SSE payloads and logs. It behaves as a bearer identifier, not a credential, so any party that has ever seen the ID can write to the stream.

## Impact

**Stream poisoning and spoofing.** An unauthenticated attacker who learns a run's `friendlyId` POSTs crafted chunks into `/realtime/v1/streams/:runId/:streamId`. Subscribers, including dashboard viewers and `@trigger.dev/react-hooks` clients, receive the injected content as legitimate task output. For AI workloads that stream model tokens to end users, this lets an attacker rewrite what the user sees mid run, forge completion data, or splice misleading or malicious content into the response.

**Cross environment reach.** Because the lookup drops environment scoping, the injection is not confined to the attacker's own tenant. Any run whose ID is known can be targeted.

## Fix

Remove the unauthenticated action and require the same authentication the GET loader already uses. Route the write path through an authenticated API builder, scope the `taskRun` lookup on the caller's `runtimeEnvironmentId`, and verify the caller owns the run before `ingestData` is reached. If older clients genuinely cannot send auth headers, gate that compatibility behind an explicit opt in rather than leaving an open write endpoint for every run in the system.

## References

* <https://github.com/triggerdotdev/trigger.dev/security/advisories/GHSA-59h8-w5q6-mfmp>
* <https://github.com/triggerdotdev/trigger.dev/pull/4250>
* <https://github.com/triggerdotdev/trigger.dev/commit/73d966ad226548b5f96fb5b4fc6fa607a3b7b8f8>
* <https://github.com/triggerdotdev/trigger.dev/releases/tag/v4.5.5>

<section class="fs-inline" aria-labelledby="h-record"><h2 id="h-record" class="no-idx">The record</h2><dl class="fs"><dt>Weakness</dt><dd><b>CWE-306</b> Missing Authentication for Critical Function</dd><dt>Affected</dt><dd>trigger.dev <b>4.5.4 and earlier</b></dd><dt>Fixed in</dt><dd><b>4.5.5</b></dd><dt>Disclosure</dt><dd><b>2026-05-22</b> Reported privately<br><span class="fs-gap">60 days later</span><b>2026-07-21</b> Published</dd><dt>Advisory</dt><dd><a href="https://github.com/advisories/GHSA-59h8-w5q6-mfmp">GHSA-59h8-w5q6-mfmp</a></dd><dt>Also in trigger.dev</dt><dd><a href="/advisories/ghsa-jc26-22qp-cgqj/">GHSA-jc26-22qp-cgqj</a> 7.9<br><a href="/advisories/ghsa-pqxw-g93w-hj9x/">GHSA-pqxw-g93w-hj9x</a> 8.1</dd></dl></section>

## About this writeup

Sanaan Fayaz Wani (GitHub [`sfwani`](https://github.com/sfwani)) reported this vulnerability to the `trigger.dev` maintainers under coordinated disclosure and is credited as a reporter in [GHSA-59h8-w5q6-mfmp](https://github.com/advisories/GHSA-59h8-w5q6-mfmp), published 2026-07-21.

All published findings: [advisory index](/advisories/).


  </div>
  <aside class="srail" aria-label="Fact sheet" data-sev="medium"><div class="sr-h"><span class="sr-num">5.3</span><span class="sr-sev">Medium</span></div><p class="sr-src">CVSS 3.1 base</p><dl class="fs"><dt>Weakness</dt><dd><b>CWE-306</b> Missing Authentication for Critical Function</dd><dt>Affected</dt><dd>trigger.dev <b>4.5.4 and earlier</b></dd><dt>Fixed in</dt><dd><b>4.5.5</b></dd><dt>Disclosure</dt><dd><b>2026-05-22</b> Reported privately<br><span class="fs-gap">60 days later</span><b>2026-07-21</b> Published</dd><dt>Advisory</dt><dd><a href="https://github.com/advisories/GHSA-59h8-w5q6-mfmp">GHSA-59h8-w5q6-mfmp</a></dd><dt>Also in trigger.dev</dt><dd><a href="/advisories/ghsa-jc26-22qp-cgqj/">GHSA-jc26-22qp-cgqj</a> 7.9<br><a href="/advisories/ghsa-pqxw-g93w-hj9x/">GHSA-pqxw-g93w-hj9x</a> 8.1</dd></dl><a class="sr-top" href="#top">Back to top</a></aside>
</section>
