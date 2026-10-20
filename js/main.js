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
      <p class="footer__brand">${cfg.bride} <span class="amp">&amp;</span> ${cfg.groom}</p>
      <p>${cfg.dateLabel} · ${cfg.venue}</p>
      ${document.querySelector(".rsvp") ? "" : '<a class="btn" data-rsvp href="#" target="_blank" rel="noopener">Potvrdit účast</a>'}
      <p class="footer__contact">Něco naléhavého v den svatby? <a href="info.html#kontakt">Kontakty na svědky</a></p>`;
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

  // ---------- Invite card: inline the SVG so it uses the site's web font ----------
  // (if you replace pozvanka.svg with a photo/scan of the real invite, this simply does nothing)
  const card = document.querySelector(".env-card");
  if (card && card.getAttribute("src")?.endsWith(".svg")) {
    fetch(card.getAttribute("src"))
      .then((r) => (r.ok ? r.text() : Promise.reject()))
      .then((text) => {
        const svg = new DOMParser().parseFromString(text, "image/svg+xml").documentElement;
        svg.removeAttribute("width");
        svg.removeAttribute("height");
        svg.setAttribute("class", "env-card");
        svg.setAttribute("role", "img");
        svg.setAttribute("aria-label", card.alt);
        card.replaceWith(svg);
      })
      .catch(() => {});
  }

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

  // ---------- Story on phones: show the first paragraph, rest behind "Číst dál" ----------
  document.querySelectorAll(".chapter__text").forEach((text) => {
    if (text.querySelectorAll("p").length < 2) return;
    const more = document.createElement("button");
    more.type = "button";
    more.className = "read-more";
    more.textContent = "Číst dál";
    more.addEventListener("click", () => text.classList.add("is-open"));
    text.append(more);
  });

  // ---------- Quiz helper: add ?kviz to the URL to highlight quiz facts ----------
  if (new URLSearchParams(location.search).has("kviz")) document.body.classList.add("show-quiz");
})();
