#!/usr/bin/env python3
"""Flatten the print edition into one plain-text file.

    python3 html-to-txt.py

Keeps the structure a reader needs — parts, page numbers, headings, rules,
measurements, worksheets — and drops everything that only exists for print.
"""
import html
import pathlib
import re
import textwrap

HERE = pathlib.Path(__file__).parent
SRC = HERE / "colettes-home-bible.html"
DST = HERE / "Colettes-Home-Bible.txt"

WIDTH = 92


def text(fragment):
    """Tags out, entities decoded, whitespace normalised."""
    fragment = re.sub(r"<br\s*/?>", " ", fragment)
    fragment = re.sub(r"<[^>]+>", "", fragment)
    return " ".join(html.unescape(fragment).split())


def wrap(body, indent="", first=None):
    if not body:
        return []
    return textwrap.wrap(body, WIDTH, initial_indent=first if first is not None else indent,
                         subsequent_indent=indent)


def render_table(block):
    """A worksheet table -> a header, a rule, and writable rows."""
    rows = re.findall(r"<tr>(.*?)</tr>", block, re.S)
    if not rows:
        return []

    grid = [re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", row, re.S) for row in rows]
    cols = max(len(row) for row in grid)
    avail = WIDTH - 4 - 3 * (cols - 1)
    rest = max(8, min(20, avail // (cols + 1)))
    first = avail - rest * (cols - 1)

    out = []
    for i, row in enumerate(grid):
        cells = [text(cell) for cell in row] + [""] * (cols - len(row))
        if i == 0 and "<th" in rows[0]:
            line = cells[0].upper()[:first].ljust(first)
            for cell in cells[1:]:
                line += " | " + cell.upper()[:rest].ljust(rest)
            out += ["    " + line.rstrip(), "    " + "-" * min(WIDTH - 4, len(line))]
            continue
        line = cells[0][:first].ljust(first)
        for cell in cells[1:]:
            line += " | " + (cell[:rest].ljust(rest) if cell else "_" * rest)
        out.append("    " + line.rstrip())
    return out + [""]


def render_page(block, folio):
    """One page section -> a list of output lines."""
    out = ["", "[ page %s ]" % folio, ""]

    part_label = re.search(r'<p class="part-label">(.*?)</p>', block, re.S)
    part_title = re.search(r'<h1 class="part-title">(.*?)</h1>', block, re.S)
    if part_label and part_title:
        out += ["=" * WIDTH, "",
                text(part_label.group(1)).upper(),
                text(part_title.group(1)).upper(), "", "=" * WIDTH, ""]
        blurb = re.search(r'<p class="part-blurb">(.*?)</p>', block, re.S)
        if blurb:
            out += wrap(text(blurb.group(1))) + [""]
        for item in re.findall(r"<li>(.*?)</li>", block, re.S):
            out.append("    " + text(item))
        return out

    cover = re.search(r'<h1 class="cover-title">(.*?)</h1>', block, re.S)
    if cover:
        out += ["", text(cover.group(1)).upper()]
        for cls in ("cover-sub", "cover-author", "cover-fr"):
            found = re.search(r'<p class="%s">(.*?)</p>' % cls, block, re.S)
            if found:
                out.append(text(found.group(1)))
        return out + [""]

    kicker = re.search(r'<p class="kicker">(.*?)</p>', block, re.S)
    title = re.search(r'<h1 class="page-title[^"]*">(.*?)</h1>', block, re.S)
    if kicker:
        out.append(text(kicker.group(1)).upper())
    if title:
        heading = text(title.group(1))
        out += [heading, "-" * min(len(heading), WIDTH), ""]

    body = re.search(r'<div class="body">(.*?)(?=<div class="footer">)', block, re.S)
    body = body.group(1) if body else block

    # Walk the page's own elements in document order.
    pattern = (r'<p class="(section-head|lead|small|pullquote)">(.*?)</p>'
               r'|<p class="law-name">(.*?)</p>\s*<p class="law-text">(.*?)</p>'
               r'|<p class="callout-label">(.*?)</p>'
               r'|<div class="measure-row">\s*<span class="measure-row__label">(.*?)</span>\s*'
               r'<span class="measure-row__value">(.*?)</span>'
               r'|<li>(.*?)</li>'
               r'|<table[^>]*>(.*?)</table>'
               r'|<span class="field-label">(.*?)</span>'
               r'|<p>(.*?)</p>')

    # Which <li> runs belong to an <ol class="steps"> - those are numbered.
    ordered = [(ol.start(), ol.end())
               for ol in re.finditer(r'<ol class="steps">(.*?)</ol>', body, re.S)]
    boxes = [(ul.start(), ul.end())
             for ul in re.finditer(r'<ul class="checklist">(.*?)</ul>', body, re.S)]

    counter, step = [0], [0]
    for match in re.finditer(pattern, body, re.S):
        (head, head_body, law, law_text, label, m_label, m_value, item,
         table, field, para) = match.groups()

        if head == "section-head":
            out += ["", text(head_body).upper(), ""]
        elif head in ("lead", "small", "pullquote"):
            out += wrap(text(head_body)) + [""]
        elif law is not None:
            out += ["  +" + "-" * (WIDTH - 4) + "+",
                    "  | " + text(law).upper()]
            out += wrap(text(law_text), indent="  | ") + ["  +" + "-" * (WIDTH - 4) + "+", ""]
        elif label is not None:
            out += ["  [ " + text(label).upper() + " ]"]
        elif m_label is not None:
            left, right = text(m_label), text(m_value)
            if len(left) + len(right) + 12 > WIDTH:
                out += wrap(left, indent="    ")
                out.append(" " * (WIDTH - len(right)) + right)
            else:
                dots = max(3, WIDTH - 6 - len(left) - len(right))
                out.append("    " + left + " " + "." * dots + " " + right)
        elif item is not None:
            inside = any(a <= match.start() < b for a, b in ordered)
            if inside:
                step[0] += 1
                out += wrap(text(item), indent="      ", first="   %d. " % step[0])
            elif any(a <= match.start() < b for a, b in boxes):
                step[0] = 0
                out += wrap(text(item), indent="        ", first="    [ ] ")
            else:
                step[0] = 0
                out += wrap(text(item), indent="      ", first="    - ")
            if body[match.end():match.end() + 40].lstrip().startswith(("</ul>", "</ol>")):
                out.append("")
        elif table is not None:
            out += render_table(table)
        elif field is not None:
            label_text = text(field)
            rule = max(12, WIDTH - 6 - len(label_text))
            out += ["    " + label_text + ": " + "_" * rule, ""]
        elif para is not None:
            out += wrap(text(para)) + [""]

    return out


def main():
    src = SRC.read_text()
    pages = re.findall(r'<section class="page.*?</section>', src[src.index("<!-- ============ 1. COVER"):], re.S)

    lines = ["COLETTE'S HOME BIBLE",
             "La Belle Maison",
             "",
             "The complete text, %d pages." % len(pages),
             "Plain-text edition, generated from the print edition.",
             ""]

    for i, block in enumerate(pages, 1):
        folio = re.search(r'class="folio">(\d+)<', block)
        lines += render_page(block, folio.group(1) if folio else str(i))

    # Collapse runs of blank lines.
    out, blank = [], 0
    for line in lines:
        blank = blank + 1 if not line.strip() else 0
        if blank < 3:
            out.append(line.rstrip())

    DST.write_text("\n".join(out) + "\n")
    print("wrote %s - %d pages, %d lines, %d KB"
          % (DST.name, len(pages), len(out), round(DST.stat().st_size / 1024)))


if __name__ == "__main__":
    main()
