"""Repoint the references that meant the old Chapter 11.

Chapter 11 is now Sampling, and six of the eight references that pointed at it
for sampling became correct without being touched. The ones below meant the
wrangling chapter, which is now part of Chapter 24.
"""
import io
import pathlib
import sys

R = pathlib.Path("/Volumes/One Touch/20-research/aura-lab/v2v")

E = {
"chapters/_v3-draft/chapter01-the-science-of-storytelling.qmd": [
 # the six-day window's limits are Chapter 15's subject, not the wrangling chapter's
 ("Working within the limits of your data is itself a methodological skill, and Chapter 11 returns to it directly.",
  "Working within the limits of your data is itself a methodological skill, and Chapter 15 returns to it directly."),
],
"chapters/_v3-draft/chapter08-from-vibes-to-variables.qmd": [
 ("it carries a caveat worth stating now because Chapter 11 will spend real effort on it",
  "it carries a caveat worth stating now because Chapter 24 will spend real effort on it"),
],
"chapters/_v3-draft/chapter27-writing-and-publishing.qmd": [
 ("the content-analysis procedure from Chapter 12, and the wrangling steps from Chapter 11",
  "the sampling design from Chapter 11, the content-analysis procedure from Chapter 12, and the wrangling steps from Chapter 24"),
],
"supplements/open-workspace.qmd": [
 ("that is one of the technical problems Chapter 11 will solve",
  "that is one of the technical problems Chapter 24 will solve"),
],
"appendices/data-dictionary.qmd": [
 ("Chapter 11 uses the mismatch as a worked example of a join that fails silently",
  "Chapter 24 uses the mismatch as a worked example of a join that fails silently"),
 ("Chapter 11's headline conversion", "Chapter 24's headline conversion"),
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
            sys.exit("[%s] NOT FOUND: %r" % (name, old[:90]))
        t = t.replace(old, new)
    if t != o:
        io.open(p, "w", encoding="utf-8", newline="\n").write(t)
        print("  patched %s" % name.split("/")[-1])
print("references repointed")
