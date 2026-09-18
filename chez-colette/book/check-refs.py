#!/usr/bin/env python3
"""Verify every 'page NN' cross-reference in the book lands where it should.

Run after appending each volume:  python3 check-refs.py
Prints the destination page title next to each reference so a wrong one is obvious.
"""
import pathlib
import re

SRC = pathlib.Path(__file__).parent / "colettes-home-bible.html"
PLANNED = {165: "The Measurements", 181: "The Room Audit", 189: "What Not to Buy"}


def main():
    src = SRC.read_text()

    titles = {}
    for match in re.finditer(r'<section class="page(.*?)</section>', src, re.S):
        block = match.group(1)
        folio = re.search(r'class="folio">(\d+)<', block)
        head = re.search(r'<h1 class="(?:page-title[^"]*|part-title)">(.*?)</h1>', block, re.S)
        if folio:
            text = " ".join(re.sub(r"<[^>]+>", " ", head.group(1)).split()) if head else "(front matter)"
            titles[int(folio.group(1))] = text[:54]

    last = max(titles)
    unresolved = 0
    print("%-7s %-54s %s" % ("REF", "LANDS ON", "CONTEXT"))
    print("-" * 132)
    for match in re.finditer(r"[Pp]age\s+(\d+)", src):
        n = int(match.group(1))
        ctx = src[max(0, match.start() - 88):match.end() + 6]
        ctx = " ".join(re.sub(r"<[^>]+>", " ", ctx).split())[-88:]
        if n in titles:
            dest = titles[n]
        elif n in PLANNED:
            dest = "(not written yet - planned: %s)" % PLANNED[n]
            unresolved += 1
        else:
            dest = "*** NO SUCH PAGE (book ends at %d) ***" % last
            unresolved += 1
        print("p%-6d %-54s %s" % (n, dest, ctx))

    print("-" * 132)
    print("book runs to page %d; %d reference(s) point past it" % (last, unresolved))


if __name__ == "__main__":
    main()
