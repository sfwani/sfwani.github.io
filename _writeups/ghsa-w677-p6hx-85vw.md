## Summary

Teable lets you protect a shared view or a shared base with an optional password. I found that the share-auth JWT is never bound to the share it is presented for. The password is verified against the `shareId` carried *inside* the token payload, while the data served comes from the `shareId` in the request URL. Those are allowed to be two different shares. Any authenticated user can mint a legitimate token for a password-protected share they own, relabel it under a victim share's cookie name, and read the victim's protected content without ever knowing the victim's password. Both the view-share and the base-share paths carry the flaw. This is an authorization bypass through a user-controlled key (CWE-639).

## Where it lives

The Passport strategy at `apps/nestjs-backend/src/features/share/strategies/jwt.strategy.ts`:

<!-- bug: return cookieObj?.[shareId] ?? null; :: the requested share only picks which cookie is read -->
<!-- bug: const { shareId, password } = payload; :: the token payload picks which share gets authenticated -->
<!-- bug: return authShareId; :: no check that the token's share matches the request -->
```ts
public static fromAuthCookieAsToken(req: Request): string | null {
  const shareId = req.params.shareId || (req.headers['tea-share-id'] as string);
  const cookieObj = cookie.parse(req.headers.cookie ?? '');
  return cookieObj?.[shareId] ?? null;              // requested share picks the COOKIE NAME
}

async validate(req, payload: IJwtShareInfo) {
  const { shareId, password } = payload;            // the PAYLOAD picks what gets authenticated
  const authShareId = await this.shareAuthService.authShareView(shareId, password, req.useV2 === true);
  if (!authShareId) throw new UnauthorizedException();
  return authShareId;                               // no payload.shareId === req.params.shareId check
}
```

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

<!-- fix: if (payload.shareId !== requestedShareId) :: rejects tokens minted for a different share -->
```ts
const requestedShareId = req.params.shareId || req.headers['tea-share-id'];
if (payload.shareId !== requestedShareId) throw new UnauthorizedException();
```

The base-share strategy needs `passReqToCallback: true` first so it can see the request at all.
