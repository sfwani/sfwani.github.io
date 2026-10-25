---
title: "GHSA-w677-p6hx-85vw"
heading: "GHSA-w677-p6hx-85vw"
role: "Share password bypass: the share access token is never bound to the share it is presented for, so a token minted for one share opens any other password-protected share (plus cleartext password disclosure)"
seo_title: "GHSA-w677-p6hx-85vw: Share password bypass: the share access token is never bound to the share it is… - Sanaan Fayaz Wani"
ghsa_id: "GHSA-w677-p6hx-85vw"
cve_id: ""
published_at: "2026-10-13"
permalink: /advisories/ghsa-w677-p6hx-85vw/
layout: c2
description: "Share password bypass: the share access token is never bound to the share it is presented for, so a token minted for one share opens any other password-protected share (plus cleartext password disclosure). teable, CVSS 7.1 High, CWE-287 Authentication bypass. Writeup by Sanaan Fayaz Wani, the credited reporter."
image: /assets/img/og/ghsa-w677-p6hx-85vw.png
kicker_repo: "teableio/teable"
comments: false
last_modified_at: 2026-10-24T23:51:00+00:00
---
<section class="sec g" id="writeup" aria-labelledby="h-writeup" data-sev="high" data-score="7.1" data-sevword="High" data-short="Upgrade to release.2026-10-12T12-45-53Z.3331">
  <h2 id="h-writeup" class="vh">GHSA-w677-p6hx-85vw</h2>
  <div class="ah" data-sev="high"><div class="ah-score"><p class="ah-num">7.1</p><p class="ah-sev">High</p><p class="ah-of">CVSS 3.1 base</p><div class="ah-meter" aria-hidden="true"><i style="width:71%"></i></div><ol class="tlv" aria-label="Disclosure timeline"><li><b>2026-09-05</b><span>Reported privately</span></li><li><span class="tlv-d">38 days later</span><b>2026-10-13</b><span>Published by the maintainer</span></li></ol></div><div class="act"><p class="act-k">What to do</p><p class="act-v">If you run <b>teable</b> <b>before release.2026-10-12T12-45-53Z.3331</b>, upgrade to <b>release.2026-10-12T12-45-53Z.3331</b> or later.</p></div><p class="ts"><em>Anyone who can reach it over the network</em>, with <em>a low-privilege account</em> and no user interaction, can <em>read sensitive data and change some data</em>.<span class="ts-src">Read from the CVSS 3.1 vector</span></p><div class="bx" style="--n:4"><div class="bx-head"><span class="k-lab">CVSS 3.1 metrics</span></div><div class="bx-row"><p class="bx-g">To exploit it</p><dl class="bx-grid"><div class="bx-c"><dt>Attack vector</dt><dd>Network</dd></div><div class="bx-c"><dt>Attack complexity</dt><dd>Low</dd></div><div class="bx-c"><dt>Privileges required</dt><dd>Low</dd></div><div class="bx-c"><dt>User interaction</dt><dd>None</dd></div></dl></div><div class="bx-row"><p class="bx-g">What it gets</p><dl class="bx-grid"><div class="bx-c"><dt>Confidentiality</dt><dd>High</dd></div><div class="bx-c"><dt>Integrity</dt><dd>Low</dd></div><div class="bx-c"><dt>Availability</dt><dd>None</dd></div><div class="bx-c"><dt>Scope</dt><dd>Unchanged</dd></div></dl></div><p class="bx-foot"><a href="https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N" rel="noopener">Open this vector in the FIRST calculator &#8599;</a></p></div><dl class="meta"><div class="meta-i wide"><dt class="k-lab">Weakness</dt><dd class="meta-v"><abbr title="Improper Authentication">CWE-287</abbr>, <abbr title="Insufficiently Protected Credentials">CWE-522</abbr>, <abbr title="Incorrect Authorization">CWE-863</abbr> <span class="meta-s">Improper Authentication · Insufficiently Protected Credentials · Incorrect Authorization</span></dd></div><div class="meta-i"><dt class="k-lab">Advisory</dt><dd class="meta-v"><a href="https://github.com/teableio/teable/security/advisories/GHSA-w677-p6hx-85vw">GHSA-w677-p6hx-85vw</a></dd></div><div class="meta-i"><dt class="k-lab">CVE</dt><dd class="meta-v">not assigned</dd></div><div class="meta-i"><dt class="k-lab">Vector</dt><dd class="meta-v"><span class="vec">CVSS:3.1/<wbr>AV:N/<wbr>AC:L/<wbr>PR:L/<wbr>UI:N/<wbr>S:U/<wbr>C:H/<wbr>I:L/<wbr>A:N</span></dd></div><div class="meta-i wide"><dt class="k-lab">Also in teable</dt><dd class="meta-v"><a href="/advisories/ghsa-jvm6-86c5-f8j8/">GHSA-jvm6-86c5-f8j8</a> 6.5</dd></div></dl><div class="tl" role="group" aria-label="Disclosure timeline"><div class="tl-n"><b>2026-09-05</b><span>Reported privately</span></div><div class="tl-seg"><span>38 days</span></div><div class="tl-n"><b>2026-10-13</b><span>Published by the maintainer</span></div></div><p class="ah-note">My analysis of this finding: root cause, the vulnerable code, the impact and the fix, in the site’s format. The official advisory of record is linked above.</p></div>
  <div class="col-body prose" markdown="1">

### Affected versions

<div class="vts"><div class="vt" aria-hidden="true"><div class="vt-pkg">teableio/teable</div><div class="vt-bar nolo"><div class="vt-bad"><b>No lower bound</b><i>Affected</i><b>before release.2026-10-12T12-45-53Z.3331</b></div><div class="vt-fix">Fixed in <b>release.2026-10-12T12-45-53Z.3331</b></div></div></div></div>

| Package | Ecosystem | Vulnerable | Fixed in |
|:--|:--|:--|:--|
| `teableio/teable` | other | < release.2026-10-12T12-45-53Z.3331 | release.2026-10-12T12-45-53Z.3331 |
{: .vh}

## Summary

Teable lets you protect a shared view or a shared base with an optional password. I found that the share-auth JWT is never bound to the share it is presented for. The password is verified against the `shareId` carried *inside* the token payload, while the data served comes from the `shareId` in the request URL. Those are allowed to be two different shares. Any authenticated user can mint a legitimate token for a password-protected share they own, relabel it under a victim share's cookie name, and read the victim's protected content without ever knowing the victim's password. Both the view-share and the base-share paths carry the flaw. This is an authorization bypass through a user-controlled key (CWE-639).

## Where it lives

The Passport strategy at `apps/nestjs-backend/src/features/share/strategies/jwt.strategy.ts`:

<pre class="has-mark"><code class="language-ts"><span class="ln">public static fromAuthCookieAsToken(req: Request): string | null {</span><span class="ln">  const shareId = req.params.shareId || (req.headers[&#x27;tea-share-id&#x27;] as string);</span><span class="ln">  const cookieObj = cookie.parse(req.headers.cookie ?? &#x27;&#x27;);</span><span class="ln bug">  return cookieObj?.[shareId] ?? null;              // requested share picks the COOKIE NAME</span><span class="ln">}</span><span class="ln"> </span><span class="ln">async validate(req, payload: IJwtShareInfo) {</span><span class="ln bug">  const { shareId, password } = payload;            // the PAYLOAD picks what gets authenticated</span><span class="ln">  const authShareId = await this.shareAuthService.authShareView(shareId, password, req.useV2 === true);</span><span class="ln">  if (!authShareId) throw new UnauthorizedException();</span><span class="ln bug">  return authShareId;                               // no payload.shareId === req.params.shareId check</span><span class="ln">}</span></code></pre>

<p class="mark-cap"><span><span class="mark-k">The bug</span>the requested share only picks which cookie is read</span><span><span class="mark-k">The bug</span>the token payload picks which share gets authenticated</span><span><span class="mark-k">The bug</span>no check that the token&#x27;s share matches the request</span></p>

`authShareView` validates the password of the share named in the payload. By the time `validate` runs, the guard has already resolved `req.shareInfo` to the *requested* (victim) share, and every handler serves from `req.shareInfo`. So the credential checked and the data returned come from two different shares.

The base-share leg is identical in `apps/nestjs-backend/src/features/base-share/strategies/jwt.strategy.ts`, calling `authBaseShare(shareId, password)` with the same missing bind.

It is an oversight, not a design choice: the sibling header-token validators bind correctly. Both `validateBaseSharePasswordToken` (`permission.service.ts:590`) and `validateShareViewPasswordToken` (`:1054`) do exactly the check the two strategies omit:

```ts
if (payload.shareId !== shareId) { return false; }
```

## Impact

I verified this end to end against `ghcr.io/teableio/teable:latest` with a base on the current default `v2Enabled=true`. A non-admin attacker minted a token for their own password share `shrau2hPeaD7RoEL23A`, then hit a victim share whose password `VictimSecretPASS123` they never learned:

```
Control  GET /api/share/shrbkg5yCzDfPtNHjB1/view/records            -> 401 (no token)
Exploit  GET /api/share/shrbkg5yCzDfPtNHjB1/view/records
         Cookie: shrbkg5yCzDfPtNHjB1=<attacker token for shrau2...> -> 200
         {"records":[{"id":"rec89zy140BEKDH2F6h",
           "fields":{"fldvuv2MTJ6gqELp2Kq":"TOP-SECRET-SALARY-999999"},...}]}
```

The share password is the only control protecting a link whose URL has leaked or been forwarded. Any authenticated holder of a victim share link reads the full protected view, and against a base share can export and copy the entire password-protected base.

## Fix

In both `validate` methods, reject when the token's shareId does not match the requested shareId, mirroring the header validators:

<pre class="has-mark"><code class="language-ts"><span class="ln">const requestedShareId = req.params.shareId || req.headers[&#x27;tea-share-id&#x27;];</span><span class="ln fix">if (payload.shareId !== requestedShareId) throw new UnauthorizedException();</span></code></pre>

<p class="mark-cap"><span><span class="mark-k fix">The fix</span>rejects tokens minted for a different share</span></p>

The base-share strategy needs `passReqToCallback: true` first so it can see the request at all.

<section class="fs-inline" aria-labelledby="h-record"><h2 id="h-record" class="no-idx">The record</h2><dl class="fs"><dt>Weakness</dt><dd><b>CWE-287</b> Improper Authentication<br><b>CWE-522</b> Insufficiently Protected Credentials<br><b>CWE-863</b> Incorrect Authorization</dd><dt>Affected</dt><dd>teable <b>before release.2026-10-12T12-45-53Z.3331</b></dd><dt>Fixed in</dt><dd><b>release.2026-10-12T12-45-53Z.3331</b></dd><dt>Disclosure</dt><dd><b>2026-09-05</b> Reported privately<br><span class="fs-gap">38 days later</span><b>2026-10-13</b> Published</dd><dt>Advisory</dt><dd><a href="https://github.com/teableio/teable/security/advisories/GHSA-w677-p6hx-85vw">GHSA-w677-p6hx-85vw</a></dd><dt>Also in teable</dt><dd><a href="/advisories/ghsa-jvm6-86c5-f8j8/">GHSA-jvm6-86c5-f8j8</a> 6.5</dd></dl></section>

## About this writeup

Sanaan Fayaz Wani (GitHub [`sfwani`](https://github.com/sfwani)) reported this vulnerability to the `teable` maintainers under coordinated disclosure and is credited as a reporter in [GHSA-w677-p6hx-85vw](https://github.com/teableio/teable/security/advisories/GHSA-w677-p6hx-85vw), published 2026-10-13.

All published findings: [advisory index](/advisories/).


  </div>
  <aside class="srail" aria-label="Fact sheet" data-sev="high"><div class="sr-h"><span class="sr-num">7.1</span><span class="sr-sev">High</span></div><p class="sr-src">CVSS 3.1 base</p><dl class="fs"><dt>Weakness</dt><dd><b>CWE-287</b> Improper Authentication<br><b>CWE-522</b> Insufficiently Protected Credentials<br><b>CWE-863</b> Incorrect Authorization</dd><dt>Affected</dt><dd>teable <b>before release.2026-10-12T12-45-53Z.3331</b></dd><dt>Fixed in</dt><dd><b>release.2026-10-12T12-45-53Z.3331</b></dd><dt>Disclosure</dt><dd><b>2026-09-05</b> Reported privately<br><span class="fs-gap">38 days later</span><b>2026-10-13</b> Published</dd><dt>Advisory</dt><dd><a href="https://github.com/teableio/teable/security/advisories/GHSA-w677-p6hx-85vw">GHSA-w677-p6hx-85vw</a></dd><dt>Also in teable</dt><dd><a href="/advisories/ghsa-jvm6-86c5-f8j8/">GHSA-jvm6-86c5-f8j8</a> 6.5</dd></dl><a class="sr-top" href="#top">Back to top</a></aside>
</section>
