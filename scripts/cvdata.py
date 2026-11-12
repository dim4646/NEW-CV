"""Shared helpers: load data/cv-data.json and resolve web/pdf variants."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "cv-data.json"

LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def load():
    with open(DATA, encoding="utf-8") as f:
        return json.load(f)


def pick(value, target):
    """Return the value for 'web' or 'pdf'. Plain values are shared by both."""
    if isinstance(value, dict) and ("web" in value or "pdf" in value):
        return value.get(target)
    return value


def pick_list(items, target):
    """Resolve each item of a list and drop the ones hidden (None) for this target."""
    out = []
    for it in items:
        v = pick(it, target)
        if v is not None:
            out.append(v)
    return out


def strip_links(text):
    """[text](url) -> text (for the PDF)."""
    return LINK_RE.sub(r"\1", text)


def cert_count(data):
    """Completed certifications (training still in progress is not counted)."""
    return sum(1 for g in data["certifications"] for c in g["items"] if not c.get("in_progress"))


def project_count(data):
    return sum(len(r["projects"]) for r in data["project_regions"])


def masked_licence(number):
    return number[:2] + "*" * (len(number) - 2)


def cert_web_meta(c):
    parts = []
    if c.get("provider"):
        parts.append(c["provider"])
    if c.get("awarded"):
        parts.append("Awarded " + c["awarded"])
    if c.get("date"):
        parts.append(c["date"])
    if c.get("valid_until"):
        parts.append("Valid until " + c["valid_until"])
    return " · ".join(parts)


def cert_pdf_name(c):
    parts = []
    if c.get("awarded"):
        parts.append(c["awarded"])
    if c.get("date"):
        parts.append(c["date"])
    if c.get("valid_until"):
        parts.append("valid until " + c["valid_until"])
    return c["name"] + (f" ({', '.join(parts)})" if parts else "")


def licence_pdf(l):
    """'Name – Class 2 (No. 123, expires 11/2027)'; optional fields are skipped."""
    text = l["name"] + (f" – {l['class']}" if l.get("class") else "")
    extra = [f"No. {l['number']}"] if l.get("number") else []
    if l.get("expires"):
        extra.append(f"expires {l['expires']}")
    return text + (f" ({', '.join(extra)})" if extra else "")


def licence_web(l):
    """Public page: masked number, short form."""
    parts = [l["class"]] if l.get("class") else []
    if l.get("number"):
        parts.append("No. " + masked_licence(l["number"]))
    if l.get("expires"):
        parts.append("Exp. " + l["expires"])
    return " · ".join(parts)
