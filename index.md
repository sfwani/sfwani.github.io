---
layout: c2
title: Sanaan Fayaz Wani
heading: Sanaan Fayaz Wani
seo_title: "Sanaan Fayaz Wani - Security Engineer and vulnerability researcher"
role: "Security Engineer at Amazon, bringing agentic AI into identity and access management. Independent vulnerability research across open source infrastructure."
description: Vulnerability research on AI agent frameworks and LLM infrastructure. Assigned CVEs and published, credited advisories, each with root cause, reproduction and fix.
permalink: /
last_modified_at: 2026-11-20T15:43:31+00:00
---

<div class="figs-lead g">
<!-- COUNTERS:START -->

      <ul class="figs">
        <li class="fig"><b>12</b><span>CVEs assigned</span></li>
        <li class="fig"><b>29</b><span>Advisories published</span></li>
        <li class="fig"><b>19</b><span>Projects credited</span></li>
        <li class="fig"><b>167</b><span>Reports filed</span></li>
        <li class="fig"><b>59</b><span>Projects audited</span></li>
      </ul>

<!-- COUNTERS:END -->
</div>

<section class="sec g" id="profile" aria-labelledby="h-profile">
      <div class="sec-head">
        <div class="sec-title">
          <p class="idx">01</p>
          <h2 id="h-profile">Profile</h2>
        </div>
        <p class="sec-sub">Amazon, Cyber Florida, University of South Florida. Independent vulnerability research separately.</p>
      </div>

      <div class="col-body prose">
        <p>Sanaan Fayaz Wani is a Security Engineer at Amazon, working in IAM security on bringing agentic AI into identity and access management. Outside that, he hunts unauthenticated remote code execution in the infrastructure that runs large language models: agent frameworks, inference servers, workflow orchestrators, and the serialization formats they trust.</p>
        <p>Before Amazon he was a security researcher at Cyber Florida, building agentic systems for open source vulnerability research and working on industrial control system security. The summer before that he was on Amazon&rsquo;s red team, building an autonomous system for red teaming and tooling against Model Context Protocol servers while the protocol was still new. He graduated magna cum laude in computer science from the University of South Florida in May 2026, where he competed with the CyberHerd team.</p>
      </div>

      <div class="col-aside">
        <p class="kicker">Disclosure</p>
        <p style="margin-top:8px; font-size:var(--t-s); line-height:1.55; color:var(--ink-2); max-width:40ch;">The work listed here is coordinated disclosure. Every finding is reported privately to the maintainer first, and nothing is named, listed or hinted at until the maintainer publishes it. What that leaves is a record anyone can check: each entry resolves to an advisory the maintainer published and credited.</p>
      </div>
    </section>

<section class="sec g" id="advisories" aria-labelledby="h-adv">
      <div class="sec-head">
        <div class="sec-title">
          <p class="idx">02</p>
          <h2 id="h-adv">Advisories</h2>
        </div>
        <p class="sec-sub">A selection of the published advisories, chosen for technical depth and
          severity. Every entry is published and credited. The full record, each entry with its base
          vector and writeup, is on the <a href="/advisories/">advisories page</a>.</p>
      </div>
<!-- ADVISORIES:START -->

      <div class="cards">
        <a class="card" data-sev="critical" href="/advisories/cve-2026-130169/"><div class="card-top"><span class="card-score">10.0</span><span class="card-sev">Critical</span></div><div class="card-proj">autogpt-platform-beta</div><p class="card-hook"></p><div class="card-foot"><span class="card-cls">Authentication bypass</span><span class="card-cwe">CWE-287</span><span class="k-cve">CVE</span></div></a>
        <a class="card" data-sev="critical" href="/advisories/ghsa-42mf-vpmr-gw5r/"><div class="card-top"><span class="card-score">9.9</span><span class="card-sev">Critical</span></div><div class="card-proj">ag2</div><p class="card-hook">Command Filter Bypass in LocalShellEnvironment via shell=True Allows Arbitrary OS Command Execution</p><div class="card-foot"><span class="card-cls">Command injection</span><span class="card-cwe">CWE-78</span><span class="k-ghsa">GHSA</span></div></a>
        <a class="card" data-sev="high" href="/advisories/ghsa-jmr9-98g4-2phv/"><div class="card-top"><span class="card-score">8.7</span><span class="card-sev">High</span></div><div class="card-proj">github.com/portainer/portainer</div><p class="card-hook">Non-admin bind-mount restriction bypass via Docker local-driver volumes and automatic Git redeploy (incomplete fix of CVE-2026-44849 and CVE-2026-44850)</p><div class="card-foot"><span class="card-cls">Access control</span><span class="card-cwe">CWE-284</span><span class="k-ghsa">GHSA</span></div></a>
        <a class="card" data-sev="critical" href="/advisories/cve-2026-49950/"><div class="card-top"><span class="card-score">9.3</span><span class="card-sev">Critical</span></div><div class="card-proj">xinference</div><p class="card-hook">Unauthenticated remote code execution through the Xinference actor transport</p><div class="card-foot"><span class="card-cls">Missing authentication</span><span class="card-cwe">CWE-306</span><span class="k-cve">CVE</span></div></a>
        <a class="card" data-sev="high" href="/advisories/cve-2026-57516/"><div class="card-top"><span class="card-score">8.8</span><span class="card-sev">High</span></div><div class="card-proj">ray</div><p class="card-hook">Arbitrary code execution via ray.data.read_webdataset default decoder: pickle.loads(value) and torch.load(weights_only=False)</p><div class="card-foot"><span class="card-cls">Code injection</span><span class="card-cwe">CWE-94</span><span class="k-cve">CVE</span></div></a>
        <a class="card" data-sev="high" href="/advisories/ghsa-5mc6-2qfj-59cg/"><div class="card-top"><span class="card-score">8.8</span><span class="card-sev">High</span></div><div class="card-proj">opik</div><p class="card-hook">Opik SDKs render Jinja2/Nunjucks prompt templates without a sandbox, allowing code execution</p><div class="card-foot"><span class="card-cls">Code injection</span><span class="card-cwe">CWE-94</span><span class="k-ghsa">GHSA</span></div></a>
        <a class="card" data-sev="high" href="/advisories/cve-2026-45675/"><div class="card-top"><span class="card-score">8.1</span><span class="card-sev">High</span></div><div class="card-proj">open-webui</div><p class="card-hook">LDAP and OAuth First-User Race Condition Allows Multiple Admin Accounts</p><div class="card-foot"><span class="card-cls">Privilege escalation</span><span class="card-cwe">CWE-269</span><span class="k-cve">CVE</span></div></a>
        <a class="card" data-sev="high" href="/advisories/ghsa-hxvp-ff3g-qcj7/"><div class="card-top"><span class="card-score">8.8</span><span class="card-sev">High</span></div><div class="card-proj">@vendure/core</div><p class="card-hook">Low-privilege administrator can read password-reset / verification / email-change tokens from Job.data and take over any customer account (cross-channel)</p><div class="card-foot"><span class="card-cls">Information disclosure</span><span class="card-cwe">CWE-200</span><span class="k-ghsa">GHSA</span></div></a>
        <a class="card card--all" href="/advisories/"><div class="all-top"><span class="all-n">29</span><span class="all-tag">Record</span></div><div class="all-title">The full record</div><div class="all-s">Every published advisory, each with its CVSS base vector, weakness class and writeup.</div><span class="all-go">Browse all advisories &rarr;</span></a>
      </div>

<!-- ADVISORIES:END -->
    </section>

<section class="sec g" id="classes" aria-labelledby="h-classes">
      <div class="sec-head">
        <div class="sec-title">
          <p class="idx">03</p>
          <h2 id="h-classes">Weakness classes</h2>
        </div>
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
        <div class="sec-title">
          <p class="idx">04</p>
          <h2 id="h-method">Method</h2>
        </div>
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
        <div class="sec-title">
          <p class="idx">05</p>
          <h2 id="h-record">Record</h2>
        </div>
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
          <p class="when">2026.05<br>graduated</p>
          <div class="what">
            <h3>University of South Florida <span>/ BSc Computer Science, cybersecurity focus</span></h3>
            <p>Graduated magna cum laude. CyberHerd, USF&rsquo;s cybersecurity competition team; former Blue Team Captain.</p>
          </div>
          <div class="org-mark org-mark--usf" aria-hidden="true"></div>
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
          <p class="when">2025.05&ndash;<br>2025.08</p>
          <div class="what">
            <h3>Amazon <span>/ Security Engineer Intern, Red Team</span></h3>
            <p>Built an autonomous agentic system for red team operations, and worked with the Model Context Protocol early in its life, before the tooling and the practice around it had settled.</p>
          </div>
          <div class="org-mark org-mark--amazon" aria-hidden="true"></div>
        </li>
      </ol>

      <h3 class="subhead">Certifications</h3>
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

      <h3 class="subhead">Competitions</h3>
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
        <li><span class="yr">2025</span><span class="pl">2nd</span><span class="ev">CPTC Southeast Regionals</span><span class="nt">Won a heartbreak</span></li>
        <li><span class="yr">2025</span><span class="pl">3rd</span><span class="ev">SecureTheFuture Research Award, Palo Alto Networks</span><span class="nt">Won a cash prize</span></li>
        <li><span class="yr">2025</span><span class="pl">3rd</span><span class="ev">NCAE CyberGames, South East Regionals</span><span class="nt">Won swag</span></li>
        <li><span class="yr">2024</span><span class="pl">1st</span><span class="ev">SHPE National CTF</span><span class="nt">Won a cash prize</span></li>
        <li><span class="yr">2024</span><span class="pl">1st</span><span class="ev">Central Florida Tech Grove CTF</span><span class="nt">Won a cash prize</span></li>
      </ol>
    </section>

<section class="sec g" id="coverage" aria-labelledby="h-coverage">
      <div class="sec-head">
        <div class="sec-title">
          <p class="idx">06</p>
          <h2 id="h-coverage">Coverage</h2>
        </div>
        <p class="sec-sub">Third party sources that name him, newest first.</p>
      </div>

      <ol class="coverage">
        <li>
          <span class="src"><b>Cyber Florida</b><time datetime="2026-06-02">2 Jun 2026</time></span>
          <span class="ttl"><a href="https://cyberflorida.org/career-launch-series-from-socap-to-security-engineering/">Career Launch Series: From SOCAP to Security Engineering</a></span>
          <span class="nt">Work shout out</span>
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
          <span class="nt">College shout out</span>
        </li>
        <li>
          <span class="src"><b>USF Bellini College</b><time datetime="2025-08-13">13 Aug 2025</time></span>
          <span class="ttl"><a href="https://www.usf.edu/ai-cybersecurity-computing/news/2025/defcon33.aspx">USF CyberHerd captures first place at world&rsquo;s largest hacker conference</a></span>
          <span class="nt">College shout out</span>
        </li>
        <li>
          <span class="src"><b>USF College of Engineering</b><time datetime="2025-01-08">8 Jan 2025</time></span>
          <span class="ttl"><a href="https://www.usf.edu/engineering/news/2025/usf-cyberherd-wrapped-2024-competitions-story.aspx">USF CyberHerd Team Dominates National Cybersecurity Competitions in 2024</a></span>
          <span class="nt">College shout out</span>
        </li>
        <li>
          <span class="src"><b>SHPE</b></span>
          <span class="ttl"><a href="https://shpe.org/wp-content/uploads/2025/02/SHPE-NC24-Wrap-Up-Report_v6-lowres-1.pdf">2024 SHPE National Convention Highlights</a></span>
          <span class="nt">Official winners roster, page 9</span>
        </li>
        <li>
          <span class="src"><b>USF College of Engineering</b><time datetime="2024-11-12">12 Nov 2024</time></span>
          <span class="ttl"><a href="https://www.usf.edu/engineering/news/2024/cse/shpe_cyberherd.aspx">CyberHerd Member Leads Team to Victory and a $4,500 Prize at SHPE National Convention</a></span>
          <span class="nt">College shout out</span>
        </li>
      </ol>
    </section>

<section class="sec g" id="contact" aria-labelledby="h-contact">
      <div class="sec-head">
        <div class="sec-title">
          <p class="idx">07</p>
          <h2 id="h-contact">Contact</h2>
        </div>
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
