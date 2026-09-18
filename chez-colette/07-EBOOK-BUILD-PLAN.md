# Colette's Home Bible — Build Plan

The ebook prompt builds 35 pages in one self-contained HTML artifact. The contents promised on the
Gumroad page need roughly 200. This file resolves that: **five runs of the same prompt, ~40 pages
each, merged into one PDF.**

## Why not 35, and why not 500

**Against 35:** the description promises seven parts plus three reference sections. Thirty-five A4
pages cannot hold that. Shipping it would mean a page that over-promises, which is the one mistake
this product cannot afford.

**Against 500:** no model produces a 500-page designed HTML artifact in a single response, so it
would have to be built in ~14 runs — and there is not 500 pages of honest material in this subject.
The remainder would be padding, and padding is visible in a book about taste. You are asking the
buyer to trust your judgement; a bloated book argues against you.

**Against competing on page count at all:** the thing that makes Bertha's book feel real in her
videos is not its size, it's that she cites *page 39*, *page 76*, *batch 77*. Specificity, not
volume. Build ~200 good pages, then go back and make every script callback cite a true page number.
That is worth more than 300 pages of filler.

**200 pages at $39** is strong value, fully deliverable, and every run stays inside the range where
the model does its best work.

---

## The five volumes

Run the ebook prompt five times. Same PRODUCT INFORMATION every time. Change only the four things
listed under each volume.

| Run | Pages | Contents |
|---|---|---|
| 1 | 1–44 | Front matter · Part One: How to Read a Room · Part Two: Light |
| 2 | 45–84 | Part Three: Colour |
| 3 | 85–124 | Part Four: Height and Proportion · Part Five: Texture and Material |
| 4 | 125–164 | Part Six: The Rented Room · Part Seven: Room by Room |
| 5 | 165–204 | The Measurements · The Room Audit · What Not to Buy · Back matter |

Merge the five PDFs in order. Any merge tool works; macOS Preview does it by dragging thumbnails.

**Before each run, also paste `COLETTE-REFERENCE.txt`** (the knowledge file from the script project)
into the chat. It carries her biography, the fourteen laws and the verified fact canon. Across five
runs and two hundred pages, that file is what stops the model inventing French history — which is
the single largest risk in this build, because French readers will be in the comments and in the
refund requests.

---

## PRODUCT INFORMATION — identical for all five runs

```
● E-book title: Colette's Home Bible
● Subtitle: La Belle Maison — Make Any Room Look Expensive Without Buying Anything New
● Topic: How to read a room, find the specific errors in it, and correct them
● Niche: French interior design and home styling — light, colour, proportion, texture and materials — applied to small, rented and ordinary homes
● Target audience: Women aged 30 to 60 in the US, UK and Canada who rent or own an ordinary home. They watch a lot of interior design content and save a lot of images, but their own rooms never look like the pictures. Many live in small flats, ground-floor rooms, or homes a previous owner or landlord renovated badly. They are not short of taste or effort — they have rearranged the furniture, bought cushions, painted a wall — and it still looks wrong. They cannot afford a decorator and would not know what to ask one for.
● Reader's current problem: Their rooms look cheaper and more chaotic than the money and effort they have put in, and they cannot work out why. They have no vocabulary for the problem, so they treat it as a shopping problem and buy more things, which usually makes it worse. They do not know what to look at, so they cannot diagnose anything.
● Reader's desired result: To walk into their own room and know exactly what is wrong with it and what to do about it. A home that looks composed, intentional and expensive, without replacing furniture or repainting everything.
● Unique method or angle: Diagnosis before decoration. A room is not decorated, it is corrected. Almost every ordinary room is suffering three or four specific, identifiable errors — of light, height, proportion or texture — and once the reader can see them, most are fixable in an afternoon with what is already in the house. Built on French domestic convention: Haussmannian proportion, window orientation, the ceiling as the fifth wall, limewash, and the tradition of curtain-making. It deliberately teaches what NOT to buy. Almost every other guide in this niche answers a design problem with a shopping list; this one is a diagnostic manual.
● Author or brand name: Colette Dubois
● Brand tagline: We do not decorate a room. We correct it.
● Reader's experience level: BEGINNER — assumes no design training, no tools beyond a tape measure, and no budget
● Preferred tone: PREMIUM and DIRECT — calm, exact, confident. An expert who is mildly irritated on the reader's behalf, never at them. Corrects the industry, never the reader. No hype, no motivational filler, no exclamation marks.
● Primary brand color: #1C1B19 (deep warm charcoal-ink)
● Secondary brand color: #8A9184 (Gris Trianon sage-grey)
● Accent color: #C08A3E (muted ochre)
● Background preference: LIGHT for interior pages — warm plaster off-white #F2EEE5 — with DARK charcoal #1C1B19 reserved for the cover, part-title pages, and the back cover
● Preferred visual style: MINIMAL — understated French editorial. Magazine-quality restraint, generous margins, generous white space.
● Call to action: Watch the channel for new corrections each week, and start with the room audit on the checklist page
● CTA link: https://chezcolette.com
● Product or offer connected to the e-book: NONE — this is the product. Do not advertise an upsell, a course, a community or a coaching offer. Do not invent any.
● Relevant experience or proof: NONE. There are no customers, reviews, testimonials, ratings, client results or sales figures. Do not reference any, do not imply any, and do not use social proof of any kind. Do not claim professional credentials, qualifications, client work or years of practice as evidence of authority. Build credibility from the specificity of the method instead: named measurements, stated mechanisms, and the fact that the reader can verify every principle in their own room the same evening.
● Required topics: [SEE THE PER-RUN LIST BELOW — paste only the current volume's list here]
● Topics to avoid: Feng shui, astrology, colour psychology presented as fact, anything requiring a contractor, anything requiring structural work, electrical work, gas work or plumbing. Never diagnose damp, mould, lead paint or asbestos — describe the problem in one sentence and route the reader to a professional. Do not give a health or safety claim of any kind.
● Additional instructions:
  FACTS. Use only the facts in the supplied COLETTE-REFERENCE.txt file. Never invent a French word, term, tradition, proverb, historical date, law, decree, statistic, study or institution. If you are not certain a French term is real and means what you are using it to mean, use plain English. Fabricated French detail is the fastest way to destroy this product's credibility, because French readers will check it. Where a claim is Colette's professional opinion rather than a verifiable fact, mark it as hers in the text: "my rule, and it is mine, not a law of physics, is that..."

  PRICES. Never state a price as current retail. Write "a few dollars", "under twenty dollars", "the cheapest one they sell". Give both metric and imperial for every measurement.

  THE READER IS NEVER THE PROBLEM. Every page must assume their taste was fine and their effort was real, and that nobody ever taught them what to look at. Never imply the reader has been lazy, tasteless or wasteful.

  BE HONEST ABOUT LIMITS. State plainly where the method does not apply: rented walls that cannot be drilled, listed buildings, rooms with no natural light. Say clearly when something genuinely is worth money — a good lamp, lined curtains, a sofa that can be reupholstered. The book is anti-wasted-spending, not anti-spending.

  DESIGN CONSISTENCY ACROSS VOLUMES. This book is built in five separate runs that will be merged into one PDF, so the design must be byte-identical between runs. Use exactly the locked CSS specification supplied below — the same page size, margins, type scale, fonts, colours, class names, header, footer and page-number position. Do not improvise a new layout, a new palette or new class names.

  PAGE NUMBERS. Interior pages carry continuous numbering across the whole book, not per volume. Start this volume's numbering at the number given in the per-run instructions.

  NO FILLER. Every page must carry a full page of real content. If a section runs short, add another mechanism, another worked example, another measurement, another worksheet — never adjectives, never a restated summary, never a page that is mostly a pull-quote.
```

---

## Per-run overrides

Change these four things in the prompt text for each run. Everything else stays as written.

### Run 1 — pages 1 to 44
- Replace every instance of "exactly 35 pages" / "35-page" with **"exactly 44 pages"** / "44-page"
- **Page numbering starts at 1.** Front matter pages 1–4 are unnumbered.
- **Use the prompt's REQUIRED structure for pages 1–4 only** (cover, copyright and disclaimer, welcome from Colette, table of contents). The table of contents must list **all seven parts and the three reference sections of the whole book**, not just this volume.
- Required topics: `Part One — How to Read a Room: the four errors every ordinary room makes; the three-question audit; why a room photographs badly when it looks fine in person; the order of operations, and why fixing colour before light wastes money. Part Two — Light: which way the window faces and what it does to every other decision; the three heights a room must be lit from; colour temperature and why shops are lit at a level a home never reaches; how many lamps, how tall, and where; the room with no natural light at all.`

### Run 2 — pages 45 to 84
- Replace "exactly 35 pages" with **"exactly 40 pages"**
- **Page numbering starts at 45.**
- **No cover, no copyright page, no welcome, no table of contents, no back cover.** Open on a dark charcoal part-title page reading "Part Three — Colour", then go straight into content.
- Required topics: `Part Three — Colour: choosing a colour by window orientation rather than by swatch; how to actually test a colour and why a two-centimetre chip tells you nothing; whites — which ones work in which light and where each one fails; why a small pale room looks smaller; the fifth wall and what to do with a ceiling; woodwork, skirtings and doors.`

### Run 3 — pages 85 to 124
- Replace "exactly 35 pages" with **"exactly 40 pages"**
- **Page numbering starts at 85.** No front or back matter. Open on a part-title page.
- Required topics: `Part Four — Height and Proportion: curtains, pole height, drop, fullness, and the four inches that lower a ceiling; hanging art at eye height; the picture rail already in the room; the furniture heights that must agree with each other; rug sizes, the most expensive common mistake in the room. Part Five — Texture and Material: the fourth texture and why three reads as a showroom; fabric weight and weave, and why linen reads as expensive; wood, stone, ceramic and metal in one room; the matched-set problem; measuring a window, calculating drops, and working out fullness.`

### Run 4 — pages 125 to 164
- Replace "exactly 35 pages" with **"exactly 40 pages"**
- **Page numbering starts at 125.** No front or back matter. Open on a part-title page.
- Required topics: `Part Six — The Rented Room: every correction that needs no drilling, no paint and no permission; reversible fixes; how to visually undo a bad landlord renovation; what a tenancy owes you, including the French legal minimum for a habitable room. Part Seven — Room by Room: living room, bedroom, kitchen, hallway and entry, bathroom, and rooms under thirty square metres.`

### Run 5 — pages 165 to 204
- Replace "exactly 35 pages" with **"exactly 40 pages"**
- **Page numbering starts at 165.** No cover and no front matter, but **this volume carries the back matter**: key lessons recap, final message from Colette, and the back cover with the call to action.
- Required topics: `The Measurements — a reference section collecting every number in the book in one place: hanging heights, curtain drops and fullness, rug sizes, seat and table heights, lamp heights, pendant drops, colour temperatures, spacing and clearances, designed as the page the reader keeps open while working. The Room Audit — a printable one-page checklist that walks through any room in ten minutes and says what to fix first. What Not to Buy — a plain list of the products this niche sells constantly that do not solve the problem, and the actual fix instead. Then: the first weekend plan, the season plan, a room-by-room correction log, key lessons recap, a final message from Colette, and the back cover.`

### Adapting the prompt's generic structure
The prompt's 35-page skeleton is built for a framework product. Most of it maps cleanly — keep the
intent, drop the infoproduct furniture that does not fit a reference manual:

| Prompt's page | Use it as |
|---|---|
| Common myths and misconceptions | keep — this niche is full of them |
| The unique method or framework | Part One's four errors and the order of operations |
| Framework step + action page | each correction, followed by a worked page the reader does |
| Recommended tools and resources | a tape measure, a colour card, two bulbs — keep it honest and tiny |
| Case study | label it clearly as a worked example, never as a real client |
| Templates / scripts / prompts | the measuring worksheets and the fabric calculation sheets |
| Checklist | The Room Audit |
| Mistakes to avoid | What Not to Buy |
| Troubleshooting | "the room still looks wrong — what did I miss" |
| Seven-day action plan | **The First Weekend** |
| Thirty-day plan | **The Season Plan** |
| Progress tracker | a room-by-room correction log |
| Cheat sheet | The Measurements |

Drop nothing else. Do not add a "mindset" section.

---

## The locked design specification

Paste this verbatim into **all five runs**. Without it you get five books that do not match, and the
merged PDF looks assembled rather than published.

```
LOCKED DESIGN SPECIFICATION — use exactly this in every volume, do not improvise.

@page { size: A4 portrait; margin: 0; }
Page box: 210mm x 297mm, overflow hidden, position relative.
Interior margins: 22mm left and right, 20mm top, 24mm bottom.

COLOUR TOKENS
--ink:      #1C1B19   deep warm charcoal — body text on light pages, background on dark pages
--plaster:  #F2EEE5   warm off-white — interior page background, text on dark pages
--sage:     #8A9184   Gris Trianon — rules, part labels, captions, secondary text
--ochre:    #C08A3E   accent — callout keylines, checkbox rules, page numbers, CTA
--paper:    #FBF9F5   worksheet and table fill, one step lighter than plaster

TYPOGRAPHY
Headings: a high-contrast editorial serif. Use the stack
  Georgia, 'Times New Roman', 'Playfair Display', serif
Body: a clean readable serif or humanist sans. Use the stack
  'Georgia', 'Iowan Old Style', serif   for body
  'Helvetica Neue', Arial, sans-serif   for labels, captions and worksheet fields
Use only these two families across the whole book.

TYPE SCALE
Part title (dark page):  48pt / 1.1, letterspacing 0.02em, all caps, plaster on ink
Page title:              26pt / 1.2, ink
Section heading:         15pt / 1.3, all caps, letterspacing 0.08em, sage
Body:                    11pt / 1.55, ink
Caption and field label: 8.5pt / 1.4, all caps, letterspacing 0.06em, sage
Pull quote:              17pt / 1.35, italic serif, ink, with a 2pt ochre rule above

REQUIRED CSS CLASSES — same names in every volume
.page .page--dark .page--worksheet
.page-title .section-head .body .lead
.callout .callout--rule .callout--warning .callout--meme
.checklist .checklist li .field .field-line
.table .table th .table td
.measure-row .measure-row__label .measure-row__value
.pullquote .divider .part-label
.footer .folio

HEADER AND FOOTER, on every interior page
Header: nothing on the left; on the right, the part name in 8.5pt all-caps sage
Footer: a 0.5pt sage rule across the text column, 6mm above the baseline.
        Below it, left: "COLETTE'S HOME BIBLE" in 8pt all-caps sage.
        Right: the folio (page number) in 9pt ochre.
Part-title pages and worksheet pages carry the folio but no header.

CALLOUT BOXES
.callout          — paper fill, 1pt sage keyline, 6mm padding
.callout--rule    — paper fill, 3pt ochre rule on the left edge, for a named law
.callout--warning — paper fill, 1pt ochre keyline, small ochre square bullet
.callout--meme    — ink fill, plaster text, for a line quoted from Mémé Suzanne's notebook

Named laws are always set in .callout--rule, in 13pt italic serif, with the law's name above it in
8.5pt all-caps sage.

RULES
No drop shadows. No gradients except a single flat ochre fill. No rounded corners above 2px.
No icons beyond simple inline SVG line marks in sage at 1.5pt stroke. No decorative flourishes.
All colour must be print-safe and readable in greyscale.
```

---

## After the build

Three things to do once the merged PDF exists, in this order:

1. **Read it end to end and check every French claim** against `COLETTE-REFERENCE.txt`. Delete
   anything that is not in there. This is the only step that genuinely cannot be skipped — a
   fabricated French fact in a paid product is a refund and a comment-section problem at once.
2. **Fill in the real page count** on the Gumroad description, and on the banner subtitle if you
   want a number there.
3. **Write down the true page numbers** for the ten or fifteen things the videos will cite most —
   the art height, the curtain drop, the window orientations, the whites, the audit, the
   measurements. Then put that list into the script project so the pitch callbacks name real pages.
   That is what made Bertha's book feel like an object rather than a file.
