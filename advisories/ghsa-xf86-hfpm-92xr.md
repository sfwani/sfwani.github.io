---
title: "GHSA-xf86-hfpm-92xr"
heading: "GHSA-xf86-hfpm-92xr"
role: "AI Chat route exposes admin-only tools to non-admin users"
seo_title: "GHSA-xf86-hfpm-92xr: AI Chat route exposes admin-only tools to non-admin users - Sanaan Fayaz Wani"
ghsa_id: "GHSA-xf86-hfpm-92xr"
cve_id: ""
published_at: "2026-10-19"
permalink: /advisories/ghsa-xf86-hfpm-92xr/
layout: c2
description: "AI Chat route exposes admin-only tools to non-admin users"
comments: false
last_modified_at: 2026-10-21T04:14:07+00:00
---
<section class="sec g" id="writeup" aria-labelledby="h-writeup">
  <div class="sec-head">
    <p class="idx idx--none">—</p>
    <h2 id="h-writeup">GHSA-xf86-hfpm-92xr</h2>
    <p class="sec-sub">Published, fixed and credited. Root cause, the vulnerable code, reproduction and the fix, as published in the advisory itself.</p>
  </div>
  <div class="col-body prose" markdown="1">

| | |
|:--|:--|
| Advisory | [GHSA-xf86-hfpm-92xr](https://github.com/directus/directus/security/advisories/GHSA-xf86-hfpm-92xr) |
| CVE | not assigned |
| Severity | Low (3.1) |
| CVSS vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:L/I:N/A:N` |
| CWE | CWE-863 (Incorrect Authorization) |
| Published | 2026-10-19 |

### Affected versions

| Package | Ecosystem | Vulnerable | Fixed in |
|:--|:--|:--|:--|
| `directus` | npm | >= 11.14.0, < 12.3.0 | n/a |

### Summary

The AI Chat endpoint (`POST /ai/chat`) did not enforce the admin-only restriction on AI tools. Any authenticated user with app access could request the `collections`, `fields`, `relations`, `flows` and `operations` tools, which are reserved for administrators. The MCP endpoint enforced this restriction correctly.

### Impact

The tools ran with the requesting user's own accountability, so they did not grant permissions beyond what the user already had:

- `collections`, `fields` and `relations` are still guarded by the admin checks in their underlying services.
- `flows` and `operations` are subject to the regular permission system. A non-admin user could only read or modify flows and operations their policies already allow, the same as through the REST API.

The issue is that the admin-only tool boundary was not applied consistently. Instances where non-admin policies grant access to `directus_flows` or `directus_operations` are most affected. We recommend keeping those collections admin-only, as described in the [security best practices](https://directus.io/docs/configuration/security-best-practices).

Exploitation requires an AI provider to be configured on the instance.

### Workarounds

- Disable the AI Chat feature by removing the configured AI provider.
- Make sure non-admin policies have no permissions on `directus_flows` and `directus_operations`.

## About this writeup

Sanaan Fayaz Wani (GitHub [`sfwani`](https://github.com/sfwani)) reported this vulnerability to the `directus` maintainers under coordinated disclosure and is credited as a reporter in [GHSA-xf86-hfpm-92xr](https://github.com/directus/directus/security/advisories/GHSA-xf86-hfpm-92xr), published 2026-10-19.

All published findings: [advisory index](/advisories/).


  </div>
</section>
