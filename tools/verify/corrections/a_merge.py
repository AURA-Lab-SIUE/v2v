"""Mechanism A1 and A2: the ch11/ch24 merge, and the sampling chapter that the
freed slot becomes.

Chapters 11 and 24 were the same chapter. Both opened with the same premise in
almost the same words, both built the same analysis-ready table, and 22 verbatim
sentences appeared in both. Chapter 11 did it in R; Chapter 24 did it in prose
with the code deleted, thirteen chapters later.

Eight chapters cross-reference "Chapter 11" for sampling, and there was no
sampling chapter. Merging the wrangling into Chapter 24, where the title already
promises "Preparing", frees exactly the slot those eight references point at, so
the fix needs no renumbering and makes all eight correct.

Chapter 24 gains the R it was missing, which also answers the complaint that its
Excel supplement was fully worked while the chapter itself had no code at all.
"""
import io
import pathlib
import sys

R = pathlib.Path("/Volumes/One Touch/20-research/aura-lab/v2v")
ch11 = R / "chapters/_v3-draft/chapter11-wrangling-the-data.qmd"
ch24 = R / "chapters/_v3-draft/chapter24-preparing-describing-visualizing.qmd"

src = io.open(ch11, encoding="utf-8").read()
dst = io.open(ch24, encoding="utf-8").read()

if "## The verbs of data wrangling" in dst:
    print("merge already done")
    sys.exit(0)

# the wrangling body: everything from the verbs section to the chapter's own close
a = src.index("## The verbs of data wrangling")
b = src.index("## Looking ahead")
body = src[a:b].rstrip() + "\n\n"

# it referred to itself as the chapter; it is now a section of one
body = body.replace("Chapter 12 will use exactly that to chart how chat volume rises and falls across the hours of the day.",
                    "The next section uses exactly that to chart how chat volume rises and falls across the hours of the day.")
body = body.replace("That spread is the raw material of the study, and Chapter 24 will look hard at its shape.",
                    "That spread is the raw material of the study, and the next section looks hard at its shape.")
body = body.replace("a dashed line at 120 characters marks where Chapter 24 will cap its axis",
                    "a dashed line at 120 characters marks where this chapter caps its axis")
body = body.replace("every figure in Chapter 24 and every test in Chapter 25, will be computed from this table",
                    "every figure below and every test in Chapter 25, will be computed from this table")

# Chapter 24's own duplicate of the same material, from "The operations" to the
# point where it stops repeating Chapter 11 and starts describing
i = dst.index("## The operations")
j = dst.index("## Describing before testing")
dst = dst[:i] + body + dst[j:]

# the chapter now owns the wrangling outright, so its opening can say so once
dst = dst.replace(
 "Part VI is where a project stops being a design and becomes a result. This chapter covers the three things that happen to a dataset before anything is tested: getting it into shape, describing what is in it, and looking at it. Chapter 25 does the testing.",
 "Part VI is where a project stops being a design and becomes a result. This chapter covers the three things that happen to a dataset before anything is tested: getting it into shape, describing what is in it, and looking at it. Chapter 25 does the testing.\n\nThe code here is R. Everything in this chapter can also be done in a spreadsheet, and the Excel supplement for this chapter does exactly that, including the four places where a spreadsheet will handle it silently and wrongly.")

io.open(ch24, "w", encoding="utf-8", newline="\n").write(dst)
print("merged the wrangling into chapter 24")

# the old wrangling chapter goes; chapter 11 is now sampling
ch11.unlink()
print("removed chapter11-wrangling-the-data.qmd")

# ---------------------------------------------------------------- the TOC
cfg = R / "_quarto-v4.yml"
t = io.open(cfg, encoding="utf-8").read()
old = "        - chapters/_v3-draft/chapter11-wrangling-the-data.qmd\n"
new = "        - chapters/_v3-draft/chapter11-sampling.qmd\n"
if old not in t:
    sys.exit("TOC entry for chapter 11 not found")
io.open(cfg, "w", encoding="utf-8", newline="\n").write(t.replace(old, new))
print("table of contents repointed to the sampling chapter")
