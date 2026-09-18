#!/usr/bin/env python3
"""Rebuild deploy/index.html from the print edition.

Re-run after appending each volume to colettes-home-bible.html:
    python3 rebuild-deploy.py
"""
import pathlib
import re

HERE = pathlib.Path(__file__).parent
SRC = HERE / "colettes-home-bible.html"
DST = HERE / "deploy" / "index.html"

ENTITIES = [
    ("&rsquo;", "’"), ("&lsquo;", "‘"),
    ("&ldquo;", "“"), ("&rdquo;", "”"),
    ("&mdash;", "—"), ("&ndash;", "–"),
    ("&agrave;", "à"), ("&egrave;", "è"), ("&eacute;", "é"),
    ("&ccedil;", "ç"), ("&nbsp;", " "), ("&thinsp;", " "),
    ("&amp;", "&"),
]


def clean(html):
    """Strip tags from a heading and normalise its entities."""
    text = " ".join(re.sub(r"<[^>]+>", " ", html).split())
    for name, char in ENTITIES:
        text = text.replace(name, char)
    return text


def extract_pages():
    """Return the page sections from the print edition, with anchor ids added."""
    src = SRC.read_text()
    pages = src[src.index("<!-- ============ 1. COVER"):].rstrip()
    counter = [0]

    def add_id(_match):
        counter[0] += 1
        return '<section id="p%d" class="page' % counter[0]

    return re.sub(r'<section class="page', add_id, pages), counter[0]


def build_contents(pages):
    """A contents list, not an index.

    Keep every part title, every worksheet, and every page that opens a
    chapter or carries a kicker label. Ordinary continuation pages are
    reachable by scrolling and would swamp the panel.
    """
    rows = []
    for match in re.finditer(r'<section id="p(\d+)" class="page(.*?)</section>', pages, re.S):
        idx, block = int(match.group(1)), match.group(2)

        folio = re.search(r'class="folio">([^<]*)<', block)
        folio = folio.group(1).strip() if folio else str(idx)

        part = re.search(r'<p class="part-label">([^<]+)</p>', block)
        if part:
            title = re.search(r'<h1 class="part-title">(.*?)</h1>', block, re.S)
            rows.append((idx, folio, part.group(1).strip(),
                         clean(title.group(1)) if title else ""))
            continue

        is_worksheet = "page--worksheet" in block[:90]
        kicker = re.search(r'<p class="kicker">([^<]+)</p>', block)
        if not (is_worksheet or kicker):
            continue

        title = re.search(r'<h1 class="page-title[^"]*">(.*?)</h1>', block, re.S)
        if not title:
            continue
        name = clean(title.group(1))
        if len(name) > 44:
            name = name[:42].rstrip() + "…"
        # Several page titles are fragments that only make sense under their
        # kicker ("That are wrong - part one"). Show the kicker as the eyebrow,
        # the same way a part label is shown.
        eyebrow = clean(kicker.group(1)) if kicker else None
        rows.append((idx, folio, eyebrow, name))

    out = ["  <h2>Contents</h2>"]
    for idx, folio, part, name in rows:
        label = f"<em>{part}</em>{name}" if part else name
        out.append(f'  <a href="#p{idx}"><span style="flex:1">{label}</span>'
                   f'<span>{folio}</span></a>')
    return "\n".join(out), len(rows)


def main():
    pages, total = extract_pages()
    contents, n_entries = build_contents(pages)

    dst = DST.read_text()
    dst = re.sub(r'(<main class="book" id="book">\n).*?(\n</main>)',
                 lambda m: m.group(1) + pages + m.group(2), dst, flags=re.S)
    dst = re.sub(r'(<nav class="toc-panel" id="toc-panel" aria-label="Contents">\n).*?(\n</nav>)',
                 lambda m: m.group(1) + contents + m.group(2), dst, flags=re.S)
    dst = re.sub(r'(id="folio-live" aria-live="off"><b>1</b>&thinsp;/&thinsp;)\d+',
                 lambda m: m.group(1) + str(total), dst)
    DST.write_text(dst)

    print(f"rebuilt deploy/index.html — {total} pages, "
          f"{n_entries} contents entries, {round(len(dst)/1024)} KB")


if __name__ == "__main__":
    main()
