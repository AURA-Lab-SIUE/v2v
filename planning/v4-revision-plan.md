# v4 revision plan, from the seven-reviewer panel

**2026-09-14.** Seven independent reviewers produced roughly 250 findings against
the 27-chapter draft, the 2 practice supplements and the 17 Excel supplements.
This plan is organized by **root cause rather than by finding**, because the
findings are not 250 independent problems. They are seven mechanisms, each of
which produced a family of symptoms, and fixing the mechanism fixes the family.

Convergence is the evidence. Where four or five reviewers who never spoke to each
other reported the same defect, it is real and it is not a matter of taste. Every
numeric claim below was verified against the shipped CSVs before it was written
down.

---

## The seven mechanisms

| # | Mechanism | Symptoms | Reviewers agreeing |
|---|---|---|---|
| A | The v4 assembly split chapters and never reconciled the copies | duplication in 4 chapter pairs; drifted numbers inside the duplicates; the missing sampling chapter | 5 of 7 |
| B | The corpus went 50 → 228 channels and the sweep missed files | index, appendix, ch1, ch6, structured-listening, ch7's "n is 50", every stale Excel range | 6 of 7 |
| C | Figures were never rewired after renumbering | ch24 and ch25 describe figures the book does not contain | 3 of 7 |
| D | Every number is hand-typed with no verification harness | the five-characters contradiction, 226 vs 201, 449 vs 460, 9,271 vs 9,716, and a dozen more | 6 of 7 |
| E | AI drafting templates, never edited out at the shape level | 419 bolded lead-ins, 85 "worth", the antithesis engine, 122 codas | 1 of 7, quantified |
| F | The book's apparatus was never written | no exercises, no key terms, no summaries, no assignment spec, no instructor preface | 2 of 7 |
| G | The book was never treated as a publication artifact | no accessibility statement, no licence scoping, no data terms, no transcripts, CI builds the wrong edition | 1 of 7 |

Two further items are **decisions, not work**, and are held at the end.

---

## Mechanism A: the unreconciled split

The 4th edition was assembled by splitting 3rd-edition chapters and writing new
ones around them. The splits were never reconciled, so several passages exist
twice and the copies have drifted.

Measured, in verbatim sentences over 90 characters shared between files:

| Pair | Shared sentences |
|---|---|
| ch12 ↔ structured-listening | 109 |
| ch08 ↔ ch09 | 24 (17 by my count, 24 by Reviewer 7's looser threshold) |
| ch11 ↔ ch24 | 22 |
| ch08 ↔ ch10 | 16 |
| ch02 ↔ ch05 | 10 |

**The drift inside the duplicates is the proof that nobody reconciled them.** The
identical sentence about the epoch timestamp points to Chapter 11 in ch08 and
Chapter 24 in ch09. The identical paragraph about the corpus says "fifty
channels" in the supplement and "228 channels" in ch12, and points sampling at
Chapter 13 in one and Chapter 11 in the other. **Both of those sampling pointers
are wrong.**

### A1. Write the sampling chapter

Eight cross-references send the reader to Chapter 11 for sampling. Chapter 11 is
"Wrangling the data" and contains no instance of *stratified*, *sampling frame*,
*random sample* or *purposive*. Four reviewers found this independently and the
instructor called it the first of three reasons not to adopt.

**The content is not missing. It was written and left behind.** The 3rd edition's
Chapter 10 was titled *The sample* and runs four sampling sections before turning
to reliability. The v4 split kept the reliability half and dropped the sampling
half. Its figure, `images/fig10-1-stratified-coverage.png`, is still on disk,
unused.

So the fix is the pattern already used twice this week: lift, with declared
repairs. But sampling is core method rather than hands-on practice, so unlike
*The Open Workspace* and *Structured Listening* it becomes a **chapter**, not a
supplement.

Where it goes matters. It must precede Chapter 12, which tells the reader to draw
a sample, and it should follow Chapter 7, which introduces cases and populations.
Merging ch11 and ch24 (A2) frees exactly one slot.

It also has to be rewritten for the census design, not merely lifted: the v4
corpus takes every non-gaming channel and a matched draw of gaming ones, which is
a more interesting sampling story than the v3 one and is the design the book
actually ships. Add unequal-probability and capped sampling, because the corpus
is capped and Mechanism D below shows the cap is doing more damage than the book
admits.

### A2. Merge Chapter 11 and Chapter 24

They are the same chapter. Both open with the same premise in the same words,
both build the same analysis-ready table, both carry the `#bobross` key-mismatch
warning and the 501-unmatched discussion. Chapter 11 does it in R; Chapter 24
does it in prose with the code removed, thirteen chapters later.

Decide which survives. My recommendation: **Chapter 11 keeps the wrangling**, and
Chapter 24 keeps only describing and visualizing, which is what its title
promises and what its missing figures (C1) are for.

### A3. Cut the duplicated sections from Chapter 8

Chapter 8 currently teaches levels of measurement in full, with a figure, and
then Chapter 9 teaches them again verbatim. Chapter 8 teaches reliability and
validity, and then Chapter 10 teaches them again verbatim. Chapter 8's own
closing sentence calls Chapter 9's material "the levels of measurement this
chapter has been using informally," which is false: it defined all four formally.

Chapter 8 should introduce the *existence* of both in about 150 words and hand
off. Chapter 9 owns measurement. Chapter 10 owns reliability and validity.

**Note against myself:** I added a worked example to Chapter 9 yesterday without
noticing Chapter 8 already taught NOIR. That extension is good and it is sitting
in the wrong chapter's duplicate. It stays; Chapter 8's copy goes.

### A4. Decide the owner of the structured-listening material

109 shared sentences with Chapter 12, and both are in the table of contents, so a
reader meets roughly 2,000 identical words twice. Reviewer 7 recommends the
supplement owns it and Chapter 12 keeps a summary. Reviewer 3 recommends the
reverse, on the grounds that Chapter 18 already cites Chapter 12 for the
field-note taxonomy. **Reviewer 3 is right about the cross-reference and Reviewer
7 is right about where a reader goes to do the work.** Resolution: the supplement
owns the procedure, Chapter 12 keeps the manifest/latent and codebook material
that is genuinely content-analytic, and Chapter 18's reference is repointed to the
supplement.

### A5. Cut Chapter 5's paradigm section

Ten verbatim sentences reproducing Chapter 2, which is titled *Three Paradigms*.
Replace with two sentences and a cross-reference.

---

## Mechanism B: the 50 → 228 sweep that missed

Six reviewers reported this. Four files still describe a 50-channel corpus, and
one chapter contradicts itself two paragraphs apart.

**Files still on 50:** `index.qmd`, `appendices/data-dictionary.qmd`,
`chapter01`, `chapter06` (five separate mentions, including inside all three
model prospectuses), `supplements/structured-listening.qmd`.

**Chapter 7 contains both**, fifteen lines apart: *"across 228 channels"* at line
51 and *"your n is 50"* at line 57. It is the unit-of-analysis chapter.

### B1. Rewrite `index.qmd`

It is page one of the book and it describes the 3rd edition: *"Third Edition"*,
*"14 chapters across five parts"*, *"All fourteen chapters are drafted"*, a
50-channel fixture, and a callout announcing the 4th edition as forthcoming. Five
reviewers hit it.

It also states a plan of record I had not seen: tool instruction moves into
**Excel, SPSS and R supplements**. There is no SPSS track and no R track. That is
a scope question for the decisions section.

### B2. Rewrite the appendix

`data-dictionary.qmd` documents a dataset that has not existed since the 3rd
edition: 50 channels, ~35,000 chat rows, ~32,000 stream rows, "25+" games,
messages "1 to 509 chars", and anchor-channel facts that contradict the
workspace supplement. It is in the v4 table of contents, so every variable a
confused student looks up is wrong.

It also prints `509` as the message maximum, which **Chapter 15 identifies as a
documentation error and corrects to 500**. The appendix is the exhibit in the
chapter's own worked example of auditing documentation, and it fails the audit.

And it publishes an absolute path on a personal drive,
`D:/hub/academic/research/sim-lab/v2v/data/report/v2v-data-report.md`, as the
place students should be "pointed to."

### B3. Sweep the remaining 50s, and fix ch7's contradiction

Mechanical once B1 and B2 are done. Chapter 6's model prospectuses need the
sample size reconsidered, not just the channel count swapped, because they
specify a stratified draw the book will now actually teach (A1).

### B4. Rebuild the Excel supplement ranges

Every range in the ch24 supplement is from the 50-channel fixture:
`$H$2:$H$32277` against 90,245 stream rows; `$K$2:$K$104` against 386
channel-game pairs; `$P$2:$P$50` and `$S$2:$S$50` against 226 channels. A student
following these literally gets `unmatched` for most of the file and is told by
the supplement that they made a mistake.

The ch07 supplement is worse because its self-check is arithmetically impossible:
it says *"If the averages run from B4 to B16869"* and then *"`=COUNT(B4:B16869)`.
It must read **61320**."* That range holds 16,866 cells. The same supplement says
*"where there are only 50 real rows"* and prints `228` in its own summary table.

**Every range in all 17 supplements needs recomputing against the shipped row
counts, and every one needs a row-count assertion after it.** This is the largest
mechanical block in the plan and it is the one that most directly strands a
student mid-task.

---

## Mechanism C: the unwired figures

Chapter 24 discusses three figures in prose (*"The figure has an obvious
headline"*, *"The figure shows a clear daily pulse"*, *"The figure shows, first, a
shape both groups share"*) and contains **zero image references**. It then claims
*"Each figure in this chapter carries one"* about alt text. Chapter 25 describes a
confidence-interval figure that is likewise absent.

**All four images exist on disk**: `fig12-1-viewers-by-game.png`,
`fig12-2-chat-by-hour.png`, `fig12-3-msglen-by-context.png`, `ch13-means-ci.png`.
They are the 3rd edition's chapter 12 and 13 figures and were never rewired after
renumbering. `fig13-1-overlap-effect-size.png` and
`fig10-1-stratified-coverage.png` are also unused.

This is an hour of work and it is the difference between a visualization chapter
and an essay about visualization.

Also: ch12 embeds `fig07-1-observation-windows.png`, a filename from the old
numbering.

---

## Mechanism D: no verification harness

Chapter 27 argues at length that numbers must be computed rather than typed:
*"Nothing is typed by hand, so nothing can fall out of date."* **Every number in
all 27 chapters is hand-typed.** There is one live code chunk in the entire
manuscript and it is a `{verbatim}` block. The eleven `build_*.py` scripts compute
the figures out of band and a human copies them in, which is exactly the workflow
Chapter 27 calls "quietly fragile."

The symptoms are the predicted ones. Verified:

| Defect | Where | Correct |
|---|---|---|
| Headline gap called "five characters" 6× and "two and a half" alongside | ch24, ch25, excel/ch25 | **2.43** |
| Channel-level table sums to 201 under text saying 226 | ch25 | **112 / 114**, t(202.5) = 1.16 |
| `!play` count | ch19 | **449**, not 460 |
| Naive LUL substring count | ch19 | **9,716** case-insensitive; 9,271 is the case-sensitive figure, and the sentence claims case-insensitivity |
| Clustering inflation factor | ch07 | **8.16**, not "roughly ten" |
| Distinct titles / mean length | ch08 vs ch09 | 613 vs 614, 48.5 vs 48.4 |
| Distinct stream categories | ch23 | **123** raw, 117 case-folded; the chapter states 117 without saying it folds |
| Messages with no text | ch15 | verify: chapter says four |
| First three message lengths | ch24 | **18, 11, 18**, not 23/441/8 |
| First timestamp | ch24 | **1542578131126**, not …127023 |

### D1. Fix every figure above

### D2. Build the harness

A script that extracts every numeric claim from the prose and checks it against
the build scripts, run in CI. The `*_lift_manifest.json` files are the beginning
of this. Without it, this table regenerates itself at the next revision.

### D3. Two findings that are not typos but errors of substance

**The word-count measure is invalid for 6.32 percent of the corpus.** Chapter 7's
headline figures (4.94 / 4.28 / 5.07 words) define a word as `[A-Za-z']+`.
**9,926 non-empty messages score exactly zero words**: Turkish, Cyrillic, Korean,
Thai. Per channel it is severe: `zilioner` 93.8 percent, `saddummy` 92.3 percent.
The channel-level mean is therefore partly a measure of which channels chat in
Latin script. Chapter 19 catches this exact bug for a different regex and the
book never applies the lesson upstream. I verified those three numbers in Excel
and pronounced them correct, which is the distinction between arithmetic and
construct validity landing on the person checking.

**Chapter 15 states the cap's bias backwards.** It says capping *"almost certainly
makes the measured concentration lower than the platform's."* Measured:

| | singleton-sender rate |
|---|---|
| 137 capped channels | **63.9%** |
| 91 uncapped channels | **43.1%** |

The cap does not truncate heavy posters. It randomly subsamples and thereby
*manufactures* singletons. So Chapter 23's headline structural claim, 62.2 percent
posting exactly once and a Gini of 0.514, is dominated by the sampling design and
the bias runs the other way. Either restrict that analysis to uncapped channels
or report it as a property of the sample.

---

## Mechanism E: the drafting templates

Reviewer 7's counts, and the only reviewer looking for this.

The lexical layer is clean: four watchlist words in 88,000, zero em dashes. That
pass worked and needs nothing further.

The structural layer is not:

| Tell | Count | Target |
|---|---|---|
| Bolded parallel lead-in paragraphs | **419** | under 150 |
| "worth" as hedged emphasis | **85** | under 25 |
| Punchy coda fragments | 122 | keep the ~40 that earn it |
| Antithesis engine | ~100 | about one per chapter |

**The voice target is not a guess.** `policies/academic/writing-style-profile.md`
is canonical and locked, derived from eight author-selected papers, and its
drafting checklist reads: *"No aphorisms, no 'This is why…', no punchy one-line
pivots"* and *"No italics on individual words for emphasis."* Its TL;DR names the
failure mode: *"Avoid the 'academic-essayist' voice: punchy declaratives,
aphorisms, dramatic causal turns… That register is more confident and more
literary than his, and reads as not-his."*

Two instruments sharing no method reach the same verdict. The 419 bolded lead-ins
are the italics prohibition wearing a different glyph.

**But the profile is journal register and this is a textbook.** Its prescriptions
(30-45 word subordinated sentences, pervasive hedging, "we contend",
citation-stacking) must not be imported, and the student reviewer already flagged
the longest subordinated sentences as the ones that lost them. So:

- **Prohibitions transfer whole**: no aphorism, no punchy pivot, no dramatic
  transition, no typographic emphasis-shouting.
- **Prescriptions stay in the journal register.**

### E1. Reduce bolded lead-ins below 150
### E2. Reduce "worth" below 25
### E3. Thin the antithesis and the codas to the instances that earn them
### E4. Rewrite the two passages a skeptical reader would screenshot

Chapter 27's opening keeps **two drafts of the same paragraph**, one of which
narrates the chapter's own title. Its closing is an anadiplosis chain chased by an
aphoristic couplet, in the last position in the book.

---

## Mechanism F: the missing apparatus

**Zero of 27 chapters have exercises, key terms, or a summary.** The only
imperatives addressed to a student sit inside `.graduate-extension` blocks, which
are hidden behind a toggle that is off by default and marked graduate-only.

The word "portfolio" appears once in the book, undefined, in the sentence telling
the student the portfolio is not complete without a reflection.

The instructor's verdict: this alone is a semester of unpaid work and the single
largest reason to pass on the book.

### F1. Exercises and key terms for all 27 chapters
### F2. A stated deliverable: what the student produces, which chapter contributes what, on what schedule
### F3. An instructor preface with a 15-week and a 16-week pacing, core/optional marking, and the dependency Chapter 26 has on Chapter 19

### F4. Make Chapter 27's closing claim true

It tells the reader they have walked a study end to end. They have not. The
Chapter 6 prospectus proposes a directed-versus-broadcast content analysis with
Krippendorff's alpha on 1,500 messages; Chapters 24 and 25 test message length on
156,579. **The study the book sets up is never executed and the study it executes
is never proposed.** Either execute the prospectus or rewrite it to be the study
the book actually runs.

---

## Mechanism G: the book as a publication artifact

### G1. Accessibility

- **236 MB of chapter audio, no transcripts.** WCAG 1.2.1 is Level A, below the
  AA bar, and it is the first thing an automated Ally scan flags.
- **No table in the manuscript has a caption or label.** `tbl-cap` appears zero
  times across ten-plus tables.
- **Graduate content is hidden with `display: none`**, which removes it from the
  accessibility tree with no announcement and no in-flow route to it.
- **The "Graduate" label is CSS generated content**, so it vanishes in the PDF and
  EPUB, where the asides then read as undifferentiated body text.
- **48 unreferenced decorative images** with no `alt=""` convention established.
- Chapter 24's alt-text conformance claim is false (Mechanism C).

### G2. Licensing and data terms

- CC BY 4.0 is applied to the whole work, which embeds 157,080 third-party chat
  messages and quotations of up to 58 words from copyrighted articles. The grant
  is not the author's to make over all of it. Needs a scope-of-licence statement.
- `data-raw/v3/` has no licence, no README, no terms, no provenance note.
- Two promised fair-use excerpts (ch16, ch17) do not exist, so the mechanism the
  book describes for marking third-party material is never demonstrated.

### G3. Front matter

Missing four of the six items an adoption committee checks: citation, correct
edition, accessibility statement, errata contact.

### G4. Build and portability

- **CI renders the 3rd edition.** `publish.yml` runs bare `quarto render`, which
  resolves `_quarto.yml`. An adopter who clones and follows the README gets the
  previous book.
- `CONTRIBUTING.md` points the errata channel at the wrong GitHub org and
  describes a file layout the manuscript does not use.
- Eight passages route students to a course site an adopter does not have, for
  materials the book treats as required.
- The provenance HTML comment I added to `structured-listening.qmd` **renders into
  the published HTML**. Verified. It must move to a YAML field or be deleted.

---

## Mechanism H: copyediting

Reviewer 6 found 31 blockers, 30 majors, 12 minors, and confirmed the em-dash
rule has been honoured completely: zero em dashes, zero curly quotes, zero
doubled spaces, zero repeated words in 120,000 words.

The heaviest recurring faults, each a single sweep:

| Fault | Instances |
|---|---|
| Periods and commas outside closing quotation marks | 28 |
| *data* as singular vs plural | 43 vs 17 |
| Statistical symbols italic vs roman | ~50 |
| Serial comma omitted | 27 of 614 |
| Three-or-more-author citations spelled out instead of `et al.` | 15 |
| Leading zeros on bounded coefficients | mixed throughout |
| British spellings | 11 |
| Number style, words vs numerals | ~200 if converted to APA |
| `intercoder` vs `inter-coder` | 12 vs 10 |
| `pre-registration` vs `preregistration` | 16 vs 3 |

Plus genuine errors: comma splices in ch02, ch04, ch08, ch26; a subject-verb
failure in ch03; a blockquote in ch06 that swallows the body text and runs the
attribution into the next sentence; two reference entries for Likert and two for
Lombard et al. that disagree with each other; a Landis and Koch citation with no
reference entry; and Chapter 27's reference list out of alphabetical order.

---

## The two decisions

### Decision 1: the corpus in the public repository

`AURA-Lab-SIUE/v2v` is public and `data-raw/v3/` is tracked: 157,080 real
usernames with verbatim message text, and `respondents.csv` carrying per-person
behavioural profiles of 6,559 named accounts.

Chapter 3 states the rule the repository breaks: *"not aggregating data in ways
that would re-identify individual users, not republishing entire chat logs
verbatim"*, and names the hazard as *"Aggregation risk (combining individually
harmless data points to create identifiable profiles)."*

Against that: Twitch chat is public, the handles are pseudonymous, and corpora
like this circulate routinely. The reviewer's point is not that the data is
scandalous. It is that **the book's own chapter forbids what the book's own
repository does**, that there is no licence or terms file, and that the corpus
demonstrably contains EU and UK data subjects with no GDPR consideration anywhere
in a chapter that covers Belmont, IRB tiers and AoIR.

Options: publish a hashed-sender, text-free derivative and hold the full corpus
under a data-use agreement; or keep it and add a data statement arguing the case
explicitly against AoIR 3.0 and reconciling it with Chapter 3. Dropping
`respondents.csv` in its current form is advisable either way.

**Not my call. Nothing has been touched.**

### Decision 2: the graduate layer, and the profile's own provenance

Already deferred to Fall 2027, which stands. Two things to note for when it
resumes:

18 of 20 new chapters have no graduate extensions, so the graduate edition does
not currently satisfy the cross-listing differential the README cites. And all 25
existing graduate boxes are post-positivist, so a graduate student doing an
ethnography or a criticism has no graduate-level guidance anywhere.

### The profile's provenance: resolved

I had flagged that three of the eight papers behind
`policies/academic/writing-style-profile.md` are 2025, against the author's
statement that his pre-2024/5 work is the clean baseline, and that a profile
partly derived from AI-assisted prose would be certifying the wrong register.

**Resolved by the owner, 2026-09-14: heavily co-authored papers are fine to
include, because co-authorship means a greater degree of human involvement in the
prose.**

That narrows the concern almost to nothing. Of the three 2025 sources, two are
second-author (*Meeting needs*, CHBR; *The Hyperpersonal Model of Communication in
virtual meetings*, HICSS 58) and therefore qualify under that rule. Only one is
2025 and first-author (*Stress and coping in VRChat*, CHBR).

So seven of the eight sources are either pre-2024 or heavily co-authored. **The
profile stands and no re-derivation is needed.** The single 2025 first-author
paper is not worth removing from a corpus of eight, and the author selected all
eight himself.

The practical consequence for Mechanism E is that the profile's prohibitions can
be applied to the v4 voice pass without qualification.

---

## Order of work

1. **Mechanism D1** — the numbers. Nothing else matters if the book contradicts
   itself on its own finding, and it is the cheapest tier.
2. **Mechanism B** — index, appendix, the remaining 50s, then the Excel ranges.
   The appendix is the highest-leverage single file in the manuscript.
3. **Mechanism C** — wire the figures. One hour.
4. **Mechanism A** — the sampling chapter, the ch11/ch24 merge, the ch8 cuts.
   This is the largest structural block and it is what makes the book teachable.
5. **Mechanism G4 + H** — the build, then the copyedit sweeps, which are
   mechanical and safe once the structure has stopped moving.
6. **Mechanism E** — the voice pass. Last, because rewriting prose that is about
   to be cut or merged is wasted work.
7. **Mechanism F** — the apparatus. Largest writing block, and the one an adopter
   most wants.
8. **Mechanism G1-G3** — accessibility, licensing, front matter.

D3, F4 and the two decisions are held for the owner.
