---
title: Sanaan Fayaz Wani
seo_title: "Sanaan Fayaz Wani - AI Security Researcher"
layout: page
description: Vulnerability research on AI agent frameworks and LLM infrastructure. Seven assigned CVEs and eleven published advisories, with root cause, reproduction and fix for each.
last_modified_at: 2026-09-17T23:54:04+00:00
---

Security Engineer at Amazon, working in IAM security on bringing agentic AI into identity and access management. Outside that, I hunt unauthenticated remote code execution in the infrastructure that runs large language models: agent frameworks, inference servers, workflow orchestrators, and the serialization formats they trust.

<!-- COUNTERS:START -->

**7 CVEs assigned.** 11 published advisories across 7 projects, from 167 reports filed against 59 open source projects.

<!-- COUNTERS:END -->

## Published advisories

<!-- ADVISORIES:START -->

| Advisory | Project | CVSS | Class |
|:---|:---|:---|:---|
| [CVE-2026-57516](/advisories/cve-2026-57516/) | `ray` | 8.8 High | Code injection (CWE-94) |
| [CVE-2026-45675](/advisories/cve-2026-45675/) | `open-webui` | 8.1 High | Privilege escalation (CWE-269) |
| [GHSA-jc26-22qp-cgqj](/advisories/ghsa-jc26-22qp-cgqj/) | `trigger.dev` | 7.9 High | Missing authentication (CWE-306) |
| [GHSA-3c52-v5v2-3r56](/advisories/ghsa-3c52-v5v2-3r56/) | `budibase` | 7.7 High | Server side request forgery (CWE-918) |
| [CVE-2026-59714](/advisories/cve-2026-59714/) | `open-webui` | 7.1 High | Missing authorization (CWE-862) |
| [GHSA-pqxw-g93w-hj9x](/advisories/ghsa-pqxw-g93w-hj9x/) | `trigger.dev` | High | Improper isolation (CWE-653) |
| [CVE-2026-53577](/advisories/cve-2026-53577/) | `kestra` | 6.5 Medium | Incorrect authorization (CWE-863) |
| [CVE-2026-63342](/advisories/cve-2026-63342/) | `hatchet` | 6.3 Medium | Incorrect authorization (CWE-863) |
| [GHSA-59h8-w5q6-mfmp](/advisories/ghsa-59h8-w5q6-mfmp/) | `trigger.dev` | 5.3 Medium | Missing authentication (CWE-306) |
| [CVE-2026-73301](/advisories/cve-2026-73301/) | `@budibase/server` | 4.3 Medium | Missing authorization (CWE-862) |
| [CVE-2026-59715](/advisories/cve-2026-59715/) | `open-webui` | 3.1 Low | Missing authentication (CWE-306) |

<!-- ADVISORIES:END -->

Each advisory above links to a full writeup with the vulnerable code, reproduction steps and the fix. The complete index is at [/advisories/](/advisories/). This table regenerates daily from the [GitHub Advisory Database](https://github.com/advisories?query=credit%3Asfwani), so it only ever lists work that is published, fixed, and credited.

## What I look for

**Unauthenticated reachability.** An auth gated code execution sink is a bug. The same sink reachable before auth is a critical. Most of my highest severity findings are reachability failures rather than novel sinks: missing authentication and missing authorization in front of machinery that was never meant to be public.

**Sandboxes that are not sandboxes.** Agent frameworks ship "safe" Python evaluators built on AST allowlists. Format string dunder traversal, decorator abuse, and incomplete node denylists walk straight out of most of them.

**Deserialization on exposed ports.** `pickle`, `cloudpickle`, `joblib`, and `torch.load(weights_only=False)` sitting behind an inference or actor pool port that quietly binds `0.0.0.0`.

**Request forgery into control planes.** My highest volume class: metadata endpoints, internal schedulers, and cluster APIs one redirect away from a user supplied URL.

## Current interests

Agentic systems and autonomous loops, and what happens to authorization when an agent acts on a user's behalf across many services. Where the tool invocation boundary quietly becomes an execution boundary. More, including competition placements and background, on the [about page](/about/).

## Elsewhere

[GitHub](https://github.com/sfwani) &nbsp;·&nbsp; [LinkedIn](https://www.linkedin.com/in/sfwani) &nbsp;·&nbsp; [Advisories](https://github.com/sfwani/advisories) &nbsp;·&nbsp; [code.sanaan@gmail.com](mailto:code.sanaan@gmail.com)
