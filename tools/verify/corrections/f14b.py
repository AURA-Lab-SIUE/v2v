import io, pathlib, sys

R = pathlib.Path("/Volumes/One Touch/20-research/aura-lab/v2v")

# ---------------------------------------------------------------- supplement
p = R / "supplements/excel/chapter14-experimental-design.qmd"
t = io.open(p, encoding="utf-8").read()

NEW = """## The other outcome, in the same file

Everything above ran on column E. The file has two more difference columns and one of them behaves differently, which is worth seeing, because a supplement that only ever shows you a null teaches half the lesson.

Column G is `d_shout`: the change in the percentage of messages that are more than half capital letters. Point the same sixteen formulas at `G2:G77` and at the channel means built from it.

| | Naive | Clustered |
|---|---|---|
| n | 76 events | 33 channels |
| mean | -3.232 | -3.628 |
| SD | 10.263 | 9.392 |
| t | -2.745 | -2.219 |
| df | 75 | 32 |
| p | .0076 | .034 |
| d | -0.315 | -0.386 |

Here there is something. Shouting falls by about three and a half percentage points after a category switch, and unlike the word-count result it is still there once the channels are counted honestly.

Read this table against the last one, because between them they show the two things clustering does.

The **p-value got worse and the finding survived anyway**, .008 to .034. That is the ordinary case: you pay for the honest degrees of freedom, and if the effect is real you can afford it.

The **effect size got larger**, from -0.32 to -0.39. This is the pattern the word-count column did not show. Averaging within a channel strips out the variation between one channel's own events, so the standard deviation fell from 10.26 to 9.39 while the mean moved away from zero rather than toward it. A standardized effect is the mean over that standard deviation, so it grew. Larger is not better; it is a different question, about how much channels differ from each other rather than how much events do.

And the third column, `d_q`, the change in question rate, returns *t*(32) = 0.33, *p* = .74. Three measures, one result. Report all three, because reporting only the one that worked is the practice Chapter 6 names and Chapter 27 will not let you get away with.

"""

anchor = "## What Excel will not do for you"
if "## The other outcome, in the same file" not in t:
    i = t.index(anchor)
    t = t[:i] + NEW + t[i:]
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("added the d_shout section to the ch14 supplement")

# ---------------------------------------------------------------- chapter
p = R / "chapters/_v3-draft/chapter14-experimental-design.qmd"
t = io.open(p, encoding="utf-8").read()
E = [
 ("Across the fifty channels there are **54 category switches into or out of Just Chatting**. Comparing chat in a symmetric 45-minute window either side, and requiring at least fifteen messages on both sides so the measures are not noise, leaves **17 usable events across seven channels**.",
  "Across the 228 channels there are **178 category switches into or out of Just Chatting**. Comparing chat in a symmetric 45-minute window either side, and requiring at least fifteen messages on both sides so the measures are not noise, leaves **76 usable events across 33 channels**."),
 ("The result is consistent. After a switch, messages get shorter by about a word: a mean change of **-1.08 words**, SD 1.54, which against zero gives t(16) = -2.89, p = .011, and a standardized effect of d = -0.70. Question rate and shouting show nothing: -0.63 and -1.53 percentage points, p = .62 and p = .39.",
  "Three measures, and only one of them moves. Message length gives a mean change of **+0.21 words**, SD 1.99, t(75) = 0.93, p = .35, d = 0.11, which is nothing. Question rate gives p = .99, which is nothing twice over. **Shouting falls**: the percentage of messages that are more than half capitals drops by **3.23 points**, SD 10.26, t(75) = -2.75, p = .008, d = -0.32.\n\nThat pattern is itself worth stating plainly. Two of the three measures were chosen in advance and returned nothing, and reporting only the third would misrepresent the study. It is also the reason the one surviving result deserves more scepticism than it would get on its own: three tests were run."),
 ("Now the part that matters more than the result. Those seventeen events are not seventeen independent observations. Five of them come from a single channel, and one streamer's audience behaving one way is one fact, not five.",
  "Now the part that matters more than the result. Those seventy-six events are not seventy-six independent observations. Eleven of them come from a single channel, and one streamer's audience behaving one way is one fact, not eleven."),
 ("Averaging within channel first and testing across the seven channels gives **M = -1.07 words, SD 1.02, t(6) = -2.77, p = .032, d = -1.05**. The effect survives, the degrees of freedom collapse from 16 to 6, and the standardized effect gets *larger* rather than smaller, because averaging removed noise within channels. Both analyses are defensible and the clustered one is the honest one, because it matches the level at which the data are actually independent.",
  "Averaging within channel first and testing the shouting measure across the 33 channels gives **M = -3.63 points, SD 9.39, t(32) = -2.22, p = .034, d = -0.39**. The effect survives, the degrees of freedom collapse from 75 to 32, and the standardized effect gets *larger* rather than smaller, because averaging removed noise within channels. The message-length null survives too, at p = .57. Both analyses are defensible and the clustered one is the honest one, because it matches the level at which the data are actually independent."),
 ("So the defensible sentence is that chat messages were shorter after a category change in this corpus, that the pattern held across seven channels, and that the design cannot separate the change itself from what prompted it.",
  "So the defensible sentence is that chat shouted less after a category change in this corpus, that the pattern held across 33 channels, that message length and question rate did not move at all, and that the design cannot separate the change itself from what prompted it."),
]
for a, b in E:
    if a not in t:
        if b in t:
            continue
        sys.exit("CHAPTER NOT FOUND: %r" % a[:110])
    t = t.replace(a, b)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("patched chapter14")
