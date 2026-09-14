"""Mechanism D1: every wrong number the panel found, fixed against the fixture.

Each replacement below was verified by recomputation from data-raw/v3/ before it
was written. Where a pattern is absent the script stops rather than continuing,
so a silent miss is impossible.
"""
import io
import pathlib
import sys

R = pathlib.Path("/Volumes/One Touch/20-research/aura-lab/v2v")

# (file, [(old, new), ...])
EDITS = {

# ---------------------------------------------------------------- the headline
"chapters/_v3-draft/chapter25-inference-and-effect.qmd": [
 ("The five-character gap between gaming and non-gaming chat",
  "The two-and-a-half-character gap between gaming and non-gaming chat"),
 ("the five-character gap is nothing but sampling noise",
  "the gap is nothing but sampling noise"),
 ("a gap at least as large as the observed five characters",
  "a gap at least as large as the observed 2.43 characters"),
 ("the difference is negligible in size, about five characters, a word's worth",
  "the difference is negligible in size, about two and a half characters, well under a word"),
 ("The test says gaming and non-gaming chat differ by five characters",
  "The test says gaming and non-gaming chat differ by 2.43 characters"),
 # the channel-level table: 106 + 95 = 201 under text saying 226
 ("| non-gaming | 106 | 32.74 | 16.0 |\n| gaming | 95 | 31.02 | 11.5 |",
  "| non-gaming | 112 | 32.64 | 16.0 |\n| gaming | 114 | 30.48 | 11.6 |"),
 ("Welch's *t*(190.2) = 0.88, *p* = .38.",
  "Welch's *t*(202.5) = 1.16, *p* = .25."),
],

"chapters/_v3-draft/chapter24-preparing-describing-visualizing.qmd": [
 ("The means of the two groups differ by about five characters",
  "The means of the two groups differ by about two and a half characters"),
 ("that five-character gap", "that two-and-a-half-character gap"),
 # the first three messages, and the first timestamp
 ("The first three messages in the corpus run 23, 441 and 8 characters: a row of punctuation, a block of copy-pasted emotes, and a single word.",
  "The first three messages in the corpus run 18, 11 and 18 characters, and none of them is English: a French stream title echoed back, a Spanish handle with a scoreline, and a Turkish phrase."),
 ("1542578127023", "1542578131126"),
 # a table row label left over from Chapter 11's R output
 ("non-gaming messages, the `FALSE` row, average 31.96 characters",
  "non-gaming messages average 31.96 characters"),
 # the cap arithmetic contradicts itself two lines apart
 ("A cap that removes three percent to make the other ninety-seven legible is a good trade",
  "A cap that removes four percent to make the other ninety-six legible is a good trade"),
 # busiest and quietest both described as the afternoon
 ("Chat is busiest through the UTC midday and afternoon, peaking at 22:00 with 10,967 messages, and quietest in the early afternoon, bottoming out at 14:00 with 4,173",
  "Chat is busiest through the UTC evening, peaking at 22:00 with 10,967 messages, and quietest in the early afternoon, bottoming out at 14:00 with 4,173"),
],

"supplements/excel/chapter25-inference-and-effect.qmd": [
 ("five-character", "two-and-a-half-character"),
],

"supplements/excel/chapter24-preparing-describing-visualizing.qmd": [
 ("The first three come back 23, 441 and 8",
  "The first three come back 18, 11 and 18"),
 ("A cap that hides three percent to make the other ninety-seven legible is a good trade",
  "A cap that hides four percent to make the other ninety-six legible is a good trade"),
],

# ------------------------------------------------------------------ ch19
"chapters/_v3-draft/chapter19-qualitative-content-analysis.qmd": [
 # the sentence claims case-insensitivity and prints the case-SENSITIVE count
 ("9,271", "9,716"),
 # 460 appears nowhere in the data; the count is 449
 ("those 460", "those 449"),
],

# ------------------------------------------------------------------ ch07
"chapters/_v3-draft/chapter07-research-design.qmd": [
 ("a difference of roughly ten times", "a difference of roughly eight times"),
 # the chapter says 228 channels fifteen lines earlier
 ("your n is 50 and no amount of chat volume changes that",
  "your *n* is 228 and no amount of chat volume changes that"),
],

# ------------------------------------------------------------------ ch15
# There are five, not four, and the chapter's own reading of them is the
# interesting part: it asserts they are missing values. They are as likely to be
# messages that say NA.
"chapters/_v3-draft/chapter15-existing-data.qmd": [
 ("**Four messages have no text at all.** They are missing values, and because the file is a CSV, they arrive as the two bare characters `NA`. A tool that knows the convention reads them as missing; a spreadsheet reads them as a two-character message. Four rows in 157,080 changes almost nothing here, and it is the shape of a problem that is not always small:",
  "**Five messages in the file are the two bare characters `NA`.** Four are from `asmongold` and one from `dyrus`. A tool that knows the convention reads them as missing; a spreadsheet reads them as a two-character message.\n\nWhich is right is not obvious, and that is the lesson rather than a footnote to it. `NA` is the standard CSV spelling of a missing value. It is also, in a gaming channel, how people write North America. Nothing in the file settles it, and a tool that decides for you has made an interpretive call and recorded it as a fact. Five rows in 157,080 changes almost nothing here, and it is the shape of a problem that is not always small:"),
],

"supplements/excel/chapter24-preparing-describing-visualizing.qmd_2": [],
}

SECOND = {
"supplements/excel/chapter24-preparing-describing-visualizing.qmd": [
 ("**Four messages in this corpus have no text at all**",
  "**Five messages in this corpus are the bare characters `NA`**"),
],
"supplements/excel/chapter25-inference-and-effect.qmd": [
 ("including the four with no text", "including the five that read `NA`"),
],
}

def apply(name, edits):
    p = R / name
    if not p.exists():
        sys.exit("missing file: %s" % name)
    t = io.open(p, encoding="utf-8").read()
    orig = t
    for old, new in edits:
        if old not in t:
            if new in t:
                continue
            sys.exit("[%s] NOT FOUND: %r" % (name, old[:100]))
        t = t.replace(old, new)
    if t != orig:
        io.open(p, "w", encoding="utf-8", newline="\n").write(t)
        print("  patched %s" % name.split("/")[-1])

print("Mechanism D1: numeric corrections")
for name, edits in EDITS.items():
    if not edits or name.endswith("_2"):
        continue
    apply(name, edits)
for name, edits in SECOND.items():
    apply(name, edits)
print("done")
