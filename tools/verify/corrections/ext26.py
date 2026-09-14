"""Extend Chapter 26.

Three gaps. The chapter names sampling as an integration point at the methods
level and never says how the sample is drawn. It promises a joint display and
sends the reader to the supplement to see one, which means the chapter's central
artifact never appears in the chapter. And it says what a bad mixed methods
study looks like without saying what a reader should check in a good one.
"""
import io
import pathlib
import sys

p = pathlib.Path("/Volumes/One Touch/20-research/aura-lab/v2v/chapters/"
                 "_v3-draft/chapter26-mixed-methods.qmd")
t = io.open(p, encoding="utf-8").read()

SAMPLING = '''## Two strands, two sampling logics

The strands do not sample the same way, and trying to make them is the error underneath a good proportion of weak mixed methods work.

A quantitative sample is drawn to **represent**: the question is whether what holds in the sample holds in the population, so it wants size, and randomness where it can get it, and it worries about who was left out. A qualitative sample is drawn to **inform**: the question is what the phenomenon is like, so it wants cases chosen because they can say something, and it stops when new cases stop bringing anything new. Teddlie and Yu (2007) set out the typology; the practical consequence is that "we interviewed a random subsample of survey respondents" is usually a mistake, because randomness buys representation the qualitative strand was not making a claim about, and spends the places you had for the people worth talking to.

**In an explanatory sequential design, the quantitative results choose the qualitative cases, and that choice is the integration.** It is the one methods-level decision that makes the design more than two studies in sequence, so it is worth making deliberately and writing down. The usual options:

**Extreme cases.** The channels with the largest and smallest effect, the respondents at the top and bottom of a scale. Good for finding the mechanism, because whatever drives the pattern should be most visible where the pattern is strongest.

**Typical cases.** Cases near the middle of the distribution. Good when the finding is about the ordinary and you want to describe it rather than explain its extremes.

**Confirming and disconfirming cases.** Deliberately including the cases that do not fit the quantitative result. This is the one most often skipped and the one that most often changes the paper, because a model of why the effect happens should also account for where it does not.

**Cases at the intersection of two variables.** The high-volume channel that is nonetheless quiet, the heavy user who reports low satisfaction. Useful when the interesting thing is the combination rather than either variable alone.

Sample sizes follow the same split. The quantitative strand's size comes from the precision it needs, worked out in advance. The qualitative strand's comes from Chapter 16's saturation argument, and it is normally an order of magnitude smaller: a study with 400 survey responses and 12 interviews is ordinary and defensible, and a reviewer who objects that 12 is too few has applied the wrong standard. What a reviewer may legitimately object to is 12 interviews chosen for convenience when the survey results were sitting there and could have chosen them.

'''

DISPLAY = '''Here is one, on the three pairings above.

| Finding | Quantitative strand | Qualitative strand | What the pairing yields |
|---|---|---|---|
| Message-level measures overstate how much talk is happening | non-gaming 31.96 characters against gaming 29.54, a gap of 2.43; *t*(145227) = -10.09, *p* < .001, *d* = 0.05 | `!play` is 449 of 1,000 messages in `dev1`; `!`-prefixed messages are 3.5 percent of the corpus and are addressed to software | setting the commands aside cuts the gap to 1.84, so roughly a quarter of the headline effect was machine traffic counted as speech |
| Most participants post once and stop | 62.2 percent of the 61,320 senders posted exactly once; the top 10 percent produced 47.4 percent of all messages, Gini 0.514 | only 10 percent of messages addressed to a named participant get an immediate reply, and the median reply arrives 11 turns later | the distribution is consistent with a room that rarely answers newcomers, which is a mechanism rather than a finding until interviews test it |
| "Typical participant" may not name anything | the naive standard error on message length is 0.0184 against a clustered 0.1502, a factor of eight | fieldwork of the kind Chapter 18 describes is what would establish whether a channel's regulars constitute one community or several | whether to cluster is not only a statistical decision; it is a claim about the setting, and the setting can be observed |

Read the third column on its own. If it reproduces either of the two before it, nothing has been integrated, and the display has told you so before a reviewer did.

Notice also that the three rows are three different **fits** in Fetters and colleagues' terms. The first is **discordance**: the strands disagree about what the number means. The second is **expansion**: the qualitative strand reaches a question the quantitative one could not ask. The third is **confirmation** running in an unusual direction, where the qualitative work would settle an assumption the quantitative analysis had to make. Naming the fit for each row is a small discipline that prevents the display from becoming a table of unrelated facts.

'''

QUALITY = '''## What a reader should check

Mixed methods papers are reviewed badly, often by someone expert in one strand and guessing at the other. O'Cathain, Murphy and Nicholl (2008) proposed a short reporting standard for exactly this problem, and its items double as the list to run over your own draft.

**Is the design named, with its notation and its purpose?** Not "a mixed methods approach was used", which says only that two things happened.

**Is each strand described to its own chapter's standard?** The quantitative half to Chapter 10's reliability and validity, the qualitative half to Chapter 21's credibility, transferability and audit trail. A mixed methods paper does not get to describe either half more thinly on the grounds that there are two.

**Is the point of integration identified?** Design, methods, or interpretation, and preferably more than one.

**Is there a joint display, or something doing its job?**

**Is there a meta-inference, and is it more than the two findings placed side by side?** This is the item most often missing, and the one the whole design exists to produce.

**Are the limitations of the integration stated, and not only of each strand?** Integration has its own failure modes. The strands may have been run on different populations, or at times far enough apart that the setting changed between them, or at sample sizes that make one strand's claim far more fragile than the other's. None of that shows up in a limitations paragraph that treats the halves separately.

A last one that is not in any framework and is worth applying anyway. **Could this study have come out the other way?** A convergent design that would have reported convergence whatever the interviews said has not tested anything. Before the qualitative data exist, write down what a result that contradicted the quantitative strand would look like. If you cannot, the design is decorative.

'''

REFS = '''O'Cathain, A., Murphy, E., & Nicholl, J. (2008). The quality of mixed methods studies in health services research. *Journal of Health Services Research & Policy*, *13*(2), 92-98. https://doi.org/10.1258/jhsrp.2007.007074

'''
REFS2 = '''Teddlie, C., & Yu, F. (2007). Mixed methods sampling: A typology with examples. *Journal of Mixed Methods Research*, *1*(1), 77-100. https://doi.org/10.1177/1558689806292430
'''

# --- splice
if "## Two strands, two sampling logics" not in t:
    anchor = "## Worked, on this book's own corpus"
    if anchor not in t:
        sys.exit("[ch26] sampling anchor not found")
    t = t.replace(anchor, SAMPLING + anchor, 1)

if "| Finding | Quantitative strand | Qualitative strand |" not in t:
    anchor = "The usual shape is one row per finding or theme"
    if anchor not in t:
        sys.exit("[ch26] display anchor not found")
    t = t.replace(anchor, DISPLAY + anchor, 1)
    t = t.replace("The supplement to this chapter builds one from the pairings above.",
                  "The supplement to this chapter builds the first row of it in a spreadsheet, "
                  "including the arithmetic behind the 1.84.")

if "## What a reader should check" not in t:
    anchor = "## Where these studies go wrong"
    if anchor not in t:
        sys.exit("[ch26] quality anchor not found")
    t = t.replace(anchor, QUALITY + anchor, 1)

# references, kept alphabetical
if "O'Cathain, A., Murphy, E., & Nicholl, J. (2008)" not in t:
    anchor = "Morse, J. M. (1991)."
    if anchor not in t:
        sys.exit("[ch26] reference anchor not found")
    t = t.replace(anchor, REFS + anchor, 1)
if "Teddlie, C., & Yu, F. (2007)" not in t:
    if not t.rstrip().endswith("00006199-199103000-00014"):
        t = t.rstrip() + "\n"
    t = t.rstrip() + "\n\n" + REFS2

io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("ch26 extended")
