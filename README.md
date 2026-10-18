# Mája & Míša – svatební web

Static site (plain HTML/CSS/JS, no build step). Four pages:

| Page | File |
| --- | --- |
| Úvod – names, envelope animation, countdown, RSVP | `index.html` |
| Program + venue map | `program.html` |
| Náš příběh – story chapters, quiz facts, photos | `pribeh.html` |
| Informace – colours, flowers, dress code, practical info | `info.html` |

## Run locally

```bash
python3 -m http.server 8080
```

Then open http://localhost:8080

## Where to change things

| What | Where |
| --- | --- |
| Names, date (countdown), venue, Google Form link | `js/config.js` |
| Menu, header, footer (shared by all pages) | `js/main.js` (top) |
| Colours | CSS variables at the top of `css/style.css` |
| Map location | `program.html` → `<iframe>` `q=` parameter and the "Navigovat" link |
| Invite in the envelope | replace `img/pozvanka.svg` with a photo/scan of the real invite (portrait, ~5:7) and update `src` in `index.html` |

## Photos

All photos are placeholders hot-linked from Unsplash (free license). Replace the
`src` URLs with your own files (e.g. put them in `img/` and use `img/name.jpg`).

## Quiz facts

Facts for the wedding quiz are wrapped in `<span data-quiz="N">` in `pribeh.html`.
Guests don't see them; open `pribeh.html?kviz` to highlight and number them.
Real so far: Coca-Cola, cat Queen, padel. Everything else is dummy text.
