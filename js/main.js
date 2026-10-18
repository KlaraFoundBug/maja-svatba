(() => {
  const cfg = {
    bride: "", groom: "", date: "", dateLabel: "", venue: "", place: "", rsvpUrl: "#",
    ...window.WEDDING,
  };
  const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
  const page = document.body.dataset.page;

  // ---------- Shared header + footer (edit menu here, once for all pages) ----------
  const links = [
    ["index", "index.html", "Úvod"],
    ["program", "program.html", "Program"],
    ["misto", "misto.html", "Místo"],
    ["pribeh", "pribeh.html", "Náš příběh"],
    ["info", "info.html", "Informace"],
  ];
  const navItems = links
    .map(([id, href, label]) => `<li><a href="${href}"${id === page ? ' aria-current="page"' : ""}>${label}</a></li>`)
    .join("");

  const header = document.querySelector("[data-masthead]");
  if (header) {
    header.className = "masthead";
    header.innerHTML = `
      <div class="masthead__top smallcaps">
        <span>${cfg.dateLabel}</span>
        <span class="hide-sm">${cfg.place}</span>
      </div>
      <nav class="nav" aria-label="Hlavní navigace" data-nav>
        <button class="nav__burger" aria-expanded="false" aria-controls="nav-list" data-burger><i></i>Menu</button>
        <ul class="nav__list" id="nav-list">
          ${navItems}
          <li><a class="nav__rsvp" data-rsvp href="#" target="_blank" rel="noopener">Potvrdit účast</a></li>
        </ul>
      </nav>`;
  }

  const footer = document.querySelector("[data-footer]");
  if (footer) {
    footer.className = "footer";
    footer.innerHTML = `
      <img class="footer__flowers" src="img/flowers/flowers-garland.webp" alt="" aria-hidden="true">
      <p class="footer__brand">${cfg.bride} <span class="amp">&amp;</span> ${cfg.groom}</p>
      <p>${cfg.dateLabel} · ${cfg.venue}</p>`;
  }

  // ---------- Flower corners on inner pages (desktop; hidden on phones/tablets via CSS) ----------
  if (page !== "index") {
    const corners = document.createElement("div");
    corners.className = "page-corners";
    corners.setAttribute("aria-hidden", "true");
    corners.innerHTML = `
      <img class="page-corners__l" src="img/flowers/flowers-corner.webp" alt="">
      <img class="page-corners__r" src="img/flowers/flowers-corner.webp" alt="">`;
    document.body.prepend(corners);
    const placeCorners = () => (corners.style.top = `${header?.offsetHeight ?? 0}px`);
    addEventListener("resize", placeCorners);
    placeCorners();
  }

  // ---------- RSVP links ----------
  document.querySelectorAll("[data-rsvp]").forEach((a) => (a.href = cfg.rsvpUrl));

  // ---------- Mobile menu ----------
  const nav = document.querySelector("[data-nav]");
  const burger = document.querySelector("[data-burger]");
  const setMenu = (open) => {
    nav.classList.toggle("is-open", open);
    burger.setAttribute("aria-expanded", String(open));
  };
  burger?.addEventListener("click", () => setMenu(!nav.classList.contains("is-open")));
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && nav?.classList.contains("is-open")) {
      setMenu(false);
      burger.focus();
    }
  });

  // ---------- Envelope scroll animation ----------
  // Scroll sets a target; each frame eases the drawn progress toward it (smooth, Apple-style).
  const stage = document.querySelector("[data-envelope-stage]");
  if (stage && !matchMedia("(prefers-reduced-motion: reduce)").matches) {
    const scene = stage.querySelector("[data-env-scene]");
    const flap = stage.querySelector("[data-env-flap]");
    const smooth = (t) => t * t * (3 - 2 * t); // smoothstep
    let target = 0;
    let current = 0;
    let frame = 0;

    const draw = () => {
      current += (target - current) * 0.12;
      if (Math.abs(target - current) < 0.0005) current = target;
      // 0–0.3 seal breaks & flap opens · 0.3–0.85 invite slides out · rest = hold
      const open = smooth(clamp(current / 0.3));
      const slide = smooth(clamp((current - 0.3) / 0.55));
      scene.style.setProperty("--open", open.toFixed(4));
      scene.style.setProperty("--slide", slide.toFixed(4));
      flap.classList.toggle("is-behind", open > 0.5);
      frame = current === target ? 0 : requestAnimationFrame(draw);
    };
    const onScroll = () => {
      const rect = stage.getBoundingClientRect();
      // starts while the envelope is still entering the screen (top at 75% of the viewport)
      const lead = innerHeight * 0.75;
      target = clamp((lead - rect.top) / (rect.height - innerHeight + lead));
      if (!frame) frame = requestAnimationFrame(draw);
    };
    addEventListener("scroll", onScroll, { passive: true });
    addEventListener("resize", onScroll);
    onScroll();
  }

  // ---------- Countdown ----------
  const cd = document.querySelector("[data-countdown]");
  if (cd && cfg.date) {
    const target = new Date(cfg.date).getTime();
    const out = {};
    cd.querySelectorAll("[data-cd]").forEach((el) => (out[el.dataset.cd] = el));
    let timer = 0;
    const tick = () => {
      let s = Math.floor((target - Date.now()) / 1000);
      if (s <= 0) {
        // the big day has come – swap the countdown for a short line
        clearInterval(timer);
        cd.closest(".countdown").innerHTML = `<span class="smallcaps kicker">${cfg.dateLabel}</span><p class="countdown__done">Řekli jsme si ano!</p>`;
        return false;
      }
      const d = Math.floor(s / 86400); s %= 86400;
      const h = Math.floor(s / 3600); s %= 3600;
      const m = Math.floor(s / 60); s %= 60;
      out.days.textContent = d;
      out.hours.textContent = String(h).padStart(2, "0");
      out.minutes.textContent = String(m).padStart(2, "0");
      out.seconds.textContent = String(s).padStart(2, "0");
    };
    if (tick() !== false) timer = setInterval(tick, 1000);
  }

  // ---------- Quiz helper: add ?kviz to the URL to highlight quiz facts ----------
  if (new URLSearchParams(location.search).has("kviz")) document.body.classList.add("show-quiz");
})();
