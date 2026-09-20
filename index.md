---
layout: c2
title: Sanaan Fayaz Wani
heading: Sanaan Fayaz Wani
seo_title: "Sanaan Fayaz Wani - Security Engineer and vulnerability researcher"
role: "Security Engineer, IAM at Amazon. Independent vulnerability research against the infrastructure that runs large language models."
description: Vulnerability research on AI agent frameworks and LLM infrastructure. Seven assigned CVEs and eleven published advisories, with root cause, reproduction and fix for each.
permalink: /
last_modified_at: 2026-09-20T03:43:55+00:00
---

<div class="figs-lead g">
<!-- COUNTERS:START -->

      <ul class="figs">
        <li class="fig"><b>7</b><span>CVEs assigned</span></li>
        <li class="fig"><b>11</b><span>Advisories published</span></li>
        <li class="fig"><b>6</b><span>Projects credited</span></li>
        <li class="fig"><b>167</b><span>Reports filed</span></li>
        <li class="fig"><b>59</b><span>Projects audited</span></li>
      </ul>

<!-- COUNTERS:END -->
</div>

<section class="sec g" id="profile" aria-labelledby="h-profile">
      <div class="sec-head">
        <p class="idx">01</p>
        <h2 id="h-profile">Profile</h2>
        <p class="sec-sub">Amazon, Cyber Florida, University of South Florida. Independent vulnerability research separately.</p>
      </div>

      <div class="col-body prose">
        <p>Sanaan Fayaz Wani is a Security Engineer at Amazon, working in IAM security on bringing agentic AI into identity and access management. Outside that, he hunts unauthenticated remote code execution in the infrastructure that runs large language models: agent frameworks, inference servers, workflow orchestrators, and the serialization formats they trust.</p>
        <p>Before Amazon he was a security researcher at Cyber Florida, building agentic systems for open source vulnerability research and working on industrial control system security. The summer before that he was on Amazon&rsquo;s red team, building an autonomous system for red teaming and tooling against Model Context Protocol servers while the protocol was still new. He graduated magna cum laude in computer science from the University of South Florida in May 2026, where he competed with the CyberHerd team.</p>
      </div>

      <div class="col-aside">
        <p class="kicker">Disclosure</p>
        <p style="margin-top:8px; font-size:var(--t-s); line-height:1.55; color:var(--ink-2); max-width:40ch;">The work listed here is coordinated disclosure. Every finding is reported privately to the maintainer first, and nothing is named, listed or hinted at until a fix ships. What that leaves is a record anyone can check: each entry resolves to an advisory the maintainer published and credited.</p>
      </div>
    </section>

<section class="sec g" id="advisories" aria-labelledby="h-adv">
      <div class="sec-head">
        <p class="sec-nr">02</p>
        <h2 id="h-adv">Advisories</h2>
        <p class="sec-sub">Every entry is published, fixed and credited. Nothing is named here until the
          maintainer ships a fix. The full record, with each CVSS base vector set out metric by metric,
          is on the <a href="/advisories/">advisories page</a>.</p>
      </div>
<!-- ADVISORIES:START -->

      <div class="tablewrap tablewrap--compact" role="region" aria-label="Published advisories" tabindex="0">
        <table role="table" class="rec rec--compact">
          <thead role="rowgroup"><tr role="row"><th role="columnheader" scope="col" class="c-nr">NR</th><th role="columnheader" scope="col" class="c-id">Advisory</th><th role="columnheader" scope="col" class="c-pkg">Project</th><th role="columnheader" scope="col" class="c-sc">CVSS</th><th role="columnheader" scope="col" class="c-sev">Severity</th><th role="columnheader" scope="col" class="c-cls">Weakness</th><th role="columnheader" scope="col" class="c-pub">Published</th></tr></thead>
          <tbody role="rowgroup"><tr role="row"><th role="rowheader" scope="row" class="c-nr">01</th><td role="cell" class="c-id"><a href="/advisories/cve-2026-57516/">CVE-2026-57516</a></td><td role="cell" class="c-pkg">ray</td><td role="cell" class="c-sc">8.8</td><td role="cell" class="c-sev sev-high">High</td><td role="cell" class="c-cls">Code injection</td><td role="cell" class="c-pub">2026-07-24</td></tr><tr role="row"><th role="rowheader" scope="row" class="c-nr">02</th><td role="cell" class="c-id"><a href="/advisories/cve-2026-45675/">CVE-2026-45675</a></td><td role="cell" class="c-pkg">open-webui</td><td role="cell" class="c-sc">8.1</td><td role="cell" class="c-sev sev-high">High</td><td role="cell" class="c-cls">Privilege escalation</td><td role="cell" class="c-pub">2026-05-14</td></tr><tr role="row"><th role="rowheader" scope="row" class="c-nr">03</th><td role="cell" class="c-id"><a href="/advisories/ghsa-pqxw-g93w-hj9x/">GHSA-pqxw-g93w-hj9x</a></td><td role="cell" class="c-pkg">trigger.dev</td><td role="cell" class="c-sc">8.1</td><td role="cell" class="c-sev sev-high">High</td><td role="cell" class="c-cls">Improper isolation</td><td role="cell" class="c-pub">2026-07-21</td></tr><tr role="row"><th role="rowheader" scope="row" class="c-nr">04</th><td role="cell" class="c-id"><a href="/advisories/ghsa-jc26-22qp-cgqj/">GHSA-jc26-22qp-cgqj</a></td><td role="cell" class="c-pkg">trigger.dev</td><td role="cell" class="c-sc">7.9</td><td role="cell" class="c-sev sev-high">High</td><td role="cell" class="c-cls">Missing authentication</td><td role="cell" class="c-pub">2026-09-14</td></tr><tr role="row"><th role="rowheader" scope="row" class="c-nr">05</th><td role="cell" class="c-id"><a href="/advisories/ghsa-3c52-v5v2-3r56/">GHSA-3c52-v5v2-3r56</a></td><td role="cell" class="c-pkg">budibase</td><td role="cell" class="c-sc">7.7</td><td role="cell" class="c-sev sev-high">High</td><td role="cell" class="c-cls">Server side request forgery</td><td role="cell" class="c-pub">2026-09-17</td></tr><tr role="row"><th role="rowheader" scope="row" class="c-nr">06</th><td role="cell" class="c-id"><a href="/advisories/cve-2026-59714/">CVE-2026-59714</a></td><td role="cell" class="c-pkg">open-webui</td><td role="cell" class="c-sc">7.1</td><td role="cell" class="c-sev sev-high">High</td><td role="cell" class="c-cls">Missing authorization</td><td role="cell" class="c-pub">2026-07-24</td></tr><tr role="row"><th role="rowheader" scope="row" class="c-nr">07</th><td role="cell" class="c-id"><a href="/advisories/cve-2026-53577/">CVE-2026-53577</a></td><td role="cell" class="c-pkg">io.kestra:kestra</td><td role="cell" class="c-sc">6.5</td><td role="cell" class="c-sev sev-med">Medium</td><td role="cell" class="c-cls">Incorrect authorization</td><td role="cell" class="c-pub">2026-06-03</td></tr><tr role="row"><th role="rowheader" scope="row" class="c-nr">08</th><td role="cell" class="c-id"><a href="/advisories/cve-2026-63342/">CVE-2026-63342</a></td><td role="cell" class="c-pkg">github.com/<wbr>hatchet-dev/<wbr>hatchet</td><td role="cell" class="c-sc">6.3</td><td role="cell" class="c-sev sev-med">Medium</td><td role="cell" class="c-cls">Incorrect authorization</td><td role="cell" class="c-pub">2026-06-30</td></tr><tr role="row"><th role="rowheader" scope="row" class="c-nr">09</th><td role="cell" class="c-id"><a href="/advisories/ghsa-59h8-w5q6-mfmp/">GHSA-59h8-w5q6-mfmp</a></td><td role="cell" class="c-pkg">trigger.dev</td><td role="cell" class="c-sc">5.3</td><td role="cell" class="c-sev sev-med">Medium</td><td role="cell" class="c-cls">Missing authentication</td><td role="cell" class="c-pub">2026-07-21</td></tr><tr role="row"><th role="rowheader" scope="row" class="c-nr">10</th><td role="cell" class="c-id"><a href="/advisories/cve-2026-73301/">CVE-2026-73301</a></td><td role="cell" class="c-pkg">@budibase/server</td><td role="cell" class="c-sc">4.3</td><td role="cell" class="c-sev sev-med">Medium</td><td role="cell" class="c-cls">Missing authorization</td><td role="cell" class="c-pub">2026-07-24</td></tr><tr role="row"><th role="rowheader" scope="row" class="c-nr">11</th><td role="cell" class="c-id"><a href="/advisories/cve-2026-59715/">CVE-2026-59715</a></td><td role="cell" class="c-pkg">open-webui</td><td role="cell" class="c-sc">3.1</td><td role="cell" class="c-sev sev-low">Low</td><td role="cell" class="c-cls">Missing authentication</td><td role="cell" class="c-pub">2026-07-24</td></tr></tbody>
        </table>
      </div>

<!-- ADVISORIES:END -->

      <div class="tfoot">
        <p class="left"><a href="/advisories/">The full record, with base vectors and writeups &rarr;</a></p>
      </div>
    </section>

<section class="sec g" id="classes" aria-labelledby="h-classes">
      <div class="sec-head">
        <p class="idx">03</p>
        <h2 id="h-classes">Weakness classes</h2>
        <p class="sec-sub">Four recurring, in rough order of volume.</p>
      </div>

      <ol class="classes">
        <li>
          <h3>Unauthenticated reachability</h3>
          <p>An auth gated code execution sink is a bug. The same sink reachable before auth is a critical. Most of the highest severity findings here are reachability failures rather than novel sinks: missing authentication and missing authorization in front of machinery that was never meant to be public.</p>
        </li>
        <li>
          <h3>Sandboxes that are not sandboxes</h3>
          <p>Agent frameworks ship &ldquo;safe&rdquo; Python evaluators built on AST allowlists. Format string dunder traversal, decorator abuse, and incomplete node denylists walk straight out of most of them.</p>
        </li>
        <li>
          <h3>Deserialization on exposed ports</h3>
          <p><span class="code">pickle</span>, <span class="code">cloudpickle</span>, <span class="code">joblib</span>, and <span class="code">torch.load(weights_only=False)</span> sitting behind an inference or actor pool port that quietly binds <span class="code">0.0.0.0</span>.</p>
        </li>
        <li>
          <h3>Request forgery into control planes</h3>
          <p>The highest volume class: metadata endpoints, internal schedulers, and cluster APIs one redirect away from a user supplied URL.</p>
        </li>
      </ol>

      <div class="col-indent" style="margin-top:calc(var(--u)*4); border-top:1px solid var(--rule); padding-top:calc(var(--u)*2);">
        <p class="kicker">Current interests</p>
        <p style="margin-top:8px; max-width:64ch;">Agentic systems and autonomous loops, and what happens to authorization when an agent acts on a user&rsquo;s behalf across many services: how delegated identity and least privilege survive an agent that plans its own steps, and where the tool invocation boundary quietly becomes an execution boundary. It is the same question as the day job, from the other direction.</p>
      </div>
    </section>

<section class="sec g" id="method" aria-labelledby="h-method">
      <div class="sec-head">
        <p class="idx">04</p>
        <h2 id="h-method">Method</h2>
        <p class="sec-sub">Reproduced before reported. Private first, public only after the fix.</p>
      </div>

      <div class="col-body prose">
        <p>Nothing is reported from code reading alone. Every finding is reproduced against a running instance first, with a real request and real output, because runtime behaviour routinely makes theoretically vulnerable code unexploitable.</p>
        <p>Reports go to maintainers privately, through GitHub Security Advisories or the project&rsquo;s stated security channel, never a public issue tracker, and nothing is named or mirrored publicly until the maintainer publishes.</p>
      </div>

      <div class="col-aside">
        <p class="kicker">Target layer</p>
        <p style="margin-top:8px; font-size:var(--t-s); line-height:1.55; color:var(--ink-2); max-width:40ch;">The layer underneath the model: agent frameworks, inference servers, workflow orchestrators, vector stores, and the serialization formats they trust. These projects grow quickly, bind to broad interfaces by default, and add execution features faster than they add authorization.</p>
        <p class="kicker" style="margin-top:calc(var(--u)*3);">Focus areas</p>
        <p style="margin-top:8px; font-size:var(--t-s); line-height:1.55; color:var(--ink-2); max-width:40ch;">AI agent security &middot; LLM infrastructure security &middot; agentic systems &middot; autonomous agents &middot; identity and access management &middot; vulnerability research &middot; coordinated disclosure &middot; sandbox escape &middot; unsafe deserialization &middot; server side request forgery</p>
      </div>
    </section>

<section class="sec g" id="record" aria-labelledby="h-record">
      <div class="sec-head">
        <p class="idx">05</p>
        <h2 id="h-record">Record</h2>
        <p class="sec-sub">Roles, degree, certifications and competition results as of September 2026. Dates are YYYY.MM.</p>
      </div>

      <ol class="stream">
        <li>
          <p class="when">2026.06&ndash;<br>present</p>
          <div class="what">
            <h3>Amazon <span>/ Security Engineer</span></h3>
            <p>Identity and access management. Bringing agentic AI into IAM, which is the same question as the independent research from the other direction: what happens to authorization when an agent acts on a user&rsquo;s behalf across many services.</p>
          </div>
          <div class="org-mark org-mark--amazon" aria-hidden="true"></div>
        </li>
        <li>
          <p class="when">2025.08&ndash;<br>2026.05</p>
          <div class="what">
            <h3>Cyber Florida <span>/ Security Researcher</span></h3>
            <p>Florida Center for Cybersecurity, the state&rsquo;s cybersecurity center, hosted at the University of South Florida. Worked in the Cyber Florida SOC. Built agentic systems for open source vulnerability research, automating discovery and triage work that normally has to be done by hand. Also worked on industrial control systems security.</p>
          </div>
          <div class="org-mark org-mark--cyber-florida" aria-hidden="true"></div>
        </li>
        <li>
          <p class="when">2026.05<br>graduated</p>
          <div class="what">
            <h3>University of South Florida <span>/ BSc Computer Science, cybersecurity focus</span></h3>
            <p>Graduated magna cum laude. CyberHerd, USF&rsquo;s cybersecurity competition team; former Blue Team Captain.</p>
          </div>
          <div class="org-mark org-mark--usf" aria-hidden="true"></div>
        </li>
        <li>
          <p class="when">2025.05&ndash;<br>2025.08</p>
          <div class="what">
            <h3>Amazon <span>/ Security Engineer Intern, Red Team</span></h3>
            <p>Built an autonomous agentic system for red team operations, and worked with the Model Context Protocol early in its life, before the tooling and the practice around it had settled. Month boundaries approximate.</p>
          </div>
          <div class="org-mark org-mark--amazon" aria-hidden="true"></div>
        </li>
      </ol>

      <p class="subhead">Certifications</p>
      <ol class="stream" style="margin-top:calc(var(--u)*3)">
        <li>
          <p class="when">2026</p>
          <div class="what">
            <h3>GICSP <span>/ Global Industrial Cyber Security Professional</span></h3>
            <p>GIAC, via SANS ICS410: ICS/SCADA Security Essentials.</p>
          </div>
          <div class="org-mark org-mark--giac" aria-hidden="true"></div>
        </li>
        <li>
          <p class="when">2025</p>
          <div class="what">
            <h3>CBBH <span>/ Certified Bug Bounty Hunter</span></h3>
            <p>Hack The Box.</p>
          </div>
          <div class="org-mark org-mark--htb" aria-hidden="true"></div>
        </li>
      </ol>

      <p class="subhead">Competitions</p>
      <ol class="comps" style="margin-top:calc(var(--u)*3)">
        <li><span class="yr">2026</span><span class="pl">1st</span><span class="ev">AI Village CTF, DEF CON 34</span><span class="nt">Won an NVIDIA DGX Spark</span></li>
        <li><span class="yr">2026</span><span class="pl">2nd</span><span class="ev">Adversary Wars CTF, Adversary Village, DEF CON 34</span><span class="nt">Won a certification</span></li>
        <li><span class="yr">2026</span><span class="pl">1st</span><span class="ev">Corelight CTF, GuidePoint Security</span><span class="nt">Won a PlayStation 5</span></li>
        <li><span class="yr">2026</span><span class="pl">1st</span><span class="ev">Hackabull CTF</span><span class="nt">Won computer accessories</span></li>
        <li><span class="yr">2026</span><span class="pl">2nd</span><span class="ev">Hack The Madness</span><span class="nt">Won swag</span></li>
        <li><span class="yr">2025</span><span class="pl">1st</span><span class="ev">Adversary Wars CTF, Adversary Village, DEF CON 33</span><span class="nt">Won a certification</span></li>
        <li><span class="yr">2025</span><span class="pl">1st</span><span class="ev">Hackabull CTF</span><span class="nt">Won swag and a lockpick set</span></li>
        <li><span class="yr">2025</span><span class="pl">1st</span><span class="ev">Social Engineering Competition, The CARE Lab at Temple University</span><span class="nt">Won a cash prize</span></li>
        <li><span class="yr">2025</span><span class="pl">2nd</span><span class="ev">SHPE National CTF</span><span class="nt">Won a cash prize</span></li>
        <li><span class="yr">2025</span><span class="pl">3rd</span><span class="ev">SecureTheFuture Research Award, Palo Alto Networks</span><span class="nt">Won a cash prize</span></li>
        <li><span class="yr">2025</span><span class="pl">3rd</span><span class="ev">NCAE CyberGames, South East Regionals</span><span class="nt">Won swag</span></li>
        <li><span class="yr">2024</span><span class="pl">1st</span><span class="ev">SHPE National CTF</span><span class="nt">Won $4,500 with the team</span></li>
        <li><span class="yr">2024</span><span class="pl">1st</span><span class="ev">Central Florida Tech Grove CTF</span><span class="nt">Won a cash prize</span></li>
      </ol>
    </section>

<section class="sec g" id="coverage" aria-labelledby="h-coverage">
      <div class="sec-head">
        <p class="idx">06</p>
        <h2 id="h-coverage">Coverage</h2>
        <p class="sec-sub">Third party sources that name him, newest first.</p>
      </div>

      <ol class="coverage">
        <li>
          <span class="src"><b>Cyber Florida</b><time datetime="2026-06-02">2 Jun 2026</time></span>
          <span class="ttl"><a href="https://cyberflorida.org/career-launch-series-from-socap-to-security-engineering/">Career Launch Series: From SOCAP to Security Engineering</a></span>
          <span class="nt">Profile</span>
        </li>
        <li>
          <span class="src"><b>Cyber Florida</b><time datetime="2026-05-20">20 May 2026</time></span>
          <span class="ttl"><a href="https://cyberflorida.org/technical-threat-advisory-cve-2026-45675/">Technical Threat Advisory: CVE-2026-45675</a></span>
          <span class="nt">Credits the CVE discovery</span>
        </li>
        <li>
          <span class="src"><b>University of South Florida</b></span>
          <span class="ttl"><a href="https://www.usf.edu/commencement/documents/spring-2026-commencement-program.pdf">138th Commencement Convocation, Spring 2026</a></span>
          <span class="nt">Degree and honors, page 56</span>
        </li>
        <li>
          <span class="src"><b>USF Bellini College</b><time datetime="2025-11-03">3 Nov 2025</time></span>
          <span class="ttl"><a href="https://www.usf.edu/ai-cybersecurity-computing/news/2025/cyberherd--cyberhawk-ctf.aspx">USF&rsquo;s CyberHerd team dominates in CyberHawk CTF win</a></span>
          
        </li>
        <li>
          <span class="src"><b>USF Bellini College</b><time datetime="2025-08-13">13 Aug 2025</time></span>
          <span class="ttl"><a href="https://www.usf.edu/ai-cybersecurity-computing/news/2025/defcon33.aspx">USF CyberHerd captures first place at world&rsquo;s largest hacker conference</a></span>
          <span class="nt">DEF CON 33</span>
        </li>
        <li>
          <span class="src"><b>USF College of Engineering</b><time datetime="2025-01-08">8 Jan 2025</time></span>
          <span class="ttl"><a href="https://www.usf.edu/engineering/news/2025/usf-cyberherd-wrapped-2024-competitions-story.aspx">USF CyberHerd Team Dominates National Cybersecurity Competitions in 2024</a></span>
          
        </li>
        <li>
          <span class="src"><b>SHPE</b></span>
          <span class="ttl"><a href="https://shpe.org/wp-content/uploads/2025/02/SHPE-NC24-Wrap-Up-Report_v6-lowres-1.pdf">2024 SHPE National Convention Highlights</a></span>
          <span class="nt">Official winners roster, page 9</span>
        </li>
        <li>
          <span class="src"><b>USF College of Engineering</b><time datetime="2024-11-12">12 Nov 2024</time></span>
          <span class="ttl"><a href="https://www.usf.edu/engineering/news/2024/cse/shpe_cyberherd.aspx">CyberHerd Member Leads Team to Victory and a $4,500 Prize at SHPE National Convention</a></span>
          
        </li>
      </ol>
    </section>

<section class="sec g" id="contact" aria-labelledby="h-contact">
      <div class="sec-head">
        <p class="idx">07</p>
        <h2 id="h-contact">Contact</h2>
      </div>

      <ul class="contact">
        <li>
          <span class="lbl">Email</span>
          <a href="mailto:code.sanaan@gmail.com">code.sanaan@gmail.com</a>
        </li>
        <li>
          <span class="lbl">GitHub</span>
          <a href="https://github.com/sfwani">github.com/sfwani</a>
        </li>
        <li>
          <span class="lbl">LinkedIn</span>
          <a href="https://www.linkedin.com/in/sfwani">linkedin.com/in/sfwani</a>
        </li>
        <li>
          <span class="lbl">Advisories</span>
          <a href="https://github.com/sfwani/advisories">github.com/sfwani/advisories</a>
        </li>
      </ul>
    </section>
