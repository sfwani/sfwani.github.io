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
    try { localStorage.setItem("theme", next); } catch (e) {}
    body.setAttribute("data-theme", next);
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
