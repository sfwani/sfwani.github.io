---
title: "GHSA-jc26-22qp-cgqj"
heading: "GHSA-jc26-22qp-cgqj"
role: "Supervisor workload API lacks cross-tenant authentication"
seo_title: "GHSA-jc26-22qp-cgqj: Supervisor workload API lacks cross-tenant authentication - Sanaan Fayaz Wani"
ghsa_id: "GHSA-jc26-22qp-cgqj"
cve_id: ""
published_at: "2026-09-14"
permalink: /advisories/ghsa-jc26-22qp-cgqj/
layout: c2
description: "Supervisor workload API lacks cross-tenant authentication. trigger.dev, CVSS 7.9 High, CWE-306 Missing authentication. Writeup by Sanaan Fayaz Wani, the credited reporter."
image: /assets/img/og/ghsa-jc26-22qp-cgqj.png
kicker_repo: "triggerdotdev/trigger.dev"
comments: false
last_modified_at: 2026-10-24T23:51:00+00:00
---
<section class="sec g" id="writeup" aria-labelledby="h-writeup" data-sev="high" data-score="7.9" data-sevword="High" data-short="Fix unclear">
  <h2 id="h-writeup" class="vh">GHSA-jc26-22qp-cgqj</h2>
  <div class="ah" data-sev="high"><div class="ah-score"><p class="ah-num">7.9</p><p class="ah-sev">High</p><p class="ah-of">CVSS 3.1 base</p><div class="ah-meter" aria-hidden="true"><i style="width:79%"></i></div><ol class="tlv" aria-label="Disclosure timeline"><li><b>2026-05-22</b><span>Reported privately</span></li><li><span class="tlv-d">115 days later</span><b>2026-09-14</b><span>Published by the maintainer</span></li></ol></div><div class="act warn"><p class="act-k">What to do</p><p class="act-v">If you run <b>trigger.dev</b> <b>4.6.0 and earlier</b>, the advisory lists <b>4.6.0</b> as both affected and fixed, so confirm the fixed release with the maintainer.</p></div><p class="ts"><em>Anyone on an adjacent network</em>, with <em>a low-privilege account</em> and no user interaction, given conditions outside the attacker's control, can <em>read and change sensitive data and degrade its availability</em>, and <em>the impact reaches beyond the vulnerable component</em>.<span class="ts-src">Read from the CVSS 3.1 vector</span></p><div class="bx" style="--n:4"><div class="bx-head"><span class="k-lab">CVSS 3.1 metrics</span></div><div class="bx-row"><p class="bx-g">To exploit it</p><dl class="bx-grid"><div class="bx-c"><dt>Attack vector</dt><dd>Adjacent</dd></div><div class="bx-c"><dt>Attack complexity</dt><dd>High</dd></div><div class="bx-c"><dt>Privileges required</dt><dd>Low</dd></div><div class="bx-c"><dt>User interaction</dt><dd>None</dd></div></dl></div><div class="bx-row"><p class="bx-g">What it gets</p><dl class="bx-grid"><div class="bx-c"><dt>Confidentiality</dt><dd>High</dd></div><div class="bx-c"><dt>Integrity</dt><dd>High</dd></div><div class="bx-c"><dt>Availability</dt><dd>Low</dd></div><div class="bx-c"><dt>Scope</dt><dd>Changed</dd></div></dl></div><p class="bx-foot"><a href="https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:A/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:L" rel="noopener">Open this vector in the FIRST calculator &#8599;</a></p></div><dl class="meta"><div class="meta-i wide"><dt class="k-lab">Weakness</dt><dd class="meta-v"><abbr title="Missing Authentication for Critical Function">CWE-306</abbr> <span class="meta-s">Missing Authentication for Critical Function</span></dd></div><div class="meta-i"><dt class="k-lab">Advisory</dt><dd class="meta-v"><a href="https://github.com/triggerdotdev/trigger.dev/security/advisories/GHSA-jc26-22qp-cgqj">GHSA-jc26-22qp-cgqj</a></dd></div><div class="meta-i"><dt class="k-lab">CVE</dt><dd class="meta-v">not assigned</dd></div><div class="meta-i"><dt class="k-lab">Vector</dt><dd class="meta-v"><span class="vec">CVSS:3.1/<wbr>AV:A/<wbr>AC:H/<wbr>PR:L/<wbr>UI:N/<wbr>S:C/<wbr>C:H/<wbr>I:H/<wbr>A:L</span></dd></div><div class="meta-i wide"><dt class="k-lab">Also in trigger.dev</dt><dd class="meta-v"><a href="/advisories/ghsa-59h8-w5q6-mfmp/">GHSA-59h8-w5q6-mfmp</a> 5.3 · <a href="/advisories/ghsa-pqxw-g93w-hj9x/">GHSA-pqxw-g93w-hj9x</a> 8.1</dd></div></dl><div class="tl" role="group" aria-label="Disclosure timeline"><div class="tl-n"><b>2026-05-22</b><span>Reported privately</span></div><div class="tl-seg"><span>115 days</span></div><div class="tl-n"><b>2026-09-14</b><span>Published by the maintainer</span></div></div><p class="ah-note">My analysis of this finding: root cause, the vulnerable code, the impact and the fix, in the site’s format. The official advisory of record is linked above.</p></div>
  <div class="col-body prose" markdown="1">

### Affected versions

<div class="vts"><div class="vt" aria-hidden="true"><div class="vt-pkg">trigger.dev<span class="k-lab">npm</span></div><div class="vt-bar nolo"><div class="vt-bad"><b>No lower bound</b><i>Affected</i><b>4.6.0</b></div><div class="vt-fix">Fixed in <b>4.6.0</b></div></div><p class="vt-note"><b>Data conflict</b> The advisory lists 4.6.0 as both affected and fixed.</p></div></div>

| Package | Ecosystem | Vulnerable | Fixed in |
|:--|:--|:--|:--|
| `trigger.dev` | npm | <= 4.6.0 | >= 4.6.0 |
{: .vh}

## Summary

The trigger.dev supervisor runs a workload server (default port 8020, bound to `0.0.0.0`) that drives the entire run lifecycle: starting attempts, completing them, heartbeating, suspending, continuing, and dequeuing work. Every HTTP route on this server in `apps/supervisor/src/workloadServer/index.ts` executes with zero authentication, and the WebSocket namespace only checks that two headers are present, never that they carry a secret. Any party that can reach the port can manipulate any run by its `friendlyId`.

## Where it lives

The server is constructed to listen on all interfaces by default:

<pre class="has-mark"><code class="language-typescript"><span class="ln">constructor(opts: WorkloadServerOptions) {</span><span class="ln">  super();</span><span class="ln bug">  const host = opts.host ?? &quot;0.0.0.0&quot;;</span><span class="ln">  const port = opts.port;</span><span class="ln">  ...</span></code></pre>

<p class="mark-cap"><span><span class="mark-k">The bug</span>listens on all interfaces by default</span></p>

Each lifecycle route takes a `runFriendlyId` and a `snapshotFriendlyId` from the URL and immediately calls the worker client. There is no bearer check, no shared secret, no mutual TLS. For example, the attempt start route:

<pre class="has-mark"><code class="language-typescript"><span class="ln">.route(</span><span class="ln">  &quot;/api/v1/workload-actions/runs/:runFriendlyId/snapshots/:snapshotFriendlyId/attempts/start&quot;,</span><span class="ln">  &quot;POST&quot;,</span><span class="ln">  {</span><span class="ln">    paramsSchema: WorkloadActionParams,</span><span class="ln">    bodySchema: WorkloadRunAttemptStartRequestBody,</span><span class="ln">    handler: async ({ req, reply, params, body }) =&gt; {</span><span class="ln bug">      const startResponse = await this.workerClient.startRunAttempt(</span><span class="ln">        params.runFriendlyId,</span><span class="ln">        params.snapshotFriendlyId,</span><span class="ln">        body,</span><span class="ln bug">        this.runnerIdFromRequest(req)</span><span class="ln">      );</span></code></pre>

<p class="mark-cap"><span><span class="mark-k">The bug</span>calls the worker client with no credential check</span><span><span class="mark-k">The bug</span>runner id comes from an unverified request header</span></p>

The same shape repeats for `/attempts/complete`, `/heartbeat`, `/suspend`, `/continue`, `/snapshots/since`, and `/deployments/:deploymentId/dequeue`. The only identity signal is a `runnerId` pulled from a request header, used for bookkeeping, not verified against anything.

The WebSocket side is no better. The namespace middleware only copies two headers into socket data and disconnects if they are missing:

<pre class="has-mark"><code class="language-typescript"><span class="ln">setSocketDataFromHeader(&quot;deploymentId&quot;, WORKLOAD_HEADERS.DEPLOYMENT_ID);</span><span class="ln">setSocketDataFromHeader(&quot;runnerId&quot;, WORKLOAD_HEADERS.RUNNER_ID);</span><span class="ln">...</span><span class="ln bug">this.logger.debug(&quot;[WS] auth success&quot;, socket.data);</span></code></pre>

<p class="mark-cap"><span><span class="mark-k">The bug</span>header presence alone counts as auth success</span></p>

Presence of a header is treated as authentication. Both values are attacker suppliable.

## Impact

**Run lifecycle hijack.** An attacker on the network forges requests for any known `runFriendlyId` and `snapshotFriendlyId` pair. They can mark attempts complete with attacker chosen results, force completion or failure, spoof heartbeats to keep dead runs alive or let live ones expire, and trigger suspend and continue transitions out of order.

**Work theft and injection.** The dequeue route hands out queued work for a deployment to anyone who asks, so an attacker can pull pending runs intended for legitimate runners. Combined with the complete route, this lets an attacker intercept a run and return forged output as the task result.

This is a direct consequence of the supervisor trusting its network. On the default self-hosted stack the runner containers share that network, so the exposure is reachable, not theoretical.

## Fix

Require a real credential on every workload route and on the WebSocket handshake. The deployment already provisions a `MANAGED_WORKER_SECRET`; verify it (or a per runner token) on each request instead of merely reading the `runnerId` header. Stop treating header presence as authentication in the socket middleware, and bind the server to a private interface rather than `0.0.0.0` unless an authenticated gateway sits in front of it.

<section class="fs-inline" aria-labelledby="h-record"><h2 id="h-record" class="no-idx">The record</h2><dl class="fs"><dt>Weakness</dt><dd><b>CWE-306</b> Missing Authentication for Critical Function</dd><dt>Affected</dt><dd>trigger.dev <b>4.6.0 and earlier</b></dd><dt>Fixed in</dt><dd><b>Unclear in the record</b></dd><dt>Disclosure</dt><dd><b>2026-05-22</b> Reported privately<br><span class="fs-gap">115 days later</span><b>2026-09-14</b> Published</dd><dt>Advisory</dt><dd><a href="https://github.com/triggerdotdev/trigger.dev/security/advisories/GHSA-jc26-22qp-cgqj">GHSA-jc26-22qp-cgqj</a></dd><dt>Also in trigger.dev</dt><dd><a href="/advisories/ghsa-59h8-w5q6-mfmp/">GHSA-59h8-w5q6-mfmp</a> 5.3<br><a href="/advisories/ghsa-pqxw-g93w-hj9x/">GHSA-pqxw-g93w-hj9x</a> 8.1</dd></dl></section>

## About this writeup

Sanaan Fayaz Wani (GitHub [`sfwani`](https://github.com/sfwani)) reported this vulnerability to the `trigger.dev` maintainers under coordinated disclosure and is credited as a reporter in [GHSA-jc26-22qp-cgqj](https://github.com/triggerdotdev/trigger.dev/security/advisories/GHSA-jc26-22qp-cgqj), published 2026-09-14.

All published findings: [advisory index](/advisories/).


  </div>
  <aside class="srail" aria-label="Fact sheet" data-sev="high"><div class="sr-h"><span class="sr-num">7.9</span><span class="sr-sev">High</span></div><p class="sr-src">CVSS 3.1 base</p><dl class="fs"><dt>Weakness</dt><dd><b>CWE-306</b> Missing Authentication for Critical Function</dd><dt>Affected</dt><dd>trigger.dev <b>4.6.0 and earlier</b></dd><dt>Fixed in</dt><dd><b>Unclear in the record</b></dd><dt>Disclosure</dt><dd><b>2026-05-22</b> Reported privately<br><span class="fs-gap">115 days later</span><b>2026-09-14</b> Published</dd><dt>Advisory</dt><dd><a href="https://github.com/triggerdotdev/trigger.dev/security/advisories/GHSA-jc26-22qp-cgqj">GHSA-jc26-22qp-cgqj</a></dd><dt>Also in trigger.dev</dt><dd><a href="/advisories/ghsa-59h8-w5q6-mfmp/">GHSA-59h8-w5q6-mfmp</a> 5.3<br><a href="/advisories/ghsa-pqxw-g93w-hj9x/">GHSA-pqxw-g93w-hj9x</a> 8.1</dd></dl><a class="sr-top" href="#top">Back to top</a></aside>
</section>
