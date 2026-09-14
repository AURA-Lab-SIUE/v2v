"""Disclose how far the book's headline finding depends on one labelling choice.

Recomputed in R on the shipped fixtures. Under the channel-level label the book
uses, non-gaming chat is longer by 5.21 characters, p < .001. Under a
per-message label taken from the category on screen at the time, the gap
reverses to -0.98 and is not significant (t(4993.6) = 1.34, p = .18). The
non-gaming group is five channels totalling 3,457 messages, of which xqcow is
29 percent.

Neither calculation is wrong; they answer different questions. The book stated
only the first, with no indication that the result turns on the decision. That
is the thing Chapters 8 to 10 exist to warn against, so it is now stated.
"""
import io
import pathlib
import sys

ROOT = pathlib.Path("/Volumes/One Touch/20-research/aura-lab/v2v")

SECTION = """## How much the finding depends on one decision

A test tells you whether a gap is larger than sampling noise. It cannot tell you whether the gap survives a different but equally defensible definition of the groups being compared. Here it does not, and that turns out to matter more than the test.

`is_gaming` was built as a property of the **channel**: each channel's modal category across the week, applied to every message that channel sent. The same data supports a second operationalization. Label each **message** by the category the channel was actually streaming when it was sent, read from the nearest earlier stream snapshot.

| How the label is defined | gaming | non-gaming | gap |
|---|---|---|---|
| the channel's modal category | 28.49 (n = 31,305) | 33.70 (n = 3,457) | +5.21 |
| the category on screen at the time | 29.11 (n = 30,707) | 28.13 (n = 4,044) | -0.98 |

Under the second definition the gap reverses direction, falls to about one character, and is no longer statistically significant: Welch's *t*(4993.6) = 1.34, *p* = .18.

Neither calculation is wrong, and they are not in competition. They answer different questions, and the distance between them is concentrated in one fact worth seeing plainly: **the non-gaming group is five channels.** `bobross`, `hitch`, `xqcow`, `tjsmith` and `darksydephil`, three of them at the corpus's 1,000-message cap, 3,457 messages between them. `xqcow` alone is 29 percent of the group, and that channel is filed under Just Chatting for most of the week while spending a good deal of it playing games. Under the channel-level label every one of its messages is non-gaming. Under the message-level label most of them are not.

Two things follow, and both belong in the write-up.

The **unit of analysis** problem is doing real work here. The label varies across 48 channels, five of which are non-gaming, while the test is computed over 34,762 messages. The p-value answers "could 34,762 independent draws have produced this gap by chance". The question that matters is "could five channels", and the answer to that one is much less comfortable.

And the **finding has to be stated at the level it was actually measured**. Not "gaming chat is shorter", but "chat on the five predominantly non-gaming channels in this sample is longer on average, by an amount too small to matter, and the difference does not survive relabelling messages by what was on screen at the time".

That is a duller sentence, and it is the one the data supports.

"""

# --- v3 chapter 13
p = ROOT / "chapters/chapter13.qmd"
t = io.open(p, encoding="utf-8").read()
anchor = "## Looking ahead"
if t.count(anchor) != 1:
    sys.exit("ch13 anchor count %d" % t.count(anchor))
t = t.replace(anchor, SECTION + anchor, 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("patched chapters/chapter13.qmd")

# --- v4 builder for chapter 25
p = ROOT / "data-raw/v3/build_ch25.py"
t = io.open(p, encoding="utf-8").read()
anchor = 'add("## What this chapter cannot do for you")'
if t.count(anchor) != 1:
    sys.exit("build_ch25 anchor count %d" % t.count(anchor))
block = 'add("""' + SECTION.rstrip() + '""")\n\n' + anchor
t = t.replace(anchor, block, 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("patched data-raw/v3/build_ch25.py")
