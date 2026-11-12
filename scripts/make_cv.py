"""Build protected/Dimokritos_Kallionakis_CV.pdf from data/cv-data.json.

Design: navy/gold, A4, 2 pages, ATS-friendly (real text, standard fonts, single reading order).
Usage: python3 scripts/make_cv.py [output.pdf]
"""
import sys
from xml.sax.saxutils import escape

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.platypus.flowables import HRFlowable

import cvdata

T = "pdf"
NAVY = HexColor("#14213d")
GOLD = HexColor("#b8912f")
GREY = HexColor("#555555")
TXT = HexColor("#222222")
W, H = A4
LM = RM = 17 * mm
CW = W - LM - RM


def S(font="Helvetica", **k):
    return ParagraphStyle("s", fontName=font, **k)


name_st = S("Helvetica-Bold", fontSize=26, leading=30, textColor=NAVY)
title_st = S(fontSize=12, leading=15, textColor=GOLD)
contact_st = S(fontSize=9, leading=13.5, textColor=GREY)
head_st = S("Helvetica-Bold", fontSize=13, leading=16, textColor=NAVY, spaceBefore=10)
body_st = S(fontSize=9.3, leading=13.6, textColor=TXT)
lab_st = S("Helvetica-Bold", fontSize=9.3, leading=13, textColor=NAVY)
val_st = S(fontSize=9, leading=13, textColor=TXT)
role_st = S("Helvetica-Bold", fontSize=10.5, leading=13, textColor=NAVY)
date_st = S("Helvetica-Oblique", fontSize=9, leading=13, textColor=GREY, alignment=2)
comp_st = S("Helvetica-Bold", fontSize=9.5, leading=12, textColor=GOLD, leftIndent=6)
loc_st = S("Helvetica-Oblique", fontSize=8.5, leading=11, textColor=GREY, leftIndent=6)
bul_st = S(fontSize=9.2, leading=13, textColor=TXT, leftIndent=18, bulletIndent=8)
sub_st = S("Helvetica-Bold", fontSize=9, leading=13, textColor=GOLD, spaceBefore=5)
cb_st = S(fontSize=8.8, leading=12, textColor=TXT, leftIndent=10, bulletIndent=4)

NOPAD = [("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0)]


def e(text):
    return escape(cvdata.strip_links(text))


def section(title):
    return [Paragraph(e(title.upper()), head_st),
            HRFlowable(width="100%", thickness=1, color=GOLD, spaceBefore=3, spaceAfter=6)]


def bullets(items, style):
    return [Paragraph(e(i), style, bulletText="•") for i in items]


def block(title, items):
    return [Paragraph(e(title), sub_st)] + bullets(items, cb_st)


def build(data, out):
    p, c = data["person"], data["contact"]
    footer_text = f"{p['name']} · {p['title']} · {c['location_short']}"

    def footer(cv, doc):
        cv.setFont("Helvetica", 7.5)
        cv.setFillColor(GREY)
        cv.drawCentredString(W / 2, 12 * mm, f"{footer_text} · Page {doc.page}")

    doc = BaseDocTemplate(out, pagesize=A4, leftMargin=LM, rightMargin=RM, topMargin=14 * mm,
                          bottomMargin=20 * mm, title=f"{p['name']} - CV", author=p["name"])
    doc.addPageTemplates([PageTemplate(frames=[Frame(LM, 20 * mm, CW, H - 34 * mm, leftPadding=0, rightPadding=0)],
                                       onPage=footer)])
    st = []

    # Header
    gold = lambda url, txt: f'<link href="{url}"><font color="#b8912f">{escape(txt)}</font></link>'
    contact_html = "<br/>".join([
        escape(c["phone"]), escape(c["email"]), escape(", ".join(c["location_lines"])),
        gold(c["linkedin_url"], cvdata.pick(c["linkedin_display"], T)),
        gold("https://" + c["website"], c["website"]),
    ])
    ht = Table([[[Paragraph(e(p["name"]), name_st), Paragraph(e(p["title"]), title_st)],
                 Paragraph(contact_html, contact_st)]], colWidths=[CW * 0.62, CW * 0.38])
    ht.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE")] + NOPAD))
    st += [ht, Spacer(1, 6), HRFlowable(width="100%", thickness=2.2, color=NAVY, spaceAfter=4)]

    # Summary
    st += section("Professional Summary")
    st.append(Paragraph(e(cvdata.pick(data["summary"], T)), body_st))

    # Skills
    st += section("Technical Skills")
    rows = []
    for s in data["skills"]:
        tags = cvdata.pick_list(s["tags"], T)
        rows.append([Paragraph(e(cvdata.pick(s["title"], T)), lab_st), Paragraph(e(" · ".join(tags)), val_st)])
    t = Table(rows, colWidths=[CW * 0.3, CW * 0.7])
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0),
                           ("TOPPADDING", (0, 0), (-1, -1), 1.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5)]))
    st.append(t)

    # Experience
    st += section("Professional Experience")
    for job in data["experience"]:
        jt = Table([[Paragraph(e(job["role"]), role_st), Paragraph(e(job["dates"]), date_st)]],
                   colWidths=[CW * 0.72, CW * 0.28])
        jt.setStyle(TableStyle(NOPAD + [("BOTTOMPADDING", (0, 0), (-1, -1), 2), ("TOPPADDING", (0, 0), (-1, -1), 6)]))
        st += [jt, Paragraph(e(job["company"]), comp_st), Paragraph(e(job["location"]), loc_st), Spacer(1, 3)]
        st += bullets(cvdata.pick(job["bullets"], T), bul_st)

    # Education & certifications (two columns)
    st += section("Education & Certifications")
    certs = {g["id"]: g for g in data["certifications"]}
    left = block("Education", [f"{ed['title']} – {ed['school']}, {cvdata.pick(ed['location'], T)} ({ed['year']})"
                               for ed in data["education"]])
    left += block("Licences", [f"{l['name']} – {l['class']} (No. {l['number']}, expires {l['expires']})"
                               for l in data["licences"]])
    right = []
    for gid, col in (("security", left), ("hanwha", right), ("networking", right)):
        g = certs[gid]
        col += block(g["title"], [cvdata.cert_pdf_name(i) for i in g["items"]])
    for g in data["certifications"]:  # any new group added later goes to the right column
        if g["id"] not in ("security", "hanwha", "networking"):
            right += block(g["title"], [cvdata.cert_pdf_name(i) for i in g["items"]])
    right += block("Languages", [f"{l['name']} — {l['level']}" for l in data["languages"]])
    t = Table([[left, right]], colWidths=[CW * 0.5, CW * 0.5])
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 8)]))
    st.append(t)

    doc.build(st)
    return doc.page


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else str(cvdata.ROOT / "protected" / "Dimokritos_Kallionakis_CV.pdf")
    pages = build(cvdata.load(), out)
    print(f"PDF written: {out} ({pages} pages)")
    if pages != 2:
        print(f"WARNING: CV is {pages} pages (target is 2)")
