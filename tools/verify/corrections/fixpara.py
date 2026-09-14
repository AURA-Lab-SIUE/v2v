import io, pathlib, sys

p = pathlib.Path("/Volumes/One Touch/20-research/aura-lab/v2v/planning/v4-read-through-review.md")
t = io.open(p, encoding="utf-8").read()

broken = ("**They have moved.** Editing them for the 4th edition made them wrong for the\n"
          "3rd, and they were still sitting in , which is what the live book\n"
          "renders from on main. A merge would have silently broken the published edition.\n"
          "All seven now live in  alongside the other twenty, with\n"
          "their relative paths deepened a level, and  is byte-identical to\n"
          "what main publishes. The two editions can no longer corrupt each other.")

fixed = ("**They have moved.** Editing them for the 4th edition made them wrong for the\n"
         "3rd, and they were still sitting in `chapters/`, which is what the live book\n"
         "renders from on main. A merge would have silently broken the published edition.\n"
         "All seven now live in `chapters/_v3-draft/` alongside the other twenty, with their\n"
         "relative paths deepened a level, and `chapters/*.qmd` is byte-identical to what main\n"
         "publishes. The two editions can no longer corrupt each other.")

if broken in t:
    io.open(p, "w", encoding="utf-8", newline="\n").write(t.replace(broken, fixed))
    print("repaired the paragraph")
elif fixed in t:
    print("already repaired")
else:
    sys.exit("paragraph not found in either form")
