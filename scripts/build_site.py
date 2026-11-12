"""Regenerate the content regions of index.html and protected/full-profile.html from data/cv-data.json.

Only the text between <!-- cv:NAME ... --> and <!-- /cv:NAME --> markers is rewritten.
Everything else (CSS, layout, scripts, access overlay, Netlify functions) is left untouched.
Usage: python3 scripts/build_site.py [--check]   (--check: report differences, write nothing)
"""
import datetime
import re
import sys

import cvdata
from cvdata import pick, pick_list

T = "web"


def esc(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def rich(text):
    """Escape text and turn [text](url) into links."""
    out, pos = [], 0
    for m in cvdata.LINK_RE.finditer(text):
        out.append(esc(text[pos:m.start()]))
        out.append(f'<a href="{m.group(2)}" target="_blank" rel="noopener">{esc(m.group(1))}</a>')
        pos = m.end()
    out.append(esc(text[pos:]))
    return "".join(out)


def ind(n, lines):
    return [(" " * n + l) if l else l for l in lines]


def linkedin_a(c):
    return f'<a href="{c["linkedin_url"]}" target="_blank" rel="noopener">{esc(pick(c["linkedin_display"], T))}</a>'


# ---------------- index.html regions ----------------

def r_hero(d):
    h, p = d["hero"], d["person"]
    out = [f'<div class="hero-tag">{esc(h["tag"])}</div>',
           f'<h1>{esc(p["first_name"])}<br><span>{esc(p["last_name"])}</span></h1>',
           f'<p class="hero-sub">{esc(h["sub"])}</p>',
           '<div class="hero-badges">']
    out += [f'  <span class="badge">{esc(b)}</span>' for b in h["badges"]]
    out += ['</div>']
    return ind(6, out)


def r_hero_contact(d):
    c = d["contact"]
    langs = " &amp; ".join(esc(l["name"]) for l in sorted(d["languages"], key=lambda l: l["name"] != "English"))
    out = [
        '<div class="contact-row">', '  <div class="contact-icon">📍</div>', f'  <div>{"<br>".join(esc(x) for x in c["location_lines"])}</div>', '</div>',
        '<div class="contact-row">', '  <div class="contact-icon">🔗</div>', f'  <div>{linkedin_a(c)}</div>', '</div>',
        '<div class="contact-row">', '  <div class="contact-icon">🌐</div>', f'  <div>{langs}</div>', '</div>',
        '<div class="contact-row">', '  <div class="contact-icon">🔒</div>', '  <div><a href="#" class="request-access-trigger">Phone &amp; email — request access</a></div>', '</div>',
        '<div style="border-top:1px solid rgba(201,168,76,.25);margin:1rem 0 .75rem;"></div>',
        '<div style="font-size:.72rem;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--gold-light);margin-bottom:.6rem;">' + ("Licences" if len(d["licences"]) > 1 else "Licence") + '</div>',
    ]
    for lic in d["licences"]:
        sub = cvdata.licence_web(lic)
        out += ['<div class="contact-row">', '  <div class="contact-icon">🪪</div>', '  <div style="font-size:.85rem;">',
                f'    <div style="font-weight:600;color:rgba(255,255,255,.9);">{esc(lic["name"])}</div>']
        if sub:
            out.append(f'    <div style="color:rgba(255,255,255,.55);font-size:.78rem;">{esc(sub)}</div>')
        out += ['  </div>', '</div>']
    return ind(6, out)


def r_about(d):
    out = [f'<p>{esc(p)}</p>' for p in pick(d["summary"], T)]
    out += ['', '<div style="margin-top:2rem;">', '  <div class="cert-group-title" style="margin-bottom:1rem;">Languages</div>']
    for l in d["languages"]:
        out += ['  <div class="lang-row">', f'    <span class="lang-name">{esc(l["name"])}</span>',
                f'    <div class="lang-bar-wrap"><div class="lang-bar" style="width:{l["bar"]}%"></div></div>',
                f'    <span class="lang-level">{esc(l["level"])}</span>', '  </div>']
    out += ['</div>']
    return ind(8, out)


def r_stats(d):
    s = d["stats"]
    boxes = [(f'{s["years"]}<span>+</span>', "Years Experience"), (f'{s["platforms"]}<span>+</span>', "Major Platforms"),
             (str(cvdata.cert_count(d)), "Certifications"), (str(s["regions"]), "Countries / Regions")]
    out = ['<div class="stat-grid">']
    for num, label in boxes:
        out += ['  <div class="stat-box">', f'    <div class="stat-num">{num}</div>', f'    <div class="stat-label">{label}</div>', '  </div>']
    out += ['</div>']
    return ind(8, out)


def r_skills(d):
    out = ['']
    for s in d["skills"]:
        card = ['<div class="skill-card">', f'  <div class="skill-card-icon">{s["icon"]}</div>',
                f'  <div class="skill-card-title">{esc(pick(s["title"], T))}</div>', '  <div class="tag-list">']
        card += [f'    <span class="tag">{esc(t)}</span>' for t in pick_list(s["tags"], T)]
        card += ['  </div>', '</div>']
        out += ind(6, card) + ['']
    return out


def r_experience_teaser(d):
    jobs = d["experience"]
    chain = " → ".join(f'{j["teaser"]["title"]} ({j["teaser"]["dates"]}, {j["teaser"]["place"]})' for j in reversed(jobs))
    out = ['<div class="locked-teaser">', '  <div class="locked-icon">🔒</div>',
           f'  <div class="locked-title">{d["stats"]["years"]}+ years across {len(jobs)} roles</div>',
           f'  <p class="locked-desc">{esc(chain)}. Full role history, responsibilities and achievements available on request.</p>',
           '  <a href="#" class="request-access-trigger locked-btn">🔓 Request Access</a>', '</div>']
    return ind(4, out)


def r_projects_teaser(d):
    regions = d["project_regions"]
    sizes = {len(r["projects"]) for r in regions}
    per = f"{sizes.pop()} per region" if len(sizes) == 1 else f"{len(regions)} regions"
    names = [r["short"] for r in regions]
    where = ", ".join(names[:-1]) + " & " + names[-1] if len(names) > 1 else names[0]
    out = ['<div class="locked-teaser">', '  <div class="locked-icon">🔒</div>',
           f'  <div class="locked-title">{cvdata.project_count(d)} projects across {esc(where)}</div>',
           f'  <p class="locked-desc">{esc(d["projects_teaser"].format(per_region=per))}</p>',
           '  <a href="#" class="request-access-trigger locked-btn">🔓 Request Access</a>', '</div>']
    return ind(4, out)


def r_certs(d):
    out = ['<div class="edu-block">', '  <div class="cert-group-title">Education</div>']
    for ed in d["education"]:
        out += ['  <div class="cert-item edu-item">', '    <div class="cert-badge edu">🎓</div>', '    <div>',
                f'      <div class="cert-name">{esc(ed["title"])}</div>',
                f'      <div class="edu-meta">{esc(ed["school"])} · {esc(pick(ed["location"], T))} · {esc(ed["year"])}</div>',
                '    </div>', '  </div>']
    out += ['</div>', '<div class="cert-groups">']
    for g in d["certifications"]:
        out += ['  <div>', f'    <div class="cert-group-title">{esc(g["title"])}</div>']
        for c in g["items"]:
            meta = cvdata.cert_web_meta(c)
            meta_html = f'<span class="cert-meta">{esc(meta)}</span>' if meta else ""
            out += ['    <div class="cert-item">', f'      <div class="cert-badge {g["badge"]}">{c["icon"]}</div>',
                    f'      <div class="cert-name">{esc(c["name"])}{meta_html}</div>', '    </div>']
        out += ['  </div>']
    out += ['</div>']
    return ind(4, out)


def r_contact(d):
    c = d["contact"]
    cards = [("📍", "Location", "<br>".join(esc(x) for x in c["location_lines"])),
             ("💼", "Availability", esc(c["availability"])),
             ("🔗", "LinkedIn", linkedin_a(c)),
             ("🔒", "Phone, Email &amp; CV", '<a href="#" class="request-access-trigger">Request access</a>')]
    out = []
    for icon, label, value in cards:
        out += ['<div class="contact-card">', f'  <span class="contact-card-icon">{icon}</span>',
                f'  <div class="contact-card-label">{label}</div>', f'  <div class="contact-card-value">{value}</div>', '</div>']
    return ind(6, out)


def r_footer(d):
    p, c = d["person"], d["contact"]
    year = datetime.date.today().year
    return [f'  © {year} <span>{esc(p["name"])}</span> · {esc(p["title"])} · {esc(c["location_short"])}']


# ---------------- protected/full-profile.html regions ----------------

def r_fp_experience(d):
    out = ['          <div class="timeline">', '      ']
    for j in d["experience"]:
        item = ['<div class="tl-item">', f'  <div class="tl-dot{" current" if j.get("current") else ""}"></div>',
                '  <div class="tl-header">', f'    <div class="tl-role">{esc(j["role"])}</div>',
                f'    <div class="tl-period">{esc(j["dates"])}</div>', '  </div>',
                f'  <div class="tl-company">{esc(j["company"])}</div>', f'  <div class="tl-location">📍 {esc(j["location"])}</div>',
                '  <ul class="tl-list">']
        item += [f'    <li>{rich(b)}</li>' for b in pick(j["bullets"], T)]
        item += ['  </ul>', '</div>']
        out += ind(12, item) + ['      ']
    out += ['          </div>']
    return out


def r_fp_projects(d):
    out = []
    for r in d["project_regions"]:
        reg = [f'<div class="region-group open" id="{r["id"]}">',
               f'  <button class="region-toggle" onclick="toggleRegion(\'{r["id"]}\')">',
               f'    <span>{esc(r["name"])} <span class="region-count">{len(r["projects"])} Projects</span></span>',
               '    <span class="chevron">▾</span>', '  </button>', '  <div class="region-body">', '    <div class="projects-grid">']
        for p in r["projects"]:
            reg += ['      <div class="project-card">', f'        <div class="project-card-title">{esc(p["title"])}</div>',
                    f'        <div class="project-card-meta">📍 {esc(p["location"])} &nbsp;|&nbsp; {esc(p["company"])}, {esc(p["years"])}</div>',
                    f'        <div class="project-card-desc">{rich(p["desc"])}</div>',
                    f'        <a class="project-card-link" href="{p["link"]}" target="_blank" rel="noopener">View Building →</a>',
                    '      </div>']
        reg += ['    </div>', '  </div>', '</div>']
        out += ind(10, reg) + ['      ']
    return out


def r_fp_contact(d):
    c = d["contact"]
    tel = re.sub(r"\D", "", c["phone"])
    return ind(6, [
        f'<div class="row"><div class="icon">📞</div><div><a href="tel:{tel}">{esc(c["phone"])}</a></div></div>',
        f'<div class="row"><div class="icon">✉️</div><div><a href="mailto:{c["email"]}">{esc(c["email"])}</a></div></div>',
        f'<div class="row"><div class="icon">📍</div><div>{"<br>".join(esc(x) for x in c["location_lines"])}</div></div>',
        f'<div class="row"><div class="icon">🔗</div><div>{linkedin_a(c)}</div></div>',
        '<a class="download-btn" href="Dimokritos_Kallionakis_CV.pdf" download>⬇️ Download Full CV (PDF)</a>',
    ])


PAGES = {
    "index.html": {"hero": r_hero, "hero-contact": r_hero_contact, "about": r_about, "stats": r_stats, "skills": r_skills,
                   "experience-teaser": r_experience_teaser, "projects-teaser": r_projects_teaser, "certs": r_certs,
                   "contact": r_contact, "footer": r_footer},
    "protected/full-profile.html": {"experience": r_fp_experience, "projects": r_fp_projects, "contact": r_fp_contact},
}


def render(path, regions, data):
    text = (cvdata.ROOT / path).read_text(encoding="utf-8")
    lines = text.split("\n")
    out, i, seen = [], 0, set()
    while i < len(lines):
        m = re.match(r"\s*<!-- cv:([\w-]+)\b.*-->\s*$", lines[i])
        if not m:
            out.append(lines[i]); i += 1; continue
        name = m.group(1)
        if name not in regions:
            sys.exit(f"{path}: unknown region '{name}'")
        end = next((k for k in range(i + 1, len(lines)) if re.match(rf"\s*<!-- /cv:{re.escape(name)} -->\s*$", lines[k])), None)
        if end is None:
            sys.exit(f"{path}: missing closing marker for '{name}'")
        out.append(lines[i]); out += regions[name](data); out.append(lines[end])
        seen.add(name); i = end + 1
    missing = set(regions) - seen
    if missing:
        sys.exit(f"{path}: markers not found for {sorted(missing)}")
    return text, "\n".join(out)


def main(check=False):
    data, changed = cvdata.load(), []
    for path, regions in PAGES.items():
        old, new = render(path, regions, data)
        if old != new:
            changed.append(path)
            if not check:
                (cvdata.ROOT / path).write_text(new, encoding="utf-8")
    verb = "would change" if check else "updated"
    print(f"Site {verb}: {', '.join(changed)}" if changed else "Site already up to date.")
    return changed


if __name__ == "__main__":
    main(check="--check" in sys.argv)
