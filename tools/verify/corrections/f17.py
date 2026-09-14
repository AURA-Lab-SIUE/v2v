import io, pathlib, sys
p = pathlib.Path("/Volumes/One Touch/20-research/aura-lab/v2v/supplements/excel/chapter17-focus-groups.qmd")
t = io.open(p, encoding="utf-8").read()
E = [
 ("| HOST | 0 | 32 |\n| P1 | 24 | 9 |\n| P2 | 30 | 2 |\n| P3 | 9 | 8 |\n| P4 | 3 | 14 |\n| P5 | 4 | 1 |\n| P6 | 1 | 3 |\n| P7 | 3 | 5 |",
  "| HOST | 0 | 29 |\n| P1 | 24 | 8 |\n| P2 | 25 | 3 |\n| P3 | 4 | 2 |\n| P4 | 7 | 6 |\n| P5 | 2 | 14 |\n| P6 | 3 | 3 |\n| P7 | 2 | 2 |"),
 ("returns **74**.", "returns **67**."),
 ("returns **0.432**.", "returns **0.433**."),
 ("The HOST has an out-degree of **zero** and an in-degree of **32**: never addresses anyone by name, and absorbs **43 percent** of everything directed at anybody.",
  "The HOST has an out-degree of **zero** and an in-degree of **29**: never addresses anyone by name, and absorbs **43 percent** of everything directed at anybody."),
 ("And notice the other 57 percent. P1 and P2 have out-degrees of 24 and 30 against in-degrees of 9 and 2, so they are talking to people other than the host and mostly not being answered.",
  "And notice the other 57 percent. P1 and P2 have out-degrees of 24 and 25 against in-degrees of 8 and 3, so they are talking to people other than the host and mostly not being answered."),
 ("The HOST took **8 turns** in this data, fewer than almost everyone,",
  "The HOST took **9 turns** in this data, fewer than almost everyone,"),
]
for a,b in E:
    if a not in t:
        if b in t: continue
        sys.exit("NOT FOUND: %r" % a[:110])
    t = t.replace(a,b)
io.open(p,"w",encoding="utf-8",newline="\n").write(t)
print("patched ch17 supplement")
