---
title: "GHSA-pqxw-g93w-hj9x"
heading: "GHSA-pqxw-g93w-hj9x"
role: "Trigger.dev Self-Hosted Deployment: Default Secrets allow Unauthenticated Infrastructure Compromise"
seo_title: "GHSA-pqxw-g93w-hj9x: Trigger.dev Self-Hosted Deployment: Default Secrets allow Unauthenticated… - Sanaan Fayaz Wani"
ghsa_id: "GHSA-pqxw-g93w-hj9x"
cve_id: ""
published_at: "2026-07-21"
permalink: /advisories/ghsa-pqxw-g93w-hj9x/
layout: c2
description: "Trigger.dev Self-Hosted Deployment: Default Secrets allow Unauthenticated Infrastructure Compromise. trigger.dev, CVSS 8.1 High, CWE-653 Improper isolation. Writeup by Sanaan Fayaz Wani, the credited reporter."
image: /assets/img/og/ghsa-pqxw-g93w-hj9x.png
kicker_repo: "triggerdotdev/trigger.dev"
comments: false
last_modified_at: 2026-10-24T23:57:10+00:00
---
<section class="sec g" id="writeup" aria-labelledby="h-writeup" data-sev="high" data-score="8.1" data-sevword="High" data-short="Upgrade to 4.5.6">
  <h2 id="h-writeup" class="vh">GHSA-pqxw-g93w-hj9x</h2>
  <div class="ah" data-sev="high"><div class="ah-score"><p class="ah-num">8.1</p><p class="ah-sev">High</p><p class="ah-of">CVSS-BT 4.0</p><div class="ah-meter" aria-hidden="true"><i style="width:81%"></i></div><ol class="tlv" aria-label="Disclosure timeline"><li><b>2026-05-22</b><span>Reported privately</span></li><li><span class="tlv-d">60 days later</span><b>2026-07-21</b><span>Published by the maintainer</span></li></ol></div><div class="act"><p class="act-k">What to do</p><p class="act-v">If you run <b>trigger.dev</b> <b>4.5.5 and earlier</b>, upgrade to <b>4.5.6</b> or later.</p></div><p class="ts"><em>Anyone who can reach it over the network</em>, with <em>no account</em> and no user interaction, if they can defeat a protection or obtain a target-specific secret, can <em>read and change sensitive data</em>.<span class="ts-src">Read from the CVSS 4.0 vector</span></p><div class="bx" style="--n:5"><div class="bx-head"><span class="k-lab">CVSS 4.0 metrics</span></div><div class="bx-row"><p class="bx-g">To exploit it</p><dl class="bx-grid"><div class="bx-c"><dt>Attack vector</dt><dd>Network</dd></div><div class="bx-c"><dt>Attack complexity</dt><dd>High</dd></div><div class="bx-c"><dt>Attack requirements</dt><dd>None</dd></div><div class="bx-c"><dt>Privileges required</dt><dd>None</dd></div><div class="bx-c"><dt>User interaction</dt><dd>None</dd></div></dl></div><div class="bx-row"><p class="bx-g">What it gets</p><dl class="bx-grid"><div class="bx-c"><dt>Confidentiality</dt><dd>High</dd></div><div class="bx-c"><dt>Integrity</dt><dd>High</dd></div><div class="bx-c"><dt>Availability</dt><dd>None</dd></div></dl></div><div class="bx-row"><p class="bx-g">Other systems</p><dl class="bx-grid"><div class="bx-c"><dt>Confidentiality</dt><dd>None</dd></div><div class="bx-c"><dt>Integrity</dt><dd>None</dd></div><div class="bx-c"><dt>Availability</dt><dd>None</dd></div></dl></div><p class="bx-threat"><span class="k-lab">Threat</span>Exploit maturity: <b>Proof of concept</b>. Because this is set, the score is CVSS-BT.</p><p class="bx-foot"><a href="https://www.first.org/cvss/calculator/4.0#CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:P" rel="noopener">Open this vector in the FIRST calculator &#8599;</a></p></div><dl class="meta"><div class="meta-i wide"><dt class="k-lab">Weakness</dt><dd class="meta-v"><abbr title="Improper Isolation or Compartmentalization">CWE-653</abbr>, <abbr title="Use of Default Password">CWE-1393</abbr> <span class="meta-s">Improper Isolation or Compartmentalization · Use of Default Password</span></dd></div><div class="meta-i"><dt class="k-lab">Advisory</dt><dd class="meta-v"><a href="https://github.com/advisories/GHSA-pqxw-g93w-hj9x">GHSA-pqxw-g93w-hj9x</a></dd></div><div class="meta-i"><dt class="k-lab">CVE</dt><dd class="meta-v">not assigned</dd></div><div class="meta-i"><dt class="k-lab">Vector</dt><dd class="meta-v"><span class="vec">CVSS:4.0/<wbr>AV:N/<wbr>AC:H/<wbr>AT:N/<wbr>PR:N/<wbr>UI:N/<wbr>VC:H/<wbr>VI:H/<wbr>VA:N/<wbr>SC:N/<wbr>SI:N/<wbr>SA:N/<wbr>E:P</span></dd></div><div class="meta-i wide"><dt class="k-lab">Also in trigger.dev</dt><dd class="meta-v"><a href="/advisories/ghsa-jc26-22qp-cgqj/">GHSA-jc26-22qp-cgqj</a> 7.9 · <a href="/advisories/ghsa-59h8-w5q6-mfmp/">GHSA-59h8-w5q6-mfmp</a> 5.3</dd></div></dl><div class="tl" role="group" aria-label="Disclosure timeline"><div class="tl-n"><b>2026-05-22</b><span>Reported privately</span></div><div class="tl-seg"><span>60 days</span></div><div class="tl-n"><b>2026-07-21</b><span>Published by the maintainer</span></div></div><p class="ah-note">My analysis of this finding: root cause, the vulnerable code, the impact and the fix, in the site’s format. The official advisory of record is linked above.</p></div>
  <div class="col-body prose" markdown="1">

### Affected versions

<div class="vts"><div class="vt" aria-hidden="true"><div class="vt-pkg">trigger.dev<span class="k-lab">npm</span></div><div class="vt-bar nolo"><div class="vt-bad"><b>No lower bound</b><i>Affected</i><b>4.5.5</b></div><div class="vt-fix">Fixed in <b>4.5.6</b></div></div></div></div>

| Package | Ecosystem | Vulnerable | Fixed in |
|:--|:--|:--|:--|
| `trigger.dev` | npm | <= 4.5.5 | 4.5.6 |
{: .vh}

<div markdown="0">
<figure class="fig fig-chain" id="fig-chain" aria-labelledby="chain-h">
  <figcaption>
    <p class="fig-h" id="chain-h">Chain &middot; GHSA-pqxw-g93w-hj9x &middot; trigger.dev</p>
    <p class="fig-note" id="chain-n">Five steps from a file committed to the repository to three data stores with their own credentials. Each step is paired with the control that was supposed to stop it and was not there. Every fact is taken from the published advisory; the right-hand column names the control that advisory says was missing.</p>
  </figcaption>

  <p class="fig-vh">Text alternative. Step 00: the repository ships hosting/docker/.env.example containing four fixed secrets, among them MAGIC_LINK_SECRET equal to 44da78b7bbb0dfe709cf38931d25dcdd; the documented install copies that file to .env. Absent control: secrets are not generated on first boot and the service does not refuse to start on a known value. Step 01: the attacker forges a magic link offline by AES-encrypting a JSON payload naming any email address with that secret, which remix-auth-email-link version 2.0.2 accepts. Absent control: the token is encryption rather than a server-side record, so nothing ties it to a link the server actually issued. Step 02: requesting /magic with the forged token returns HTTP 302 and sets a __session cookie. Absent control: validateSessionMagicLink defaults to false in the library and trigger.dev never overrides it, so no session-side check confirms this browser asked for the link. Step 03: the account is created on the spot because WHITELISTED_EMAILS is unset, which is the self-hosted default; the attacker is now any user they named. Absent control: no allowlist and no email delivery step proving control of the address. Step 04: hosting/docker/worker/docker-compose.yml line 42 sets DOCKER_RUNNER_NETWORKS to webapp and supervisor, placing runner containers on the same Docker networks as the platform's own data stores. Absent control: no segmentation between run sandboxes and infrastructure. From there the advisory verifies Postgres reachable with the default password unsafe-postgres-pw and returning the User table, Redis answering PING with no authentication, and ClickHouse answering a version query as default colon password; separately, ENCRYPTION_KEY sits in the same shipped file, so data the platform encrypted at rest is decryptable.</p>

  <ol class="ch-steps" aria-hidden="true">
    <li class="ch-step">
      <p class="ch-i">00</p>
      <div class="ch-b">
        <p class="ch-act">The secret ships in the repository</p>
        <p class="ch-ev"><code>hosting/docker/.env.example</code> lines 9 to 12 hold four fixed values, among them <code>MAGIC_LINK_SECRET=44da78b7bbb0dfe709cf38931d25dcdd</code>. The documented install is <code>cp .env.example .env</code>.</p>
      </div>
      <p class="ch-gate"><span class="ch-gk">Absent control</span>Secrets are not generated on first boot, and the service does not refuse to start on a known value.</p>
    </li>
    <li class="ch-step">
      <p class="ch-i">01</p>
      <div class="ch-b">
        <p class="ch-act">Forge a magic link, offline</p>
        <p class="ch-ev"><code>CryptoJS.AES.encrypt(JSON.stringify({e:'attacker@evil.com',c:Date.now()}), secret)</code>. No contact with the target yet. <code>remix-auth-email-link@2.0.2</code> accepts the result.</p>
      </div>
      <p class="ch-gate"><span class="ch-gk">Absent control</span>The token is encryption, not a server-side record. Nothing binds it to a link the server actually issued.</p>
    </li>
    <li class="ch-step">
      <p class="ch-i">02</p>
      <div class="ch-b">
        <p class="ch-act">Redeem it</p>
        <p class="ch-ev"><code>GET /magic?token=&hellip;</code> returns <code>HTTP 302</code> with <code>set-cookie: __session=&hellip;</code></p>
      </div>
      <p class="ch-gate"><span class="ch-gk">Absent control</span><code>validateSessionMagicLink</code> defaults to <code>false</code> in the library and is never overridden, so nothing checks that this browser asked for the link.</p>
    </li>
    <li class="ch-step">
      <p class="ch-i">03</p>
      <div class="ch-b">
        <p class="ch-act">Become any user</p>
        <p class="ch-ev">The account is created on the spot: <code>WHITELISTED_EMAILS</code> unset is the self-hosted default.</p>
      </div>
      <p class="ch-gate"><span class="ch-gk">Absent control</span>No allowlist, and no email delivery step that would prove control of the address.</p>
    </li>
    <li class="ch-step">
      <p class="ch-i">04</p>
      <div class="ch-b">
        <p class="ch-act">Stand on the infrastructure network</p>
        <p class="ch-ev"><code>DOCKER_RUNNER_NETWORKS: webapp,supervisor</code> at <code>hosting/docker/worker/docker-compose.yml:42</code> puts runner containers on the same Docker networks as the platform&rsquo;s own data stores.</p>
      </div>
      <p class="ch-gate"><span class="ch-gk">Absent control</span>No segmentation between run sandboxes and infrastructure.</p>
    </li>
  </ol>

  <div class="ch-bus" aria-hidden="true"></div>

  <ul class="ch-leaves" aria-hidden="true">
    <li>
      <p class="ch-ln">Postgres</p>
      <p class="ch-le">Default password <code>unsafe-postgres-pw</code>. <code>SELECT id, email FROM "User"</code> returns the forged account.</p>
    </li>
    <li>
      <p class="ch-ln">Redis</p>
      <p class="ch-le">No authentication configured. <code>redis-cli -h redis PING</code> answers <code>PONG</code>.</p>
    </li>
    <li>
      <p class="ch-ln">ClickHouse</p>
      <p class="ch-le">Default <code>default:password</code>. A version query answers <code>25.5.2.47</code>.</p>
    </li>
    <li>
      <p class="ch-ln">Secrets at rest</p>
      <p class="ch-le">No network needed: <code>ENCRYPTION_KEY</code> is in the same shipped file, so stored secrets decrypt.</p>
    </li>
  </ul>

  <p class="ch-scope"><b>Scope changed.</b> The vulnerable component is the webapp. Postgres, Redis and ClickHouse are separate security authorities with credentials of their own, and the chain reaches them anyway. That is the <code>S:C</code> in the vector, and it is most of what separates this from a single-app compromise.</p>

  <p class="fig-foot">Steps 3 to 5 of the advisory verify Postgres, Redis and ClickHouse with commands; pushing backdoored images to the registry and manipulating job queues are stated in its impact section without a verification step. Affects trigger.dev <code>&lt;= 4.5.5</code>. Published 2026-07-21.</p>
</figure>
</div>

## Summary

The self-hosting stack for trigger.dev v4 ships a `.env.example` at `hosting/docker/.env.example` that contains real, working secret values rather than placeholders. Operators who copy it to `.env` (the documented path) inherit a publicly known `MAGIC_LINK_SECRET`, `ENCRYPTION_KEY`, `SESSION_SECRET`, and default database, Redis, ClickHouse and object store credentials. I verified a full unauthenticated chain against a live default instance: forge a magic link, land an authenticated session with no email delivery, and reach every infrastructure service with its shipped password.

## Where it lives

The secrets are committed in plaintext. These are not throwaway placeholders, they are the values the compose stack actually loads:

<pre class="has-mark"><code class="language-bash"><span class="ln">SESSION_SECRET=2818143646516f6fffd707b36f334bbb</span><span class="ln bug">MAGIC_LINK_SECRET=44da78b7bbb0dfe709cf38931d25dcdd</span><span class="ln bug">ENCRYPTION_KEY=f686147ab967943ebbe9ed3b496e465a</span><span class="ln">MANAGED_WORKER_SECRET=447c29678f9eaf289e9c4b70d3dd8a7f</span><span class="ln">...</span><span class="ln">POSTGRES_PASSWORD=unsafe-postgres-pw</span><span class="ln">DATABASE_URL=postgresql://postgres:unsafe-postgres-pw@postgres:5432/main?...</span><span class="ln">CLICKHOUSE_URL=http://default:password@clickhouse:8123?secure=false</span><span class="ln">OBJECT_STORE_ACCESS_KEY_ID=admin</span><span class="ln">OBJECT_STORE_SECRET_ACCESS_KEY=very-safe-password</span></code></pre>

<p class="mark-cap"><span><span class="mark-k">The bug</span>shipped magic link secret lets anyone mint login tokens</span><span><span class="mark-k">The bug</span>published key decrypts every stored tenant secret</span></p>

The `MAGIC_LINK_SECRET` is the keystone. trigger.dev's passwordless login encrypts the magic link token with this secret, so knowing it lets anyone mint a valid login token for any email without ever receiving the email. My PoC reproduces the exact token the server expects:

```javascript
const MAGIC_LINK_SECRET = "44da78b7bbb0dfe709cf38931d25dcdd";
const payload = JSON.stringify({ e: email, c: Date.now() });
const encrypted = CryptoJS.AES.encrypt(payload, MAGIC_LINK_SECRET).toString();
// GET /magic?token=<encodeURIComponent(encrypted)>  -> session cookie, user auto-created
```

## Impact

**Unauthenticated session forging.** Visiting the forged `/magic?token=...` URL auto-creates the account and sets a session cookie. Against a live default instance the chain produced a working session (`HTTP 302 -> /orgs/new`) with no interaction from any real user.

**Full infrastructure access.** With the webapp network reachable (the default stack places runner containers on it), the shipped credentials opened every backend service directly: PostgreSQL via `postgres:unsafe-postgres-pw` with all tenant tables readable (`User`, `SecretStore`, `PersonalAccessToken`, `EnvironmentVariable`, `RuntimeEnvironment`, `OrgMember`), Redis answering `PONG` with no auth, and ClickHouse returning its version via `default:password`.

**Secret decryption.** `ENCRYPTION_KEY=f686147ab967943ebbe9ed3b496e465a` is the key used to encrypt stored secrets, so the `SecretStore` contents an attacker reads from PostgreSQL are decryptable with the same published value. The breach is not limited to metadata, it extends to the credentials trigger.dev holds on behalf of every tenant.

Taken together this is a complete, cross tenant compromise of any self hosted instance left on the defaults, reachable by an unauthenticated remote attacker.

## Fix

Stop shipping live secrets in a file operators are told to copy. The stack should generate unique secrets at deploy time through a bootstrap step, and the webapp should refuse to start when `MAGIC_LINK_SECRET`, `ENCRYPTION_KEY` or `SESSION_SECRET` match a known published default or are empty. Enable Redis authentication with an auto generated password, give the task runners an isolated network that can reach only the supervisor workload API, and require real credentials on the infrastructure services rather than the committed ones.

## References

* <https://github.com/triggerdotdev/trigger.dev/security/advisories/GHSA-pqxw-g93w-hj9x>
* <https://github.com/triggerdotdev/trigger.dev/pull/4316>
* <https://github.com/triggerdotdev/trigger.dev/commit/6997aeb05e27d2db47f9eda01fdc8a17c81a1ae0>
* <https://github.com/triggerdotdev/trigger.dev/releases/tag/v4.5.6>

<section class="fs-inline" aria-labelledby="h-record"><h2 id="h-record" class="no-idx">The record</h2><dl class="fs"><dt>Weakness</dt><dd><b>CWE-653</b> Improper Isolation or Compartmentalization<br><b>CWE-1393</b> Use of Default Password</dd><dt>Affected</dt><dd>trigger.dev <b>4.5.5 and earlier</b></dd><dt>Fixed in</dt><dd><b>4.5.6</b></dd><dt>Disclosure</dt><dd><b>2026-05-22</b> Reported privately<br><span class="fs-gap">60 days later</span><b>2026-07-21</b> Published</dd><dt>Advisory</dt><dd><a href="https://github.com/advisories/GHSA-pqxw-g93w-hj9x">GHSA-pqxw-g93w-hj9x</a></dd><dt>Also in trigger.dev</dt><dd><a href="/advisories/ghsa-jc26-22qp-cgqj/">GHSA-jc26-22qp-cgqj</a> 7.9<br><a href="/advisories/ghsa-59h8-w5q6-mfmp/">GHSA-59h8-w5q6-mfmp</a> 5.3</dd></dl></section>

## About this writeup

Sanaan Fayaz Wani (GitHub [`sfwani`](https://github.com/sfwani)) reported this vulnerability to the `trigger.dev` maintainers under coordinated disclosure and is credited as a reporter in [GHSA-pqxw-g93w-hj9x](https://github.com/advisories/GHSA-pqxw-g93w-hj9x), published 2026-07-21.

All published findings: [advisory index](/advisories/).


  </div>
  <aside class="srail" aria-label="Fact sheet" data-sev="high"><div class="sr-h"><span class="sr-num">8.1</span><span class="sr-sev">High</span></div><p class="sr-src">CVSS-BT 4.0</p><dl class="fs"><dt>Weakness</dt><dd><b>CWE-653</b> Improper Isolation or Compartmentalization<br><b>CWE-1393</b> Use of Default Password</dd><dt>Affected</dt><dd>trigger.dev <b>4.5.5 and earlier</b></dd><dt>Fixed in</dt><dd><b>4.5.6</b></dd><dt>Disclosure</dt><dd><b>2026-05-22</b> Reported privately<br><span class="fs-gap">60 days later</span><b>2026-07-21</b> Published</dd><dt>Advisory</dt><dd><a href="https://github.com/advisories/GHSA-pqxw-g93w-hj9x">GHSA-pqxw-g93w-hj9x</a></dd><dt>Also in trigger.dev</dt><dd><a href="/advisories/ghsa-jc26-22qp-cgqj/">GHSA-jc26-22qp-cgqj</a> 7.9<br><a href="/advisories/ghsa-59h8-w5q6-mfmp/">GHSA-59h8-w5q6-mfmp</a> 5.3</dd></dl><a class="sr-top" href="#top">Back to top</a></aside>
</section>
