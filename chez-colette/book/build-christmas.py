#!/usr/bin/env python3
"""Build The Christmas Pages, the seasonal supplement, as its own book.

    python3 build-christmas.py      # writes christmas/the-christmas-pages.html
    node render-pdf.cjs christmas/the-christmas-pages.html christmas/The-Christmas-Pages.pdf
    node render-cover.cjs christmas/the-christmas-pages.html christmas/epub-src/cover.jpg
    python3 build-christmas-epub.py     # christmas/The-Christmas-Pages.epub

It borrows the main book's fonts and stylesheet, so the typography matches,
and lays christmas/noel.css over them for the December colours. Pages are
numbered 1-24; references to the main book read "page NN of the book".
Kept separate so the supplement can be withdrawn after the season without
touching the Home Bible.
"""
import pathlib

HERE = pathlib.Path(__file__).parent
BOOK = HERE / "colettes-home-bible.html"
DIR = HERE / "christmas"
OUT = DIR / "the-christmas-pages.html"


def main():
    src = BOOK.read_text()
    head = src[:src.index("<!-- ============ 1. COVER")]
    head = head.replace("<title>Colette's Home Bible</title>",
                        "<title>The Christmas Pages — Colette's Home Bible</title>")
    css = "<style>\n" + (DIR / "noel.css").read_text() + "</style>\n\n"
    pages = (DIR / "christmas-pages.html").read_text().strip()
    OUT.write_text(head + css + pages + "\n")
    print("wrote", OUT, "-", pages.count('<section class="page'), "pages")


if __name__ == "__main__":
    main()
