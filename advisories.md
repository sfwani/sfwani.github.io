---
layout: c2
title: Advisories
heading: Advisories
seo_title: "Published security advisories credited to Sanaan Fayaz Wani"
role: "Every advisory below is published and credited. Reports still in coordinated disclosure are not listed, named or hinted at until the maintainer publishes them."
description: Published security advisories credited to Sanaan Fayaz Wani, with CVSS base vectors, weakness classes and full writeups.
permalink: /advisories/
last_modified_at: 2026-11-20T15:43:31+00:00
---

<section class="sec g" id="advisories" aria-labelledby="h-adv">
      <div class="sec-head">
        <div class="sec-title">
          <p class="idx">29</p>
          <h2 id="h-adv">Full record</h2>
        </div>
        <p class="sec-sub">Every entry is published and credited. Ordered by CVSS base score. Each row opens to the base vector in plain language, what to do, and how long disclosure took.</p>
      </div>

      <!-- RECORD:START -->

      <div class="tablewrap" role="region" aria-label="Published advisories, full table" tabindex="0">
        <table role="table">
          <thead role="rowgroup">
            <tr role="row">
              <th role="columnheader" scope="col" class="c-nr">NR</th>
              <th role="columnheader" scope="col" class="c-id">Advisory</th>
              <th role="columnheader" scope="col" class="c-pkg">Package</th>
              <th role="columnheader" scope="col" class="c-sc">CVSS</th>
              <th role="columnheader" scope="col" class="c-sev">Severity</th>
              <th role="columnheader" scope="col" class="c-cls">Weakness</th>
              <th role="columnheader" scope="col" class="c-cwe">CWE</th>
              <th role="columnheader" scope="col" class="c-vec">Base vector</th>
              <th role="columnheader" scope="col" class="c-pub">Published</th>
            </tr>
          </thead>
          <tbody role="rowgroup">
            <tr role="row" data-sev="critical">
              <th role="rowheader" scope="row" class="c-nr">01</th>
              <td role="cell" class="c-id"><a href="/advisories/cve-2026-130169/">CVE-2026-130169</a></td>
              <td role="cell" class="c-pkg">autogpt-platform-beta</td>
              <td role="cell" class="c-sc">10.0</td>
              <td role="cell" class="c-sev sev-crit">Critical</td>
              <td role="cell" class="c-cls">Authentication bypass</td>
              <td role="cell" class="c-cwe">287</td>
              <td role="cell" class="c-vec"><span class="vm-s">v3.1</span><span class="vm"><i>AV</i><b>N</b></span><span class="vm"><i>AC</i><b>L</b></span><span class="vm"><i>PR</i><b>N</b></span><span class="vm"><i>UI</i><b>N</b></span><span class="vm"><i>S</i><b>C</b></span><span class="vm"><i>C</i><b>H</b></span><span class="vm"><i>I</i><b>H</b></span><span class="vm"><i>A</i><b>H</b></span></td>
              <td role="cell" class="c-pub">2026-10-05</td>
            </tr>
            <tr role="row" class="peek" id="peek-01" data-sev="critical" hidden><td role="cell" colspan="9"><div class="pk"><div><p class="pk-s"><em>Anyone who can reach it over the network</em>, with <em>no account</em> and no user interaction, can <em>read and change sensitive data and make it unavailable</em>, and <em>the impact reaches beyond the vulnerable component</em>.</p></div><div class="pk-f"><span class="k-lab">What to do</span><b>Upgrade to 0.8.0</b></div><div class="pk-f"><span class="k-lab">Published</span><b>2026-10-05</b><small>Published by the maintainer</small></div><a class="pk-a" href="/advisories/cve-2026-130169/">Read the writeup &rarr;</a></div></td></tr>
            <tr role="row" data-sev="critical">
              <th role="rowheader" scope="row" class="c-nr">02</th>
              <td role="cell" class="c-id"><a href="/advisories/ghsa-42mf-vpmr-gw5r/">GHSA-42mf-vpmr-gw5r</a></td>
              <td role="cell" class="c-pkg">ag2</td>
              <td role="cell" class="c-sc">9.9</td>
              <td role="cell" class="c-sev sev-crit">Critical</td>
              <td role="cell" class="c-cls">Command injection</td>
              <td role="cell" class="c-cwe">78</td>
              <td role="cell" class="c-vec"><span class="vm-s">v3.1</span><span class="vm"><i>AV</i><b>N</b></span><span class="vm"><i>AC</i><b>L</b></span><span class="vm"><i>PR</i><b>L</b></span><span class="vm"><i>UI</i><b>N</b></span><span class="vm"><i>S</i><b>C</b></span><span class="vm"><i>C</i><b>H</b></span><span class="vm"><i>I</i><b>H</b></span><span class="vm"><i>A</i><b>H</b></span></td>
              <td role="cell" class="c-pub">2026-10-03</td>
            </tr>
            <tr role="row" class="peek" id="peek-02" data-sev="critical" hidden><td role="cell" colspan="9"><div class="pk"><div><p class="pk-s"><em>Anyone who can reach it over the network</em>, with <em>a low-privilege account</em> and no user interaction, can <em>read and change sensitive data and make it unavailable</em>, and <em>the impact reaches beyond the vulnerable component</em>.</p><div class="pk-f"><small>Score is my assessment; GitHub published no CVSS for this advisory.</small></div></div><div class="pk-f"><span class="k-lab">What to do</span><b>Upgrade to 1.1.2</b></div><div class="pk-f"><span class="k-lab">Report to publication</span><b>134 days</b><small>Reported privately 2026-05-22, published 2026-10-03</small></div><a class="pk-a" href="/advisories/ghsa-42mf-vpmr-gw5r/">Read the writeup &rarr;</a></div></td></tr>
            <tr role="row" data-sev="critical">
              <th role="rowheader" scope="row" class="c-nr">03</th>
              <td role="cell" class="c-id"><a href="/advisories/cve-2026-49950/">CVE-2026-49950</a></td>
              <td role="cell" class="c-pkg">xinference</td>
              <td role="cell" class="c-sc">9.3</td>
              <td role="cell" class="c-sev sev-crit">Critical</td>
              <td role="cell" class="c-cls">Missing authentication</td>
              <td role="cell" class="c-cwe">306</td>
              <td role="cell" class="c-vec"><span class="vm-s">v4.0</span><span class="vm"><i>AV</i><b>N</b></span><span class="vm"><i>AC</i><b>L</b></span><span class="vm"><i>AT</i><b>N</b></span><span class="vm"><i>PR</i><b>N</b></span><span class="vm"><i>UI</i><b>N</b></span><span class="vm"><i>VC</i><b>H</b></span><span class="vm"><i>VI</i><b>H</b></span><span class="vm"><i>VA</i><b>H</b></span><span class="vm"><i>SC</i><b>N</b></span><span class="vm"><i>SI</i><b>N</b></span><span class="vm"><i>SA</i><b>N</b></span></td>
              <td role="cell" class="c-pub">2026-10-16</td>
            </tr>
            <tr role="row" class="peek" id="peek-03" data-sev="critical" hidden><td role="cell" colspan="9"><div class="pk"><div><p class="pk-s"><em>Anyone who can reach it over the network</em>, with <em>no account</em> and no user interaction, can <em>read and change sensitive data and make it unavailable</em>.</p></div><div class="pk-f"><span class="k-lab">What to do</span><b class="quiet">No fix listed</b></div><div class="pk-f"><span class="k-lab">Published</span><b>2026-10-16</b><small>Published by the maintainer</small></div><a class="pk-a" href="/advisories/cve-2026-49950/">Read the writeup &rarr;</a></div></td></tr>
            <tr role="row" data-sev="high">
              <th role="rowheader" scope="row" class="c-nr">04</th>
              <td role="cell" class="c-id"><a href="/advisories/ghsa-hxvp-ff3g-qcj7/">GHSA-hxvp-ff3g-qcj7</a></td>
              <td role="cell" class="c-pkg">@vendure/core</td>
              <td role="cell" class="c-sc">8.8</td>
              <td role="cell" class="c-sev sev-high">High</td>
              <td role="cell" class="c-cls">Information disclosure</td>
              <td role="cell" class="c-cwe">200</td>
              <td role="cell" class="c-vec"><span class="vm-s">v3.1</span><span class="vm"><i>AV</i><b>N</b></span><span class="vm"><i>AC</i><b>L</b></span><span class="vm"><i>PR</i><b>L</b></span><span class="vm"><i>UI</i><b>N</b></span><span class="vm"><i>S</i><b>U</b></span><span class="vm"><i>C</i><b>H</b></span><span class="vm"><i>I</i><b>H</b></span><span class="vm"><i>A</i><b>H</b></span></td>
              <td role="cell" class="c-pub">2026-10-23</td>
            </tr>
            <tr role="row" class="peek" id="peek-04" data-sev="high" hidden><td role="cell" colspan="9"><div class="pk"><div><p class="pk-s"><em>Anyone who can reach it over the network</em>, with <em>a low-privilege account</em> and no user interaction, can <em>read and change sensitive data and make it unavailable</em>.</p></div><div class="pk-f"><span class="k-lab">What to do</span><b class="quiet">No fix listed</b></div><div class="pk-f"><span class="k-lab">Report to publication</span><b>19 days</b><small>Reported privately 2026-10-04, published 2026-10-23</small></div><a class="pk-a" href="/advisories/ghsa-hxvp-ff3g-qcj7/">Read the writeup &rarr;</a></div></td></tr>
            <tr role="row" data-sev="high">
              <th role="rowheader" scope="row" class="c-nr">05</th>
              <td role="cell" class="c-id"><a href="/advisories/ghsa-v3vj-mch3-x6c2/">GHSA-v3vj-mch3-x6c2</a></td>
              <td role="cell" class="c-pkg">omnigent</td>
              <td role="cell" class="c-sc">8.8</td>
              <td role="cell" class="c-sev sev-high">High</td>
              <td role="cell" class="c-cls">Resource exposure</td>
              <td role="cell" class="c-cwe">668</td>
              <td role="cell" class="c-vec"><span class="vm-s">v3.1</span><span class="vm"><i>AV</i><b>L</b></span><span class="vm"><i>AC</i><b>L</b></span><span class="vm"><i>PR</i><b>L</b></span><span class="vm"><i>UI</i><b>N</b></span><span class="vm"><i>S</i><b>C</b></span><span class="vm"><i>C</i><b>H</b></span><span class="vm"><i>I</i><b>H</b></span><span class="vm"><i>A</i><b>H</b></span></td>
              <td role="cell" class="c-pub">2026-10-13</td>
            </tr>
            <tr role="row" class="peek" id="peek-05" data-sev="high" hidden><td role="cell" colspan="9"><div class="pk"><div><p class="pk-s"><em>Someone with local access</em>, with <em>a low-privilege account</em> and no user interaction, can <em>read and change sensitive data and make it unavailable</em>, and <em>the impact reaches beyond the vulnerable component</em>.</p></div><div class="pk-f"><span class="k-lab">What to do</span><b>Upgrade to 0.18.0</b></div><div class="pk-f"><span class="k-lab">Report to publication</span><b>59 days</b><small>Reported privately 2026-08-15, published 2026-10-13</small></div><a class="pk-a" href="/advisories/ghsa-v3vj-mch3-x6c2/">Read the writeup &rarr;</a></div></td></tr>
            <tr role="row" data-sev="high">
              <th role="rowheader" scope="row" class="c-nr">06</th>
              <td role="cell" class="c-id"><a href="/advisories/ghsa-5mc6-2qfj-59cg/">GHSA-5mc6-2qfj-59cg</a></td>
              <td role="cell" class="c-pkg">opik</td>
              <td role="cell" class="c-sc">8.8</td>
              <td role="cell" class="c-sev sev-high">High</td>
              <td role="cell" class="c-cls">Code injection</td>
              <td role="cell" class="c-cwe">94</td>
              <td role="cell" class="c-vec"><span class="vm-s">v3.1</span><span class="vm"><i>AV</i><b>N</b></span><span class="vm"><i>AC</i><b>L</b></span><span class="vm"><i>PR</i><b>N</b></span><span class="vm"><i>UI</i><b>R</b></span><span class="vm"><i>S</i><b>U</b></span><span class="vm"><i>C</i><b>H</b></span><span class="vm"><i>I</i><b>H</b></span><span class="vm"><i>A</i><b>H</b></span></td>
              <td role="cell" class="c-pub">2026-11-05</td>
            </tr>
            <tr role="row" class="peek" id="peek-06" data-sev="high" hidden><td role="cell" colspan="9"><div class="pk"><div><p class="pk-s"><em>Anyone who can reach it over the network</em>, with <em>no account</em>, if a user takes some action, can <em>read and change sensitive data and make it unavailable</em>.</p></div><div class="pk-f"><span class="k-lab">What to do</span><b>Fix differs by range</b></div><div class="pk-f"><span class="k-lab">Report to publication</span><b>11 days</b><small>Reported privately 2026-10-25, published 2026-11-05</small></div><a class="pk-a" href="/advisories/ghsa-5mc6-2qfj-59cg/">Read the writeup &rarr;</a></div></td></tr>
            <tr role="row" data-sev="high">
              <th role="rowheader" scope="row" class="c-nr">07</th>
              <td role="cell" class="c-id"><a href="/advisories/cve-2026-57516/">CVE-2026-57516</a></td>
              <td role="cell" class="c-pkg">ray</td>
              <td role="cell" class="c-sc">8.8</td>
              <td role="cell" class="c-sev sev-high">High</td>
              <td role="cell" class="c-cls">Code injection</td>
              <td role="cell" class="c-cwe">94</td>
              <td role="cell" class="c-vec"><span class="vm-s">v3.1</span><span class="vm"><i>AV</i><b>N</b></span><span class="vm"><i>AC</i><b>L</b></span><span class="vm"><i>PR</i><b>N</b></span><span class="vm"><i>UI</i><b>R</b></span><span class="vm"><i>S</i><b>U</b></span><span class="vm"><i>C</i><b>H</b></span><span class="vm"><i>I</i><b>H</b></span><span class="vm"><i>A</i><b>H</b></span></td>
              <td role="cell" class="c-pub">2026-07-01</td>
            </tr>
            <tr role="row" class="peek" id="peek-07" data-sev="high" hidden><td role="cell" colspan="9"><div class="pk"><div><p class="pk-s"><em>Anyone who can reach it over the network</em>, with <em>no account</em>, if a user takes some action, can <em>read and change sensitive data and make it unavailable</em>.</p></div><div class="pk-f"><span class="k-lab">What to do</span><b>Upgrade to 2.56.0</b></div><div class="pk-f"><span class="k-lab">Published</span><b>2026-07-01</b><small>Published by the maintainer</small></div><a class="pk-a" href="/advisories/cve-2026-57516/">Read the writeup &rarr;</a></div></td></tr>
            <tr role="row" data-sev="high">
              <th role="rowheader" scope="row" class="c-nr">08</th>
              <td role="cell" class="c-id"><a href="/advisories/ghsa-jmr9-98g4-2phv/">GHSA-jmr9-98g4-2phv</a></td>
              <td role="cell" class="c-pkg">github.com/<wbr>portainer/<wbr>portainer</td>
              <td role="cell" class="c-sc">8.7</td>
              <td role="cell" class="c-sev sev-high">High</td>
              <td role="cell" class="c-cls">Access control</td>
              <td role="cell" class="c-cwe">284</td>
              <td role="cell" class="c-vec"><span class="vm-s">v4.0</span><span class="vm"><i>AV</i><b>N</b></span><span class="vm"><i>AC</i><b>L</b></span><span class="vm"><i>AT</i><b>N</b></span><span class="vm"><i>PR</i><b>L</b></span><span class="vm"><i>UI</i><b>N</b></span><span class="vm"><i>VC</i><b>H</b></span><span class="vm"><i>VI</i><b>H</b></span><span class="vm"><i>VA</i><b>H</b></span><span class="vm"><i>SC</i><b>N</b></span><span class="vm"><i>SI</i><b>N</b></span><span class="vm"><i>SA</i><b>N</b></span></td>
              <td role="cell" class="c-pub">2026-10-08</td>
            </tr>
            <tr role="row" class="peek" id="peek-08" data-sev="high" hidden><td role="cell" colspan="9"><div class="pk"><div><p class="pk-s"><em>Anyone who can reach it over the network</em>, with <em>a low-privilege account</em> and no user interaction, can <em>read and change sensitive data and make it unavailable</em>.</p></div><div class="pk-f"><span class="k-lab">What to do</span><b class="quiet">Fix differs by range</b></div><div class="pk-f"><span class="k-lab">Published</span><b>2026-10-08</b><small>Published by the maintainer</small></div><a class="pk-a" href="/advisories/ghsa-jmr9-98g4-2phv/">Read the writeup &rarr;</a></div></td></tr>
            <tr role="row" data-sev="high">
              <th role="rowheader" scope="row" class="c-nr">09</th>
              <td role="cell" class="c-id"><a href="/advisories/cve-2026-132257/">CVE-2026-132257</a></td>
              <td role="cell" class="c-pkg">autogpt-platform-beta</td>
              <td role="cell" class="c-sc">8.2</td>
              <td role="cell" class="c-sev sev-high">High</td>
              <td role="cell" class="c-cls">Hard-coded crypto key</td>
              <td role="cell" class="c-cwe">321</td>
              <td role="cell" class="c-vec"><span class="vm-s">v3.1</span><span class="vm"><i>AV</i><b>N</b></span><span class="vm"><i>AC</i><b>H</b></span><span class="vm"><i>PR</i><b>L</b></span><span class="vm"><i>UI</i><b>N</b></span><span class="vm"><i>S</i><b>C</b></span><span class="vm"><i>C</i><b>H</b></span><span class="vm"><i>I</i><b>H</b></span><span class="vm"><i>A</i><b>N</b></span></td>
              <td role="cell" class="c-pub">2026-10-05</td>
            </tr>
            <tr role="row" class="peek" id="peek-09" data-sev="high" hidden><td role="cell" colspan="9"><div class="pk"><div><p class="pk-s"><em>Anyone who can reach it over the network</em>, with <em>a low-privilege account</em> and no user interaction, given conditions outside the attacker's control, can <em>read and change sensitive data</em>, and <em>the impact reaches beyond the vulnerable component</em>.</p></div><div class="pk-f"><span class="k-lab">What to do</span><b>Upgrade to 0.8.0</b></div><div class="pk-f"><span class="k-lab">Published</span><b>2026-10-05</b><small>Published by the maintainer</small></div><a class="pk-a" href="/advisories/cve-2026-132257/">Read the writeup &rarr;</a></div></td></tr>
            <tr role="row" data-sev="high">
              <th role="rowheader" scope="row" class="c-nr">10</th>
              <td role="cell" class="c-id"><a href="/advisories/ghsa-qrjx-72xx-xhmh/">GHSA-qrjx-72xx-xhmh</a></td>
              <td role="cell" class="c-pkg">ag2</td>
              <td role="cell" class="c-sc">8.1</td>
              <td role="cell" class="c-sev sev-high">High</td>
              <td role="cell" class="c-cls">Path traversal</td>
              <td role="cell" class="c-cwe">22</td>
              <td role="cell" class="c-vec"><span class="vm-s">v3.1</span><span class="vm"><i>AV</i><b>N</b></span><span class="vm"><i>AC</i><b>L</b></span><span class="vm"><i>PR</i><b>L</b></span><span class="vm"><i>UI</i><b>N</b></span><span class="vm"><i>S</i><b>U</b></span><span class="vm"><i>C</i><b>H</b></span><span class="vm"><i>I</i><b>H</b></span><span class="vm"><i>A</i><b>N</b></span></td>
              <td role="cell" class="c-pub">2026-09-25</td>
            </tr>
            <tr role="row" class="peek" id="peek-10" data-sev="high" hidden><td role="cell" colspan="9"><div class="pk"><div><p class="pk-s"><em>Anyone who can reach it over the network</em>, with <em>a low-privilege account</em> and no user interaction, can <em>read and change sensitive data</em>.</p><div class="pk-f"><small>Score is my assessment; GitHub published no CVSS for this advisory.</small></div></div><div class="pk-f"><span class="k-lab">What to do</span><b class="quiet">Fix differs by range</b></div><div class="pk-f"><span class="k-lab">Report to publication</span><b>126 days</b><small>Reported privately 2026-05-22, published 2026-09-25</small></div><a class="pk-a" href="/advisories/ghsa-qrjx-72xx-xhmh/">Read the writeup &rarr;</a></div></td></tr>
            <tr role="row" data-sev="high">
              <th role="rowheader" scope="row" class="c-nr">11</th>
              <td role="cell" class="c-id"><a href="/advisories/cve-2026-45675/">CVE-2026-45675</a></td>
              <td role="cell" class="c-pkg">open-webui</td>
              <td role="cell" class="c-sc">8.1</td>
              <td role="cell" class="c-sev sev-high">High</td>
              <td role="cell" class="c-cls">Privilege escalation</td>
              <td role="cell" class="c-cwe">269</td>
              <td role="cell" class="c-vec"><span class="vm-s">v3.1</span><span class="vm"><i>AV</i><b>N</b></span><span class="vm"><i>AC</i><b>H</b></span><span class="vm"><i>PR</i><b>N</b></span><span class="vm"><i>UI</i><b>N</b></span><span class="vm"><i>S</i><b>U</b></span><span class="vm"><i>C</i><b>H</b></span><span class="vm"><i>I</i><b>H</b></span><span class="vm"><i>A</i><b>H</b></span></td>
              <td role="cell" class="c-pub">2026-05-11</td>
            </tr>
            <tr role="row" class="peek" id="peek-11" data-sev="high" hidden><td role="cell" colspan="9"><div class="pk"><div><p class="pk-s"><em>Anyone who can reach it over the network</em>, with <em>no account</em> and no user interaction, given conditions outside the attacker's control, can <em>read and change sensitive data and make it unavailable</em>.</p></div><div class="pk-f"><span class="k-lab">What to do</span><b>Upgrade to 0.9.0</b></div><div class="pk-f"><span class="k-lab">Report to publication</span><b>34 days</b><small>Reported privately 2026-04-07, published 2026-05-11</small></div><a class="pk-a" href="/advisories/cve-2026-45675/">Read the writeup &rarr;</a></div></td></tr>
            <tr role="row" data-sev="high">
              <th role="rowheader" scope="row" class="c-nr">12</th>
              <td role="cell" class="c-id"><a href="/advisories/ghsa-pqxw-g93w-hj9x/">GHSA-pqxw-g93w-hj9x</a></td>
              <td role="cell" class="c-pkg">trigger.dev</td>
              <td role="cell" class="c-sc">8.1</td>
              <td role="cell" class="c-sev sev-high">High</td>
              <td role="cell" class="c-cls">Improper isolation</td>
              <td role="cell" class="c-cwe">653</td>
              <td role="cell" class="c-vec"><span class="vm-s">v4.0</span><span class="vm"><i>AV</i><b>N</b></span><span class="vm"><i>AC</i><b>H</b></span><span class="vm"><i>AT</i><b>N</b></span><span class="vm"><i>PR</i><b>N</b></span><span class="vm"><i>UI</i><b>N</b></span><span class="vm"><i>VC</i><b>H</b></span><span class="vm"><i>VI</i><b>H</b></span><span class="vm"><i>VA</i><b>N</b></span><span class="vm"><i>SC</i><b>N</b></span><span class="vm"><i>SI</i><b>N</b></span><span class="vm"><i>SA</i><b>N</b></span><span class="vm"><i>E</i><b>P</b></span></td>
              <td role="cell" class="c-pub">2026-07-21</td>
            </tr>
            <tr role="row" class="peek" id="peek-12" data-sev="high" hidden><td role="cell" colspan="9"><div class="pk"><div><p class="pk-s"><em>Anyone who can reach it over the network</em>, with <em>no account</em> and no user interaction, if they can defeat a protection or obtain a target-specific secret, can <em>read and change sensitive data</em>.</p></div><div class="pk-f"><span class="k-lab">What to do</span><b>Upgrade to 4.5.6</b></div><div class="pk-f"><span class="k-lab">Report to publication</span><b>60 days</b><small>Reported privately 2026-05-22, published 2026-07-21</small></div><a class="pk-a" href="/advisories/ghsa-pqxw-g93w-hj9x/">Read the writeup &rarr;</a></div></td></tr>
            <tr role="row" data-sev="high">
              <th role="rowheader" scope="row" class="c-nr">13</th>
              <td role="cell" class="c-id"><a href="/advisories/ghsa-jc26-22qp-cgqj/">GHSA-jc26-22qp-cgqj</a></td>
              <td role="cell" class="c-pkg">trigger.dev</td>
              <td role="cell" class="c-sc">7.9</td>
              <td role="cell" class="c-sev sev-high">High</td>
              <td role="cell" class="c-cls">Missing authentication</td>
              <td role="cell" class="c-cwe">306</td>
              <td role="cell" class="c-vec"><span class="vm-s">v3.1</span><span class="vm"><i>AV</i><b>A</b></span><span class="vm"><i>AC</i><b>H</b></span><span class="vm"><i>PR</i><b>L</b></span><span class="vm"><i>UI</i><b>N</b></span><span class="vm"><i>S</i><b>C</b></span><span class="vm"><i>C</i><b>H</b></span><span class="vm"><i>I</i><b>H</b></span><span class="vm"><i>A</i><b>L</b></span></td>
              <td role="cell" class="c-pub">2026-09-14</td>
            </tr>
            <tr role="row" class="peek" id="peek-13" data-sev="high" hidden><td role="cell" colspan="9"><div class="pk"><div><p class="pk-s"><em>Anyone on an adjacent network</em>, with <em>a low-privilege account</em> and no user interaction, given conditions outside the attacker's control, can <em>read and change sensitive data and degrade its availability</em>, and <em>the impact reaches beyond the vulnerable component</em>.</p></div><div class="pk-f"><span class="k-lab">What to do</span><b class="quiet">Fix unclear</b></div><div class="pk-f"><span class="k-lab">Report to publication</span><b>115 days</b><small>Reported privately 2026-05-22, published 2026-09-14</small></div><a class="pk-a" href="/advisories/ghsa-jc26-22qp-cgqj/">Read the writeup &rarr;</a></div></td></tr>
            <tr role="row" data-sev="high">
              <th role="rowheader" scope="row" class="c-nr">14</th>
              <td role="cell" class="c-id"><a href="/advisories/ghsa-3c52-v5v2-3r56/">GHSA-3c52-v5v2-3r56</a></td>
              <td role="cell" class="c-pkg">budibase</td>
              <td role="cell" class="c-sc">7.7</td>
              <td role="cell" class="c-sev sev-high">High</td>
              <td role="cell" class="c-cls">Server side request forgery</td>
              <td role="cell" class="c-cwe">918</td>
              <td role="cell" class="c-vec"><span class="vm-s">v3.1</span><span class="vm"><i>AV</i><b>N</b></span><span class="vm"><i>AC</i><b>L</b></span><span class="vm"><i>PR</i><b>L</b></span><span class="vm"><i>UI</i><b>N</b></span><span class="vm"><i>S</i><b>C</b></span><span class="vm"><i>C</i><b>H</b></span><span class="vm"><i>I</i><b>N</b></span><span class="vm"><i>A</i><b>N</b></span></td>
              <td role="cell" class="c-pub">2026-09-17</td>
            </tr>
            <tr role="row" class="peek" id="peek-14" data-sev="high" hidden><td role="cell" colspan="9"><div class="pk"><div><p class="pk-s"><em>Anyone who can reach it over the network</em>, with <em>a low-privilege account</em> and no user interaction, can <em>read sensitive data</em>, and <em>the impact reaches beyond the vulnerable component</em>.</p></div><div class="pk-f"><span class="k-lab">What to do</span><b>Upgrade past 3.41.0</b></div><div class="pk-f"><span class="k-lab">Report to publication</span><b>118 days</b><small>Reported privately 2026-05-22, published 2026-09-17</small></div><a class="pk-a" href="/advisories/ghsa-3c52-v5v2-3r56/">Read the writeup &rarr;</a></div></td></tr>
            <tr role="row" data-sev="high">
              <th role="rowheader" scope="row" class="c-nr">15</th>
              <td role="cell" class="c-id"><a href="/advisories/cve-2026-56673/">CVE-2026-56673</a></td>
              <td role="cell" class="c-pkg">ComfyUI</td>
              <td role="cell" class="c-sc">7.5</td>
              <td role="cell" class="c-sev sev-high">High</td>
              <td role="cell" class="c-cls">Path traversal</td>
              <td role="cell" class="c-cwe">22</td>
              <td role="cell" class="c-vec"><span class="vm-s">v3.1</span><span class="vm"><i>AV</i><b>N</b></span><span class="vm"><i>AC</i><b>L</b></span><span class="vm"><i>PR</i><b>N</b></span><span class="vm"><i>UI</i><b>N</b></span><span class="vm"><i>S</i><b>U</b></span><span class="vm"><i>C</i><b>H</b></span><span class="vm"><i>I</i><b>N</b></span><span class="vm"><i>A</i><b>N</b></span></td>
              <td role="cell" class="c-pub">2026-07-15</td>
            </tr>
            <tr role="row" class="peek" id="peek-15" data-sev="high" hidden><td role="cell" colspan="9"><div class="pk"><div><p class="pk-s"><em>Anyone who can reach it over the network</em>, with <em>no account</em> and no user interaction, can <em>read sensitive data</em>.</p></div><div class="pk-f"><span class="k-lab">What to do</span><b>Upgrade to 0.28.0</b></div><div class="pk-f"><span class="k-lab">Published</span><b>2026-07-15</b><small>Published by the maintainer</small></div><a class="pk-a" href="/advisories/cve-2026-56673/">Read the writeup &rarr;</a></div></td></tr>
            <tr role="row" data-sev="high">
              <th role="rowheader" scope="row" class="c-nr">16</th>
              <td role="cell" class="c-id"><a href="/advisories/cve-2026-56671/">CVE-2026-56671</a></td>
              <td role="cell" class="c-pkg">ComfyUI</td>
              <td role="cell" class="c-sc">7.5</td>
              <td role="cell" class="c-sev sev-high">High</td>
              <td role="cell" class="c-cls">Path traversal</td>
              <td role="cell" class="c-cwe">22</td>
              <td role="cell" class="c-vec"><span class="vm-s">v3.1</span><span class="vm"><i>AV</i><b>N</b></span><span class="vm"><i>AC</i><b>L</b></span><span class="vm"><i>PR</i><b>N</b></span><span class="vm"><i>UI</i><b>N</b></span><span class="vm"><i>S</i><b>U</b></span><span class="vm"><i>C</i><b>H</b></span><span class="vm"><i>I</i><b>N</b></span><span class="vm"><i>A</i><b>N</b></span></td>
              <td role="cell" class="c-pub">2026-07-15</td>
            </tr>
            <tr role="row" class="peek" id="peek-16" data-sev="high" hidden><td role="cell" colspan="9"><div class="pk"><div><p class="pk-s"><em>Anyone who can reach it over the network</em>, with <em>no account</em> and no user interaction, can <em>read sensitive data</em>.</p></div><div class="pk-f"><span class="k-lab">What to do</span><b>Upgrade to 0.28.0</b></div><div class="pk-f"><span class="k-lab">Published</span><b>2026-07-15</b><small>Published by the maintainer</small></div><a class="pk-a" href="/advisories/cve-2026-56671/">Read the writeup &rarr;</a></div></td></tr>
            <tr role="row" data-sev="high">
              <th role="rowheader" scope="row" class="c-nr">17</th>
              <td role="cell" class="c-id"><a href="/advisories/cve-2026-59714/">CVE-2026-59714</a></td>
              <td role="cell" class="c-pkg">open-webui</td>
              <td role="cell" class="c-sc">7.1</td>
              <td role="cell" class="c-sev sev-high">High</td>
              <td role="cell" class="c-cls">Missing authorization</td>
              <td role="cell" class="c-cwe">862</td>
              <td role="cell" class="c-vec"><span class="vm-s">v3.1</span><span class="vm"><i>AV</i><b>N</b></span><span class="vm"><i>AC</i><b>L</b></span><span class="vm"><i>PR</i><b>L</b></span><span class="vm"><i>UI</i><b>N</b></span><span class="vm"><i>S</i><b>U</b></span><span class="vm"><i>C</i><b>N</b></span><span class="vm"><i>I</i><b>H</b></span><span class="vm"><i>A</i><b>L</b></span></td>
              <td role="cell" class="c-pub">2026-07-02</td>
            </tr>
            <tr role="row" class="peek" id="peek-17" data-sev="high" hidden><td role="cell" colspan="9"><div class="pk"><div><p class="pk-s"><em>Anyone who can reach it over the network</em>, with <em>a low-privilege account</em> and no user interaction, can <em>change data with serious effect and degrade its availability</em>.</p></div><div class="pk-f"><span class="k-lab">What to do</span><b>Upgrade to 0.10.0</b></div><div class="pk-f"><span class="k-lab">Report to publication</span><b>49 days</b><small>Reported privately 2026-05-14, published 2026-07-02</small></div><a class="pk-a" href="/advisories/cve-2026-59714/">Read the writeup &rarr;</a></div></td></tr>
            <tr role="row" data-sev="high">
              <th role="rowheader" scope="row" class="c-nr">18</th>
              <td role="cell" class="c-id"><a href="/advisories/ghsa-w677-p6hx-85vw/">GHSA-w677-p6hx-85vw</a></td>
              <td role="cell" class="c-pkg">teableio/teable</td>
              <td role="cell" class="c-sc">7.1</td>
              <td role="cell" class="c-sev sev-high">High</td>
              <td role="cell" class="c-cls">Authentication bypass</td>
              <td role="cell" class="c-cwe">287</td>
              <td role="cell" class="c-vec"><span class="vm-s">v3.1</span><span class="vm"><i>AV</i><b>N</b></span><span class="vm"><i>AC</i><b>L</b></span><span class="vm"><i>PR</i><b>L</b></span><span class="vm"><i>UI</i><b>N</b></span><span class="vm"><i>S</i><b>U</b></span><span class="vm"><i>C</i><b>H</b></span><span class="vm"><i>I</i><b>L</b></span><span class="vm"><i>A</i><b>N</b></span></td>
              <td role="cell" class="c-pub">2026-10-13</td>
            </tr>
            <tr role="row" class="peek" id="peek-18" data-sev="high" hidden><td role="cell" colspan="9"><div class="pk"><div><p class="pk-s"><em>Anyone who can reach it over the network</em>, with <em>a low-privilege account</em> and no user interaction, can <em>read sensitive data and change some data</em>.</p></div><div class="pk-f"><span class="k-lab">What to do</span><b>Upgrade to release.2026-10-12T12-45-53Z.3331</b></div><div class="pk-f"><span class="k-lab">Report to publication</span><b>38 days</b><small>Reported privately 2026-09-05, published 2026-10-13</small></div><a class="pk-a" href="/advisories/ghsa-w677-p6hx-85vw/">Read the writeup &rarr;</a></div></td></tr>
            <tr role="row" data-sev="medium">
              <th role="rowheader" scope="row" class="c-nr">19</th>
              <td role="cell" class="c-id"><a href="/advisories/ghsa-8p4j-2mm9-rh78/">GHSA-8p4j-2mm9-rh78</a></td>
              <td role="cell" class="c-pkg">Tracecat</td>
              <td role="cell" class="c-sc">6.5</td>
              <td role="cell" class="c-sev sev-med">Medium</td>
              <td role="cell" class="c-cls">Server side request forgery</td>
              <td role="cell" class="c-cwe">918</td>
              <td role="cell" class="c-vec"><span class="vm-s">v3.1</span><span class="vm"><i>AV</i><b>N</b></span><span class="vm"><i>AC</i><b>L</b></span><span class="vm"><i>PR</i><b>L</b></span><span class="vm"><i>UI</i><b>N</b></span><span class="vm"><i>S</i><b>U</b></span><span class="vm"><i>C</i><b>H</b></span><span class="vm"><i>I</i><b>N</b></span><span class="vm"><i>A</i><b>N</b></span></td>
              <td role="cell" class="c-pub">2026-09-20</td>
            </tr>
            <tr role="row" class="peek" id="peek-19" data-sev="medium" hidden><td role="cell" colspan="9"><div class="pk"><div><p class="pk-s"><em>Anyone who can reach it over the network</em>, with <em>a low-privilege account</em> and no user interaction, can <em>read sensitive data</em>.</p></div><div class="pk-f"><span class="k-lab">What to do</span><b>Upgrade to 1.0.0-beta.52-rc.3</b></div><div class="pk-f"><span class="k-lab">Report to publication</span><b>115 days</b><small>Reported privately 2026-05-28, published 2026-09-20</small></div><a class="pk-a" href="/advisories/ghsa-8p4j-2mm9-rh78/">Read the writeup &rarr;</a></div></td></tr>
            <tr role="row" data-sev="medium">
              <th role="rowheader" scope="row" class="c-nr">20</th>
              <td role="cell" class="c-id"><a href="/advisories/cve-2026-53577/">CVE-2026-53577</a></td>
              <td role="cell" class="c-pkg">io.kestra:kestra</td>
              <td role="cell" class="c-sc">6.5</td>
              <td role="cell" class="c-sev sev-med">Medium</td>
              <td role="cell" class="c-cls">Incorrect authorization</td>
              <td role="cell" class="c-cwe">863</td>
              <td role="cell" class="c-vec"><span class="vm-s">v3.1</span><span class="vm"><i>AV</i><b>N</b></span><span class="vm"><i>AC</i><b>L</b></span><span class="vm"><i>PR</i><b>L</b></span><span class="vm"><i>UI</i><b>N</b></span><span class="vm"><i>S</i><b>U</b></span><span class="vm"><i>C</i><b>H</b></span><span class="vm"><i>I</i><b>N</b></span><span class="vm"><i>A</i><b>N</b></span></td>
              <td role="cell" class="c-pub">2026-06-03</td>
            </tr>
            <tr role="row" class="peek" id="peek-20" data-sev="medium" hidden><td role="cell" colspan="9"><div class="pk"><div><p class="pk-s"><em>Anyone who can reach it over the network</em>, with <em>a low-privilege account</em> and no user interaction, can <em>read sensitive data</em>.</p></div><div class="pk-f"><span class="k-lab">What to do</span><b>Fixed in 1.0.45 or 1.3.21</b></div><div class="pk-f"><span class="k-lab">Report to publication</span><b>12 days</b><small>Reported privately 2026-05-22, published 2026-06-03</small></div><a class="pk-a" href="/advisories/cve-2026-53577/">Read the writeup &rarr;</a></div></td></tr>
            <tr role="row" data-sev="medium">
              <th role="rowheader" scope="row" class="c-nr">21</th>
              <td role="cell" class="c-id"><a href="/advisories/ghsa-jcc2-3vff-7867/">GHSA-jcc2-3vff-7867</a></td>
              <td role="cell" class="c-pkg">nocodb</td>
              <td role="cell" class="c-sc">6.5</td>
              <td role="cell" class="c-sev sev-med">Medium</td>
              <td role="cell" class="c-cls">CWE-522</td>
              <td role="cell" class="c-cwe">522</td>
              <td role="cell" class="c-vec"><span class="vm-s">v3.1</span><span class="vm"><i>AV</i><b>N</b></span><span class="vm"><i>AC</i><b>L</b></span><span class="vm"><i>PR</i><b>L</b></span><span class="vm"><i>UI</i><b>N</b></span><span class="vm"><i>S</i><b>U</b></span><span class="vm"><i>C</i><b>H</b></span><span class="vm"><i>I</i><b>N</b></span><span class="vm"><i>A</i><b>N</b></span></td>
              <td role="cell" class="c-pub">2026-11-02</td>
            </tr>
            <tr role="row" class="peek" id="peek-21" data-sev="medium" hidden><td role="cell" colspan="9"><div class="pk"><div><p class="pk-s"><em>Anyone who can reach it over the network</em>, with <em>a low-privilege account</em> and no user interaction, can <em>read sensitive data</em>.</p></div><div class="pk-f"><span class="k-lab">What to do</span><b>Upgrade to 2026.10.1</b></div><div class="pk-f"><span class="k-lab">Published</span><b>2026-11-02</b><small>Published by the maintainer</small></div><a class="pk-a" href="/advisories/ghsa-jcc2-3vff-7867/">Read the writeup &rarr;</a></div></td></tr>
            <tr role="row" data-sev="medium">
              <th role="rowheader" scope="row" class="c-nr">22</th>
              <td role="cell" class="c-id"><a href="/advisories/ghsa-jvm6-86c5-f8j8/">GHSA-jvm6-86c5-f8j8</a></td>
              <td role="cell" class="c-pkg">teableio/teable</td>
              <td role="cell" class="c-sc">6.5</td>
              <td role="cell" class="c-sev sev-med">Medium</td>
              <td role="cell" class="c-cls">Server side request forgery</td>
              <td role="cell" class="c-cwe">918</td>
              <td role="cell" class="c-vec"><span class="vm-s">v3.1</span><span class="vm"><i>AV</i><b>N</b></span><span class="vm"><i>AC</i><b>L</b></span><span class="vm"><i>PR</i><b>L</b></span><span class="vm"><i>UI</i><b>N</b></span><span class="vm"><i>S</i><b>U</b></span><span class="vm"><i>C</i><b>H</b></span><span class="vm"><i>I</i><b>N</b></span><span class="vm"><i>A</i><b>N</b></span></td>
              <td role="cell" class="c-pub">2026-10-13</td>
            </tr>
            <tr role="row" class="peek" id="peek-22" data-sev="medium" hidden><td role="cell" colspan="9"><div class="pk"><div><p class="pk-s"><em>Anyone who can reach it over the network</em>, with <em>a low-privilege account</em> and no user interaction, can <em>read sensitive data</em>.</p></div><div class="pk-f"><span class="k-lab">What to do</span><b>Upgrade to release.2026-10-12T12-45-53Z.3331</b></div><div class="pk-f"><span class="k-lab">Report to publication</span><b>39 days</b><small>Reported privately 2026-09-04, published 2026-10-13</small></div><a class="pk-a" href="/advisories/ghsa-jvm6-86c5-f8j8/">Read the writeup &rarr;</a></div></td></tr>
            <tr role="row" data-sev="medium">
              <th role="rowheader" scope="row" class="c-nr">23</th>
              <td role="cell" class="c-id"><a href="/advisories/cve-2026-63342/">CVE-2026-63342</a></td>
              <td role="cell" class="c-pkg">github.com/<wbr>hatchet-dev/<wbr>hatchet</td>
              <td role="cell" class="c-sc">6.3</td>
              <td role="cell" class="c-sev sev-med">Medium</td>
              <td role="cell" class="c-cls">Incorrect authorization</td>
              <td role="cell" class="c-cwe">863</td>
              <td role="cell" class="c-vec"><span class="vm-s">v3.1</span><span class="vm"><i>AV</i><b>N</b></span><span class="vm"><i>AC</i><b>H</b></span><span class="vm"><i>PR</i><b>L</b></span><span class="vm"><i>UI</i><b>N</b></span><span class="vm"><i>S</i><b>C</b></span><span class="vm"><i>C</i><b>H</b></span><span class="vm"><i>I</i><b>N</b></span><span class="vm"><i>A</i><b>N</b></span></td>
              <td role="cell" class="c-pub">2026-06-30</td>
            </tr>
            <tr role="row" class="peek" id="peek-23" data-sev="medium" hidden><td role="cell" colspan="9"><div class="pk"><div><p class="pk-s"><em>Anyone who can reach it over the network</em>, with <em>a low-privilege account</em> and no user interaction, given conditions outside the attacker's control, can <em>read sensitive data</em>, and <em>the impact reaches beyond the vulnerable component</em>.</p></div><div class="pk-f"><span class="k-lab">What to do</span><b>Upgrade to 0.91.1</b></div><div class="pk-f"><span class="k-lab">Report to publication</span><b>39 days</b><small>Reported privately 2026-05-22, published 2026-06-30</small></div><a class="pk-a" href="/advisories/cve-2026-63342/">Read the writeup &rarr;</a></div></td></tr>
            <tr role="row" data-sev="medium">
              <th role="rowheader" scope="row" class="c-nr">24</th>
              <td role="cell" class="c-id"><a href="/advisories/ghsa-59h8-w5q6-mfmp/">GHSA-59h8-w5q6-mfmp</a></td>
              <td role="cell" class="c-pkg">trigger.dev</td>
              <td role="cell" class="c-sc">5.3</td>
              <td role="cell" class="c-sev sev-med">Medium</td>
              <td role="cell" class="c-cls">Missing authentication</td>
              <td role="cell" class="c-cwe">306</td>
              <td role="cell" class="c-vec"><span class="vm-s">v3.1</span><span class="vm"><i>AV</i><b>N</b></span><span class="vm"><i>AC</i><b>L</b></span><span class="vm"><i>PR</i><b>N</b></span><span class="vm"><i>UI</i><b>N</b></span><span class="vm"><i>S</i><b>U</b></span><span class="vm"><i>C</i><b>N</b></span><span class="vm"><i>I</i><b>L</b></span><span class="vm"><i>A</i><b>N</b></span></td>
              <td role="cell" class="c-pub">2026-07-21</td>
            </tr>
            <tr role="row" class="peek" id="peek-24" data-sev="medium" hidden><td role="cell" colspan="9"><div class="pk"><div><p class="pk-s"><em>Anyone who can reach it over the network</em>, with <em>no account</em> and no user interaction, can <em>change some data</em>.</p></div><div class="pk-f"><span class="k-lab">What to do</span><b>Upgrade to 4.5.5</b></div><div class="pk-f"><span class="k-lab">Report to publication</span><b>60 days</b><small>Reported privately 2026-05-22, published 2026-07-21</small></div><a class="pk-a" href="/advisories/ghsa-59h8-w5q6-mfmp/">Read the writeup &rarr;</a></div></td></tr>
            <tr role="row" data-sev="medium">
              <th role="rowheader" scope="row" class="c-nr">25</th>
              <td role="cell" class="c-id"><a href="/advisories/cve-2026-73301/">CVE-2026-73301</a></td>
              <td role="cell" class="c-pkg">@budibase/server</td>
              <td role="cell" class="c-sc">4.3</td>
              <td role="cell" class="c-sev sev-med">Medium</td>
              <td role="cell" class="c-cls">Missing authorization</td>
              <td role="cell" class="c-cwe">862</td>
              <td role="cell" class="c-vec"><span class="vm-s">v3.1</span><span class="vm"><i>AV</i><b>N</b></span><span class="vm"><i>AC</i><b>L</b></span><span class="vm"><i>PR</i><b>L</b></span><span class="vm"><i>UI</i><b>N</b></span><span class="vm"><i>S</i><b>U</b></span><span class="vm"><i>C</i><b>L</b></span><span class="vm"><i>I</i><b>N</b></span><span class="vm"><i>A</i><b>N</b></span></td>
              <td role="cell" class="c-pub">2026-07-22</td>
            </tr>
            <tr role="row" class="peek" id="peek-25" data-sev="medium" hidden><td role="cell" colspan="9"><div class="pk"><div><p class="pk-s"><em>Anyone who can reach it over the network</em>, with <em>a low-privilege account</em> and no user interaction, can <em>read some data</em>.</p></div><div class="pk-f"><span class="k-lab">What to do</span><b class="quiet">No fix listed</b></div><div class="pk-f"><span class="k-lab">Report to publication</span><b>61 days</b><small>Reported privately 2026-05-22, published 2026-07-22</small></div><a class="pk-a" href="/advisories/cve-2026-73301/">Read the writeup &rarr;</a></div></td></tr>
            <tr role="row" data-sev="medium">
              <th role="rowheader" scope="row" class="c-nr">26</th>
              <td role="cell" class="c-id"><a href="/advisories/ghsa-64mc-4p6f-r7x9/">GHSA-64mc-4p6f-r7x9</a></td>
              <td role="cell" class="c-pkg">vaultwarden</td>
              <td role="cell" class="c-sc">4.3</td>
              <td role="cell" class="c-sev sev-med">Medium</td>
              <td role="cell" class="c-cls">Incorrect authorization</td>
              <td role="cell" class="c-cwe">863</td>
              <td role="cell" class="c-vec"><span class="vm-s">v3.1</span><span class="vm"><i>AV</i><b>N</b></span><span class="vm"><i>AC</i><b>L</b></span><span class="vm"><i>PR</i><b>L</b></span><span class="vm"><i>UI</i><b>N</b></span><span class="vm"><i>S</i><b>U</b></span><span class="vm"><i>C</i><b>L</b></span><span class="vm"><i>I</i><b>N</b></span><span class="vm"><i>A</i><b>N</b></span></td>
              <td role="cell" class="c-pub">2026-10-28</td>
            </tr>
            <tr role="row" class="peek" id="peek-26" data-sev="medium" hidden><td role="cell" colspan="9"><div class="pk"><div><p class="pk-s"><em>Anyone who can reach it over the network</em>, with <em>a low-privilege account</em> and no user interaction, can <em>read some data</em>.</p></div><div class="pk-f"><span class="k-lab">What to do</span><b>Upgrade to 1.37.4</b></div><div class="pk-f"><span class="k-lab">Report to publication</span><b>41 days</b><small>Reported privately 2026-09-17, published 2026-10-28</small></div><a class="pk-a" href="/advisories/ghsa-64mc-4p6f-r7x9/">Read the writeup &rarr;</a></div></td></tr>
            <tr role="row" data-sev="low">
              <th role="rowheader" scope="row" class="c-nr">27</th>
              <td role="cell" class="c-id"><a href="/advisories/ghsa-xf86-hfpm-92xr/">GHSA-xf86-hfpm-92xr</a></td>
              <td role="cell" class="c-pkg">directus</td>
              <td role="cell" class="c-sc">3.1</td>
              <td role="cell" class="c-sev sev-low">Low</td>
              <td role="cell" class="c-cls">Incorrect authorization</td>
              <td role="cell" class="c-cwe">863</td>
              <td role="cell" class="c-vec"><span class="vm-s">v3.1</span><span class="vm"><i>AV</i><b>N</b></span><span class="vm"><i>AC</i><b>H</b></span><span class="vm"><i>PR</i><b>L</b></span><span class="vm"><i>UI</i><b>N</b></span><span class="vm"><i>S</i><b>U</b></span><span class="vm"><i>C</i><b>L</b></span><span class="vm"><i>I</i><b>N</b></span><span class="vm"><i>A</i><b>N</b></span></td>
              <td role="cell" class="c-pub">2026-10-19</td>
            </tr>
            <tr role="row" class="peek" id="peek-27" data-sev="low" hidden><td role="cell" colspan="9"><div class="pk"><div><p class="pk-s"><em>Anyone who can reach it over the network</em>, with <em>a low-privilege account</em> and no user interaction, given conditions outside the attacker's control, can <em>read some data</em>.</p></div><div class="pk-f"><span class="k-lab">What to do</span><b>Upgrade to 12.3.0</b></div><div class="pk-f"><span class="k-lab">Report to publication</span><b>150 days</b><small>Reported privately 2026-05-22, published 2026-10-19</small></div><a class="pk-a" href="/advisories/ghsa-xf86-hfpm-92xr/">Read the writeup &rarr;</a></div></td></tr>
            <tr role="row" data-sev="low">
              <th role="rowheader" scope="row" class="c-nr">28</th>
              <td role="cell" class="c-id"><a href="/advisories/cve-2026-59715/">CVE-2026-59715</a></td>
              <td role="cell" class="c-pkg">open-webui</td>
              <td role="cell" class="c-sc">3.1</td>
              <td role="cell" class="c-sev sev-low">Low</td>
              <td role="cell" class="c-cls">Missing authentication</td>
              <td role="cell" class="c-cwe">306</td>
              <td role="cell" class="c-vec"><span class="vm-s">v3.1</span><span class="vm"><i>AV</i><b>N</b></span><span class="vm"><i>AC</i><b>H</b></span><span class="vm"><i>PR</i><b>L</b></span><span class="vm"><i>UI</i><b>N</b></span><span class="vm"><i>S</i><b>U</b></span><span class="vm"><i>C</i><b>N</b></span><span class="vm"><i>I</i><b>L</b></span><span class="vm"><i>A</i><b>N</b></span></td>
              <td role="cell" class="c-pub">2026-07-02</td>
            </tr>
            <tr role="row" class="peek" id="peek-28" data-sev="low" hidden><td role="cell" colspan="9"><div class="pk"><div><p class="pk-s"><em>Anyone who can reach it over the network</em>, with <em>a low-privilege account</em> and no user interaction, given conditions outside the attacker's control, can <em>change some data</em>.</p></div><div class="pk-f"><span class="k-lab">What to do</span><b>Upgrade to 0.10.0</b></div><div class="pk-f"><span class="k-lab">Report to publication</span><b>86 days</b><small>Reported privately 2026-04-07, published 2026-07-02</small></div><a class="pk-a" href="/advisories/cve-2026-59715/">Read the writeup &rarr;</a></div></td></tr>
            <tr role="row" data-sev="low">
              <th role="rowheader" scope="row" class="c-nr">29</th>
              <td role="cell" class="c-id"><a href="/advisories/ghsa-jmgj-cq6g-6hr2/">GHSA-jmgj-cq6g-6hr2</a></td>
              <td role="cell" class="c-pkg">nocodb</td>
              <td role="cell" class="c-sc">2.7</td>
              <td role="cell" class="c-sev sev-low">Low</td>
              <td role="cell" class="c-cls">Incorrect authorization</td>
              <td role="cell" class="c-cwe">863</td>
              <td role="cell" class="c-vec"><span class="vm-s">v3.1</span><span class="vm"><i>AV</i><b>N</b></span><span class="vm"><i>AC</i><b>L</b></span><span class="vm"><i>PR</i><b>H</b></span><span class="vm"><i>UI</i><b>N</b></span><span class="vm"><i>S</i><b>U</b></span><span class="vm"><i>C</i><b>N</b></span><span class="vm"><i>I</i><b>L</b></span><span class="vm"><i>A</i><b>N</b></span></td>
              <td role="cell" class="c-pub">2026-11-02</td>
            </tr>
            <tr role="row" class="peek" id="peek-29" data-sev="low" hidden><td role="cell" colspan="9"><div class="pk"><div><p class="pk-s"><em>Anyone who can reach it over the network</em>, with <em>a high-privilege account</em> and no user interaction, can <em>change some data</em>.</p></div><div class="pk-f"><span class="k-lab">What to do</span><b>Upgrade to 2026.09.1</b></div><div class="pk-f"><span class="k-lab">Report to publication</span><b>39 days</b><small>Reported privately 2026-09-24, published 2026-11-02</small></div><a class="pk-a" href="/advisories/ghsa-jmgj-cq6g-6hr2/">Read the writeup &rarr;</a></div></td></tr>
          </tbody>
        </table>
      </div>

<!-- RECORD:END -->
      <div class="tfoot">
        <p class="right">Every entry regenerates daily from the <a href="https://github.com/advisories?query=credit%3Asfwani">GitHub Advisory Database</a>, so this list only ever shows work that is published and credited.</p>
      </div>

      <ol class="notes">
        <li><b>01</b>
          <span class="nid">GHSA-pqxw-g93w-hj9x &middot; trigger.dev</span>
          Self-hosted deployment: default secrets allow unauthenticated infrastructure compromise.
        </li>
        <li><b>02</b>
          <span class="nid">GHSA-hhrp-gw25-jr43 &middot; ray</span>
          Arbitrary code execution via the <span class="code">ray.data.read_webdataset</span> default decoder: <span class="code">pickle.loads(value)</span> and <span class="code">torch.load(weights_only=False)</span>.
        </li>
        <li><b>03</b>
          <span class="nid">GHSA-h3ww-q6xx-w7x3 &middot; open-webui</span>
          LDAP and OAuth first-user race condition allows multiple admin accounts.
        </li>
        <li><b>04</b>
          <span class="nid">GHSA-jc26-22qp-cgqj &middot; trigger.dev</span>
          Supervisor workload API lacks cross-tenant authentication.
        </li>
        <li><b>05</b>
          <span class="nid">GHSA-3c52-v5v2-3r56 &middot; budibase</span>
          SSRF in AI table generation via <span class="code">uploadUrl</span>: raw fetch without blacklist protection.
        </li>
        <li><b>06</b>
          <span class="nid">GHSA-x2ff-v5v8-m75m &middot; open-webui</span>
          Cross-channel message overwrite via the chat completion API, in both single-model and multimodel <span class="code">message_ids</span>.
        </li>
        <li><b>07</b>
          <span class="nid">GHSA-r6v3-xxwj-9h42 &middot; io.kestra:kestra</span>
          Cross-execution file read via the preview endpoint (IDOR).
        </li>
        <li><b>08</b>
          <span class="nid">GHSA-g26x-m427-f48f &middot; hatchet</span>
          Cross-tenant durable task event log disclosure via a missing authorization check.
        </li>
        <li><b>09</b>
          <span class="nid">GHSA-59h8-w5q6-mfmp &middot; trigger.dev</span>
          Unauthenticated realtime stream data injection via run <span class="code">friendlyId</span>.
        </li>
        <li><b>10</b>
          <span class="nid">GHSA-4qcj-m5wp-jmf4 &middot; @budibase/server</span>
          Missing RBAC on <span class="code">GET /api/global/groups</span> allows BASIC users to enumerate all tenant groups and role mappings.
        </li>
        <li><b>11</b>
          <span class="nid">GHSA-gmfw-g93r-vg53 &middot; open-webui</span>
          Unauthenticated WebSocket access to collaborative document handlers, <span class="code">ydoc:awareness:update</span> and <span class="code">ydoc:document:leave</span>.
        </li>
      </ol>
    </section>
