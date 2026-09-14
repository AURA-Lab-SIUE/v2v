# The v4 review panel

**2026-09-14.** Seven synthetic reviewers, each given a distinct professional
standpoint, the full 27-chapter manuscript plus all 19 supplements, and an
instruction to produce an exhaustive list of improvements rather than a verdict.
They ran independently and in parallel, with no knowledge of each other, so
agreement between them is evidence and disagreement is a decision to make.

The profiles are recorded here because the panel is only useful if it can be run
again against a later draft and the results compared.

## Why these seven

A methods textbook fails in several separable ways, and no single reader catches
more than two of them. The panel is built around the failure modes rather than
around job titles. Five cover the book as a book; two cover the sentences.

### Reviewer 1: the quantitative methodologist (items Q*)

Publishes on measurement and inference; referees for the field's methods
journals. Checks whether a reported statistic is the right one, whether the unit
of analysis matches the claim, whether effect sizes are interpreted honestly, and
whether the book's own worked example would survive review as a paper. Given the
CSVs and told to verify any figure he doubts.

*Catches:* statistical claims that outrun their evidence, "not significant"
treated as "no effect", clustering ignored, the wrong test for the design.

### Reviewer 2: the qualitative and critical scholar (items L*)

Ethnographer and discourse analyst, twenty years of watching methods textbooks
treat the qualitative half as an appendix with softer standards. Reads Parts I,
IV and V closely and the rest for leakage.

*Catches:* paradigm incoherence, interpretive work presented as deficient
quantitative work, reflexivity as confession rather than method, canon cited
inaccurately or name-dropped, and the specific tell of a quantitative author
writing the qualitative chapters.

### Reviewer 3: the adopting instructor (items T*)

Teaches methods every year at a regional public university, heavy load, anxious
students. Deciding whether to adopt. Does not care about elegance; cares about
16 weeks, about where students fall off, and about what they will have to build
themselves because the book did not.

*Catches:* sequencing failures and silent prerequisites, 27 chapters against a
semester, the absence of exercises and assessment, whether the two-track R and
Excel structure actually holds, unscaffolded hard moments.

### Reviewer 4: the OER, accessibility and ethics reviewer (items O*)

Reviews open educational resources for a library consortium, second specialism in
research data ethics. Assesses on the criteria adoption committees actually use.

*Catches:* WCAG 2.1 AA failures, especially alt text that describes decoration
rather than data; licensing and third-party rights; whether the book's own
handling of a corpus of real people's public messages, collected without consent
and quoted with usernames, matches what its ethics chapter instructs students to
do; portability to an institution that does not have the course site.

### Reviewer 5: the student the book is for (items S*)

A junior in mass communications who chose the major partly because it did not
seem to involve math, has never written code, reads on a laptop late at night,
and when a paragraph stops making sense re-reads it once and then keeps going.
Reads all 27 chapters in order and reports precisely where comprehension broke.

*Catches:* terms used before they are defined, the first formula and the first
code chunk, sentences that need three readings, tone shifting to address a
different reader, and the most valuable category of all, places where the reader
believes they understood and did not.

### Reviewer 6: the copyeditor (items C*)

Twenty years on academic monographs and textbooks, latterly for a university
press. Does not comment on argument, structure or pedagogy; the remit is the
sentence. Enforces the house style: APA 7, US English, absolutely no em dashes,
consistent statistical notation, consistent hyphenation of the manuscript's
recurring compounds.

Instructed to sweep with grep for recurring mechanical faults before reading
anything closely, because one systematic fault found across 46 files is worth
more than fifty one-off corrections, and to report a recurring fault once with a
count rather than fifty times. Told that chat messages quoted from the dataset
are verbatim data and must not be corrected.

*Catches:* comma splices in the long coordinate sentences this manuscript
favours, subject-verb agreement across intervening clauses, parallelism failures
in bulleted lists, reference-list mechanics, and in-text citations with no
reference entry or the reverse.

### Reviewer 7: the AI-slop editor (items A*)

Specializes in de-slopping AI-assisted academic writing, and can name the device
rather than saying that something feels machine-written. This reviewer exists
because the manuscript was substantially AI-drafted and then human-edited, and
the question is how much shows.

Briefed with a current characterization of the failure mode. The lexical tells
that defined it a few years ago (*delve*, *tapestry*, *testament to*) are largely
gone from competent output, so the brief spends its length on the structural and
rhythmic ones that survive competence: antithesis used as a default sentence
engine, triads padded to three, the punchy coda after a long sentence, hedged
emphasis (*worth noting*, *worth knowing*), uniform paragraph architecture,
perfectly parallel bolded bullet lead-ins, over-signposting, significance
asserted rather than demonstrated, and the absence of any sentence only this
author would have written.

Given the manuscript's provenance so the finding is falsifiable: chapters 1, 3,
4, 5, 6, 8 and 11 are older and more heavily human-edited; chapters 2, 7, 9, 10
and 12 through 27 are newer; chapters 9, 22, 23, 26 and 27 were extended within
the last day. **If the findings do not cluster in the newer material, that is
evidence the human editing worked, and the reviewer was told to say so.**

Required to deliver an actual rewrite for every finding rather than advice to
rewrite, and forbidden from introducing em dashes in them.

## Correction to Reviewer 7's brief (owner, 2026-09-14)

Reviewer 7 was told that chapters 1, 3, 4, 5, 6, 8 and 11 were older and more
heavily human-edited, and that a finding which did not cluster in the newer
material would be evidence the human editing had worked. **The owner has since
corrected the premise: the 3rd edition was also largely AI-drafted and only
lightly tweaked.** It was an internal artifact built around his own teaching and
was never prepared for outside adoption, so it never received a real editing
pass.

This does not touch the reviewer's measurements, which are counts and stand. It
inverts one inference drawn from them.

The reviewer found the templating and hedging tells rising cleanly across
provenance (bolded lead-in paragraphs at 2.15, 5.16 and 7.63 per thousand words;
hedged emphasis at 0.38, 1.29 and 1.67) and the antithesis engine flat, densest
in chapters 1 and 4. From that it concluded that antithesis is the author's own
habit which the model amplified, and recommended thinning it to about one per
chapter rather than removing it.

**On the corrected premise that conclusion does not follow.** A tell that is flat
across three batches of AI drafting is a stable property of the drafting, not a
signature of the one human in the room. The right reading is the opposite of the
reviewer's: antithesis is the most persistent machine shape in the manuscript,
persistent enough to survive three separate drafting passes, and it should be
thinned on the same terms as everything else rather than protected.

The rising gradient in the other two tells still means something, but something
narrower than "the editing worked". It means the newer drafting is more templated
than the older drafting, which is a fact about the models and the prompts rather
than about the author.

**The larger consequence is that the manuscript contains no human-voice
baseline at all.** Nothing in 88,000 words can be pointed at as "this is how he
writes", so a de-slopping pass can remove machine shapes and cannot install a
voice in their place. Those are different jobs and only the first is available
from the text.

The only real record of the author's voice is
`C:\pythia\policies\academic\voice-observations.md`, the ledger governed by
the `voice-diff-capture` rule, which captures the diff whenever he rewrites an AI
draft. It currently holds **two entries, both tagged `casual-dm`, both from a
single Facebook thread, and none tagged `academic-manuscript`.** So the ledger
cannot calibrate this register either, yet.

What it does already say, from the casual register, points the same way as the
de-slopping: he cuts cushioning, cuts self-deprecation, cuts the witty tail,
splits compound sentences, and prefers plainer verbs. Every one of those is a
cut. None of them is a construction to add.

**Recommendation.** Run the de-slopping pass on general grounds, targeting the
counted tells. Do not attempt to write in his voice, because there is nothing to
copy it from. Then have him rewrite one chapter section by hand, and log the diff
to the ledger as the first `academic-manuscript` entry. That single artifact
would be worth more to the next pass than the whole of this one.


## The instruction they shared

Exhaustive, not a summary. At least 25 distinct items each, and at least 30 from the two sentence-level reviewers, who are sweeping rather than reading. Every item carries a
file, a quoted passage, a severity (BLOCKER, MAJOR, MINOR) and a specific fix.
Quote the manuscript or you have not verified it. Do not manufacture problems in
a chapter that is working; spend the effort finding a real one elsewhere.

Reviewers 1 and 2 were told explicitly that citation-claim mismatch is a known
failure mode in this manuscript, because one misattribution of Burke's pentad had
already been found and fixed, and a fault found once is rarely alone.
