import io, pathlib, sys

p = pathlib.Path("/Volumes/One Touch/20-research/aura-lab/v2v/planning/v4-read-through-review.md")
t = io.open(p, encoding="utf-8").read()

old = ("**Length.** New chapters average about 2,690 words against 3,780 for the\n"
       "carried-over ones. Chapter 2 is no longer the outlier it was. The short ones now\n"
       "are ch26 (1,772), ch27 (1,867), ch09 (1,913), ch23 (2,001) and ch22 (2,022).\n"
       "Chapter 27 closing a 27-chapter book in 1,867 words is the one I would look at.")

new = ("**Length.** New chapters average about 2,690 words against 3,780 for the\n"
       "carried-over ones. Chapters 2, 26 and 27 are no longer outliers: 2 went from 1,755\n"
       "to 2,458 when the replication-crisis material came back into it, 26 from 1,772 to\n"
       "2,948 and 27 from 1,867 to 2,891.\n\n"
       "**Chapter 26** gained a section on sampling, which it had named as an integration\n"
       "point and never explained: the two strands sample on opposite logics, and in an\n"
       "explanatory sequential design the quantitative results choosing the qualitative\n"
       "cases *is* the integration. It also now contains a joint display rather than a\n"
       "promise of one in the supplement, built on the three pairings the chapter already\n"
       "names, with each row labelled by its fit. And it gained a section on what a reader\n"
       "should check, since the chapter said what a bad mixed methods study looks like and\n"
       "not what to verify in a good one.\n\n"
       "**Chapter 27** was missing the section its own opening promised. It says the report\n"
       "is \"close to a single action: one click\" and cited Knuth (1984) in its reference\n"
       "list, and both belonged to a passage lost when the 3rd edition's Chapter 14 was\n"
       "folded in. That passage is lifted back, with its repairs declared. It also gained a\n"
       "section on the title and abstract, which are the only part of a paper most people\n"
       "read and which the chapter did not mention, and one on where materials are actually\n"
       "deposited, since the open-materials section said what to share and not where or how\n"
       "to make it citable. Three errors fixed along the way: the Methods paragraph\n"
       "attributed the codebook and the sampling procedure to the wrong chapters, the\n"
       "clustering penalty was still \"a factor of ten\" against the current 8.16, and the\n"
       "bot-command figure was still 46 percent against 45.\n\n"
       "The short ones now are ch09 (1,913), ch23 (2,001) and ch22 (2,022).")

if old in t:
    io.open(p, "w", encoding="utf-8", newline="\n").write(t.replace(old, new))
    print("review updated")
elif "no longer outliers" in t:
    print("already updated")
else:
    sys.exit("length paragraph not found")
