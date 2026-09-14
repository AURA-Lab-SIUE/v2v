"""Extend Chapter 27, and fix three things reading it closely turned up.

The chapter opens by promising a report that is "close to a single action: one
click", cites Knuth (1984) in its reference list, and then never explains either.
Both belong to a section the 4th edition dropped when it folded the 3rd
edition's Chapter 14 into this one. That section is lifted back here from
chapters/chapter14.qmd rather than rewritten, so it stays the text that was
already reviewed, with its repairs declared below.
"""
import io
import pathlib
import sys

R = pathlib.Path("/Volumes/One Touch/20-research/aura-lab/v2v")
src = R / "chapters/chapter14.qmd"
dst = R / "chapters/_v3-draft/chapter27-writing-and-publishing.qmd"

# ---------------------------------------------------------------- the lift
s = io.open(src, encoding="utf-8").read()
a = s.index("## A report that rebuilds itself")
b = s.index("## The shape of a report: IMRaD")
block = s[a:b]

LIFT = [
 # the histogram moved from the 3rd edition's Chapter 12 to the 4th edition's 24
 ("The histogram from Chapter 12 is not pasted in;",
  "The histogram from Chapter 24 is not pasted in;"),
 # "this chapter's title" was "The one-click report"; Chapter 27 is titled differently
 ('and the "one click" of this chapter\'s title is its render button.',
  'and the "one click" this chapter opened with is its render button.'),
]
for old, new in LIFT:
    if old not in block:
        sys.exit("[lift] NOT FOUND: %r" % old[:80])
    block = block.replace(old, new)

t = io.open(dst, encoding="utf-8").read()

if "## A report that rebuilds itself" in t:
    print("ch27: lift already present")
else:
    anchor = "## The shape of a report: IMRaD"
    t = t.replace(anchor, block + anchor, 1)
    print("ch27: lifted the reproducible-report section")

# ------------------------------------------------------- corrections + new
NEW_ABSTRACT = '''## The two hundred words almost everyone reads

Most people who encounter your study will read the title and the abstract and nothing else. That is not a failure of attention on their part. It is how anyone surveying a literature works, and it means the two hundred words at the front do more work than any other part of the paper.

**The title should say what was studied and, where possible, what was found.** "Chat participation on Twitch" names a topic. "Message length does not distinguish gaming from non-gaming Twitch chat once channels are the unit of analysis" names a finding, and a reader deciding whether to open it now has what they need. Titles that end in a question mark usually mean the answer did not fit, which is a signal worth noticing in your own drafts.

**The abstract is IMRaD in miniature, in that order, with no citations and no suspense.** One or two sentences on the problem and the question. One or two on the design, the data and the analysis, with the actual sample size. Two or three on the findings, with the numbers, not "results are discussed". One on what it means and what it does not.

The commonest fault in a student abstract is that it describes the paper instead of reporting the study: "this paper examines", "findings are presented", "implications are considered". None of those sentences tells a reader anything. Replace each with what was actually examined, found and implied. A useful test is to read the abstract to someone who has not seen the paper and ask them what the study found. If they cannot say, it is not finished.

Write it last, and then check it against the Results section line by line, because an abstract drafted early and never revisited is one of the easier ways to publish a number that appears nowhere else in the paper.

'''

NEW_MATERIALS = '''## Where the materials actually live

Saying the data and code are "available on request" is, in practice, the same as saying they are not available. Requests go to email addresses that expire, to people who change institutions, and to hard drives that fail. Deposit instead.

**A repository, with a persistent identifier.** A general-purpose archive such as the Open Science Framework or Zenodo will mint a DOI for a deposit, which is what makes it citable and what keeps the link working after your university changes its web platform. A GitHub repository is an excellent place to *develop* the analysis and a poor place to *archive* it, because anyone with access can rewrite its history; the usual arrangement is to develop on GitHub and archive a release of it, which Zenodo will do automatically.

**Deposit at submission, not at acceptance.** Reviewers who can run the analysis review it better, and a link that already exists is one less thing to produce under deadline eight months later.

**Say in the paper what is deposited and what is not, and why.** "All data and analysis code are available at [DOI]" is a claim a reader can check. If the raw data cannot be shared because your consent form did not cover it, say that; it is a legitimate reason and Chapter 3 governs when it applies. What is not legitimate is silence, which reads to an informed reader as a decision you did not want to explain.

A README in the deposit that says what each file is, what order the scripts run in, and what software versions produced the result costs twenty minutes and is the difference between materials that can be used and materials that merely exist.

'''

FIX = [
 # the Methods paragraph attributes three things to the wrong chapters
 ("This is the home of the codebook from Chapter 12, the sampling procedure from Chapter 11 and the inter-coder reliability check from Chapter 10, and the wrangling steps from Chapter 11.",
  "This is the home of the codebook from Chapter 8, the reliability check from Chapter 10, the content-analysis procedure from Chapter 12, and the wrangling steps from Chapter 11."),
 # both figures moved with the census re-sample
 ("the reported precision is optimistic by roughly a factor of ten; one channel's chat is 46 percent bot commands,",
  "the reported precision is optimistic by roughly a factor of eight; one channel's chat is 45 percent bot commands,"),
]
for old, new in FIX:
    if old not in t:
        if new in t:
            continue
        sys.exit("[ch27 fix] NOT FOUND: %r" % old[:100])
    t = t.replace(old, new)

if "## The two hundred words almost everyone reads" not in t:
    t = t.replace("## Authorship", NEW_ABSTRACT + "## Authorship", 1)
if "## Where the materials actually live" not in t:
    t = t.replace("## Getting it published", NEW_MATERIALS + "## Getting it published", 1)

# Peng (2011) arrives with the lifted section and needs its entry
PENG = ("Peng, R. D. (2011). Reproducible research in computational science. *Science*, "
        "*334*(6060), 1226-1227. https://doi.org/10.1126/science.1213847\n\n")
if "Peng, R. D. (2011)" not in t:
    nosek = "Nosek, B. A., Ebersole, C. R., DeHaven, A. C., & Mellor, D. T. (2018)."
    if nosek not in t:
        sys.exit("[ch27] reference anchor not found")
    t = t.replace(nosek, PENG + nosek, 1)

io.open(dst, "w", encoding="utf-8", newline="\n").write(t)
print("ch27 extended")
