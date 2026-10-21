---
title: "GHSA-v3vj-mch3-x6c2"
heading: "GHSA-v3vj-mch3-x6c2"
role: "Sandbox launcher isolation failure permits host-level code execution"
seo_title: "GHSA-v3vj-mch3-x6c2: Sandbox launcher isolation failure permits host-level code execution - Sanaan Fayaz Wani"
ghsa_id: "GHSA-v3vj-mch3-x6c2"
cve_id: ""
published_at: "2026-10-13"
permalink: /advisories/ghsa-v3vj-mch3-x6c2/
layout: c2
description: "Sandbox launcher isolation failure permits host-level code execution"
comments: false
last_modified_at: 2026-10-21T04:14:07+00:00
---
<section class="sec g" id="writeup" aria-labelledby="h-writeup">
  <div class="sec-head">
    <p class="idx idx--none">—</p>
    <h2 id="h-writeup">GHSA-v3vj-mch3-x6c2</h2>
    <p class="sec-sub">Published, fixed and credited. Root cause, the vulnerable code, reproduction and the fix, as published in the advisory itself.</p>
  </div>
  <div class="col-body prose" markdown="1">

| | |
|:--|:--|
| Advisory | [GHSA-v3vj-mch3-x6c2](https://github.com/omnigent-ai/omnigent/security/advisories/GHSA-v3vj-mch3-x6c2) |
| CVE | not assigned |
| Severity | High (8.8) |
| CVSS vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| CWE | CWE-668 (Exposure of Resource to Wrong Sphere), CWE-732 (Incorrect Permission Assignment for Critical Resource) |
| Published | 2026-10-13 |

### Affected versions

| Package | Ecosystem | Vulnerable | Fixed in |
|:--|:--|:--|:--|
| `omnigent` | pip | < 0.18.0 | n/a |

## Impact

On affected Linux deployments using the bubblewrap sandbox, helper executors granted access to host temporary files that needed to remain outside the sandbox. Code already running inside the sandbox could compromise the launcher and execute with the privileges of the operating-system account running Omnigent.

This can expose or modify data accessible to that account and disrupt its processes. Exploitation requires code execution inside an affected sandbox; it does not require administrator privileges. Timing requirements differ between executors.

## Patched version

Upgrade Omnigent to **0.18.0 or later** on agent hosts and restart affected helper processes. The fix removes broad temporary-directory write grants and rejects sandbox configurations that expose the launcher's directory.

## Workaround

Until upgraded, run untrusted agents in a separate disposable VM or container without sensitive host credentials or host filesystem mounts.

## References

- [Fix](https://github.com/omnigent-ai/omnigent/pull/9844)
- [Omnigent 0.18.0](https://github.com/omnigent-ai/omnigent/releases/tag/v0.18.0)

## About this writeup

Sanaan Fayaz Wani (GitHub [`sfwani`](https://github.com/sfwani)) reported this vulnerability to the `omnigent` maintainers under coordinated disclosure and is credited as a reporter in [GHSA-v3vj-mch3-x6c2](https://github.com/omnigent-ai/omnigent/security/advisories/GHSA-v3vj-mch3-x6c2), published 2026-10-13.

All published findings: [advisory index](/advisories/).


  </div>
</section>
