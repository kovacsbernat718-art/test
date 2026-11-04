#!/usr/bin/env python3
"""Add The Christmas Pages (204-227) to the print edition.

    python3 add-christmas.py

Pages 1-203 keep their numbers, because the films cite them. The supplement
goes after the back matter, the colophon moves from 204 to 228, and the
contents page gains one line
(its last two paragraphs merge to make room). Safe to run twice: it does nothing the second
time.
"""
import pathlib

HERE = pathlib.Path(__file__).parent
SRC = HERE / "colettes-home-bible.html"
PAGES = HERE / "christmas-pages.html"
MARK = "<!-- ============ THE CHRISTMAS PAGES (204-227) ============ -->"

COLOPHON = '<section class="page page--dark">'
OLD_TOC = """        <div><span class="toc-part__num">And last</span><span class="toc-part__name">Thirty days, and the glossaries</span></div>
        <span class="toc-part__n">197</span>
      </div>"""
NEW_TOC = OLD_TOC + """
      <div class="toc-part">
        <div><span class="toc-part__num">A supplement</span><span class="toc-part__name">The Christmas Pages</span></div>
        <span class="toc-part__n">204</span>
      </div>"""
OLD_ED = "First edition &mdash; two hundred and four pages."
NEW_ED = "Second edition &mdash; two hundred and twenty-eight pages,<br>\n      with the Christmas pages."
OLD_HOW = """    <p>If you want to do something tonight, turn to <strong>The Room Audit</strong> on page 181. It
    is one page, it takes ten minutes, and it will tell you which part of the book to open.</p>
    <p>If you are mid-job and just need a number &mdash; how high to hang a picture, what size rug
    a sofa needs &mdash; go to <strong>The Measurements</strong> on page 165, where every figure in
    the book is collected.</p>"""
NEW_HOW = """    <p>If you want to do something tonight, turn to <strong>The Room Audit</strong> on page 181:
    one page, ten minutes, and it tells you which part to open. If you just need a number,
    <strong>The Measurements</strong> on page 165 collects every figure in the book.</p>"""
OLD_FOLIO = '<div class="footer"><span>&nbsp;</span><span class="folio">204</span></div>'
NEW_FOLIO = '<div class="footer"><span>&nbsp;</span><span class="folio">228</span></div>'


def main():
    src = SRC.read_text()
    if MARK in src:
        print("already added")
        return
    for old in (COLOPHON, OLD_TOC, OLD_HOW, OLD_ED, OLD_FOLIO):
        assert src.count(old) == 1, old[:60]
    at = src.index(COLOPHON)
    src = src[:at] + PAGES.read_text().rstrip() + "\n\n<!-- ============ 228. COLOPHON ============ -->\n" + src[at:]
    src = src.replace(OLD_TOC, NEW_TOC).replace(OLD_HOW, NEW_HOW).replace(OLD_ED, NEW_ED).replace(OLD_FOLIO, NEW_FOLIO)
    SRC.write_text(src)
    print("added the Christmas pages; the book now has", src.count('<section class="page'), "pages")


if __name__ == "__main__":
    main()
