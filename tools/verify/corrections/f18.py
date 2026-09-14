import io, pathlib, sys
p = pathlib.Path("/Volumes/One Touch/20-research/aura-lab/v2v/supplements/excel/chapter18-ethnography.qmd")
t = io.open(p, encoding="utf-8").read()
E = [
 ("You should get a total of **178,792**, a busiest hour of **23** UTC, a quietest hour of **7** UTC, and a ratio of **3.39**.",
  "You should get a total of **110,495**, a busiest hour of **22** UTC, a quietest hour of **7** UTC, and a ratio of **2.92**."),
 ("The curve falls through the small hours, bottoms out around 07 UTC, and climbs to its peak late. **The setting is three and a half times busier at its peak than at its trough.**",
  "The curve falls through the small hours, bottoms out at 07 UTC, and climbs to its peak late. **The setting is nearly three times busier at its peak than at its trough.**"),
 ("**Evenings only,** hours 0, 22 and 23. That is **12.5 percent** of the clock and **20.4 percent** of the activity.",
  "**Evenings only,** hours 0, 22 and 23. That is **12.5 percent** of the clock and **19.2 percent** of the activity."),
 ("**Spread out,** hours 2, 7, 11, 15, 19 and 23. That is **25 percent** of the clock and **24.6 percent** of the activity.",
  "**Spread out,** hours 2, 7, 11, 15, 19 and 23. That is **25 percent** of the clock and **25.1 percent** of the activity."),
 ("Three hours buy a fifth of everything happening", "Three hours buy a fifth of everything happening"),
 ("A channel with four thousand viewers behaves differently from the same channel with twelve thousand:",
  "A channel with two and a half thousand viewers behaves differently from the same channel with seven and a half thousand:"),
 ("The spread schedule buys almost exactly proportional coverage, 25 percent of the clock for 24.6 percent of the activity,",
  "The spread schedule buys almost exactly proportional coverage, 25 percent of the clock for 25.1 percent of the activity,"),
]
for a,b in E:
    if a not in t:
        if b in t: continue
        sys.exit("NOT FOUND: %r" % a[:110])
    t = t.replace(a,b)
io.open(p,"w",encoding="utf-8",newline="\n").write(t)
print("patched ch18 supplement")
