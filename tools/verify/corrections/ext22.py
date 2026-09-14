"""Extend Chapter 22, and correct a citation that attributes the pentad to the
wrong Burke.

The pentad is from A Grammar of Motives (1945). Identification is from A Rhetoric
of Motives (1950). The chapter uses both ideas and lists only the second book,
which is the citation-claim mismatch reviewers catch.

Two gaps besides. The chapter offers four lenses without saying why a field ever
came to have four, which is the history that makes the choice intelligible
rather than arbitrary. And it tells the reader to argue and judge without saying
what the resulting document looks like, in a book whose only other account of
report structure is IMRaD, which Chapter 27 says explicitly does not fit here.
"""
import io
import pathlib
import sys

p = pathlib.Path("/Volumes/One Touch/20-research/aura-lab/v2v/chapters/"
                 "_v3-draft/chapter22-rhetorical-criticism.qmd")
t = io.open(p, encoding="utf-8").read()

HISTORY = '''## Why there is more than one lens

A reader arriving from Part III will want to know why a method offers four vocabularies and lets you pick. The answer is historical, and knowing it is what keeps the choice from feeling arbitrary.

For the first half of the twentieth century there was essentially one approach. A criticism reconstructed a speech's occasion, sorted its persuasive work into Aristotle's categories, and assessed whether it achieved its aim with its immediate audience. It was rigorous, it was teachable, and it produced a great deal of competent work on a narrow range of objects: single speeches, by public men, on formal occasions.

Black's (1978) critique, first published in 1965, is the hinge. His argument was not that the approach was wrong but that it was one method being mistaken for the whole enterprise, and that its assumptions quietly decided the findings in advance. It assumed the significant unit was a single speech, so campaigns, movements and bodies of work were invisible. It assumed the relevant audience was the one in the room, so a text's longer effect on how a public could think was out of scope. And it assumed effect could be read off the text, which is the boundary this chapter's last section polices.

What followed was not a replacement but a proliferation, and the lenses below are a small selection from it. That is why the method asks you to justify your choice: the vocabulary you bring determines what you are able to notice, so choosing one is already an analytic decision and belongs in the write-up rather than in the background.

It is also why "I applied rhetorical criticism" is not a methods section. Which lens, on what artifact, and why that pairing, is.

'''

WRITEUP = '''## The shape of the write-up

Chapter 27 gives IMRaD and says plainly that it fits an ethnography badly. It fits a criticism worse: there is no Results section, because the analysis and the finding are the same paragraphs.

What a criticism has instead is the shape of an argument.

**An opening that states the claim.** Not "this essay examines the rhetoric of X" but what you concluded about how X works. A criticism that withholds its thesis for suspense reads as though the critic found it late, and the reader spends the essay guessing what to attend to.

**The artifact and why it.** What the text is, where you got it, when, and what makes it worth a reader's time. This is the section that carries Chapter 2's traceability obligation, and it is short.

**The situation.** Exigence, audience, constraints, with the historical work visible. A reader who disagrees with your reading often disagrees here first, and putting it early lets them see where the disagreement starts.

**The lens, named and justified.** One paragraph. Why this vocabulary suits this artifact.

**The analysis, organized by the argument rather than by the text.** This is the section students most often get wrong, by walking through the artifact chronologically and commenting as they go. The result is a summary with observations attached. Organize instead by the claims you are making, and bring in whatever part of the text supports each, in whatever order the argument needs.

**The inconvenient material, on purpose.** A subsection or a sustained passage dealing with what resists your reading. Burying it is worse than useless, because a reader who finds it themselves stops trusting the rest.

**The judgment, and what follows.** What the text accomplishes, at whose expense, and what it makes harder to say next.

Length is usually the surprise: a criticism of a ten-minute video routinely runs six to eight thousand words, because the evidence is quotation and quotation takes room. If your draft is short, the usual cause is that you have described the text rather than argued about it.

'''

FIX = [
 # the pentad is Grammar (1945); identification is Rhetoric (1950)
 ("Burke offers a vocabulary for how a text characterizes an event.",
  "Burke (1969a) offers a vocabulary for how a text characterizes an event."),
 ("Burke's other central idea, **identification**, is that persuasion works",
  "Burke's other central idea, **identification** (1969b), is that persuasion works"),
 # Aristotle is used and not cited
 ("Aristotle's three modes of persuasion are still the most economical starting vocabulary.",
  "Aristotle's three modes of persuasion (2007) are still the most economical starting vocabulary."),
 # Chapter 11 is wrangling; the logic being set aside is Chapter 7's, about cases
 ("Chapter 11's logic does not apply and is not being flouted:",
  "Chapter 7's logic about cases and populations does not apply here, and is not being flouted:"),
 # the reference entry, corrected and split
 ("Burke, K. (1969). *A rhetoric of motives*. University of California Press. (Original work published 1950)",
  "Burke, K. (1969a). *A grammar of motives*. University of California Press. (Original work published 1945)\n\nBurke, K. (1969b). *A rhetoric of motives*. University of California Press. (Original work published 1950)"),
 # Black's date matters to the history section
 ("Black, E. (1978). *Rhetorical criticism: A study in method*. University of Wisconsin Press.",
  "Aristotle. (2007). *On rhetoric: A theory of civic discourse* (G. A. Kennedy, Trans.; 2nd ed.). Oxford University Press.\n\nBlack, E. (1978). *Rhetorical criticism: A study in method*. University of Wisconsin Press. (Original work published 1965)"),
]
for old, new in FIX:
    if old not in t:
        if new in t:
            continue
        sys.exit("[ch22] NOT FOUND: %r" % old[:90])
    t = t.replace(old, new)

if "## Why there is more than one lens" not in t:
    anchor = "## Three lenses"
    if anchor not in t:
        sys.exit("[ch22] history anchor not found")
    t = t.replace(anchor, HISTORY + anchor, 1)

if "## The shape of the write-up" not in t:
    anchor = "## What makes one good"
    if anchor not in t:
        sys.exit("[ch22] write-up anchor not found")
    t = t.replace(anchor, WRITEUP + anchor, 1)

# the section is headed "Three lenses" and offers four
t = t.replace("## Three lenses\n\nA lens is a vocabulary",
              "## Four lenses\n\nA lens is a vocabulary")
t = t.replace("Do not run all four; a criticism that applies every vocabulary",
              "Do not run all four; a criticism that applies every vocabulary")

io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("ch22 extended")
