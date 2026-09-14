"""Correct Chapter 15 and its supplement.

Three things I got wrong when drafting them, all found by going back to the
primary sources rather than to the help page:

1. The 1,000-per-channel cap IS documented, in the V2V data report, which the
   help page explicitly points to. It is absent only from the help page itself.
   "Not stated anywhere in the documentation" was false.
2. The 509-character maximum is not wrong. It is the maximum of the full
   21,964,296-message population, quoted in a help page describing the
   35,267-row sample. That is a scope error, which is a better lesson.
3. "No empty messages" was false. Four messages are missing, and the CSV
   spells that NA.
"""
import io
import pathlib
import sys

ROOT = pathlib.Path("/Volumes/One Touch/20-research/aura-lab/v2v")

CH = "chapters/_v3-draft/chapter15-existing-data.qmd"
SUP = "supplements/excel/chapter15-existing-data.qmd"

EDITS = {
CH: [
("**The row and channel counts hold.** 35,267 messages, 50 channels, all eight anchors present. There are no duplicate identifiers and no empty messages.",
 "**The row and channel counts hold.** 35,267 messages, 50 channels, all eight anchors present, and no duplicate identifiers.\n\n"
 "**Four messages have no text at all.** They are missing values, and because the file is a CSV, they arrive as the two bare characters `NA`. A tool that knows the convention reads them as missing; a spreadsheet reads them as a two-character message. Four rows in 35,267 changes almost nothing here, and it is the shape of a problem that is not always small: a CSV cannot distinguish a missing value from the text that spells it, and `NA`, `NULL`, `N/A`, `-99` and an empty cell all arrive as something."),

("**One documented figure is wrong.** The documentation says messages run up to 509 characters. The longest message in the file is **501**, and exactly one message exceeds 500. Trivial in itself, and the point is not the eight characters: it is that a stated property of the data was not true, you found it in one formula, and anything else in that documentation is now something you check rather than something you assume.",
 "**One documented figure describes a different dataset.** The help page says messages run up to 509 characters. The longest message in this file is **501**, and exactly one exceeds 500.\n\n"
 "The 509 is not an invention. It is the maximum of the full 21,964,296-message population the sample was drawn from, and it is correct about that population. It is quoted in the help page for a 35,267-row sample, where a reader will take it as a property of the file in front of them.\n\n"
 "That is worth more than a simple error would be. **A documented property can be true of the population and false of your extract**, and nothing marks which one a given number refers to. Every figure in a data dictionary carries an implied scope, and the scope is usually not stated."),

("**And one undocumented property matters a great deal.** Count the messages per channel and the distribution is strange: **31 of the 50 channels have exactly 1,000 messages**, including all eight anchors, and **no channel has more than 1,000**. Nine channels have fewer than a hundred, and the smallest has one.",
 "**And one property that matters a great deal is documented somewhere else.** Count the messages per channel and the distribution is strange: **31 of the 50 channels have exactly 1,000 messages**, including all eight anchors, and **no channel has more than 1,000**. Nine channels have fewer than a hundred, and the smallest has one."),

("A distribution does not pile up on a round number by accident, and a hard ceiling with nothing above it is not a coincidence either. **The sample was capped at 1,000 messages per channel**, and that is not stated anywhere in the documentation. You can only learn it by looking.",
 "A distribution does not pile up on a round number by accident, and a hard ceiling with nothing above it is not a coincidence either. **The sample was capped at 1,000 messages per channel.**\n\n"
 "That cap is documented, and not in the help page. It is in the project's data report, which the help page points to in one line at the end of its source note. The help page is what a reader opens; the data report is where the sampling design actually lives.\n\n"
 "This is the more common situation, and the more dangerous one. Documentation is rarely absent. It is distributed across a help page, a README, a methods report and a paper, at different levels of detail and written at different times, and the thing that governs your analysis is frequently in the document you did not open. **Read every document the first one points at, and check the ones you cannot find against the data.**"),
],

SUP: [
("It takes about twenty minutes. Run it on every dataset you did not collect yourself, before you write a single research question against it, because two of the things it finds here change how earlier chapters should be read.",
 "It takes about twenty minutes. Run it on every dataset you did not collect yourself, before you write a single research question against it. Two of the things it finds here change how earlier chapters should be read, and neither of them is a defect in the data."),

("**0**. Do this for every column. A column that is 30 percent blank is a column you cannot use as you planned, and it is better to learn that now than after building an analysis on it.",
 "**0**, and that answer is misleading, which is the point of running it.\n\n"
 "Four messages in this corpus are genuinely missing. R writes a missing value into a CSV as the two bare characters `NA`, so the cells are not blank, they contain text, and `COUNTBLANK` is right that nothing is empty. Count them properly:\n\n"
 "```\n=COUNTIF($D$2:$D$35268,\"NA\")\n```\n\n"
 "which returns **4**. Before trusting either number, check that no real message is the word `NA`; here none is, so the count is clean.\n\n"
 "Do both for every column. A column that is 30 percent missing is a column you cannot use as you planned, and it is better to learn that now than after building an analysis on it."),

("The package says messages run **up to 509 characters**.",
 "The package help page says messages run **up to 509 characters**."),

("Eight characters is nothing. What it tells you is worth a great deal: **a stated property of this dataset was not true, and you found it in one cell.** Everything else in that documentation has now moved from assumed to checkable, which is the correct state for documentation to be in.",
 "Eight characters is nothing, and the reason for the gap is worth a great deal. The 509 is the longest message in the **full 21.9-million-message population** this sample was drawn from. It is correct about that population and it is printed in the help page for your 35,267-row extract.\n\n"
 "**A documented figure can be true of the population and false of your file**, and nothing in the help page marks which it means. That is not a typo you can correct once; it is a question to ask of every number in a data dictionary."),

("## Where the documentation is silent",
 "## Where the documentation is somewhere else"),

("Real counts do not do that. A hard ceiling with 31 channels resting on it and none above is a cap, applied when the sample was drawn, and it appears nowhere in the documentation.",
 "Real counts do not do that. A hard ceiling with 31 channels resting on it and none above is a cap, applied when the sample was drawn.\n\n"
 "It is documented, in the project's data report, which the help page points to in a single line. It is not in the help page itself, which is the document you actually read. **Open everything the first document points at**, and audit the data for the properties none of them mention."),

("It will not tell you why the cap is there, whether the 42 non-anchor channels really were drawn as documented, or what was in the 1.6 GB dump that did not make it into these 35,267 rows. Those questions go to whoever made the file, and \"we asked and could not find out\" is a legitimate and reportable answer.",
 "It will not tell you whether the 42 non-anchor channels really were drawn as documented, or what was in the 1.6 GB dump that did not make it into these 35,267 rows. Those questions go to whoever made the file, and \"we asked and could not find out\" is a legitimate and reportable answer."),
],
}

for name, subs in EDITS.items():
    p = ROOT / name
    t = io.open(p, encoding="utf-8").read()
    for old, new in subs:
        if old not in t:
            sys.exit("NOT FOUND in %s:\n  %r" % (name, old[:110]))
        if t.count(old) != 1:
            sys.exit("NOT UNIQUE in %s (%d)" % (name, t.count(old)))
        t = t.replace(old, new)
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("patched %s (%d edits)" % (name, len(subs)))
