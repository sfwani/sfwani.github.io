---
title: "GHSA-59h8-w5q6-mfmp"
heading: "GHSA-59h8-w5q6-mfmp: Unauthenticated Realtime Stream Data Injection via Run FriendlyId"
seo_title: "GHSA-59h8-w5q6-mfmp: Unauthenticated Realtime Stream Data Injection via Run FriendlyId - Sanaan Fayaz Wani"
ghsa_id: "GHSA-59h8-w5q6-mfmp"
cve_id: ""
published_at: "2026-07-21"
permalink: /advisories/ghsa-59h8-w5q6-mfmp/
layout: page
description: "Unauthenticated Realtime Stream Data Injection via Run FriendlyId"
comments: false
last_modified_at: 2026-09-18T05:11:47+00:00
---
| | |
|:--|:--|
| Advisory | [GHSA-59h8-w5q6-mfmp](https://github.com/triggerdotdev/trigger.dev/security/advisories/GHSA-59h8-w5q6-mfmp) |
| CVE | not assigned |
| Severity | Medium (5.3) |
| CVSS vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:N` |
| CWE | CWE-306 (Missing Authentication for Critical Function) |
| Published | 2026-07-21 |

### Affected versions

| Package | Ecosystem | Vulnerable | Fixed in |
|:--|:--|:--|:--|
| `trigger.dev` | npm | <= 4.5.4 | n/a |

## Summary

The POST handler for `/realtime/v1/streams/:runId/:streamId` has no authentication. Any entity that knows or guesses a run friendlyId can inject arbitrary data into its realtime stream.

## Vulnerability Details

**File:** `apps/webapp/app/routes/realtime.v1.streams.$runId.$streamId.ts`

The `action` handler (line 17) has no auth wrapper. The code comment says: "Plain action for backwards compatibility with older clients that don't send auth headers."

The run lookup at line 29 uses `where: { friendlyId: runId }` with NO environment scoping (`runtimeEnvironmentId` is not checked), so production runs are accessible.

Run friendlyIds follow predictable patterns (e.g., `run_1234abcd`).

## Steps to Reproduce

```bash
# No authentication required
curl -X POST "http://localhost:8030/realtime/v1/streams/run_KNOWN_ID/stream_1"   -H "Content-Type: application/json"   -d '{"injected": "data"}'
```

## Impact

Unauthenticated data injection into any run realtime stream. Cross-environment access (no scoping).

## About this writeup

Sanaan Fayaz Wani (GitHub [`sfwani`](https://github.com/sfwani)) reported this vulnerability to the `trigger.dev` maintainers under coordinated disclosure and is credited as a reporter in [GHSA-59h8-w5q6-mfmp](https://github.com/triggerdotdev/trigger.dev/security/advisories/GHSA-59h8-w5q6-mfmp), published 2026-07-21.

All published findings: [advisory index](/advisories/). About the researcher: [about](/about/) and [experience](/experience/).
