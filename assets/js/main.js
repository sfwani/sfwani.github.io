(() => {
  // Theme switch
  const body = document.body;
  const lamp = document.getElementById("mode");

  const toggleTheme = () => {
    // Effective theme: an explicit attribute if present, else what the OS says.
    const current =
      body.getAttribute("data-theme") ||
      (window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
    const next = current === "dark" ? "light" : "dark";
    const commit = () => {
      try { localStorage.setItem("theme", next); } catch (e) {}
      body.setAttribute("data-theme", next);
    };
    // M5d. The switch was a hard cut of the whole viewport. A View Transition
    // crossfades it in 200ms. The site-wide reduced-motion block cannot reach
    // the view-transition pseudo tree, so the guard has to be here too.
    if (!document.startViewTransition ||
        window.matchMedia("(prefers-reduced-motion: reduce)").matches) return commit();
    document.startViewTransition(commit);
  };

  if (lamp) lamp.addEventListener("click", toggleTheme);

  // Blur the content when the menu is open
  const cbox = document.getElementById("menu-trigger");

  cbox.addEventListener("change", function () {
    const area = document.querySelector(".wrapper");
    this.checked
      ? area.classList.add("blurry")
      : area.classList.remove("blurry");
  });
})();

/* P1  Margin measure rail */
(function () {
  var main = document.querySelector("main.page-content");
  if (!main) return;
  var hs = main.querySelectorAll("h2[id]");
  if (hs.length < 3) return;

  var rail = document.createElement("nav");
  rail.className = "fm-rail";
  rail.setAttribute("aria-label", "Sections");
  rail.innerHTML =
    '<span class="fm-rail__spine" aria-hidden="true"></span>' +
    '<span class="fm-rail__cursor" aria-hidden="true"></span>';

  var items = [];
  Array.prototype.forEach.call(hs, function (h, i) {
    var a = document.createElement("a");
    a.className = "fm-rail__tick";
    a.href = "#" + h.id;
    a.style.setProperty("--i", i);
    a.innerHTML =
      '<span class="fm-rail__num">' + (i < 9 ? "0" : "") + (i + 1) + "</span>" +
      '<span class="fm-rail__label"></span>';
    a.querySelector(".fm-rail__label").textContent = h.textContent.trim();
    rail.appendChild(a);
    items.push({ h: h, a: a, y: 0 });
  });
  document.body.appendChild(rail);

  var PAD = 72;           /* html{scroll-padding-top:4rem} plus a line */
  var current = -1, queued = false;

  function place() {
    var span = document.documentElement.scrollHeight - window.innerHeight;
    if (span < 320) { rail.hidden = true; return; }
    rail.hidden = false;
    for (var i = 0; i < items.length; i++) {
      items[i].y = items[i].h.getBoundingClientRect().top + window.pageYOffset - PAD;
      var f = Math.max(0, Math.min(1, items[i].y / span));
      items[i].a.style.setProperty("--t", (f * 100).toFixed(3) + "%");
    }
    mark();
  }
  function mark() {
    queued = false;
    var y = window.pageYOffset, n = -1;
    for (var i = 0; i < items.length; i++) if (items[i].y <= y + 2) n = i;
    if (n === current) return;
    if (current > -1) items[current].a.classList.remove("is-current");
    if (n > -1) items[n].a.classList.add("is-current");
    current = n;
  }
  function onScroll() { if (!queued) { queued = true; requestAnimationFrame(mark); } }

  place();
  addEventListener("load", place);
  addEventListener("resize", place, { passive: true });
  addEventListener("scroll", onScroll, { passive: true });
})();
