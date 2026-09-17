---
title: Security Research
layout: page
description: Published security advisories against AI agent frameworks and LLM infrastructure, with root cause, reproduction, and fix for each.
---

Sanaan Fayaz Wani. Security Engineer at Amazon, working in IAM security on bringing agentic AI into identity and access management. Outside that, I hunt unauthenticated remote code execution in the infrastructure that runs large language models: agent frameworks, inference servers, workflow orchestrators, and the serialization formats they trust.

<!-- COUNTERS:START -->

**7 CVEs assigned.** 11 published advisories across 7 projects, from 167 reports filed against 59 open source projects.

<!-- COUNTERS:END -->

## Published advisories

<!-- ADVISORIES:START -->

| Advisory | Project | CVSS | Class |
|:---|:---|:---|:---|
| [CVE-2026-57516](https://github.com/advisories/GHSA-hhrp-gw25-jr43) | `ray` | 8.8 High | Code injection (CWE-94) |
| [CVE-2026-45675](https://github.com/advisories/GHSA-h3ww-q6xx-w7x3) | `open-webui` | 8.1 High | Privilege escalation (CWE-269) |
| [GHSA-jc26-22qp-cgqj](https://github.com/triggerdotdev/trigger.dev/security/advisories/GHSA-jc26-22qp-cgqj) | `trigger.dev` | 7.9 High | Missing authentication (CWE-306) |
| [GHSA-3c52-v5v2-3r56](https://github.com/Budibase/budibase/security/advisories/GHSA-3c52-v5v2-3r56) | `budibase` | 7.7 High | Server side request forgery (CWE-918) |
| [CVE-2026-59714](https://github.com/advisories/GHSA-x2ff-v5v8-m75m) | `open-webui` | 7.1 High | Missing authorization (CWE-862) |
| [GHSA-pqxw-g93w-hj9x](https://github.com/triggerdotdev/trigger.dev/security/advisories/GHSA-pqxw-g93w-hj9x) | `trigger.dev` | High | Improper isolation (CWE-653) |
| [CVE-2026-53577](https://github.com/kestra-io/kestra/security/advisories/GHSA-r6v3-xxwj-9h42) | `kestra` | 6.5 Medium | Incorrect authorization (CWE-863) |
| [CVE-2026-63342](https://github.com/hatchet-dev/hatchet/security/advisories/GHSA-g26x-m427-f48f) | `hatchet` | 6.3 Medium | Incorrect authorization (CWE-863) |
| [GHSA-59h8-w5q6-mfmp](https://github.com/triggerdotdev/trigger.dev/security/advisories/GHSA-59h8-w5q6-mfmp) | `trigger.dev` | 5.3 Medium | Missing authentication (CWE-306) |
| [CVE-2026-73301](https://github.com/advisories/GHSA-4qcj-m5wp-jmf4) | `@budibase/server` | 4.3 Medium | Missing authorization (CWE-862) |
| [CVE-2026-59715](https://github.com/advisories/GHSA-gmfw-g93r-vg53) | `open-webui` | 3.1 Low | Missing authentication (CWE-306) |

<!-- ADVISORIES:END -->

Full writeups, with the vulnerable code, reproduction steps, and the fix diff for each, are at [github.com/sfwani/advisories](https://github.com/sfwani/advisories). This table regenerates daily from the [GitHub Advisory Database](https://github.com/advisories?query=credit%3Asfwani), so it only ever lists work that is published, fixed, and credited.

## What I look for

**Unauthenticated reachability.** An auth gated code execution sink is a bug. The same sink reachable before auth is a critical. Most of my highest severity findings are reachability failures rather than novel sinks: missing authentication and missing authorization in front of machinery that was never meant to be public.

**Sandboxes that are not sandboxes.** Agent frameworks ship "safe" Python evaluators built on AST allowlists. Format string dunder traversal, decorator abuse, and incomplete node denylists walk straight out of most of them.

**Deserialization on exposed ports.** `pickle`, `cloudpickle`, `joblib`, and `torch.load(weights_only=False)` sitting behind an inference or actor pool port that quietly binds `0.0.0.0`.

**Request forgery into control planes.** My highest volume class: metadata endpoints, internal schedulers, and cluster APIs one redirect away from a user supplied URL.

## Competitions

| Placement | Event |
|:---|:---|
| **1st** | AI Village CTF, DEF CON 34 |
| **2nd** | Adversary Wars CTF, Adversary Village, DEF CON 34 |
| **1st** | Adversary Wars CTF, Adversary Village, DEF CON 33 |
| **1st** | SHPE National CTF |
| **1st** | Hackabull CTF |
| **1st** | Central Florida Tech Grove CTF |
| **1st** | Social Engineering Competition, The CARE Lab at Temple University |
| **3rd** | SecureTheFuture Research Award, Palo Alto Networks |
| **3rd** | NCAE CyberGames, South East Regionals |

## Elsewhere

[GitHub](https://github.com/sfwani) &nbsp;·&nbsp; [LinkedIn](https://www.linkedin.com/in/sfwani) &nbsp;·&nbsp; [Advisories](https://github.com/sfwani/advisories) &nbsp;·&nbsp; [code.sanaan@gmail.com](mailto:code.sanaan@gmail.com)
