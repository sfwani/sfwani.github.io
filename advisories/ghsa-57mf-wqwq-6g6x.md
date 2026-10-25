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
description: "Hardcoded Default Fernet Encryption Key Exposes All Stored OAuth Credentials. autogpt-platform-backend, CVSS 8.2 High, CWE-321 Hard-coded crypto key. Writeup by Sanaan Fayaz Wani, the credited reporter."
image: /assets/img/og/ghsa-57mf-wqwq-6g6x.png
kicker_repo: "Significant-Gravitas/AutoGPT"
comments: false
last_modified_at: 2026-10-24T23:51:00+00:00
---
<section class="sec g" id="writeup" aria-labelledby="h-writeup" data-sev="high" data-score="8.2" data-sevword="High" data-short="Upgrade to 0.8.0">
  <h2 id="h-writeup" class="vh">GHSA-57mf-wqwq-6g6x</h2>
  <div class="ah" data-sev="high"><div class="ah-score"><p class="ah-num">8.2</p><p class="ah-sev">High</p><p class="ah-of">CVSS 3.1 base</p><div class="ah-meter" aria-hidden="true"><i style="width:82%"></i></div><ol class="tlv" aria-label="Disclosure timeline"><li><b>2026-10-05</b><span>Published by the maintainer</span></li></ol></div><div class="act"><p class="act-k">What to do</p><p class="act-v">If you run <b>autogpt-platform-backend</b> <b>0.6.23 to 0.7.4</b>, upgrade to <b>0.8.0</b> or later.</p></div><p class="ts"><em>Anyone who can reach it over the network</em>, with <em>a low-privilege account</em> and no user interaction, given conditions outside the attacker's control, can <em>read and change sensitive data</em>, and <em>the impact reaches beyond the vulnerable component</em>.<span class="ts-src">Read from the CVSS 3.1 vector</span></p><div class="bx" style="--n:4"><div class="bx-head"><span class="k-lab">CVSS 3.1 metrics</span></div><div class="bx-row"><p class="bx-g">To exploit it</p><dl class="bx-grid"><div class="bx-c"><dt>Attack vector</dt><dd>Network</dd></div><div class="bx-c"><dt>Attack complexity</dt><dd>High</dd></div><div class="bx-c"><dt>Privileges required</dt><dd>Low</dd></div><div class="bx-c"><dt>User interaction</dt><dd>None</dd></div></dl></div><div class="bx-row"><p class="bx-g">What it gets</p><dl class="bx-grid"><div class="bx-c"><dt>Confidentiality</dt><dd>High</dd></div><div class="bx-c"><dt>Integrity</dt><dd>High</dd></div><div class="bx-c"><dt>Availability</dt><dd>None</dd></div><div class="bx-c"><dt>Scope</dt><dd>Changed</dd></div></dl></div><p class="bx-foot"><a href="https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N" rel="noopener">Open this vector in the FIRST calculator &#8599;</a></p></div><dl class="meta"><div class="meta-i wide"><dt class="k-lab">Weakness</dt><dd class="meta-v"><abbr title="Use of Hard-coded Cryptographic Key">CWE-321</abbr>, <abbr title="Use of Hard-coded Credentials">CWE-798</abbr> <span class="meta-s">Use of Hard-coded Cryptographic Key · Use of Hard-coded Credentials</span></dd></div><div class="meta-i"><dt class="k-lab">Advisory</dt><dd class="meta-v"><a href="https://github.com/Significant-Gravitas/AutoGPT/security/advisories/GHSA-57mf-wqwq-6g6x">GHSA-57mf-wqwq-6g6x</a></dd></div><div class="meta-i"><dt class="k-lab">CVE</dt><dd class="meta-v">not assigned</dd></div><div class="meta-i"><dt class="k-lab">Vector</dt><dd class="meta-v"><span class="vec">CVSS:3.1/<wbr>AV:N/<wbr>AC:H/<wbr>PR:L/<wbr>UI:N/<wbr>S:C/<wbr>C:H/<wbr>I:H/<wbr>A:N</span></dd></div><div class="meta-i wide"><dt class="k-lab">Also in AutoGPT</dt><dd class="meta-v"><a href="/advisories/ghsa-24q6-6h89-f9p7/">GHSA-24q6-6h89-f9p7</a> 10.0</dd></div></dl><p class="ah-note">My analysis of this finding: root cause, the vulnerable code, the impact and the fix, in the site’s format. The official advisory of record is linked above.</p></div>
  <div class="col-body prose" markdown="1">

### Affected versions

<div class="vts"><div class="vt" aria-hidden="true"><div class="vt-pkg">autogpt-platform-backend</div><div class="vt-bar"><div class="vt-pre">Not listed as affected</div><div class="vt-bad"><b>0.6.23</b><i>Affected</i><b>0.7.4</b></div><div class="vt-fix">Fixed in <b>0.8.0</b></div></div></div></div>

| Package | Ecosystem | Vulnerable | Fixed in |
|:--|:--|:--|:--|
| `autogpt-platform-backend` | other | >= 0.6.23, <= 0.7.4 | 0.8.0 |
{: .vh}

## Summary

The AutoGPT platform shipped a hardcoded `ENCRYPTION_KEY` in `backend/.env.default`, committed to the public repository and loaded automatically by the default Docker Compose configuration. That one key does two jobs: it encrypts every stored user credential with Fernet, and it derives the HMAC key that signs pickle serialized cache entries in Redis. Because the key is public, both protections collapse for any deployment left on the default.

## Where it lives

Three places tie the public key to real impact.

Credential encryption, `backend/util/encryption.py`:

<pre class="has-mark"><code class="language-python"><span class="ln bug">ENCRYPTION_KEY = Settings().secrets.encryption_key  # from .env.default</span><span class="ln"> </span><span class="ln">class JSONCryptor:</span><span class="ln">    def __init__(self, key=None):</span><span class="ln">        self.key = key or ENCRYPTION_KEY</span><span class="ln">        self.fernet = Fernet(self.key.encode())</span></code></pre>

<p class="mark-cap"><span><span class="mark-k">The bug</span>credential key comes from the published default env file</span></p>

`backend/data/user.py` uses this to encrypt and decrypt `UserIntegrations`, which hold OAuth tokens, API keys and refresh tokens.

Cache HMAC signing, `backend/util/cache.py`:

<pre class="has-mark"><code class="language-python"><span class="ln">def _get_hmac_key() -&gt; bytes:</span><span class="ln bug">    secret = settings.secrets.encryption_key</span><span class="ln">    if not secret:</span><span class="ln">        secret = &quot;autogpt-cache-default-hmac-key&quot;</span><span class="ln">    return hashlib.sha256(secret.encode()).digest()</span></code></pre>

<p class="mark-cap"><span><span class="mark-k">The bug</span>derives the cache HMAC key from the public encryption key</span></p>

The derived key HMAC signs pickle serialized cache entries before they are stored in Redis. Reads call `pickle.loads()` after verifying the HMAC.

Default loading, `docker-compose.platform.yml`:

<pre class="has-mark"><code class="language-yaml"><span class="ln">x-backend-env-files: &amp;backend-env-files</span><span class="ln">  env_file:</span><span class="ln bug">    - backend/.env.default   # base defaults, always present</span><span class="ln">    - path: backend/.env     # user overrides, optional</span><span class="ln">      required: false</span></code></pre>

<p class="mark-cap"><span><span class="mark-k">The bug</span>the default env file is always loaded</span></p>

The default file is always loaded, so a deployment that never sets its own key runs on the published one.

## Impact

Two distinct chains, separated by what the attacker can reach.

**Credential decryption.** Anyone who can read the PostgreSQL store (a backup leak, SQL injection, misconfigured access, a compromised admin surface) can decrypt every stored credential with the public key: GitHub and Discord OAuth tokens, model provider API keys, and every other integration secret.

**Remote code execution.** Anyone who can write to Redis can forge an HMAC signed pickle payload with the derived key `sha256(ENCRYPTION_KEY)`. When the application next reads that poisoned entry, `pickle.loads()` runs attacker controlled code. The HMAC stops being a defense the moment its key is public.

A working proof of concept demonstrated all three steps end to end: encrypt and decrypt with the known key, forge a signature that passes the application's own verification, and deserialize the forged payload.

## Fix

Remove the shipped key and fail closed on it: refuse to start when `ENCRYPTION_KEY` is empty, matches a known published default, or is not a valid Fernet key, and document a rotation procedure. For the cache specifically, a safe serializer such as JSON or msgpack removes the deserialization sink entirely, so an HMAC bypass can no longer reach code execution.

<section class="fs-inline" aria-labelledby="h-record"><h2 id="h-record" class="no-idx">The record</h2><dl class="fs"><dt>Weakness</dt><dd><b>CWE-321</b> Use of Hard-coded Cryptographic Key<br><b>CWE-798</b> Use of Hard-coded Credentials</dd><dt>Affected</dt><dd>autogpt-platform-backend <b>0.6.23 to 0.7.4</b></dd><dt>Fixed in</dt><dd><b>0.8.0</b></dd><dt>Disclosure</dt><dd><b>2026-10-05</b> Published</dd><dt>Advisory</dt><dd><a href="https://github.com/Significant-Gravitas/AutoGPT/security/advisories/GHSA-57mf-wqwq-6g6x">GHSA-57mf-wqwq-6g6x</a></dd><dt>Also in AutoGPT</dt><dd><a href="/advisories/ghsa-24q6-6h89-f9p7/">GHSA-24q6-6h89-f9p7</a> 10.0</dd></dl></section>

## About this writeup

Sanaan Fayaz Wani (GitHub [`sfwani`](https://github.com/sfwani)) reported this vulnerability to the `autogpt-platform-backend` maintainers under coordinated disclosure and is credited as a reporter in [GHSA-57mf-wqwq-6g6x](https://github.com/Significant-Gravitas/AutoGPT/security/advisories/GHSA-57mf-wqwq-6g6x), published 2026-10-05.

All published findings: [advisory index](/advisories/).


  </div>
  <aside class="srail" aria-label="Fact sheet" data-sev="high"><div class="sr-h"><span class="sr-num">8.2</span><span class="sr-sev">High</span></div><p class="sr-src">CVSS 3.1 base</p><dl class="fs"><dt>Weakness</dt><dd><b>CWE-321</b> Use of Hard-coded Cryptographic Key<br><b>CWE-798</b> Use of Hard-coded Credentials</dd><dt>Affected</dt><dd>autogpt-platform-backend <b>0.6.23 to 0.7.4</b></dd><dt>Fixed in</dt><dd><b>0.8.0</b></dd><dt>Disclosure</dt><dd><b>2026-10-05</b> Published</dd><dt>Advisory</dt><dd><a href="https://github.com/Significant-Gravitas/AutoGPT/security/advisories/GHSA-57mf-wqwq-6g6x">GHSA-57mf-wqwq-6g6x</a></dd><dt>Also in AutoGPT</dt><dd><a href="/advisories/ghsa-24q6-6h89-f9p7/">GHSA-24q6-6h89-f9p7</a> 10.0</dd></dl><a class="sr-top" href="#top">Back to top</a></aside>
</section>
