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
description: "AI Chat route exposes admin-only tools to non-admin users. directus, CVSS 3.1 Low, CWE-863 Incorrect authorization. Writeup by Sanaan Fayaz Wani, the credited reporter."
image: /assets/img/og/ghsa-xf86-hfpm-92xr.png
kicker_repo: "directus/directus"
comments: false
last_modified_at: 2026-10-24T23:51:00+00:00
---
<section class="sec g" id="writeup" aria-labelledby="h-writeup" data-sev="low" data-score="3.1" data-sevword="Low" data-short="Upgrade to 12.3.0">
  <h2 id="h-writeup" class="vh">GHSA-xf86-hfpm-92xr</h2>
  <div class="ah" data-sev="low"><div class="ah-score"><p class="ah-num">3.1</p><p class="ah-sev">Low</p><p class="ah-of">CVSS 3.1 base</p><div class="ah-meter" aria-hidden="true"><i style="width:31%"></i></div><ol class="tlv" aria-label="Disclosure timeline"><li><b>2026-05-22</b><span>Reported privately</span></li><li><span class="tlv-d">150 days later</span><b>2026-10-19</b><span>Published by the maintainer</span></li></ol></div><div class="act"><p class="act-k">What to do</p><p class="act-v">If you run <b>directus</b> <b>11.14.0 to before 12.3.0</b>, upgrade to <b>12.3.0</b> or later.</p></div><p class="ts"><em>Anyone who can reach it over the network</em>, with <em>a low-privilege account</em> and no user interaction, given conditions outside the attacker's control, can <em>read some data</em>.<span class="ts-src">Read from the CVSS 3.1 vector</span></p><div class="bx" style="--n:4"><div class="bx-head"><span class="k-lab">CVSS 3.1 metrics</span></div><div class="bx-row"><p class="bx-g">To exploit it</p><dl class="bx-grid"><div class="bx-c"><dt>Attack vector</dt><dd>Network</dd></div><div class="bx-c"><dt>Attack complexity</dt><dd>High</dd></div><div class="bx-c"><dt>Privileges required</dt><dd>Low</dd></div><div class="bx-c"><dt>User interaction</dt><dd>None</dd></div></dl></div><div class="bx-row"><p class="bx-g">What it gets</p><dl class="bx-grid"><div class="bx-c"><dt>Confidentiality</dt><dd>Low</dd></div><div class="bx-c"><dt>Integrity</dt><dd>None</dd></div><div class="bx-c"><dt>Availability</dt><dd>None</dd></div><div class="bx-c"><dt>Scope</dt><dd>Unchanged</dd></div></dl></div><p class="bx-foot"><a href="https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:L/I:N/A:N" rel="noopener">Open this vector in the FIRST calculator &#8599;</a></p></div><dl class="meta"><div class="meta-i wide"><dt class="k-lab">Weakness</dt><dd class="meta-v"><abbr title="Incorrect Authorization">CWE-863</abbr> <span class="meta-s">Incorrect Authorization</span></dd></div><div class="meta-i"><dt class="k-lab">Advisory</dt><dd class="meta-v"><a href="https://github.com/directus/directus/security/advisories/GHSA-xf86-hfpm-92xr">GHSA-xf86-hfpm-92xr</a></dd></div><div class="meta-i"><dt class="k-lab">CVE</dt><dd class="meta-v">not assigned</dd></div><div class="meta-i"><dt class="k-lab">Vector</dt><dd class="meta-v"><span class="vec">CVSS:3.1/<wbr>AV:N/<wbr>AC:H/<wbr>PR:L/<wbr>UI:N/<wbr>S:U/<wbr>C:L/<wbr>I:N/<wbr>A:N</span></dd></div></dl><div class="tl" role="group" aria-label="Disclosure timeline"><div class="tl-n"><b>2026-05-22</b><span>Reported privately</span></div><div class="tl-seg"><span>150 days</span></div><div class="tl-n"><b>2026-10-19</b><span>Published by the maintainer</span></div></div><p class="ah-note">My analysis of this finding: root cause, the vulnerable code, the impact and the fix, in the site’s format. The official advisory of record is linked above.</p></div>
  <div class="col-body prose" markdown="1">

### Affected versions

<div class="vts"><div class="vt" aria-hidden="true"><div class="vt-pkg">directus<span class="k-lab">npm</span></div><div class="vt-bar"><div class="vt-pre">Not listed as affected</div><div class="vt-bad"><b>11.14.0</b><i>Affected</i><b>before 12.3.0</b></div><div class="vt-fix">Fixed in <b>12.3.0</b></div></div></div></div>

| Package | Ecosystem | Vulnerable | Fixed in |
|:--|:--|:--|:--|
| `directus` | npm | >= 11.14.0, < 12.3.0 | 12.3.0 |
{: .vh}

## Summary

Directus (versions `<= 11.17.4`) ships two different ways to call its AI tools: the MCP server and the AI chat route. The MCP server guards the five tools marked `admin: true` (`collections`, `fields`, `relations`, `flows`, `operations`), but the chat route does not. Any authenticated user with `app_access` can ask the chat endpoint to run admin tools the MCP path would refuse them, so the two entry points disagree on who is allowed to do what.

## Where it lives

The chat route converts each requested tool into an AI SDK tool in `api/src/ai/chat/utils/chat-request-tool-to-ai-sdk-tool.ts`. At lines 21 to 26 it looks the tool up by name from `ALL_TOOLS` and wires it in, but it never reads `directusTool.admin`:

<pre class="has-mark"><code class="language-typescript"><span class="ln">// api/src/ai/chat/utils/chat-request-tool-to-ai-sdk-tool.ts:21-26</span><span class="ln">// looks up the tool by name from ALL_TOOLS</span><span class="ln">// and builds the AI SDK tool</span><span class="ln bug">// no check of directusTool.admin anywhere here</span></code></pre>

<p class="mark-cap"><span><span class="mark-k">The bug</span>the admin flag is never read on this path</span></p>

The MCP server, by contrast, enforces the flag in both the listing and the execution path:

```typescript
// api/src/ai/mcp/server.ts:200  (listing)
if (req.accountability?.admin !== true && tool.admin === true) continue;

// api/src/ai/mcp/server.ts:223  (execution)
if (req.accountability?.admin !== true && tool.admin === true)
    throw new ForbiddenError(...);
```

So the same tool definitions carry an `admin: true` flag that one dispatcher honors and the other ignores. The flag is the intended control; the chat route simply skips it.

## Impact

This is an incorrect authorization flaw (CWE-863). A non-admin user who holds `app_access` can drive the chat route to invoke `collections`, `fields`, `relations`, `flows`, and `operations`, the schema and automation tooling that Directus reserves for admins. The MCP server denies these to non-admins, which confirms the intended trust boundary and makes the chat route's omission a genuine bypass rather than a design choice. A low privilege `app_access` user, with no further interaction, gains read access to the schema and flow metadata that should be admin-only. The maintainers scored the impact as limited disclosure with no integrity impact (`C:L/I:N`), and because the runtime run below was not completed I do not claim any write effect beyond that.

I want to be precise about what I verified. The missing check is confirmed at the code level by comparing the two dispatchers line for line. The live end-to-end run was not completed because exercising the chat route needs a configured AI provider key, so I did not capture a runtime transcript for this one. The authorization gap in the source is unambiguous; the runtime proof is the piece I flag as outstanding.

## Fix

Mirror the MCP server's guard in the chat route. After the tool lookup at line 26, reject admin tools for non-admin callers before the tool is ever handed to the model:

<pre class="has-mark"><code class="language-typescript"><span class="ln fix">if (directusTool.admin &amp;&amp; accountability.admin !== true) {</span><span class="ln">    throw new ForbiddenError({</span><span class="ln">        reason: &#x27;You must be an admin to access this tool&#x27;,</span><span class="ln">    });</span><span class="ln">}</span></code></pre>

<p class="mark-cap"><span><span class="mark-k fix">The fix</span>rejects admin tools for non-admin callers</span></p>

Better still, both dispatchers should share one admin-enforcement helper so the `admin` flag cannot be honored in one place and forgotten in another.

<section class="fs-inline" aria-labelledby="h-record"><h2 id="h-record" class="no-idx">The record</h2><dl class="fs"><dt>Weakness</dt><dd><b>CWE-863</b> Incorrect Authorization</dd><dt>Affected</dt><dd>directus <b>11.14.0 to before 12.3.0</b></dd><dt>Fixed in</dt><dd><b>12.3.0</b></dd><dt>Disclosure</dt><dd><b>2026-05-22</b> Reported privately<br><span class="fs-gap">150 days later</span><b>2026-10-19</b> Published</dd><dt>Advisory</dt><dd><a href="https://github.com/directus/directus/security/advisories/GHSA-xf86-hfpm-92xr">GHSA-xf86-hfpm-92xr</a></dd></dl></section>

## About this writeup

Sanaan Fayaz Wani (GitHub [`sfwani`](https://github.com/sfwani)) reported this vulnerability to the `directus` maintainers under coordinated disclosure and is credited as a reporter in [GHSA-xf86-hfpm-92xr](https://github.com/directus/directus/security/advisories/GHSA-xf86-hfpm-92xr), published 2026-10-19.

All published findings: [advisory index](/advisories/).


  </div>
  <aside class="srail" aria-label="Fact sheet" data-sev="low"><div class="sr-h"><span class="sr-num">3.1</span><span class="sr-sev">Low</span></div><p class="sr-src">CVSS 3.1 base</p><dl class="fs"><dt>Weakness</dt><dd><b>CWE-863</b> Incorrect Authorization</dd><dt>Affected</dt><dd>directus <b>11.14.0 to before 12.3.0</b></dd><dt>Fixed in</dt><dd><b>12.3.0</b></dd><dt>Disclosure</dt><dd><b>2026-05-22</b> Reported privately<br><span class="fs-gap">150 days later</span><b>2026-10-19</b> Published</dd><dt>Advisory</dt><dd><a href="https://github.com/directus/directus/security/advisories/GHSA-xf86-hfpm-92xr">GHSA-xf86-hfpm-92xr</a></dd></dl><a class="sr-top" href="#top">Back to top</a></aside>
</section>
