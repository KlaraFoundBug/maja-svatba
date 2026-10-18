(() => {
  const cfg = window.WEDDING || {};
  const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));

  // ---------- RSVP links ----------
  document.querySelectorAll("[data-rsvp]").forEach((a) => (a.href = cfg.rsvpUrl || "#"));

  // ---------- Nav: solid on scroll + mobile menu ----------
  const nav = document.querySelector("[data-nav]");
  const burger = document.querySelector("[data-burger]");
  const setMenu = (open) => {
    nav.classList.toggle("is-open", open);
    burger.setAttribute("aria-expanded", String(open));
    burger.setAttribute("aria-label", open ? "Zavřít menu" : "Otevřít menu");
    document.body.style.overflow = open ? "hidden" : "";
  };
  burger?.addEventListener("click", () => setMenu(!nav.classList.contains("is-open")));
  nav?.querySelectorAll("[data-overlay] a").forEach((a) => a.addEventListener("click", () => setMenu(false)));
  document.addEventListener("keydown", (e) => e.key === "Escape" && setMenu(false));

  // ---------- Reveal on scroll ----------
  const io = new IntersectionObserver(
    (entries) => entries.forEach((e) => e.isIntersecting && (e.target.classList.add("is-visible"), io.unobserve(e.target))),
    { threshold: 0, rootMargin: "0px 0px -12% 0px" }
  );
  document.querySelectorAll(".reveal").forEach((el) => io.observe(el));

  // ---------- Envelope scroll animation ----------
  const stage = document.querySelector("[data-envelope-stage]");
  const scene = document.querySelector("[data-env-scene]");
  const flap = document.querySelector("[data-env-flap]");
  const caption = document.querySelector("[data-env-caption]");
  const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const ease = (t) => 1 - Math.pow(1 - t, 3);

  function updateEnvelope() {
    if (!stage || reduced) return;
    const rect = stage.getBoundingClientRect();
    const total = rect.height - innerHeight;
    const p = clamp(-rect.top / total);
    // 0–0.25 flap opens · 0.3–0.8 card slides out · rest = hold
    const open = ease(clamp(p / 0.25));
    const slide = ease(clamp((p - 0.3) / 0.5));
    scene.style.setProperty("--open", open.toFixed(4));
    scene.style.setProperty("--slide", slide.toFixed(4));
    flap.classList.toggle("is-behind", open > 0.5);
    caption.style.opacity = String(1 - clamp(p / 0.2));
  }

  function onScroll() {
    nav?.classList.toggle("is-solid", scrollY > 40);
    updateEnvelope();
  }
  addEventListener("scroll", onScroll, { passive: true });
  addEventListener("resize", onScroll);
  onScroll();

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

  // ---------- Cross-page anchors (pribeh.html#info): re-jump once fonts/images settle ----------
  if (location.hash) {
    addEventListener("load", () => {
      const target = document.getElementById(decodeURIComponent(location.hash.slice(1)));
      target?.scrollIntoView({ behavior: "instant" });
    });
  }

  // ---------- Quiz helper: add ?kviz to the URL to highlight quiz facts ----------
  if (new URLSearchParams(location.search).has("kviz")) document.body.classList.add("show-quiz");
})();
