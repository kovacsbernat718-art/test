# Colette's Home Bible

`index.html` is the whole book. One file — HTML, CSS and JavaScript inline, no build step,
no dependencies to install.

## Deploy on GitHub Pages

1. Put `index.html` in the root of the repository.
2. **Settings → Pages → Source:** *Deploy from a branch* → `main` / `/ (root)` → **Save**.
3. It goes live at `https://<user>.github.io/<repo>/` in about a minute.

Works identically on Netlify, Vercel or Cloudflare Pages — drag the folder in, no configuration.

## What the reader does

| | |
|---|---|
| **Pages / Reflow** | Two reading modes. *Pages* shows true A4 spreads, scaled to fit any screen. *Reflow* drops the fixed page and sets the text at 16px for comfortable phone reading. Defaults to Reflow under 820px and Pages above, and remembers the choice. |
| **Contents** | Slide-out panel, jumps to any chapter. |
| **Save as PDF** | Opens the browser print dialog. Prints as **104 exact A4 pages** from either mode — the reader chrome is hidden and the true page geometry is restored. |
| **Page counter** | Live folio, `12 / 104`, from the book's own page numbers. |
| **Progress bar** | Under the top bar. |
| **Keyboard** | `←` `→` page, `Home` `End` jump, `c` contents, `r` switch mode, `Esc` close. |
| **Resume** | Remembers the last page read, per browser. |

## Two things to know

**Turn on background graphics when printing.** Chrome: *More settings → Background graphics*.
Safari: *Print backgrounds*. Without it the dark cover and part-title pages come out white.
`Colettes-Home-Bible.pdf` in this folder already has it baked in.

**Fonts come from Google Fonts** — Bodoni Moda, Spectral, Archivo — via one stylesheet link.
It is the only external request the page makes. If you need a genuinely offline file, the fallback
stack (Didot / Georgia / Helvetica) is already declared and the layout holds without them.

## Contents

Front matter · **Part One — How to Read a Room** (pp. 5–20) · **Part Two — Light** (pp. 21–44) ·
**Part Three — Colour** (pp. 45–84) · **Part Four — Height and Proportion** (pp. 85–104)

Part Five to Part Seven and the reference sections are still to be written.

Regenerate this file after each new volume with `python3 ../rebuild-deploy.py` — it re-splices the
pages from the print edition and rebuilds the contents panel and the page count.
