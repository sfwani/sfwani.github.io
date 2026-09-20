---
layout: c2
title: Advisories
heading: Advisories
seo_title: "Published security advisories credited to Sanaan Fayaz Wani"
role: "Every advisory below is published, fixed and credited. Reports still in coordinated disclosure are not listed, named or hinted at until the maintainer ships a fix."
description: Eleven published security advisories credited to Sanaan Fayaz Wani, with CVSS base vectors, weakness classes and full writeups.
permalink: /advisories/
last_modified_at: 2026-09-20T03:35:01+00:00
---

<section class="sec g" id="advisories" aria-labelledby="h-adv">
      <div class="sec-head">
        <p class="idx idx--none">&mdash;</p>
        <h2 id="h-adv">Full record</h2>
        <p class="sec-sub">Eleven, published, fixed and credited. Descending by CVSS v3.1 base score. Summaries are keyed to the NR column and set below the table.</p>
      </div>

      <!-- RECORD:START -->

      <div class="tablewrap" role="region" aria-label="Published advisories, full table" tabindex="0">
        <table role="table">
          <caption>Published advisories, 2026-05-14 to 2026-09-17</caption>
          <thead role="rowgroup">
            <tr role="row">
              <th role="columnheader" scope="col" rowspan="2" class="c-nr">NR</th>
              <th role="columnheader" scope="col" rowspan="2" class="c-id">Advisory</th>
              <th role="columnheader" scope="col" rowspan="2" class="c-pkg">Package</th>
              <th role="columnheader" scope="col" rowspan="2" class="c-sc">CVSS</th>
              <th role="columnheader" scope="col" rowspan="2" class="c-sev">Severity</th>
              <th role="columnheader" scope="col" rowspan="2" class="c-cls">Weakness</th>
              <th role="columnheader" scope="col" rowspan="2" class="c-cwe">CWE</th>
              <th role="columnheader" scope="colgroup" colspan="8" class="vgroup">Base vector</th>
              <th role="columnheader" scope="col" rowspan="2" class="c-pub">Published</th>
            </tr>
            <tr role="row">
              <th role="columnheader" scope="col" class="v" title="Attack vector">AV</th>
              <th role="columnheader" scope="col" class="v" title="Attack complexity">AC</th>
              <th role="columnheader" scope="col" class="v" title="Privileges required">PR</th>
              <th role="columnheader" scope="col" class="v" title="User interaction">UI</th>
              <th role="columnheader" scope="col" class="v" title="Scope">S</th>
              <th role="columnheader" scope="col" class="v" title="Confidentiality">C</th>
              <th role="columnheader" scope="col" class="v" title="Integrity">I</th>
              <th role="columnheader" scope="col" class="v" title="Availability">A</th>
            </tr>
          </thead>
          <tbody role="rowgroup">
            <tr role="row">
              <th role="rowheader" scope="row" class="c-nr">01</th>
              <td role="cell" class="c-id"><a href="/advisories/cve-2026-57516/">CVE-2026-57516</a></td>
              <td role="cell" class="c-pkg">ray</td>
              <td role="cell" class="c-sc">8.8</td>
              <td role="cell" class="c-sev sev-high">High</td>
              <td role="cell" class="c-cls">Code injection</td>
              <td role="cell" class="c-cwe">94</td>
              <td role="cell" class="v" data-m="AV">N</td><td role="cell" class="v" data-m="AC">L</td><td role="cell" class="v" data-m="PR">N</td><td role="cell" class="v" data-m="UI">R</td>
              <td role="cell" class="v" data-m="S">U</td><td role="cell" class="v" data-m="C">H</td><td role="cell" class="v" data-m="I">H</td><td role="cell" class="v" data-m="A">H</td>
              <td role="cell" class="c-pub">2026-07-24</td>
            </tr>
            <tr role="row">
              <th role="rowheader" scope="row" class="c-nr">02</th>
              <td role="cell" class="c-id"><a href="/advisories/cve-2026-45675/">CVE-2026-45675</a></td>
              <td role="cell" class="c-pkg">open-webui</td>
              <td role="cell" class="c-sc">8.1</td>
              <td role="cell" class="c-sev sev-high">High</td>
              <td role="cell" class="c-cls">Privilege escalation</td>
              <td role="cell" class="c-cwe">269</td>
              <td role="cell" class="v" data-m="AV">N</td><td role="cell" class="v" data-m="AC">H</td><td role="cell" class="v" data-m="PR">N</td><td role="cell" class="v" data-m="UI">N</td>
              <td role="cell" class="v" data-m="S">U</td><td role="cell" class="v" data-m="C">H</td><td role="cell" class="v" data-m="I">H</td><td role="cell" class="v" data-m="A">H</td>
              <td role="cell" class="c-pub">2026-05-14</td>
            </tr>
            <tr role="row">
              <th role="rowheader" scope="row" class="c-nr">03</th>
              <td role="cell" class="c-id"><a href="/advisories/ghsa-pqxw-g93w-hj9x/">GHSA-pqxw-g93w-hj9x</a></td>
              <td role="cell" class="c-pkg">trigger.dev</td>
              <td role="cell" class="c-sc">8.1</td>
              <td role="cell" class="c-sev sev-high">High</td>
              <td role="cell" class="c-cls">Improper isolation</td>
              <td role="cell" class="c-cwe">653</td>
              <td role="cell" class="v" data-m="AV">N</td><td role="cell" class="v" data-m="AC">H</td><td role="cell" class="v" data-m="PR">N</td><td role="cell" class="v" data-m="UI">N</td>
              <td role="cell" class="v" data-m="S">U</td><td role="cell" class="v" data-m="C">H</td><td role="cell" class="v" data-m="I">H</td><td role="cell" class="v" data-m="A">H</td>
              <td role="cell" class="c-pub">2026-07-21</td>
            </tr>
            <tr role="row">
              <th role="rowheader" scope="row" class="c-nr">04</th>
              <td role="cell" class="c-id"><a href="/advisories/ghsa-jc26-22qp-cgqj/">GHSA-jc26-22qp-cgqj</a></td>
              <td role="cell" class="c-pkg">trigger.dev</td>
              <td role="cell" class="c-sc">7.9</td>
              <td role="cell" class="c-sev sev-high">High</td>
              <td role="cell" class="c-cls">Missing authentication</td>
              <td role="cell" class="c-cwe">306</td>
              <td role="cell" class="v" data-m="AV">A</td><td role="cell" class="v" data-m="AC">H</td><td role="cell" class="v" data-m="PR">L</td><td role="cell" class="v" data-m="UI">N</td>
              <td role="cell" class="v" data-m="S">C</td><td role="cell" class="v" data-m="C">H</td><td role="cell" class="v" data-m="I">H</td><td role="cell" class="v" data-m="A">L</td>
              <td role="cell" class="c-pub">2026-09-14</td>
            </tr>
            <tr role="row">
              <th role="rowheader" scope="row" class="c-nr">05</th>
              <td role="cell" class="c-id"><a href="/advisories/ghsa-3c52-v5v2-3r56/">GHSA-3c52-v5v2-3r56</a></td>
              <td role="cell" class="c-pkg">budibase</td>
              <td role="cell" class="c-sc">7.7</td>
              <td role="cell" class="c-sev sev-high">High</td>
              <td role="cell" class="c-cls">Server side request forgery</td>
              <td role="cell" class="c-cwe">918</td>
              <td role="cell" class="v" data-m="AV">N</td><td role="cell" class="v" data-m="AC">L</td><td role="cell" class="v" data-m="PR">L</td><td role="cell" class="v" data-m="UI">N</td>
              <td role="cell" class="v" data-m="S">C</td><td role="cell" class="v" data-m="C">H</td><td role="cell" class="v" data-m="I">N</td><td role="cell" class="v" data-m="A">N</td>
              <td role="cell" class="c-pub">2026-09-17</td>
            </tr>
            <tr role="row">
              <th role="rowheader" scope="row" class="c-nr">06</th>
              <td role="cell" class="c-id"><a href="/advisories/cve-2026-59714/">CVE-2026-59714</a></td>
              <td role="cell" class="c-pkg">open-webui</td>
              <td role="cell" class="c-sc">7.1</td>
              <td role="cell" class="c-sev sev-high">High</td>
              <td role="cell" class="c-cls">Missing authorization</td>
              <td role="cell" class="c-cwe">862</td>
              <td role="cell" class="v" data-m="AV">N</td><td role="cell" class="v" data-m="AC">L</td><td role="cell" class="v" data-m="PR">L</td><td role="cell" class="v" data-m="UI">N</td>
              <td role="cell" class="v" data-m="S">U</td><td role="cell" class="v" data-m="C">N</td><td role="cell" class="v" data-m="I">H</td><td role="cell" class="v" data-m="A">L</td>
              <td role="cell" class="c-pub">2026-07-24</td>
            </tr>
            <tr role="row">
              <th role="rowheader" scope="row" class="c-nr">07</th>
              <td role="cell" class="c-id"><a href="/advisories/cve-2026-53577/">CVE-2026-53577</a></td>
              <td role="cell" class="c-pkg">io.kestra:kestra</td>
              <td role="cell" class="c-sc">6.5</td>
              <td role="cell" class="c-sev sev-med">Medium</td>
              <td role="cell" class="c-cls">Incorrect authorization</td>
              <td role="cell" class="c-cwe">863</td>
              <td role="cell" class="v" data-m="AV">N</td><td role="cell" class="v" data-m="AC">L</td><td role="cell" class="v" data-m="PR">L</td><td role="cell" class="v" data-m="UI">N</td>
              <td role="cell" class="v" data-m="S">U</td><td role="cell" class="v" data-m="C">H</td><td role="cell" class="v" data-m="I">N</td><td role="cell" class="v" data-m="A">N</td>
              <td role="cell" class="c-pub">2026-06-03</td>
            </tr>
            <tr role="row">
              <th role="rowheader" scope="row" class="c-nr">08</th>
              <td role="cell" class="c-id"><a href="/advisories/cve-2026-63342/">CVE-2026-63342</a></td>
              <td role="cell" class="c-pkg">github.com/<wbr>hatchet-dev/<wbr>hatchet</td>
              <td role="cell" class="c-sc">6.3</td>
              <td role="cell" class="c-sev sev-med">Medium</td>
              <td role="cell" class="c-cls">Incorrect authorization</td>
              <td role="cell" class="c-cwe">863</td>
              <td role="cell" class="v" data-m="AV">N</td><td role="cell" class="v" data-m="AC">H</td><td role="cell" class="v" data-m="PR">L</td><td role="cell" class="v" data-m="UI">N</td>
              <td role="cell" class="v" data-m="S">C</td><td role="cell" class="v" data-m="C">H</td><td role="cell" class="v" data-m="I">N</td><td role="cell" class="v" data-m="A">N</td>
              <td role="cell" class="c-pub">2026-06-30</td>
            </tr>
            <tr role="row">
              <th role="rowheader" scope="row" class="c-nr">09</th>
              <td role="cell" class="c-id"><a href="/advisories/ghsa-59h8-w5q6-mfmp/">GHSA-59h8-w5q6-mfmp</a></td>
              <td role="cell" class="c-pkg">trigger.dev</td>
              <td role="cell" class="c-sc">5.3</td>
              <td role="cell" class="c-sev sev-med">Medium</td>
              <td role="cell" class="c-cls">Missing authentication</td>
              <td role="cell" class="c-cwe">306</td>
              <td role="cell" class="v" data-m="AV">N</td><td role="cell" class="v" data-m="AC">L</td><td role="cell" class="v" data-m="PR">N</td><td role="cell" class="v" data-m="UI">N</td>
              <td role="cell" class="v" data-m="S">U</td><td role="cell" class="v" data-m="C">N</td><td role="cell" class="v" data-m="I">L</td><td role="cell" class="v" data-m="A">N</td>
              <td role="cell" class="c-pub">2026-07-21</td>
            </tr>
            <tr role="row">
              <th role="rowheader" scope="row" class="c-nr">10</th>
              <td role="cell" class="c-id"><a href="/advisories/cve-2026-73301/">CVE-2026-73301</a></td>
              <td role="cell" class="c-pkg">@budibase/server</td>
              <td role="cell" class="c-sc">4.3</td>
              <td role="cell" class="c-sev sev-med">Medium</td>
              <td role="cell" class="c-cls">Missing authorization</td>
              <td role="cell" class="c-cwe">862</td>
              <td role="cell" class="v" data-m="AV">N</td><td role="cell" class="v" data-m="AC">L</td><td role="cell" class="v" data-m="PR">L</td><td role="cell" class="v" data-m="UI">N</td>
              <td role="cell" class="v" data-m="S">U</td><td role="cell" class="v" data-m="C">L</td><td role="cell" class="v" data-m="I">N</td><td role="cell" class="v" data-m="A">N</td>
              <td role="cell" class="c-pub">2026-07-24</td>
            </tr>
            <tr role="row">
              <th role="rowheader" scope="row" class="c-nr">11</th>
              <td role="cell" class="c-id"><a href="/advisories/cve-2026-59715/">CVE-2026-59715</a></td>
              <td role="cell" class="c-pkg">open-webui</td>
              <td role="cell" class="c-sc">3.1</td>
              <td role="cell" class="c-sev sev-low">Low</td>
              <td role="cell" class="c-cls">Missing authentication</td>
              <td role="cell" class="c-cwe">306</td>
              <td role="cell" class="v" data-m="AV">N</td><td role="cell" class="v" data-m="AC">H</td><td role="cell" class="v" data-m="PR">L</td><td role="cell" class="v" data-m="UI">N</td>
              <td role="cell" class="v" data-m="S">U</td><td role="cell" class="v" data-m="C">N</td><td role="cell" class="v" data-m="I">L</td><td role="cell" class="v" data-m="A">N</td>
              <td role="cell" class="c-pub">2026-07-24</td>
            </tr>
          </tbody>
        </table>
      </div>

<!-- RECORD:END -->
      <div class="tfoot">
        <p class="right">Every entry regenerates daily from the <a href="https://github.com/advisories?query=credit%3Asfwani">GitHub Advisory Database</a>, so this list only ever shows work that is published, fixed and credited.</p>
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
