---
title: About
permalink: /about/
layout: page
excerpt: Sanaan Wani is a Security Engineer at Amazon working on identity and access management, and an independent vulnerability researcher with seven assigned CVEs in AI agent frameworks and LLM infrastructure.
comments: false
---

Sanaan Wani is a Security Engineer at Amazon, working in IAM security on bringing agentic AI into identity and access management. Separately, he does independent vulnerability research against the infrastructure that runs large language models. Roles, education and competition record are on the [experience page](/experience/).

## Research

The target is the layer underneath the model: agent frameworks, inference servers, workflow orchestrators, vector stores, and the serialization formats they trust. Most of what he finds comes down to reachability rather than novel bug classes. An authenticated code execution sink is a bug. The same sink reachable before authentication is a critical, and AI infrastructure is unusually prone to shipping the second kind, because these projects grow quickly, bind to broad interfaces by default, and add execution features faster than they add authorization.

Seven CVEs have been assigned from that work, with eleven advisories published and credited against projects including Ray, Open WebUI, Kestra, Hatchet, Budibase and trigger.dev. Those are the ones that reached publication; the wider body of work is 167 advisories filed across 59 open source projects, most still in coordinated disclosure or closed by maintainers as accepted risk. Each published finding, with root cause, vulnerable code, reproduction and fix, is listed on the [home page](/).

The recurring classes, in rough order of volume: server side request forgery into control planes, missing authentication and authorization in front of machinery that was never meant to be public, unsafe deserialization on exposed inference ports, and sandbox escapes out of the AST allowlist evaluators that agent frameworks ship as safe Python.

## Method

Nothing is reported from code reading alone. Every finding is reproduced against a running instance first, with a real request and real output, because runtime behaviour routinely makes theoretically vulnerable code unexploitable. Reports go to maintainers privately, through GitHub Security Advisories or the project's stated security channel, never a public issue tracker, and nothing is named or mirrored publicly until the maintainer publishes.

## Current interests

Agentic systems and autonomous loops, and specifically what happens to authorization when an agent acts on a user's behalf across many services: how delegated identity and least privilege survive an agent that plans its own steps, and where the tool invocation boundary becomes an execution boundary. It is the same question as the day job from the other direction.

## Focus areas

AI agent security · LLM infrastructure security · agentic systems · autonomous agents · identity and access management · vulnerability research · coordinated disclosure · sandbox escape · unsafe deserialization · server side request forgery

## Contact

[code.sanaan@gmail.com](mailto:code.sanaan@gmail.com) · [GitHub](https://github.com/sfwani) · [LinkedIn](https://www.linkedin.com/in/sfwani)
