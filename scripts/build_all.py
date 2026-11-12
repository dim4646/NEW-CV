"""One command to rebuild everything from data/cv-data.json:
    python3 scripts/build_all.py

1. PDF  -> protected/Dimokritos_Kallionakis_CV.pdf
2. Site -> index.html + protected/full-profile.html (generated regions only)
Then check the PDF + both pages, update PENDING.md and push to main.
"""
import build_site
import cvdata
import make_cv

if __name__ == "__main__":
    data = cvdata.load()
    pdf = cvdata.ROOT / "protected" / "Dimokritos_Kallionakis_CV.pdf"
    pages = make_cv.build(data, str(pdf))
    print(f"PDF written: {pdf.relative_to(cvdata.ROOT)} ({pages} pages)")
    if pages != 2:
        print(f"WARNING: CV is {pages} pages (target is 2)")
    build_site.main()
    print("Done. Next: check the PDF and both pages, update PENDING.md, commit and push to main.")
