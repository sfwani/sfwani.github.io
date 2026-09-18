---
title: Sanaan Fayaz Wani
seo_title: "Sanaan Fayaz Wani - AI Security Researcher"
layout: page
description: Vulnerability research on AI agent frameworks and LLM infrastructure. Seven assigned CVEs and eleven published advisories, with root cause, reproduction and fix for each.
last_modified_at: 2026-09-18T04:13:38+00:00
---

Sanaan Fayaz Wani is a Security Engineer at Amazon, working in IAM security on bringing agentic AI into identity and access management. Outside that, he hunts unauthenticated remote code execution in the infrastructure that runs large language models: agent frameworks, inference servers, workflow orchestrators, and the serialization formats they trust.

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

## Where the bugs are

<!-- CHART:START -->

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 302" class="fig-cwe" role="img" aria-labelledby="cweT cweD" preserveAspectRatio="xMidYMid meet">
<title id="cweT">Weakness classes across the published advisories</title>
<desc id="cweD">7 of 11 published advisories are authentication or authorization failures; 4 are other classes.</desc>
<style>.fig-cwe{font-family:inherit;font-feature-settings:"tnum" 1}.fig-cwe text{fill:currentColor}.cw-eyebrow{font-size:10.5px;fill-opacity:.55;letter-spacing:.1em}.cw-meta{font-size:11px;fill-opacity:.55}.cw-label{font-size:12px}.cw-muted{fill-opacity:.62}.cw-count{font-size:11px;fill-opacity:.6}.cw-lead{font-size:15px}.cw-note{font-size:11px;fill-opacity:.62}</style>
<text class="cw-eyebrow" x="0" y="11">WEAKNESS CLASS</text>
<text class="cw-meta" x="640" y="11" text-anchor="end">11 published advisories</text>
<line x1="0" y1="23.5" x2="640" y2="23.5" stroke="currentColor" stroke-opacity=".28" stroke-width="1"/>
<g fill="currentColor">
<text class="cw-label" x="0" y="46">CWE-306 Missing authentication</text>
<rect x="0" y="55" width="300.0" height="10" fill-opacity=".88"/>
<text class="cw-count" x="308.0" y="63.5">3</text>
<text class="cw-label" x="0" y="80">CWE-862 Missing authorization</text>
<rect x="0" y="89" width="200.0" height="10" fill-opacity=".88"/>
<text class="cw-count" x="208.0" y="97.5">2</text>
<text class="cw-label" x="0" y="114">CWE-863 Incorrect authorization</text>
<rect x="0" y="123" width="200.0" height="10" fill-opacity=".88"/>
<text class="cw-count" x="208.0" y="131.5">2</text>
<text class="cw-label cw-muted" x="0" y="148">CWE-269 Privilege escalation</text>
<rect x="0" y="157" width="100.0" height="10" fill-opacity=".3"/>
<text class="cw-count" x="108.0" y="165.5">1</text>
<text class="cw-label cw-muted" x="0" y="182">CWE-653 Improper isolation</text>
<rect x="0" y="191" width="100.0" height="10" fill-opacity=".3"/>
<text class="cw-count" x="108.0" y="199.5">1</text>
<text class="cw-label cw-muted" x="0" y="216">CWE-918 Server side request forgery</text>
<rect x="0" y="225" width="100.0" height="10" fill-opacity=".3"/>
<text class="cw-count" x="108.0" y="233.5">1</text>
<text class="cw-label cw-muted" x="0" y="250">CWE-94 Code injection</text>
<rect x="0" y="259" width="100.0" height="10" fill-opacity=".3"/>
<text class="cw-count" x="108.0" y="267.5">1</text>
</g>
<path d="M424 55 L430 55 L430 133 L424 133" fill="none" stroke="currentColor" stroke-opacity=".5" stroke-width="1"/>
<text class="cw-lead" x="442" y="91.0">7 of 11</text>
<text class="cw-note" x="442" y="106.0">authentication or</text>
<text class="cw-note" x="442" y="119.0">authorization failures</text>
<path d="M424 157 L430 157 L430 269 L424 269" fill="none" stroke="currentColor" stroke-opacity=".35" stroke-width="1"/>
<text class="cw-lead" x="442" y="210.0">4 of 11</text>
<text class="cw-note" x="442" y="225.0">everything else</text>
</svg>

<!-- CHART:END -->

## Current interests

Agentic systems and autonomous loops, and what happens to authorization when an agent acts on a user's behalf across many services. Where the tool invocation boundary quietly becomes an execution boundary. More on the [roles, degree and competition record](/experience/), and on the [research approach](/about/).

## Elsewhere

[GitHub](https://github.com/sfwani) &nbsp;·&nbsp; [LinkedIn](https://www.linkedin.com/in/sfwani) &nbsp;·&nbsp; [Advisories](https://github.com/sfwani/advisories) &nbsp;·&nbsp; [code.sanaan@gmail.com](mailto:code.sanaan@gmail.com)
