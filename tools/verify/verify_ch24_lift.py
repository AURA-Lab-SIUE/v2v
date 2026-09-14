"""Confirm the Chapter 24 merge preserved the owner's prose exactly.

Every paragraph build_ch24.py lifted from chapter11.qmd or chapter12.qmd must
appear byte-identical in the new chapter, except the repairs the builder
declares. Anything else that changed is drift introduced by the merge, which is
what this check exists to catch.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path("/Volumes/One Touch/20-research/aura-lab/v2v")
new = (ROOT / "chapters/_v3-draft/chapter24-preparing-describing-visualizing.qmd").read_text(encoding="utf-8")

SOURCES = {
    "ch11": (ROOT / "chapters/chapter11.qmd").read_text(encoding="utf-8"),
    "ch12": (ROOT / "chapters/chapter12.qmd").read_text(encoding="utf-8"),
}

# (source, anchor, repaired?) - repaired paragraphs are expected to differ.
LIFTED = [
    ("ch11", "The chat table you loaded in Chapter 9 cannot answer", True),
    ("ch11", "This is the ordinary situation at this stage of a study", False),
    ("ch11", "The reason these verbs combine so well is a shared design", True),
    ("ch11", "The third transformation is the one the central research question turns on", False),
    ("ch11", "Gaming or non-gaming is best understood as a property of the channel", False),
    ("ch11", "The first step reaches into the stream table", False),
    ("ch11", "The second step is a judgment, and it should be visible rather than buried", False),
    ("ch11", "A join is only as good as the match between its keys", False),
    ("ch11", "This is what wrangling was for. The table is now **tidy**", False),
    ("ch11", "None of this was analysis. Not a single result has been computed.", True),
    ("ch12", "A figure is the instrument that makes the pattern visible", True),
    ("ch12", "Three parts do most of the work. The first is the **data**", False),
    ("ch12", "The first question is about viewership", False),
    ("ch12", "When the horizontal axis is time and the vertical axis is a quantity that rises and falls", False),
    ("ch12", "The second question is about timing", False),
    ("ch12", "Hour of day is not a continuous sweep the way a date is", False),
    ("ch12", "The figure shows a clear daily pulse", False),
    ("ch12", "The third question is the study's central one", False),
    ("ch12", "This question is not about a total or a trend. It is about a **distribution**", False),
    ("ch12", "The figure shows, first, a shape both groups share", False),
    ("ch12", "The histogram explains how both things can be true at once", False),
    ("ch12", "This is what it means to treat descriptive statistics as a visual setup rather than a verdict", False),
    ("ch12", "Read the `mean` column and a story jumps out", False),
    ("ch12", "Three figures are built. Before they are finished", False),
    ("ch12", "The first duty is **color**", False),
    ("ch12", "The second duty is the **alt text**", False),
    ("ch12", "A figure that is honest about its choices", False),
    ("ch12", "The histogram left a precise question on the table", False),
]


def para(src, anchor):
    body = re.sub(r"^```.*?^```", "", src, flags=re.S | re.M)
    hits = [p.strip() for p in body.split("\n\n") if anchor in p]
    if len(hits) != 1:
        sys.exit("anchor matched %d paragraphs in source: %r" % (len(hits), anchor[:60]))
    return hits[0]


identical, repaired, drift = 0, [], []
for where, anchor, is_repaired in LIFTED:
    p = para(SOURCES[where], anchor)
    if p in new:
        identical += 1
        if is_repaired:
            drift.append((where, anchor, "declared a repair but lifted unchanged"))
    elif is_repaired:
        repaired.append((where, anchor))
    else:
        drift.append((where, anchor, "NOT FOUND and no repair declared"))

print("paragraphs lifted byte-identical : %d" % identical)
print("paragraphs changed by declared repair: %d" % len(repaired))
for w, a in repaired:
    print("   [%s] %s..." % (w, a[:58]))

if drift:
    print("\n** UNDECLARED DRIFT, %d paragraph(s):" % len(drift))
    for w, a, why in drift:
        print("   [%s] %s\n        %s" % (w, a[:70], why))
    sys.exit(1)
print("\nOK: no undeclared drift.")
