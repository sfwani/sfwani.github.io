---
title: Sanaan Fayaz Wani
seo_title: "Sanaan Fayaz Wani - AI Security Researcher"
layout: page
description: Vulnerability research on AI agent frameworks and LLM infrastructure. Seven assigned CVEs and eleven published advisories, with root cause, reproduction and fix for each.
last_modified_at: 2026-09-19T20:14:11+00:00
---

Sanaan Fayaz Wani is a Security Engineer at Amazon, working in IAM security on bringing agentic AI into identity and access management. Outside that, he hunts unauthenticated remote code execution in the infrastructure that runs large language models: agent frameworks, inference servers, workflow orchestrators, and the serialization formats they trust.

Before Amazon he was a security researcher at Cyber Florida, building agentic systems for open
source vulnerability research and working on industrial control system security. The summer before
that he was on Amazon's red team, building an autonomous system for red teaming and tooling against
Model Context Protocol servers while the protocol was still new. He graduated magna cum laude in
computer science from the University of South Florida in May 2026, where he competed with the
CyberHerd team.

The work below is coordinated disclosure. Every finding is reported privately to the maintainer
first, and nothing is named, listed or hinted at on this site until a fix ships. What that leaves
is a record anyone can check: each entry resolves to an advisory the maintainer published and
credited.

<!-- COUNTERS:START -->

**7 CVEs assigned.** 11 published advisories across 7 projects, from 167 reports filed against 59 open source projects.

<!-- COUNTERS:END -->

## Selected findings

<!-- ADVISORIES:START -->

<div class="sel" markdown="0"><ol class="sel-list"><li class="sel-item"><p class="sel-head"><a href="/advisories/ghsa-pqxw-g93w-hj9x/">GHSA-pqxw-g93w-hj9x</a><span class="sel-proj"><code>trigger.dev</code></span><span class="sel-score">9.0<abbr title="Scored by me, not by the coordinating database">&dagger;</abbr></span></p><p class="sel-sum">Self-Hosted Deployment: Default Secrets allow Unauthenticated Infrastructure Compromise</p></li><li class="sel-item"><p class="sel-head"><a href="/advisories/cve-2026-57516/">CVE-2026-57516</a><span class="sel-proj"><code>ray</code></span><span class="sel-score">8.8</span></p><p class="sel-sum">Ray: Arbitrary code execution via ray.data.read_webdataset default decoder: pickle.loads(value) and torch.load(weights_only=False)</p></li><li class="sel-item"><p class="sel-head"><a href="/advisories/cve-2026-45675/">CVE-2026-45675</a><span class="sel-proj"><code>open-webui</code></span><span class="sel-score">8.1</span></p><p class="sel-sum">Open WebUI: LDAP and OAuth First-User Race Condition Allows Multiple Admin Accounts</p></li></ol><p class="sel-foot">&dagger; Scored by me, not by the coordinating database; that advisory was published without a CVSS score or vector.</p><p class="sel-more"><a href="/advisories/">All 11 advisories, with CVSS vectors and full writeups &rarr;</a></p></div>

<!-- ADVISORIES:END -->

Every entry regenerates daily from the [GitHub Advisory Database](https://github.com/advisories?query=credit%3Asfwani), so this page only ever shows work that is published, fixed and credited.

## What I look for

**Unauthenticated reachability.** An auth gated code execution sink is a bug. The same sink reachable before auth is a critical. Most of my highest severity findings are reachability failures rather than novel sinks: missing authentication and missing authorization in front of machinery that was never meant to be public.

**Sandboxes that are not sandboxes.** Agent frameworks ship "safe" Python evaluators built on AST allowlists. Format string dunder traversal, decorator abuse, and incomplete node denylists walk straight out of most of them.

**Deserialization on exposed ports.** `pickle`, `cloudpickle`, `joblib`, and `torch.load(weights_only=False)` sitting behind an inference or actor pool port that quietly binds `0.0.0.0`.

**Request forgery into control planes.** My highest volume class: metadata endpoints, internal schedulers, and cluster APIs one redirect away from a user supplied URL.


## Current interests

Agentic systems and autonomous loops, and what happens to authorization when an agent acts on a user's behalf across many services. Where the tool invocation boundary quietly becomes an execution boundary. More on the [roles, degree and competition record](/experience/), and on the [research approach](/about/).

## Elsewhere

[GitHub](https://github.com/sfwani) &nbsp;·&nbsp; [LinkedIn](https://www.linkedin.com/in/sfwani) &nbsp;·&nbsp; [Advisories](https://github.com/sfwani/advisories) &nbsp;·&nbsp; [code.sanaan@gmail.com](mailto:code.sanaan@gmail.com)
