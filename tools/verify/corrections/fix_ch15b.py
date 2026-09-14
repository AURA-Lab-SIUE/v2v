"""Second correction to Chapter 15, after reading the whole help page.

The per-channel cap is documented, plainly, in the \\details section of
twitch_chat_sample's own help page: "Each channel contributes up to 1,000
messages to the sample." My first draft said it was undocumented; my second said
it was documented elsewhere. Both were wrong, and both came from reading the
\\format block and stopping.

What the audit actually finds, checked against the complete documentation:
  - the sampling design, the cap and the window are documented and confirmed
  - the 509-character maximum is the population's, printed in a sample's help
    page, which is a scope error
  - four missing messages are genuinely undocumented
  - the consequence of the cap for cross-channel quantities is not drawn out
    anywhere, which is the reader's job rather than a documentation defect
"""
import io
import pathlib
import sys

ROOT = pathlib.Path("/Volumes/One Touch/20-research/aura-lab/v2v")
CH = "chapters/_v3-draft/chapter15-existing-data.qmd"
SUP = "supplements/excel/chapter15-existing-data.qmd"

EDITS = {
CH: [
("The package documents 35,267 messages across 50 channels, sampled from a 1.6 GB database dump of Twitch chat captured in November 2018, with the random seed recorded, eight named anchor channels, and the remaining 42 drawn as a stratified random sample. It states that channel names had their IRC `#` prefix stripped so the table joins cleanly, and that timestamps are Unix epoch in milliseconds rather than seconds.\n\nThat is more than most datasets tell you, and the audit still finds things.",
 "The package documents 35,267 messages across 50 channels, sampled from a 1.6 GB database dump of Twitch chat captured in November 2018, with the random seed recorded, eight named anchor channels, and the remaining 42 drawn as a stratified random sample by chat-volume decile. It states that channel names had their IRC `#` prefix stripped so the table joins cleanly, that timestamps are Unix epoch in milliseconds rather than seconds, and that **each channel contributes at most 1,000 messages**, with smaller channels contributing everything they have.\n\nThat is more than most datasets tell you, and the audit still finds three things."),

("**And one property that matters a great deal is documented somewhere else.** Count the messages per channel and the distribution is strange: **31 of the 50 channels have exactly 1,000 messages**, including all eight anchors, and **no channel has more than 1,000**. Nine channels have fewer than a hundred, and the smallest has one.",
 "**And one documented property has a consequence the documentation does not draw out.** Count the messages per channel: **31 of the 50 have exactly 1,000**, including all eight anchors, **none has more than 1,000**, nine have fewer than a hundred, and the smallest has one."),

("A distribution does not pile up on a round number by accident, and a hard ceiling with nothing above it is not a coincidence either. **The sample was capped at 1,000 messages per channel.**\n\nThat cap is documented, and not in the help page. It is in the project's data report, which the help page points to in one line at the end of its source note. The help page is what a reader opens; the data report is where the sampling design actually lives.\n\nThis is the more common situation, and the more dangerous one. Documentation is rarely absent. It is distributed across a help page, a README, a methods report and a paper, at different levels of detail and written at different times, and the thing that governs your analysis is frequently in the document you did not open. **Read every document the first one points at, and check the ones you cannot find against the data.**",
 "That is the cap, exactly as documented, and the audit confirms it. Confirmation is a perfectly good result: you now know the sentence in the help page is true of the file in front of you, which you did not know before.\n\nBut read the sentence again. *Each channel contributes up to 1,000 messages.* It says what was done. It does not say what follows, and what follows is the most important fact about this corpus.\n\n**Documentation tells you what was done. Working out what it means for your question is your job, and nobody else's.** The next section does that work, and it is the reason the audit was worth running even though the documentation turned out to be accurate.\n\nA note on how I nearly missed this. The cap is in the help page's details section, below the table of columns. Reading the column definitions and stopping, which is what one naturally does when the question is \"what is in this file\", skips it entirely. **Read the whole document, not the part that answers your immediate question.**"),
],

SUP: [
("## Where the documentation is somewhere else",
 "## Where the documentation is right, and still not enough"),

("Real counts do not do that. A hard ceiling with 31 channels resting on it and none above is a cap, applied when the sample was drawn.\n\nIt is documented, in the project's data report, which the help page points to in a single line. It is not in the help page itself, which is the document you actually read. **Open everything the first document points at**, and audit the data for the properties none of them mention.",
 "Real counts do not do that. A hard ceiling with 31 channels resting on it and none above is a cap, applied when the sample was drawn.\n\nThe help page says so: *each channel contributes up to 1,000 messages to the sample*. So this check confirms the documentation rather than contradicting it, which is the outcome you should expect most of the time and should still run the check to establish.\n\nTwo lessons survive the confirmation. **That sentence is in the details section, below the column definitions**, and a reader who opens the help page to find out what the columns mean will never reach it. And the sentence says what was done without saying what it implies, which is that the corpus is balanced across channels rather than proportional to chat volume. Chapter 15 works through what that costs."),
],
}

for name, subs in EDITS.items():
    p = ROOT / name
    t = io.open(p, encoding="utf-8").read()
    for old, new in subs:
        if old not in t:
            sys.exit("NOT FOUND in %s:\n  %r" % (name, old[:120]))
        if t.count(old) != 1:
            sys.exit("NOT UNIQUE in %s (%d)" % (name, t.count(old)))
        t = t.replace(old, new)
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("patched %s (%d edits)" % (name, len(subs)))
