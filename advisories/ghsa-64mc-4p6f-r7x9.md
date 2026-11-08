---
title: "GHSA-64mc-4p6f-r7x9"
heading: "GHSA-64mc-4p6f-r7x9"
role: "Revoked or unconfirmed organization Admin can read cipher audit logs"
seo_title: "GHSA-64mc-4p6f-r7x9: Revoked or unconfirmed organization Admin can read cipher audit logs - Sanaan Fayaz Wani"
ghsa_id: "GHSA-64mc-4p6f-r7x9"
cve_id: ""
published_at: "2026-10-28"
permalink: /advisories/ghsa-64mc-4p6f-r7x9/
layout: c2
description: "Revoked or unconfirmed organization Admin can read cipher audit logs. vaultwarden, CVSS 4.3 Medium, CWE-863 Incorrect authorization. Writeup by Sanaan Fayaz Wani, the credited reporter."
image: /assets/img/og/ghsa-64mc-4p6f-r7x9.png
kicker_repo: "dani-garcia/vaultwarden"
comments: false
last_modified_at: 2026-11-07T21:22:25+00:00
---
<section class="sec g" id="writeup" aria-labelledby="h-writeup" data-sev="medium" data-score="4.3" data-sevword="Medium" data-short="Upgrade to 1.37.4">
  <h2 id="h-writeup" class="vh">GHSA-64mc-4p6f-r7x9</h2>
  <div class="ah" data-sev="medium"><div class="ah-score"><p class="ah-num">4.3</p><p class="ah-sev">Medium</p><p class="ah-of">CVSS 3.1 base</p><div class="ah-meter" aria-hidden="true"><i style="width:43%"></i></div><ol class="tlv" aria-label="Disclosure timeline"><li><b>2026-09-17</b><span>Reported privately</span></li><li><span class="tlv-d">41 days later</span><b>2026-10-28</b><span>Published by the maintainer</span></li></ol></div><div class="act"><p class="act-k">What to do</p><p class="act-v">If you run <b>vaultwarden</b> <b>1.37.3 and earlier</b>, upgrade to <b>1.37.4</b> or later.</p></div><p class="ts"><em>Anyone who can reach it over the network</em>, with <em>a low-privilege account</em> and no user interaction, can <em>read some data</em>.<span class="ts-src">Read from the CVSS 3.1 vector</span></p><div class="bx" style="--n:4"><div class="bx-head"><span class="k-lab">CVSS 3.1 metrics</span></div><div class="bx-row"><p class="bx-g">To exploit it</p><dl class="bx-grid"><div class="bx-c"><dt>Attack vector</dt><dd>Network</dd></div><div class="bx-c"><dt>Attack complexity</dt><dd>Low</dd></div><div class="bx-c"><dt>Privileges required</dt><dd>Low</dd></div><div class="bx-c"><dt>User interaction</dt><dd>None</dd></div></dl></div><div class="bx-row"><p class="bx-g">What it gets</p><dl class="bx-grid"><div class="bx-c"><dt>Confidentiality</dt><dd>Low</dd></div><div class="bx-c"><dt>Integrity</dt><dd>None</dd></div><div class="bx-c"><dt>Availability</dt><dd>None</dd></div><div class="bx-c"><dt>Scope</dt><dd>Unchanged</dd></div></dl></div><p class="bx-foot"><a href="https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:N" rel="noopener">Open this vector in the FIRST calculator &#8599;</a></p></div><dl class="meta"><div class="meta-i wide"><dt class="k-lab">Weakness</dt><dd class="meta-v"><abbr title="Incorrect Authorization">CWE-863</abbr> <span class="meta-s">Incorrect Authorization</span></dd></div><div class="meta-i"><dt class="k-lab">Advisory</dt><dd class="meta-v"><a href="https://github.com/dani-garcia/vaultwarden/security/advisories/GHSA-64mc-4p6f-r7x9">GHSA-64mc-4p6f-r7x9</a></dd></div><div class="meta-i"><dt class="k-lab">CVE</dt><dd class="meta-v">not assigned</dd></div><div class="meta-i"><dt class="k-lab">Vector</dt><dd class="meta-v"><span class="vec">CVSS:3.1/<wbr>AV:N/<wbr>AC:L/<wbr>PR:L/<wbr>UI:N/<wbr>S:U/<wbr>C:L/<wbr>I:N/<wbr>A:N</span></dd></div></dl><div class="tl" role="group" aria-label="Disclosure timeline"><div class="tl-n"><b>2026-09-17</b><span>Reported privately</span></div><div class="tl-seg"><span>41 days</span></div><div class="tl-n"><b>2026-10-28</b><span>Published by the maintainer</span></div></div><p class="ah-note">This page reproduces the published advisory for this finding. The advisory of record is linked above.</p></div>
  <div class="col-body prose" markdown="1">

### Affected versions

<div class="vts"><div class="vt" aria-hidden="true"><div class="vt-pkg">vaultwarden<span class="k-lab">rust</span></div><div class="vt-bar nolo"><div class="vt-bad"><b>No lower bound</b><i>Affected</i><b>1.37.3</b></div><div class="vt-fix">Fixed in <b>1.37.4</b></div></div></div></div>

| Package | Ecosystem | Vulnerable | Fixed in |
|:--|:--|:--|:--|
| `vaultwarden` | rust | <= 1.37.3 | 1.37.4 |
{: .vh}

## Summary

`GET /api/ciphers/<cipher_id>/events` returns an organization cipher's audit log to any
authenticated user whose membership row carries `atype` Owner or Admin, **regardless of
membership status**. A member who was invited but never confirmed, or who was confirmed and
later revoked, keeps indefinite read access to that cipher's access history: who viewed,
edited, copied or autofilled the credential, when, from which IP and device type.

The two sibling event endpoints in the same file are guarded correctly. This one is not.

Requires `ORG_EVENTS_ENABLED=true`, which is not the default.

## Affected

1.37.3 (current release) and `main` at commit `25dfedaf` (2026-09-09). Verified on both.

## Root cause

`src/api/core/events.rs` has three event endpoints. Two require `AdminHeaders`:

```rust
:34  async fn get_org_events(..., headers: AdminHeaders, ...)      // organization events
:92  async fn get_user_events(..., headers: AdminHeaders, ...)     // per member events
:66  async fn get_cipher_events(..., headers: Headers, ...)        // per cipher events
```

`AdminHeaders` resolves through `is_confirmed_and_admin()` at `src/auth.rs:725`:

```rust
fn is_confirmed_and_admin(&self) -> bool {
    self.membership_status == MembershipStatus::Confirmed && self.membership_type >= MembershipType::Admin
}
```

`get_cipher_events` instead takes the generic `Headers` guard, which only proves a valid user
JWT, and hand rolls its own check via `Membership::user_has_ge_admin_access_to_cipher` at
`src/db/models/organization.rs:1105`:

```rust
users_organizations::table
    .inner_join(ciphers::table.on(ciphers::uuid.eq(cipher_uuid)
        .and(ciphers::organization_uuid.eq(users_organizations::org_uuid.nullable()))))
    .filter(users_organizations::user_uuid.eq(user_uuid))
    .filter(users_organizations::atype.eq_any(vec![MembershipType::Owner as i32,
                                                   MembershipType::Admin as i32]))
```

That reproduces the `membership_type >= Admin` half of `is_confirmed_and_admin` and drops the
`membership_status == Confirmed` half.

Every other membership query in `organization.rs` states the invariant in its own name and
enforces it: `find_confirmed_by_user`, `find_confirmed_by_user_and_org`, `find_confirmed_by_org`,
`find_confirmed_and_manage_all_by_org`, `count_confirmed_by_org_and_type`,
`find_by_user_and_policy`. The one function that deliberately omits it is named
`find_any_state_by_user`. `user_has_ge_admin_access_to_cipher` omits it without saying so.

Upstream Bitwarden gates the equivalent endpoint with the same check it uses for organization
events (`src/Api/Dirt/Controllers/EventsController.cs`, `AccessEventLogs`). The comment at
`src/api/core/events.rs:32` cites that controller as the reference implementation.

## Steps to Reproduce

```
docker run -d --name vw-repro \
  -e ORG_EVENTS_ENABLED=true -e SIGNUPS_ALLOWED=true \
  -e I_REALLY_WANT_VOLATILE_STORAGE=true -e ROCKET_PORT=8080 \
  -p 127.0.0.1:8081:8080 vaultwarden/server:1.37.3
```

`repro.py` in the attached archive runs both variants end to end and prints a verdict. It needs
only the `cryptography` package.

### Variant 1, never confirmed invitee

1. Alice creates an organization and a cipher in it, then views it once.
2. Alice invites Bob with `type: 1` (Admin). With SMTP disabled his membership is
   `type=1, status=1` (Accepted). He has never been confirmed and holds no organization key.
3. Bob requests the cipher itself: `GET /api/ciphers/<cipher_id>` returns **HTTP 400**.
4. Bob requests its audit log: `GET /api/ciphers/<cipher_id>/events?start=...&end=...`
   returns **HTTP 200 with the event list**.

Observed:

```
Bob membership: type=1 status=1  (Accepted, never confirmed, holds no org key)
GET /api/ciphers/{id}          -> HTTP 400   (cipher itself denied)
GET /api/ciphers/{id}/events   -> HTTP 200, 1 events
```

### Variant 2, revoked admin, and the leak is ongoing

1. Bob is confirmed as Admin and reads the audit log: HTTP 200, 3 events.
2. Alice revokes him: `PUT /api/organizations/<org_id>/users/<member_id>/revoke`.
   His membership becomes `type=1, status=-1`.
3. Bob calls `GET /api/organizations/<org_id>/users`: **HTTP 401**. Revocation is enforced.
4. Bob calls the audit log again: **HTTP 200, same 3 events**.
5. Bob logs in from scratch while revoked and repeats: **HTTP 200, 3 events**. Not a stale token.
6. Alice rotates the credential *after* the revocation. Bob reads again: **the new event is
   present**. This is ongoing visibility, not a stale snapshot.

Observed:

```
events visible to Bob now: 1
Alice rotates the password AFTER Bob's access should have ended
events visible to Bob now: 2  (delta +1)
```

Fully removing the member does close the hole, because the membership row is deleted.

## Impact

Event records returned include `type`, `actingUserId`, `date`, `deviceType` and `ipAddress`
(`src/db/models/event.rs:178`). The `type` enum (`event.rs:71`) distinguishes
`CipherClientViewed`, `CipherClientToggledPasswordVisible`, `CipherClientCopiedPassword` and
`CipherClientAutofilled`, so per cipher the caller learns which colleague used a shared
credential, in what way, from which IP, and when. `continuationToken` pagination returns full
history rather than one page.

`actingUserId` is a UUID, but anyone who held Admin previously harvested the UUID to email
mapping from the member list while they had it.

Cipher contents are not disclosed, and events cannot be forged: `post_events_collect` requires
a confirmed membership or cipher access (`events.rs:187`, `events.rs:207`).

The realistic scenario is an offboarded administrator or contractor. Revoke is the documented
way to suspend a member while keeping their record, so it is the path an administrator is most
likely to take.

## Suggested fix

`src/db/models/organization.rs:1113`

```diff
             .filter(users_organizations::user_uuid.eq(user_uuid))
+            .filter(users_organizations::status.eq(MembershipStatus::Confirmed as i32))
             .filter(
                 users_organizations::atype.eq_any(vec![MembershipType::Owner as i32, MembershipType::Admin as i32]),
             )
```

This restores parity with `is_confirmed_and_admin()` at `src/auth.rs:725` and with
`find_confirmed_by_user_and_org` in the same file.

## CVSS and CWE

CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:N (4.3, Medium)

CWE-863 Incorrect Authorization

<section class="fs-inline" aria-labelledby="h-record"><h2 id="h-record" class="no-idx">The record</h2><dl class="fs"><dt>Weakness</dt><dd><b>CWE-863</b> Incorrect Authorization</dd><dt>Affected</dt><dd>vaultwarden <b>1.37.3 and earlier</b></dd><dt>Fixed in</dt><dd><b>1.37.4</b></dd><dt>Disclosure</dt><dd><b>2026-09-17</b> Reported privately<br><span class="fs-gap">41 days later</span><b>2026-10-28</b> Published</dd><dt>Advisory</dt><dd><a href="https://github.com/dani-garcia/vaultwarden/security/advisories/GHSA-64mc-4p6f-r7x9">GHSA-64mc-4p6f-r7x9</a></dd></dl></section>

## About this writeup

Sanaan Fayaz Wani (GitHub [`sfwani`](https://github.com/sfwani)) reported this vulnerability to the `vaultwarden` maintainers under coordinated disclosure and is credited as a reporter in [GHSA-64mc-4p6f-r7x9](https://github.com/dani-garcia/vaultwarden/security/advisories/GHSA-64mc-4p6f-r7x9), published 2026-10-28.

All published findings: [advisory index](/advisories/).


  </div>
  <aside class="srail" aria-label="Fact sheet" data-sev="medium"><div class="sr-h"><span class="sr-num">4.3</span><span class="sr-sev">Medium</span></div><p class="sr-src">CVSS 3.1 base</p><dl class="fs"><dt>Weakness</dt><dd><b>CWE-863</b> Incorrect Authorization</dd><dt>Affected</dt><dd>vaultwarden <b>1.37.3 and earlier</b></dd><dt>Fixed in</dt><dd><b>1.37.4</b></dd><dt>Disclosure</dt><dd><b>2026-09-17</b> Reported privately<br><span class="fs-gap">41 days later</span><b>2026-10-28</b> Published</dd><dt>Advisory</dt><dd><a href="https://github.com/dani-garcia/vaultwarden/security/advisories/GHSA-64mc-4p6f-r7x9">GHSA-64mc-4p6f-r7x9</a></dd></dl><a class="sr-top" href="#top">Back to top</a></aside>
</section>
