(() => {
  const cfg = window.WEDDING || {};
  const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
  const page = document.body.dataset.page;

  // ---------- Shared header + footer (edit menu here, once for all pages) ----------
  const links = [
    ["index", "index.html", "Úvod"],
    ["program", "program.html", "Program"],
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
        <span class="hide-sm">${cfg.dateLabel}</span>
        <span>${cfg.place}</span>
        <span class="hide-sm">Svatební listy · No. 1</span>
      </div>
      <a class="masthead__brand" href="index.html">${cfg.bride} <span class="amp">&amp;</span> ${cfg.groom}</a>
      <nav class="nav" aria-label="Hlavní navigace" data-nav>
        <button class="nav__burger" aria-expanded="false" data-burger><i></i>Menu</button>
        <ul class="nav__list">
          ${navItems}
          <li><a class="nav__rsvp" data-rsvp href="#" target="_blank" rel="noopener">Potvrdit účast</a></li>
        </ul>
      </nav>`;
  }

  const footer = document.querySelector("[data-footer]");
  if (footer) {
    footer.className = "footer";
    footer.innerHTML = `
      <p class="footer__brand">${cfg.bride} <span class="amp">&amp;</span> ${cfg.groom}</p>
      <p>${cfg.dateLabel} · ${cfg.venue}</p>
      <ul class="footer__links">${navItems}</ul>`;
  }

  // ---------- RSVP links ----------
  document.querySelectorAll("[data-rsvp]").forEach((a) => (a.href = cfg.rsvpUrl || "#"));

  // ---------- Mobile menu ----------
  const nav = document.querySelector("[data-nav]");
  const burger = document.querySelector("[data-burger]");
  burger?.addEventListener("click", () => {
    const open = !nav.classList.contains("is-open");
    nav.classList.toggle("is-open", open);
    burger.setAttribute("aria-expanded", String(open));
  });

  // ---------- Envelope scroll animation ----------
  const stage = document.querySelector("[data-envelope-stage]");
  if (stage && !matchMedia("(prefers-reduced-motion: reduce)").matches) {
    const scene = stage.querySelector("[data-env-scene]");
    const flap = stage.querySelector("[data-env-flap]");
    const caption = stage.querySelector("[data-env-caption]");
    const ease = (t) => (t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2);
    const update = () => {
      const rect = stage.getBoundingClientRect();
      const p = clamp(-rect.top / (rect.height - innerHeight));
      // 0.05–0.3 seal breaks & flap opens · 0.35–0.8 invite slides out · rest = hold
      const open = ease(clamp((p - 0.05) / 0.25));
      const slide = ease(clamp((p - 0.35) / 0.45));
      scene.style.setProperty("--open", open.toFixed(4));
      scene.style.setProperty("--slide", slide.toFixed(4));
      flap.classList.toggle("is-behind", open > 0.5);
      caption.style.opacity = String(1 - clamp(p / 0.15));
    };
    addEventListener("scroll", update, { passive: true });
    addEventListener("resize", update);
    update();
  }

  // ---------- Countdown ----------
  const cd = document.querySelector("[data-countdown]");
  if (cd && cfg.date) {
    const target = new Date(cfg.date).getTime();
    const out = {};
    cd.querySelectorAll("[data-cd]").forEach((el) => (out[el.dataset.cd] = el));
    const tick = () => {
      let s = Math.max(0, Math.floor((target - Date.now()) / 1000));
      const d = Math.floor(s / 86400); s %= 86400;
      const h = Math.floor(s / 3600); s %= 3600;
      const m = Math.floor(s / 60); s %= 60;
      out.days.textContent = d;
      out.hours.textContent = String(h).padStart(2, "0");
      out.minutes.textContent = String(m).padStart(2, "0");
      out.seconds.textContent = String(s).padStart(2, "0");
    };
    tick();
    setInterval(tick, 1000);
  }

  // ---------- Quiz helper: add ?kviz to the URL to highlight quiz facts ----------
  if (new URLSearchParams(location.search).has("kviz")) document.body.classList.add("show-quiz");
})();
