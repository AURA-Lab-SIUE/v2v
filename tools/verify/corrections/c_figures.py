"""Mechanism C: wire the four Part VI figures in.

Chapter 24 discussed three figures and contained zero image references, then
claimed "Each figure in this chapter carries one" about alt text. Chapter 25
described a confidence-interval figure that was likewise absent.

The images that were on disk depicted the 50-channel corpus and could not be
reused; tools/make_figs_v4.R regenerates all four from the v0.3.0 fixture. Alt
text below carries the figure's information rather than describing its
appearance, which is the standard Chapter 24 itself sets.
"""
import io
import pathlib
import sys

R = pathlib.Path("/Volumes/One Touch/20-research/aura-lab/v2v")

F1 = ('![Total concurrent viewers across the 228 channels, summed within six-hour UTC buckets '
      'and split by category, over the November 2018 collection week.]'
      '(../../images/fig24-1-viewers-by-game.png){fig-alt="A line chart running from 18 to 24 '
      'November 2018, with one line per category and a sixth line pooling all others. The '
      'pooled line sits far above the rest for the whole week, peaking near 28.7 million '
      'summed concurrent viewers. Just Chatting is the largest named category and still runs '
      'well below the pooled line. Fortnite, Pokemon, Art and ASMR stay low and close to the '
      'axis throughout. Every line shows the same daily rise and fall."}')

F2 = ('![Chat messages by hour of day in UTC, across the collection window.]'
      '(../../images/fig24-2-chat-by-hour.png){fig-alt="A bar chart of message counts for each '
      'of the 24 hours of the day in UTC. The tallest bar is 22:00 at 10,967 messages and the '
      'shortest is 14:00 at 4,173, a ratio of about two and a half to one. Counts climb through '
      'the evening hours, peak between 21:00 and 23:00, and fall to their lowest in the early '
      'UTC afternoon."}')

F3 = ('![Message length for gaming and non-gaming channels, bin width five characters, lengths '
      'capped at 120.](../../images/fig24-3-msglen-by-context.png){fig-alt="Two histograms of '
      'message length, one panel per group, each with its own vertical scale so the shapes can '
      'be compared rather than the totals. Both are heavily right-skewed: most messages are '
      'under 20 characters and a long thin tail runs to the right. The two shapes are close to '
      'identical. A small pile-up appears at the 120-character cap in both panels, holding the '
      '3.6 percent of messages that run longer."}')

F4 = ('![Mean message length for each group with a ninety-five percent confidence interval, on '
      'an axis starting at zero.](../../images/fig25-1-means-ci.png){fig-alt="A dot-and-interval '
      'chart with two points on a vertical axis of message length running from zero to about 35 '
      'characters. Gaming channels average 29.5 characters and non-gaming channels 32.0. Both '
      'intervals are so short they are barely visible at this scale and the two do not overlap. '
      'The visual point is that both means sit close together and far above zero, so the gap '
      'between them is small next to the quantity being measured."}')

E = {
"chapters/_v3-draft/chapter24-preparing-describing-visualizing.qmd": [
 ("The figure has an obvious headline", F1 + "\n\nThe figure has an obvious headline"),
 ("The figure shows a clear daily pulse", F2 + "\n\nThe figure shows a clear daily pulse"),
 ("The figure shows, first, a shape both groups share", F3 + "\n\nThe figure shows, first, a shape both groups share"),
],
"chapters/_v3-draft/chapter25-inference-and-effect.qmd": [
 ("The intervals are so short they nearly vanish behind the points",
  F4 + "\n\nThe intervals are so short they nearly vanish behind the points"),
],
}

for name, edits in E.items():
    p = R / name
    t = io.open(p, encoding="utf-8").read()
    o = t
    for old, new in edits:
        if old not in t:
            sys.exit("[%s] anchor NOT FOUND: %r" % (name, old[:70]))
        if new.split("\n\n")[0] in t:
            continue
        t = t.replace(old, new, 1)
    if t != o:
        io.open(p, "w", encoding="utf-8", newline="\n").write(t)
        print("  wired figures into %s" % name.split("/")[-1])
print("C done")
