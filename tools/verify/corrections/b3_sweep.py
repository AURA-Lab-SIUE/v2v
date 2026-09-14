"""Mechanism B3: the last files still describing a 50-channel corpus.

Chapter 1's roles paragraph, Chapter 6's three model prospectuses and its
feasibility test, and the structured-listening supplement, which says "fifty
channels" inside a sentence that is otherwise word-for-word identical to
Chapter 12's "228 channels".
"""
import io
import pathlib
import sys

R = pathlib.Path("/Volumes/One Touch/20-research/aura-lab/v2v")

E = {
"chapters/_v3-draft/chapter01-the-science-of-storytelling.qmd": [
 ("The **working corpus** is a 50-channel subset stratified by chat volume so that the head, the middle, and the long tail of Twitch are all represented in the sample students actually load into R. The **anchor set** is eight channels inside that 50",
  "The **working corpus** is a 228-channel subset built so that both sides of the book's central comparison are usable: every non-gaming channel in the population, and an equal number of gaming channels drawn across the head, the middle, and the long tail of Twitch. The **anchor set** is eight channels inside those 228"),
],
"chapters/_v3-draft/chapter06-the-prospectus.qmd": [
 ("from the 50-channel Twitch working corpus, code each message",
  "from the Twitch working corpus, code each message"),
 ('"Chat participation in the 50-channel Twitch working corpus" is.',
  '"Chat participation in the 228-channel Twitch working corpus" is.'),
 ("among the 50 channels in the Twitch working corpus?",
  "among the 228 channels in the Twitch working corpus?"),
 ("a stratified sample of 1,500 chat messages from the 50-channel Twitch working corpus shipped with the course",
  "a stratified sample of 1,500 chat messages from the 228-channel Twitch working corpus shipped with the course"),
 ("a stratified sample of 1,000 chat messages from the 50-channel working corpus, split between",
  "a stratified sample of 1,000 chat messages from the 228-channel working corpus, split between"),
 ("A stratified sample of 1,000 chat messages from the 50-channel working corpus will be drawn",
  "A stratified sample of 1,000 chat messages from the 228-channel working corpus will be drawn"),
 ("Fifty channels is manageable; the full population of 1,690 is not, for one person in a semester.",
  "Two hundred and twenty-eight channels is manageable, because the sampling was done for you; the full population of 1,690 is not, for one person in a semester."),
],
"supplements/structured-listening.qmd": [
 ("fifty channels drawn from across the platform's volume distribution",
  "228 channels drawn from across the platform's volume distribution"),
],
}

for name, edits in E.items():
    p = R / name
    if not p.exists():
        sys.exit("missing %s" % name)
    t = io.open(p, encoding="utf-8").read()
    o = t
    for old, new in edits:
        if old not in t:
            if new in t:
                continue
            sys.exit("[%s] NOT FOUND: %r" % (name, old[:100]))
        t = t.replace(old, new)
    if t != o:
        io.open(p, "w", encoding="utf-8", newline="\n").write(t)
        print("  patched %s" % name.split("/")[-1])
print("B3 done")
