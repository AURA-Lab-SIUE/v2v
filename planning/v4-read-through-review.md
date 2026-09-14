# 4th edition: read-through review and its resolutions

**Reviewed 2026-09-14; resolved the same day.** Against the full 27-chapter draft
as rendered by `tools/render-v4.sh`, plus the two practice supplements and the
17 Excel supplements. Read the book at `_preview-v4/index.html`; it is gitignored
and regenerable, and the build cannot touch `docs/`.

The prose is in good shape. Every substantive problem was structural: things the
draft inherited from being assembled out of a 14-chapter book, not things wrong
with the new writing.

---

## The part structure, now written down

There was no table of contents for the 4th edition anywhere in the repo. The
chapters state their own structure in prose, consistently, and `_quarto-v4.yml`
now records it with the citation for every boundary.

| Part | Chapters |
|---|---|
| I: Foundation | 1 to 3 |
| II: Planning | 4 to 6 |
| III: Quantitative Methods | 7 to 15 |
| IV: Qualitative Methods | 16 to 21 |
| V: Rhetorical and Critical Analysis | 22, 23 |
| VI: Analysis and Publication | 24 to 27 |
| Practice Supplements | The Open Workspace, Structured Listening |
| Excel Supplements | 17, for chapter 7 and chapters 12 to 27 |

My first attempt split Part III at chapter 11 and put the qualitative chapters in
Part V. It rendered cleanly and it was wrong. What caught it was chapter 2 saying
"Part IV works inside this paradigm" about interpretive work, and chapter 15
saying "Part III ends here, and with it the quantitative methods half."

**Still open:** whether Part V should exist at two chapters. Folding 22 and 23
into Part IV would give five parts of 3, 3, 9, 8, 4.

## RESOLVED: the 3rd edition's Chapter 2 and Chapter 7

Two chapters the 4th edition dropped were carrying material the rest of the book
depends on. Both are now **practice supplements**, which is where hands-on
material belongs: installers, menus and version numbers date faster than
anything else in the book, and the reasoning around them does not date at all.

**`supplements/open-workspace.qmd`**, lifted from v3's "The Open Workspace":
the tool ecology, the install sequence, first contact with the ten rows of
`stream_log`, and the `v2v` package. Its fixture description is updated to the
228-channel corpus.

**`supplements/structured-listening.qmd`**, lifted from v3's "Structured
listening": immersion, the three modes of attention, field notes, the edge-case
log, and knowing when to stop. Chapter 8 depends on the field notes it produces,
so it has to be worked through before operationalizing anything. Chapter 18 is
where observation is treated as a *method*; this is the practice.

Both lifts declare their repairs in `tools/verify/corrections/v4_wire.py` rather
than making them by hand.

**What stayed in the book.** The conceptual half of old Chapter 2 was not
supplemental and could not go: the Open Science Collaboration replication study,
the replication crisis, researcher degrees of freedom, the point-and-click
problem and code-as-documentation. That is now a section of Chapter 2, "When the
answers did not hold up", placed after the social scientific paradigm because it
is that paradigm accounting for its own failure. It has the side effect of making
chapter 3's and chapter 6's existing references to "Chapter 2's discussion of
researcher degrees of freedom" correct again without touching them, and it takes
chapter 2 from 1,755 words to 2,458.

## RESOLVED: the seven carried-over chapters

**They have moved.** Editing them for the 4th edition made them wrong for the
3rd, and they were still sitting in `chapters/`, which is what the live book
renders from on main. A merge would have silently broken the published edition.
All seven now live in `chapters/_v3-draft/` alongside the other twenty, with their
relative paths deepened a level, and `chapters/*.qmd` is byte-identical to what main
publishes. The two editions can no longer corrupt each other.

Chapters 1, 3, 4, 5, 6, 8 and 11 were carried over unchanged, and their
cross-references were written when chapters 2, 7, 9, 10, 12, 13 and 14 held
completely different content. All of them now point at the right place. Chapters
4 and 5 turned out to need nothing; every reference in them was to chapters 3 to
6, which did not move.

- **ch01's roadmap** described a five-part, fourteen-chapter book. Rewritten for
  the six parts above, with a paragraph on what the supplements are for.
- **ch01's looking-ahead** promised that Chapter 2 would install the tools.
  Rewritten to promise the paradigms and point at the workspace supplement.
- **ch01** "Chapter 5 explores these paradigms in more depth" is now Chapter 2.
- **ch06's looking-ahead** promised structured listening from Chapter 7 and now
  describes research design, then sends the reader to the supplement.
- **ch08** pointed four times at Chapter 7's field notes and observation log, at
  Chapter 2 for the data preview, and at Chapter 13 for inferential tests. Now:
  the supplements, and Chapter 25.
- **ch08's looking-ahead** promised that Chapter 9 was first contact with R. It
  is Measurement, Scales and Items, and the passage now says what 9 and 10
  actually do.
- **ch11** pointed five times at Chapter 12 for visualizing and once at Chapter
  13 for tests. Those are Chapters 24 and 25. Its looking-ahead now hands off to
  Chapter 12 for content analysis and forward to Chapter 24 for the figures.
- **ch07 (draft)** still described "the 50 sampled channels".

## RESOLVED: six live chapters were carrying 4th-edition data

Found while separating the editions, and worth recording because it had been
sitting in the branch since the re-sample. Commit `d5a18d5` updated chapters 8,
9, 10, 11, 12 and 13 **in `chapters/`**, the 3rd edition's own files, to the
228-channel census: 157,080 rows where the published book says 35,267, a peak
hour of 22:00 where it says 13:00, a gap of 29.54 against 31.96 where it says
28.49 against 33.70.

That was invisible because this branch never renders the live book. It would
have become visible the moment `v3-draft` merged to main, and it is the same
inconsistency the package hold exists to prevent: 4th-edition figures on a site
whose readers hold the 50-channel fixture.

All six are restored to `origin/main`, and every file in `chapters/` on this
branch is now byte-identical to what is published. Chapters 8 and 11 keep their
census figures in the 4th edition, in their `_v3-draft` copies, where they
belong. Chapters 9, 10, 12 and 13 are superseded by new drafts, so their census
versions were not needed anywhere.

One thing to lift back out of history. The reverted `chapters/chapter10.qmd`
carried the **reproducible** version of the kappa example, wired to
`data-raw/v3/build_reliability.py` and `pilot_coding.csv`, with the coder counts
and `v2v::reliability()` call written out. It is at `d5a18d5:chapters/chapter10.qmd`.
That is the passage to adapt when reconnecting the 4th edition's chapter 10,
which currently has the right numbers and no fixture behind them.

## DEFERRED to Fall 2027: the graduate layer

18 of the 20 new chapters have no `graduate-extension` blocks, against 3 to 5 per
chapter throughout the 3rd edition. Only chapter 12 (4 blocks) and chapter 14 (1)
have any, so with the graduate toggle on, most of the 4th edition is currently
identical to the undergraduate version.

**Owner decision, 2026-09-14: not before Spring, and the graduate course does not
run again until Fall 2027.** So this does not gate anything, and the time is
better spent on a question that was never actually asked: what, in the
literature and in practice, distinguishes a graduate methods textbook from an
undergraduate one? The 3rd edition's four pillars (a priori power, preregistration,
two-coder reliability, audit trail) were a reasonable guess. The 4th edition's
graduate layer should be built on something better than a guess, and there is a
year to do the reading.

The existing blocks in the seven carried-over chapters and the two practice
supplements are untouched and still work.

## Fixed while reading

- **ch19** claimed "6.3 percent contain no alphabetic characters at all." The
  rule behind it was `[A-Za-z]`, and 5,957 of those 9,944 messages are Cyrillic,
  Hangul, Thai and Greek. They have letters. Under a rule that counts any
  alphabet the figure is 2.5 percent. Rewritten to give both numbers and make the
  gap the lesson, since it is chapter 9's validity problem inside one regular
  expression.
- **ch20** still carried the old fixture's adjacency figures (6.5 percent
  immediate, median 16, 22 percent within five, 20 percent never). Correct
  figures are 10, 11, 26 and 18 percent, on 89 addressed messages. The chapter
  also described the measurement as covering "every message in the corpus"; it is
  a thousand consecutive turns from one channel, and now says so.
- **ch26** quoted ch20's stale 6.5 percent.
- **ch23** called its own surroundings Part IV. It is Part V.
- **ch27** had an orphan `:::` closing a fenced div that was never opened, which
  Quarto warned about on every render.
- **ch12** linked an image as `../images/`, which from `chapters/_v3-draft/`
  resolves to a directory that does not exist.
- Chapters 12, 15 and 24 still said "fifty channels".

## Still open

**Chapter audio.** All 7 carried-over chapters carry a `chapter-audio` block and
none of the 20 new ones do, so a reader loses the audio at chapter 2 and gets it
back at chapter 3. Twenty recordings, and they cannot be made until the prose
stops moving.

**Length.** New chapters average about 2,690 words against 3,780 for the
carried-over ones. Chapters 2, 26 and 27 are no longer outliers: 2 went from 1,755
to 2,458 when the replication-crisis material came back into it, 26 from 1,772 to
2,948 and 27 from 1,867 to 2,891.

**Chapter 26** gained a section on sampling, which it had named as an integration
point and never explained: the two strands sample on opposite logics, and in an
explanatory sequential design the quantitative results choosing the qualitative
cases *is* the integration. It also now contains a joint display rather than a
promise of one in the supplement, built on the three pairings the chapter already
names, with each row labelled by its fit. And it gained a section on what a reader
should check, since the chapter said what a bad mixed methods study looks like and
not what to verify in a good one.

**Chapter 27** was missing the section its own opening promised. It says the report
is "close to a single action: one click" and cited Knuth (1984) in its reference
list, and both belonged to a passage lost when the 3rd edition's Chapter 14 was
folded in. That passage is lifted back, with its repairs declared. It also gained a
section on the title and abstract, which are the only part of a paper most people
read and which the chapter did not mention, and one on where materials are actually
deposited, since the open-materials section said what to share and not where or how
to make it citable. Three errors fixed along the way: the Methods paragraph
attributed the codebook and the sampling procedure to the wrong chapters, the
clustering penalty was still "a factor of ten" against the current 8.16, and the
bot-command figure was still 46 percent against 45.

The short ones now are ch09 (1,913), ch23 (2,001) and ch22 (2,022).

**The kappa example in ch10 is a thought experiment that does not need to be.**
It says "Imagine the codebook included a loosely worded variable", and its
numbers (80 percent observed, 0.797 expected, kappa 0.015) are correct. The old
chapter 10 wired the same example to a real fixture,
`data-raw/v3/build_reliability.py` and `pilot_coding.csv`, so a reader can run
it. The v4 chapter dropped the wiring and kept the numbers. Reconnecting it is a
paragraph.

**No sampling chapter.** v3 had one, "The sample". In v4 sampling appears inside
chapter 13 for surveys and chapter 15 for the fixture's own stratified design,
and nowhere as a topic. The structured-listening supplement's reference to
"statistical sampling in Chapter 13" is the best available target rather than a
good one. Worth deciding whether Part III wants a sampling chapter.

**Supplement coverage.** Chapters 1 to 6 and 8 to 11 have no Excel supplement.
Most do not need one; 9 and 10 plausibly do, and chapter 10's pilot-coding
fixture already exists.

**Nothing to report on em dashes.** Zero across all draft chapters and all
supplements.
