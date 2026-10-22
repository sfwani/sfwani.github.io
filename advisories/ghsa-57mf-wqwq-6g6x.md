---
title: "GHSA-57mf-wqwq-6g6x"
heading: "GHSA-57mf-wqwq-6g6x"
role: "Hardcoded Default Fernet Encryption Key Exposes All Stored OAuth Credentials"
seo_title: "GHSA-57mf-wqwq-6g6x: Hardcoded Default Fernet Encryption Key Exposes All Stored OAuth Credentials - Sanaan Fayaz Wani"
ghsa_id: "GHSA-57mf-wqwq-6g6x"
cve_id: ""
published_at: "2026-10-05"
permalink: /advisories/ghsa-57mf-wqwq-6g6x/
layout: c2
description: "Hardcoded Default Fernet Encryption Key Exposes All Stored OAuth Credentials"
comments: false
last_modified_at: 2026-10-22T03:49:44+00:00
---
<section class="sec g" id="writeup" aria-labelledby="h-writeup">
  <div class="sec-head">
    <p class="idx idx--none">—</p>
    <h2 id="h-writeup">GHSA-57mf-wqwq-6g6x</h2>
    <p class="sec-sub">My analysis of this finding: root cause, the vulnerable code, the impact and the fix, in the site's format. The official advisory of record is linked in the table below.</p>
  </div>
  <div class="col-body prose" markdown="1">

| | |
|:--|:--|
| Advisory | [GHSA-57mf-wqwq-6g6x](https://github.com/Significant-Gravitas/AutoGPT/security/advisories/GHSA-57mf-wqwq-6g6x) |
| CVE | not assigned |
| Severity | High (8.2) |
| CVSS vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| CWE | CWE-321 (Use of Hard-coded Cryptographic Key), CWE-798 (Use of Hard-coded Credentials) |
| Published | 2026-10-05 |

### Affected versions

| Package | Ecosystem | Vulnerable | Fixed in |
|:--|:--|:--|:--|
| `autogpt-platform-backend` | other | >= 0.6.23, <= 0.7.4 | n/a |

## Summary

The AutoGPT platform shipped a hardcoded `ENCRYPTION_KEY` in `backend/.env.default`, committed to the public repository and loaded automatically by the default Docker Compose configuration. That one key does two jobs: it encrypts every stored user credential with Fernet, and it derives the HMAC key that signs pickle serialized cache entries in Redis. Because the key is public, both protections collapse for any deployment left on the default.

## Where it lives

Three places tie the public key to real impact.

Credential encryption, `backend/util/encryption.py`:

```python
ENCRYPTION_KEY = Settings().secrets.encryption_key  # from .env.default

class JSONCryptor:
    def __init__(self, key=None):
        self.key = key or ENCRYPTION_KEY
        self.fernet = Fernet(self.key.encode())
```

`backend/data/user.py` uses this to encrypt and decrypt `UserIntegrations`, which hold OAuth tokens, API keys and refresh tokens.

Cache HMAC signing, `backend/util/cache.py`:

```python
def _get_hmac_key() -> bytes:
    secret = settings.secrets.encryption_key
    if not secret:
        secret = "autogpt-cache-default-hmac-key"
    return hashlib.sha256(secret.encode()).digest()
```

The derived key HMAC signs pickle serialized cache entries before they are stored in Redis. Reads call `pickle.loads()` after verifying the HMAC.

Default loading, `docker-compose.platform.yml`:

```yaml
x-backend-env-files: &backend-env-files
  env_file:
    - backend/.env.default   # base defaults, always present
    - path: backend/.env     # user overrides, optional
      required: false
```

The default file is always loaded, so a deployment that never sets its own key runs on the published one.

## Impact

Two distinct chains, separated by what the attacker can reach.

**Credential decryption.** Anyone who can read the PostgreSQL store (a backup leak, SQL injection, misconfigured access, a compromised admin surface) can decrypt every stored credential with the public key: GitHub and Discord OAuth tokens, model provider API keys, and every other integration secret.

**Remote code execution.** Anyone who can write to Redis can forge an HMAC signed pickle payload with the derived key `sha256(ENCRYPTION_KEY)`. When the application next reads that poisoned entry, `pickle.loads()` runs attacker controlled code. The HMAC stops being a defense the moment its key is public.

A working proof of concept demonstrated all three steps end to end: encrypt and decrypt with the known key, forge a signature that passes the application's own verification, and deserialize the forged payload.

## Fix

Remove the shipped key and fail closed on it: refuse to start when `ENCRYPTION_KEY` is empty, matches a known published default, or is not a valid Fernet key, and document a rotation procedure. For the cache specifically, a safe serializer such as JSON or msgpack removes the deserialization sink entirely, so an HMAC bypass can no longer reach code execution.

## About this writeup

Sanaan Fayaz Wani (GitHub [`sfwani`](https://github.com/sfwani)) reported this vulnerability to the `autogpt-platform-backend` maintainers under coordinated disclosure and is credited as a reporter in [GHSA-57mf-wqwq-6g6x](https://github.com/Significant-Gravitas/AutoGPT/security/advisories/GHSA-57mf-wqwq-6g6x), published 2026-10-05.

All published findings: [advisory index](/advisories/).


  </div>
</section>
