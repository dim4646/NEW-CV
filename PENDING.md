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

- [ ] **EWPA Yellow Card** — trained Feb 2021, card lost/stolen; renewal/replacement email sent to EWPA on 2026-11-12 (from Dimos's older email address) — waiting for reply.
      Dimos chose to keep it on the CV without a "renewal" note.

- [ ] **Telegram notifications** — code is ready; add `TELEGRAM_BOT_TOKEN` (secret) and `TELEGRAM_CHAT_ID` in
      Netlify → dimosk → Environment variables, then redeploy. Until then requests arrive by email only.

## Changelog

| Date | Change |
|------|--------|
| 2026-11-12 | Access requests now need Dimos's approval: visitor request → Telegram/email to Dimos with Approve/Reject (confirmation page, 7-day expiry) → on approve the visitor gets the 24-hour link. OWNER_EMAIL set in Netlify. |
| 2026-11-12 | Updated CV sent to AustCorp; EWPA renewal request sent. |
| 2026-11-12 | Skills: "AI & Automation" → "Automation & Scripting" (Python, Automation Scripting, Network Monitoring, GitHub). PDF: three Cisco courses merged into one line (site keeps them separate). |
| 2026-11-12 | Added EWPA Yellow Card (VL, SL, BL) to Licences. No other cards held (no ACMA, Heights, First Aid). |
| 2026-11-12 | Subcontractor role rewritten after discussion: works directly with clients, Gold Coast + Brisbane, offering installation, service and maintenance; on-site fault rectification. |
| 2026-11-12 | Added White Card (General Construction Induction) and Current Driver Licence to Licences (PDF + homepage card). |
| 2026-11-12 | New role: Security Systems Technician (Subcontractor), Self-employed, 2026 – Present (company name intentionally not shown for now). WHITE Main Beach → Epsilon Security, 2016, travelled from Canberra to programme and complete the job (resolves the 2015 vs May 2016 conflict). |
| 2026-11-12 | Single source of truth set up: `data/cv-data.json` + `scripts/` (make_cv, build_site, build_all), markers in both pages, public access blocked for source files. Output verified identical to the live site and PDF. |
| 2026-11-12 | WHITE Main Beach → "Epsilon Security, 2015". |
| 2026-11-12 | CV review fixes: Education added to PDF, ICT ProtegeWX dates (Dec 2025 – Dec 2027), Hanwha Cybersecurity date (Jun 2026), "2023–Jun 2026" instead of "present", "Cisco/Fortinet Trained" badges, Google cert year, Ubiquiti only under Networking, footer © 2026, consistent date dashes. |
| 2026-10-20 | Award/validity dates added to ICT ProtegeWX and Hanwha Cybersecurity (site only — PDF was not updated at the time; this is what single source prevents). |
