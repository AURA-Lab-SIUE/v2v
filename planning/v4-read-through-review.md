# 4th edition: read-through review

**2026-09-14.** Against the full 27-chapter draft as rendered by `tools/render-v4.sh`,
plus all 17 Excel supplements. Read the book at `_preview-v4/index.html`; it is
gitignored and regenerable, and the build cannot touch `docs/`.

The prose is in good shape. Every substantive problem below is structural: things
the draft inherited from being assembled out of a 14-chapter book, not things
wrong with the new writing.

---

## 1. The part structure was only ever stated inside the chapters

There was no table of contents for the 4th edition anywhere in the repo. The
chapters state their own structure in prose, consistently, and it is now written
down in `_quarto-v4.yml`:

| Part | Chapters |
|---|---|
| I: Foundation | 1 to 3 |
| II: Planning | 4 to 6 |
| III: Quantitative Methods | 7 to 15 |
| IV: Qualitative Methods | 16 to 21 |
| V: Rhetorical and Critical Analysis | 22, 23 |
| VI: Analysis and Publication | 24 to 27 |

My first attempt split Part III at chapter 11 and put the qualitative chapters in
Part V. It rendered cleanly and it was wrong. What caught it was chapter 2 saying
"Part IV works inside this paradigm" about interpretive work, and chapter 15
saying "Part III ends here, and with it the quantitative methods half."

**Worth deciding:** whether Part V should exist at two chapters. Chapters 22 and 23
are the only ones in it, and 23 already slips and calls its own surroundings Part
IV (now corrected). Folding them into Part IV and renaming it would give five
parts of 3, 3, 9, 8, 4.

## 2. The 3rd edition's Chapter 2 is gone and nothing replaced it

The old Chapter 2, "The Open Workspace", covered the tooling, version control,
reproducibility, researcher degrees of freedom, and the reader's first contact
with the dataset. The 4th edition's Chapter 2 is "Three Paradigms", which is a
better chapter and covers none of that.

Nothing else in the 27 covers it either. Searching every draft chapter for
RStudio, version control or reproducibility returns one file, chapter 27, and
only in the sense of open materials at publication time.

Four chapters still point at the chapter that is no longer there:

- **ch01** "Chapter 2 turns to the technical infrastructure that makes research reproducible"
- **ch01** "Chapter 2 also brings you face to face with the dataset for the first time"
- **ch03** "Chapter 2's discussion of researcher degrees of freedom returns here"
- **ch06** "the researcher degrees of freedom Chapter 2 introduced"
- **ch08** "Chapter 2: channel, title, game, viewers, date"

So researcher degrees of freedom is used by three chapters and introduced by
none, and the dataset is never formally introduced. This is the one gap I would
fix before showing the draft to anybody outside.

**Options:** restore the workspace material as a new chapter (which makes it a
28-chapter book), fold the reproducibility half into chapter 1 and the dataset
introduction into chapter 8, or write a short Part I chapter that does both.
I did not choose, because it changes the shape of the book.

## 3. The seven carried-over chapters still talk to the 3rd edition

Chapters 1, 3, 4, 5, 6, 8 and 11 are carried over unchanged, and their
cross-references were written when chapters 2, 7, 9, 10, 12, 13 and 14 held
completely different content. Roughly 25 references are now wrong. The worst:

**ch01's roadmap section** describes the old structure outright: "Part III:
Operationalization (Chapters 7 to 9)", "Part IV: Execution (Chapters 10 to 12)",
"Part V: Inference and publication (Chapters 13 to 14)". All three are wrong, and
it is the passage a reader hits first.

**ch11** points five times at "Chapter 12" for visualizing and charting, and at
"every test in Chapter 13". In the 4th edition those are chapter 24 and chapter
25; chapter 12 is Quantitative Content Analysis and chapter 13 is Survey
Research.

**ch08** points at "Chapter 7's observation log" and "the structured listening in
Chapter 7" (now Research Design), "Chapter 9 is first contact with the data inside
R" (now Measurement, Scales and Items), and "Chapter 10 covers those statistics"
(now Reliability and Validity).

**ch06** "Chapter 7 begins Part III" is right about the part and wrong about the
content: it promises structured listening and delivers research design.

These are mechanical to fix once the chapter 2 question above is settled, because
several of them want to point at whatever replaces it. I left them alone for that
reason rather than because they are hard.

## 4. Two features present in every old chapter and absent from every new one

**Chapter audio.** All 7 carried-over chapters carry a `chapter-audio` block. None
of the 20 new ones do. A reader moving from chapter 1 to chapter 2 loses the
audio and gets it back at chapter 3.

**Graduate extensions.** The 3rd edition averages 3 to 5 `graduate-extension`
blocks per chapter, and the read-time graduate toggle in `_quarto.yml` is built
around them. Of the 20 new chapters, 18 have none. Only chapter 12 (4 blocks) and
chapter 14 (1) have any. With the toggle on, most of the 4th edition is
indistinguishable from the undergraduate version.

That is 18 chapters times 3 or 4 blocks. It is the largest remaining piece of
writing in the project, and it is worth scoping deliberately rather than
discovering late.

## 5. Length is uneven in a way a reader will feel

Carried-over chapters average about 3,780 words. New chapters average about
2,690. The gap is visible where they sit next to each other:

| | words |
|---|---|
| ch01 (carried) | 4,303 |
| **ch02 (new)** | **1,755** |
| ch03 (carried) | 3,597 |

Chapter 2 is doing foundational work at 40 percent of the length of the chapters
on either side of it. Also short: ch26 (1,772), ch27 (1,867), ch09 (1,913),
ch23 (2,001), ch22 (2,022).

Chapter 27 closing a 27-chapter book in 1,867 words is the one I would look at
after chapter 2. Neither is padding work; both have obvious material they stop
short of.

## 6. Things I fixed while reading

- **ch19** claimed "6.3 percent contain no alphabetic characters at all." The rule
  behind it was `[A-Za-z]`, and 5,957 of those 9,944 messages are Cyrillic,
  Hangul, Thai and Greek. They have letters. Under a rule that counts any
  alphabet the figure is 2.5 percent. Rewritten to give both numbers and make the
  gap the lesson, since it is chapter 9's validity problem inside one regular
  expression.
- **ch20** still carried the old fixture's adjacency figures (6.5 percent
  immediate, median 16, 22 percent within five, 20 percent never). Correct
  figures from the regenerated `adjacency.csv` are 10, 11, 26 and 18 percent, on
  89 addressed messages. The chapter also described the measurement as covering
  "every message in the corpus"; it is a thousand consecutive turns from one
  channel, and now says so.
- **ch26** quoted ch20's stale 6.5 percent. Updated.
- **ch23** called its own surroundings Part IV. It is Part V.
- **ch27** had an orphan `:::` closing a fenced div that was never opened, which
  Quarto warned about on every render.
- **ch12** linked an image as `../images/`, which from `chapters/_v3-draft/`
  resolves to a directory that does not exist. Now `../../images/`.
- Chapters 12, 15 and 24 still said "fifty channels".

## 7. Smaller notes

**The kappa example in ch10 is a thought experiment that does not need to be.**
It says "Imagine the codebook included a loosely worded variable", and its
numbers (80 percent observed, 0.797 expected, kappa 0.015) are correct. The old
chapter 10 wired the same example to a real fixture,
`data-raw/v3/build_reliability.py` and `pilot_coding.csv`, so a reader can run it.
The v4 chapter dropped the wiring and kept the numbers. Reconnecting it is a
paragraph, and it is the difference between a worked example and an assertion.

**Supplement coverage.** 17 supplements for 27 chapters: 7, then 12 through 27.
Chapters 1 to 6, 8, 9, 10 and 11 have none. Most of those do not need one;
chapters 9 and 10 plausibly do, since measurement and reliability are exactly
where a spreadsheet earns its place, and chapter 10's pilot-coding fixture already
exists.

**Nothing to report on em dashes.** Zero across all 20 draft chapters and all 17
supplements.

---

## What I would do next, in order

1. Decide the Chapter 2 question in section 2. It gates section 3.
2. Fix the ~25 cross-references in the seven carried-over chapters, ch01's
   roadmap first.
3. Scope the graduate extensions for 18 chapters.
4. Extend chapter 2 and chapter 27.
5. Reconnect ch10's kappa example to its fixture.
