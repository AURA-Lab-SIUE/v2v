"""The appendix I just wrote claimed sample_v3.py ships inside the package. It
does not: data/v2v-source/ is untracked in v2v-r and the file exists only on the
author's machine. That is the same defect as the D:/hub/... path this rewrite
removed, reintroduced two paragraphs later by me.

What IS reachable: the v2v book repository tracks 17 build scripts in
data-raw/v3/ which produce every derived CSV the chapters and supplements quote.
The fixture sampler is not among them.
"""
import io
import pathlib
import sys

p = pathlib.Path("/Volumes/One Touch/20-research/aura-lab/v2v/appendices/data-dictionary.qmd")
t = io.open(p, encoding="utf-8").read()

old = """The sampling script that produced these fixtures is `sample_v3.py`, shipped inside the package at `data/v2v-source/`. It is deterministic: the seed is recorded, and re-running it reproduces the fixtures exactly. It also carries a superset guarantee, which refuses to write output unless every channel from the previous fixture is retained, so that every worked example in earlier editions of this book still resolves.

If you want to know where a number in this book came from, that script and the `build_*.py` scripts alongside it are the answer, and they are the only answer this appendix will give you: no figure in the book is traceable to a document a reader cannot open."""

new = """**The derived files are fully traceable.** Every CSV the chapters and supplements quote from is produced by a script in the book's own repository under `data-raw/v3/`: `build_coded.py` makes the coded messages, `build_respondents.py` the respondent table, `build_switch.py` the category-switch events, and so on. If you want to know where a number came from, open the script that made it. They are public, they are deterministic, and they are the reason a reader can check this book rather than trust it.

**The fixtures themselves are one step less traceable, and the gap is worth naming.** The sampling script that drew the 228 channels, `sample_v3.py`, is deterministic and records its seed, and it carries a superset guarantee that refuses to write output unless every channel from the previous fixture is retained, so that examples in earlier editions still resolve. It is not currently published alongside the package. Until it is, the sampling design is documented in this appendix and reproducible in principle rather than in practice, which is a weaker claim than the one the rest of this section makes and is stated here rather than glossed over.

Chapter 27 argues that materials available on request are, in practice, unavailable. That applies to this book."""

if old in t:
    io.open(p, "w", encoding="utf-8", newline="\n").write(t.replace(old, new))
    print("appendix provenance corrected")
elif "one step less traceable" in t:
    print("already corrected")
else:
    sys.exit("provenance passage not found")
