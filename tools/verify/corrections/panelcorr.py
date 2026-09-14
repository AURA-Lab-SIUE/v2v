"""Record the owner's correction to Reviewer 7's provenance briefing.

The brief told Reviewer 7 that chapters 1, 3, 4, 5, 6, 8 and 11 were "older,
more heavily human-edited material", and invited it to treat a finding that did
not cluster in the newer chapters as evidence the human editing worked. The
owner has since corrected that: the 3rd edition was also largely AI-drafted and
only lightly tweaked, because it was an internal artifact aimed at his own
teaching and was never prepared for outside adoption.

That removes the control. Recording it here because the panel is meant to be
re-runnable, and re-running it on a bad premise would reproduce the bad
inference.
"""
import io
import pathlib
import sys

p = pathlib.Path("/Volumes/One Touch/20-research/aura-lab/v2v/planning/v4-review-panel.md")
t = io.open(p, encoding="utf-8").read()

NOTE = """
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
`C:\\pythia\\policies\\academic\\voice-observations.md`, the ledger governed by
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

"""

if "Correction to Reviewer 7's brief" in t:
    print("already recorded")
    sys.exit(0)

anchor = "## The instruction they shared"
if anchor not in t:
    sys.exit("anchor not found")
t = t.replace(anchor, NOTE.lstrip() + "\n" + anchor, 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("correction recorded in the panel document")
