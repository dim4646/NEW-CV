# PENDING — open items & changelog

> **Read this file at the start of every session. Update it at the end of every session.**

## Workflow (every change)

1. Edit **only** `data/cv-data.json`
2. Run `python3 scripts/build_all.py` (needs `pip install reportlab`)
3. Check: PDF is 2 pages and reads correctly · `index.html` · `protected/full-profile.html`
4. Update this file (open items + changelog)
5. Commit and push to `main` → Netlify deploys automatically

Notes:
- Never edit text between `<!-- cv:… -->` and `<!-- /cv:… -->` markers by hand; it is overwritten on every build.
  Design/CSS/scripts outside the markers can be edited normally.
- Where the site and the PDF need different wording, the JSON holds `{"web": …, "pdf": …}`.
  Experience bullets and the summary have two versions on purpose (detailed for the site, concise for the PDF):
  **when a fact changes, update both versions.**
- Certification count on the site is calculated automatically (training "in progress" is not counted).
- `data/`, `scripts/`, `PENDING.md`, `CLAUDE.md` are blocked from public access in `netlify.toml`.

## Open items

- [ ] **Epsilon Security start date** — WHITE Main Beach project is "Epsilon Security, 2015", but the
      "Security Service Technician" role starts "May 2016". Confirm with Dimos whether the role should start in 2015.
- [ ] **Experience gap Jun 2026 → today** — decide whether to add current activity (e.g. own business) to the CV.

## Changelog

| Date | Change |
|------|--------|
| 2026-11-12 | Single source of truth set up: `data/cv-data.json` + `scripts/` (make_cv, build_site, build_all), markers in both pages, public access blocked for source files. Output verified identical to the live site and PDF. |
| 2026-11-12 | WHITE Main Beach → "Epsilon Security, 2015". |
| 2026-11-12 | CV review fixes: Education added to PDF, ICT ProtegeWX dates (Dec 2025 – Dec 2027), Hanwha Cybersecurity date (Jun 2026), "2023–Jun 2026" instead of "present", "Cisco/Fortinet Trained" badges, Google cert year, Ubiquiti only under Networking, footer © 2026, consistent date dashes. |
| 2026-10-20 | Award/validity dates added to ICT ProtegeWX and Hanwha Cybersecurity (site only — PDF was not updated at the time; this is what single source prevents). |
