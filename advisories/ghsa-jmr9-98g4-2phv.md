---
title: "GHSA-jmr9-98g4-2phv"
heading: "GHSA-jmr9-98g4-2phv"
role: "Non-admin bind-mount restriction bypass via Docker local-driver volumes and automatic Git redeploy (incomplete fix of CVE-2026-44849 and CVE-2026-44850)"
seo_title: "GHSA-jmr9-98g4-2phv: Non-admin bind-mount restriction bypass via Docker local-driver volumes and… - Sanaan Fayaz Wani"
ghsa_id: "GHSA-jmr9-98g4-2phv"
cve_id: ""
published_at: "2026-10-08"
permalink: /advisories/ghsa-jmr9-98g4-2phv/
layout: c2
description: "Non-admin bind-mount restriction bypass via Docker local-driver volumes and automatic Git redeploy (incomplete fix of CVE-2026-44849 and CVE-2026-44850). portainer, CVSS 9.4 Critical, CWE-284 Access control. Writeup by Sanaan Fayaz Wani, the credited reporter."
image: /assets/img/og/ghsa-jmr9-98g4-2phv.png
kicker_repo: "portainer/portainer"
comments: false
last_modified_at: 2026-10-24T23:51:00+00:00
---
<section class="sec g" id="writeup" aria-labelledby="h-writeup" data-sev="critical" data-score="9.4" data-sevword="Critical" data-short="Fix differs by range">
  <h2 id="h-writeup" class="vh">GHSA-jmr9-98g4-2phv</h2>
  <div class="ah" data-sev="critical"><div class="ah-score"><p class="ah-num">9.4</p><p class="ah-sev">Critical</p><p class="ah-of">CVSS 4.0 base</p><div class="ah-meter" aria-hidden="true"><i style="width:94%"></i></div><ol class="tlv" aria-label="Disclosure timeline"><li><b>2026-10-08</b><span>Published by the maintainer</span></li></ol></div><div class="act warn"><p class="act-k">What to do</p><p class="act-v multi">If you run <b>2.40.0 to before 2.45.2</b>, upgrade to <b>2.45.2</b> or later.<br>If you run <b>2.39.0 and later</b>, no fixed version is listed in the advisory.</p></div><p class="ts"><em>Anyone who can reach it over the network</em>, with <em>a low-privilege account</em> and no user interaction, can <em>read and change sensitive data and make it unavailable</em>, and <em>other systems are affected too</em>.<span class="ts-src">Read from the CVSS 4.0 vector</span></p><div class="bx" style="--n:5"><div class="bx-head"><span class="k-lab">CVSS 4.0 metrics</span></div><div class="bx-row"><p class="bx-g">To exploit it</p><dl class="bx-grid"><div class="bx-c"><dt>Attack vector</dt><dd>Network</dd></div><div class="bx-c"><dt>Attack complexity</dt><dd>Low</dd></div><div class="bx-c"><dt>Attack requirements</dt><dd>None</dd></div><div class="bx-c"><dt>Privileges required</dt><dd>Low</dd></div><div class="bx-c"><dt>User interaction</dt><dd>None</dd></div></dl></div><div class="bx-row"><p class="bx-g">What it gets</p><dl class="bx-grid"><div class="bx-c"><dt>Confidentiality</dt><dd>High</dd></div><div class="bx-c"><dt>Integrity</dt><dd>High</dd></div><div class="bx-c"><dt>Availability</dt><dd>High</dd></div></dl></div><div class="bx-row"><p class="bx-g">Other systems</p><dl class="bx-grid"><div class="bx-c"><dt>Confidentiality</dt><dd>High</dd></div><div class="bx-c"><dt>Integrity</dt><dd>High</dd></div><div class="bx-c"><dt>Availability</dt><dd>High</dd></div></dl></div><p class="bx-foot"><a href="https://www.first.org/cvss/calculator/4.0#CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H" rel="noopener">Open this vector in the FIRST calculator &#8599;</a></p></div><dl class="meta"><div class="meta-i wide"><dt class="k-lab">Weakness</dt><dd class="meta-v"><abbr title="Improper Access Control">CWE-284</abbr> <span class="meta-s">Improper Access Control</span></dd></div><div class="meta-i"><dt class="k-lab">Advisory</dt><dd class="meta-v"><a href="https://github.com/portainer/portainer/security/advisories/GHSA-jmr9-98g4-2phv">GHSA-jmr9-98g4-2phv</a></dd></div><div class="meta-i"><dt class="k-lab">CVE</dt><dd class="meta-v">not assigned</dd></div><div class="meta-i"><dt class="k-lab">Vector</dt><dd class="meta-v"><span class="vec">CVSS:4.0/<wbr>AV:N/<wbr>AC:L/<wbr>AT:N/<wbr>PR:L/<wbr>UI:N/<wbr>VC:H/<wbr>VI:H/<wbr>VA:H/<wbr>SC:H/<wbr>SI:H/<wbr>SA:H</span></dd></div></dl><p class="ah-note">My analysis of this finding: root cause, the vulnerable code, the impact and the fix, in the site’s format. The official advisory of record is linked above.</p></div>
  <div class="col-body prose" markdown="1">

### Affected versions

<div class="vts"><div class="vt" aria-hidden="true"><div class="vt-pkg">github.com/portainer/portainer<span class="k-lab">go</span></div><div class="vt-bar"><div class="vt-pre">Not listed as affected</div><div class="vt-bad"><b>2.40.0</b><i>Affected</i><b>before 2.45.2</b></div><div class="vt-fix">Fixed in <b>2.45.2</b></div></div></div><div class="vt" aria-hidden="true"><div class="vt-pkg">github.com/portainer/portainer<span class="k-lab">go</span></div><div class="vt-bar"><div class="vt-pre">Not listed as affected</div><div class="vt-bad"><b>2.39.0</b><i>Affected</i><b>No upper bound</b></div><div class="vt-fix none">No fixed version listed</div></div></div></div>

| Package | Ecosystem | Vulnerable | Fixed in |
|:--|:--|:--|:--|
| `github.com/portainer/portainer` | go | >= 2.40.0, < 2.45.2 | 2.45.2 |
| `github.com/portainer/portainer` | go | >= 2.39.0 | n/a |
{: .vh}

## Summary

Portainer lets administrators disable bind mounts for regular users through the `AllowBindMountsForRegularUsers` endpoint security setting. The container creation proxy enforces that setting, but it only understands one of the two ways Docker can create a bind mount. A regular user can smuggle a host bind mount past the check by describing it as a `Type: "volume"` mount whose local driver config requests `type=bind`, mounting any path from the Docker host into their container. This is the same class of bypass that was fixed for Swarm services but never carried over to plain container creation.

## Where it lives

The container creation decorator parses an intentionally narrow view of the request body. In `api/http/proxy/factory/docker/containers.go`, the `Mounts` entries are reduced to a single field:

<pre class="has-mark"><code class="language-go"><span class="ln">Mounts      []struct {</span><span class="ln bug">    Type string `json:&quot;Type&quot;`</span><span class="ln">} `json:&quot;Mounts&quot;`</span></code></pre>

<p class="mark-cap"><span><span class="mark-k">The bug</span>mounts are parsed down to the Type field only</span></p>

and the enforcement loop only rejects the mount when that field is the literal string `bind`:

<pre class="has-mark"><code class="language-go"><span class="ln">if !securitySettings.AllowBindMountsForRegularUsers &amp;&amp; len(partialContainer.HostConfig.Mounts) &gt; 0 {</span><span class="ln">    for _, mount := range partialContainer.HostConfig.Mounts {</span><span class="ln bug">        if mount.Type == &quot;bind&quot; {</span><span class="ln">            return forbiddenResponse, ErrBindMountsForbidden</span></code></pre>

<p class="mark-cap"><span><span class="mark-k">The bug</span>only rejects mounts literally typed bind</span></p>

`VolumeOptions.DriverConfig.Options` is never parsed, so a mount declared as `Type: "volume"` sails through. The sibling code for Swarm services, in `api/http/proxy/factory/docker/services.go`, already knows about this trick. Its `partialServiceSpec` parses the nested struct and checks it explicitly:

```go
VolumeOptions *struct {
    DriverConfig *struct {
        Options map[string]string `json:"Options"`
    } `json:"DriverConfig"`
} `json:"VolumeOptions"`
...
if mount.VolumeOptions != nil && mount.VolumeOptions.DriverConfig != nil {
    if mount.VolumeOptions.DriverConfig.Options["type"] == "bind" {
```

The fix existed in one path and was simply absent in the other.

## Impact

A regular Portainer user with endpoint access, on an endpoint where bind mounts are supposed to be forbidden, posts a container create request whose mount is `Type: "volume"` with `DriverConfig.Options` of `type=bind`, `device=/`, `o=bind`. Docker's local volume driver turns that into a bind mount of the host root into the container. I confirmed this against v2.42.0: a container reading `/hostroot/etc/shadow` returned the real host file.

```
root:*:20535:0:99999:7:::
daemon:*:20535:0:99999:7:::
bin:*:20535:0:99999:7:::
```

From there the user has full read and write access to the host filesystem, including `/root/.ssh`, the Docker socket, and everything else, which is a complete escape of the restriction and of the container boundary. The affected range covers `>= 2.33.0` through `2.42.0`, every then current release.

## Fix

Teach the container path the same thing the service path already knows. Extend the `Mounts` struct with the `VolumeOptions.DriverConfig.Options` map and reject any mount whose `Options["type"]` is `bind`, in addition to the existing `Type == "bind"` check. The same validation belongs in the Docker Compose stack path so stacks cannot reintroduce the bypass.

<section class="fs-inline" aria-labelledby="h-record"><h2 id="h-record" class="no-idx">The record</h2><dl class="fs"><dt>Weakness</dt><dd><b>CWE-284</b> Improper Access Control</dd><dt>Affected</dt><dd><span class="fs-v">portainer <b>2.40.0 to before 2.45.2</b><span class="fs-gap">fixed in 2.45.2</span></span><span class="fs-v">portainer <b>2.39.0 and later</b><span class="fs-gap">no fix listed</span></span></dd><dt>Disclosure</dt><dd><b>2026-10-08</b> Published</dd><dt>Advisory</dt><dd><a href="https://github.com/portainer/portainer/security/advisories/GHSA-jmr9-98g4-2phv">GHSA-jmr9-98g4-2phv</a></dd></dl></section>

## About this writeup

Sanaan Fayaz Wani (GitHub [`sfwani`](https://github.com/sfwani)) reported this vulnerability to the `portainer` maintainers under coordinated disclosure and is credited as a reporter in [GHSA-jmr9-98g4-2phv](https://github.com/portainer/portainer/security/advisories/GHSA-jmr9-98g4-2phv), published 2026-10-08.

All published findings: [advisory index](/advisories/).


  </div>
  <aside class="srail" aria-label="Fact sheet" data-sev="critical"><div class="sr-h"><span class="sr-num">9.4</span><span class="sr-sev">Critical</span></div><p class="sr-src">CVSS 4.0 base</p><dl class="fs"><dt>Weakness</dt><dd><b>CWE-284</b> Improper Access Control</dd><dt>Affected</dt><dd><span class="fs-v">portainer <b>2.40.0 to before 2.45.2</b><span class="fs-gap">fixed in 2.45.2</span></span><span class="fs-v">portainer <b>2.39.0 and later</b><span class="fs-gap">no fix listed</span></span></dd><dt>Disclosure</dt><dd><b>2026-10-08</b> Published</dd><dt>Advisory</dt><dd><a href="https://github.com/portainer/portainer/security/advisories/GHSA-jmr9-98g4-2phv">GHSA-jmr9-98g4-2phv</a></dd></dl><a class="sr-top" href="#top">Back to top</a></aside>
</section>
