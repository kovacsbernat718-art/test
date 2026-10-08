# New Claude project: The Japanese Method structure, with Colette's family and French words kept

A third script project. It uses The Japanese Method's structure and keeps Colette's family, background and French words, placed where they hold viewers instead of where they lose them. It's built around one problem: **AVD falling when YouTube shows your videos to new people.**

Your other two projects stay as they are.

---

## Setting it up (5 minutes)

**1. Create a new project** in Claude, for example *Chez Colette — JM + Family*.

**2. Instructions box:** paste the whole of `PROJECT-INSTRUCTIONS.txt`.

> If Claude ever says the instructions are too long, upload `PROJECT-INSTRUCTIONS.txt` as a knowledge file instead, and put this one line in the instructions box:
> `Follow PROJECT-INSTRUCTIONS.txt in the project knowledge exactly. It is your only set of instructions.`

**3. Knowledge:** unzip `Chez-Colette-JM-Family-KNOWLEDGE.zip` and upload **all 13 files**:

- `COLETTE-REFERENCE.txt`, the same file as your other projects
- `JM-TOP01` … `JM-TOP10`: The Japanese Method's 10 best-performing videos right now
- `SPENT-002-…` and `SPENT-003-…`: your published scripts, so nothing in them gets repeated

---

## After every video you publish

Copy the exact script you recorded into a text file named `SPENT-` + number + short title (for example `SPENT-004-trends-out-2026.txt`) and upload it to this project's knowledge.

**Your "10 Interior Design Trends That Are OUT of Style in 2026" video:** once it's published, add its script as a SPENT file too.

---

## Writing a script

**Step 1.** Open a new chat inside the project and paste:

```
TITLE: 
THUMBNAIL TEXT: 
DURATION: 15 minutes, 2,775 words
LAST VIDEO: [topic] | hook shape used: [COUNT / SCENE / CYCLE] | quiet-part target used: [from PART 5 of the Colette file, or none]
NEXT VIDEO: 
REFERENCE TRANSCRIPT: [paste]

First, give me three different openings for the first sixty seconds, each with a different hook shape. I'll pick one, then write the full script from it.
```

- **DURATION:** minutes × 185 = words. 12 min = 2,220 · 14 = 2,590 · 15 = 2,775 · 16 = 2,960 · 18 = 3,330.
- **Hook shapes:**
  - **COUNT** opens with a number: "there are N things in your room right now that…"
  - **SCENE** sends the viewer somewhere in their home: "go and look at…"
  - **CYCLE** describes the loop they're stuck in: "you bought…, you repainted…, and it still…"
  - 002 and 003 both used **SCENE**.
- **NEXT VIDEO** is optional. It's the video your end screen points to, and the script's last sentence leads into it.

**Step 2.** You get three openings. The shape your last video used is marked, so you can avoid repeating it. Reply:

```
Use the COUNT opening. Write the full script.
```

**Step 3.** Before recording, check the facts (see below).

| Runtime | Words | Shape | Family moments | French words |
|---|---|---|---|---|
| 10–12 min | 1,850–2,220 | 5–6 items | 2 | 2 |
| **13–16 min** (default) | **2,405–2,960** | **7–8 items** | **3** | **3** |
| 17–20 min | 3,145–3,700 | 9–11 items | 4 | 4 |
| 21–24 min | 3,885–4,440 | 11–15 items | 5 | 5 |

*"ma chère" is counted separately and also scales with length.*

---

## What changed from your published scripts, and why

| | Video 002 / 003 | **This project** |
|---|---|---|
| First tip starts at | 2:11 / 2:51 | **before 0:55** |
| "My name is Colette…" block | 1:20 / 1:39 | **gone** |
| Facts like the 2002 decree or Haussmann | 0:32 / 0:39 | **only inside a tip**, after the viewer has seen why it matters |
| Family and background | 14 / 17 mentions, many up front | **3 short moments** (15 min), each inside a tip as proof, none in the first minute, the strongest one near the end |
| French words | a few, in the intro | **3, spread across the tips**, from the approved list plus everyday words (brocante, vide-grenier, armoire, l'heure bleue, …) |
| Book pitch | the same 75-word grandmother story, after **one** tip | **new every video**: 2–3 plain sentences in JM's style, after **at least two** tips |
| What each tip is built on | Colette's order: light, height, texture, colour | **one "I didn't know that" discovery** that's surprising, useful and clearly belongs in this video. No preset categories. |
| Reassurance lines ("it's not your taste…", "nobody showed you…") | in the hook, items and close | **banned**, in any wording |
| End of each tip | — | **one thing to do tonight, then a tease for the next tip** |
| Ending | long | **120–200 words**, finishing on your next video |

The full reasoning is in `COMPETITOR-ANALYSIS.md`.

---

## Turning the family up or down

Everything is controlled by one line per length in the **LENGTH TIERS** section of the instructions, for example:

```
Family moments: three. French words: three. "ma chère": three or four.
```

Change the numbers and save. Nothing else needs to change.

---

## Before you record: check the facts

The scripts now go looking for surprising facts beyond Colette's reference file, so check them once before recording. In the same chat, send:

```
List every factual claim in this script, how certain you are of each one, and where I can check it.
```

If anything comes back as less than certain, have it replaced:

```
The claim about … is uncertain. Replace that discovery with one you are certain of.
```

---

## If a script gets something wrong

Tell it exactly what broke, in the same chat:

```
The hook mentions Colette's grandmother. Move that story into item four and rewrite the hook.
```

```
Item one starts at word 240. Cut the hook to under 170 words.
```

```
This sentence is in SPENT-003: "…". Rewrite it.
```

```
Item five has nothing surprising in it. Replace it with a discovery that passes all four tests.
```

```
This line reassures the viewer: "…". Cut it and put information there instead.
```

---

## How you'll know it's working

In YouTube Studio, for each new video: **Analytics → Engagement → audience retention**.

- **The first 30 seconds:** the line should drop much less steeply than on 002 and 003.
- **After the pitch:** no cliff right after it.
- **Average percentage viewed** once the video has spread beyond your subscribers.

Make at least three videos with this project before judging it. Send me the retention graphs and I'll read them with you.
