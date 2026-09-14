"""Two residual instances of the old headline figure, plus a gloss I got wrong.

Line 78's "fifty-five characters" is a false positive and is left alone. Line 189
is real: "what those five characters are made of" still refers to the gap.

The gloss on the first three messages called the second one Spanish. Its sender
is `gabrielecaruso17` and the phrase is Italian.
"""
import io
import pathlib
import sys

R = pathlib.Path("/Volumes/One Touch/20-research/aura-lab/v2v")

E = {
"chapters/_v3-draft/chapter25-inference-and-effect.qmd": [
 ("it does not say what those five characters are made of",
  "it does not say what those 2.43 characters are made of"),
],
"chapters/_v3-draft/chapter24-preparing-describing-visualizing.qmd": [
 ("a French stream title echoed back, a Spanish handle with a scoreline, and a Turkish phrase",
  "a French stream title echoed back, an Italian one with a scoreline, and a Turkish phrase"),
],
}

for name, edits in E.items():
    p = R / name
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
        print("patched %s" % name.split("/")[-1])
