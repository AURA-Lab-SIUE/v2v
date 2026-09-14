"""Extend Chapter 9.

Three gaps. It is the only chapter in Part III with no worked example from the
corpus, which is odd in a chapter whose whole argument is that level of
measurement is a decision rather than a property of the data: the decision is
easiest to see made. It defines scales and indices and never says how to compute
one, which is where the practical errors are. And it has zero in-text citations
and one orphan reference, Wickham's tidy-data paper, which belongs to Chapter 11
and is uncited here.
"""
import io
import pathlib
import sys

p = pathlib.Path("/Volumes/One Touch/20-research/aura-lab/v2v/chapters/"
                 "_v3-draft/chapter09-measurement-scales-items.qmd")
t = io.open(p, encoding="utf-8").read()

WORKED = '''## One column, measured three ways

The claim that level of measurement is a decision is worth making concrete, because the corpus lets you watch the decision being made and see what each version costs.

Take `title`, the stream title, across the 90,245 snapshots in `twitch_streams_sample`.

**As a nominal variable** it is the string itself. There are **614 distinct titles** in the file. That sounds like a usable category count until you notice what the unit is: the snapshot, taken about once a minute, and a streamer sets a title once and leaves it up for hours. The 228 channels carry **2.7 distinct titles each on average**. So a nominal `title` barely varies within a channel and is almost a second name for the channel, which means a crosstab of title against anything else is really a crosstab of channel against that thing, with 614 categories and most cells empty.

That is not a flaw in the column. It is a mismatch between the level of measurement and the unit of analysis, and it is exactly the failure Chapter 7 describes from the other direction. Measured nominally, `title` wants the unit to be the *stream session*, not the snapshot.

**As a ratio variable** it is the character count. Now the column behaves: mean **48.4** characters, median **44**, running from **0** to **128**. There are **96 snapshots with an empty title**, and a true zero is exactly what makes the mean legitimate, because zero characters really does mean no title rather than a missing one. Every arithmetic operation is available, and the variable now varies within channels too, because a streamer who changes title mid-session changes its length.

**As an ordinal variable** it is those lengths binned. Cut at the tertiles, 33 and 54 characters, and you get **31,335 short, 29,892 medium and 29,018 long**. Three tidy groups, and a median you can report.

Now look at what the third version threw away. The 33-character cut and the 54-character cut are not equal distances apart, so the bins are not comparable widths; a title of 54 characters and one of 128 are both "long" and are not similar; and the mean of 48.4, the thing most worth reporting, cannot be recovered from the bins at all. The binning cost information and bought nothing the ratio version did not already offer, because nothing here required categories.

**Bin when the analysis needs categories, not when the table looks tidier.** The ordinal version is the right choice if your design compares three groups, or if the relationship you expect is a step rather than a slope. It is the wrong choice by default, and by default is how it usually gets made.

'''

COMPOSITE = '''## Computing one

Defining a composite is the conceptual half. The arithmetic has three decisions in it, and each has a wrong answer that is easy to reach.

**Sum or mean.** For a scale they carry the same information, since the mean is the sum divided by a constant. Prefer the **mean**, for one practical reason: it stays on the metric of the original items, so a mean of 4.2 on a five-point scale is immediately interpretable, where a sum of 21 is not until the reader counts your items. It also makes scores comparable across studies that used a different number of items.

**Reverse-coded items must be reversed first.** A well-built scale deliberately words some items in the opposite direction, so that agreeing with everything is not a way through the instrument. Those items have to be flipped before anything is combined: on a 1 to 5 scale, `6 - x`; in general, `(min + max) - x`. Forgetting is common, and its signature is a reliability coefficient that comes out near zero or negative, because half the items are pulling against the other half. Chapter 10 will show you that number; this is what it usually means.

**Missing data.** If a respondent skipped two of eight items, a sum is wrong and a mean of the six they answered is defensible, which is a second argument for the mean. The usual rule is to compute the mean when at least some proportion of items is present, commonly 80 percent, and to treat the case as missing below that. Whatever you choose, decide it before you look and report it, because a rule chosen after seeing which cases it excludes is one of Chapter 2's researcher degrees of freedom.

**Indices have a fourth decision that scales do not: the components are on different metrics.** Hours watched runs to the hundreds, subscriptions held to single digits. Add them raw and the composite is almost entirely the hours column wearing a new name. Convert each component to a common scale first, either by standardizing it, subtracting the mean and dividing by the standard deviation, or by rescaling each to run from 0 to 1. Then decide whether the components should be weighted equally, and say so, because equal weighting is a substantive claim about the construct rather than a neutral default.

DeVellis (2017) is the standard practical treatment if you are building a scale rather than borrowing one, and building one properly is a project in itself rather than a step in a study.

'''

FIX = [
 # NOIR has a canonical source and the chapter is entirely about it
 ("The four levels are easy to remember as **NOIR**: nominal, ordinal, interval, ratio.",
  "The four levels are easy to remember as **NOIR**: nominal, ordinal, interval, ratio. The "
  "scheme is Stevens's (1946), proposed to settle an argument about what counts as measurement "
  "at all, and the argument it settled is the one this section is making: what you may do with "
  "a number depends on what the number is."),
 ("**Likert-type items** present a statement and ask for agreement on an ordered set of options.",
  "**Likert-type items** present a statement and ask for agreement on an ordered set of options. "
  "The format is Likert's (1932) and has outlasted almost everything proposed alongside it."),
]
for old, new in FIX:
    if old not in t:
        if new in t:
            continue
        sys.exit("[ch09] NOT FOUND: %r" % old[:90])
    t = t.replace(old, new)

if "## One column, measured three ways" not in t:
    anchor = "## Where variables come from"
    if anchor not in t:
        sys.exit("[ch09] worked-example anchor not found")
    t = t.replace(anchor, WORKED + anchor, 1)

if "## Computing one" not in t:
    anchor = "## Common response structures"
    if anchor not in t:
        sys.exit("[ch09] composite anchor not found")
    t = t.replace(anchor, COMPOSITE + anchor, 1)

# references: Wickham's tidy-data paper is Chapter 11's and is uncited here
REFS = """## References

DeVellis, R. F. (2017). *Scale development: Theory and applications* (4th ed.). SAGE.

Likert, R. (1932). A technique for the measurement of attitudes. *Archives of Psychology*, *140*, 1-55.

Stevens, S. S. (1946). On the theory of scales of measurement. *Science*, *103*(2684), 677-680. https://doi.org/10.1126/science.103.2684.677
"""
i = t.index("## References")
t = t[:i] + REFS
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("ch09 extended")
