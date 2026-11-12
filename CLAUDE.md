# NEW-CV — Dimos Kallionakis portfolio + CV

- Live site: https://dimosk.netlify.app (auto-deploys from `main`)
- **Start of session:** read `PENDING.md` and mention any open items to Dimos.
- **All CV content lives in `data/cv-data.json`.** Never edit the generated regions
  (`<!-- cv:… -->` … `<!-- /cv:… -->`) in `index.html` or `protected/full-profile.html` by hand.
- After any change: `python3 scripts/build_all.py` → check PDF (2 pages) + both pages →
  update `PENDING.md` (open items + changelog) → commit → push to `main`.
- When a fact changes, update both `web` and `pdf` variants in the JSON if present.
- Phone, email and full licence number only appear in `protected/` (behind the access gate) and in the
  blocked `data/` folder — never on the public `index.html`.
- Talk to Dimos in Greek; CV/site content is in English.
