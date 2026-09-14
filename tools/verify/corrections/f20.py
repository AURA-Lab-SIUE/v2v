import io, pathlib, sys

R = pathlib.Path("/Volumes/One Touch/20-research/aura-lab/v2v")

p = R / "chapters/_v3-draft/chapter20-discourse-conversation-analysis.qmd"
t = io.open(p, encoding="utf-8").read()
E = [
 ("That is measurable here. Taking every message in the corpus that addresses another participant by name and looking for the addressee's next message:\n\n"
  "- Only **6.5 percent** of addressed messages are followed *immediately* by the person addressed.\n"
  "- The median number of messages intervening is **16**.\n"
  "- Just **22 percent** see the addressee speak within five messages.\n"
  "- In **20 percent** of cases the addressee does not speak again in the channel at all.",
  "That is measurable here. Taking a thousand consecutive turns from one channel, finding every message that addresses another participant by name, and looking for the addressee's next message gives **89 addressed messages**:\n\n"
  "- Only **10 percent** of them are followed *immediately* by the person addressed.\n"
  "- Where a reply does come, the median number of messages intervening is **11**.\n"
  "- Just **26 percent** see the addressee speak within five messages.\n"
  "- In **18 percent** of cases the addressee does not speak again in the channel at all."),
 ("the addressee's reply, when it comes, arrives with a median of sixteen other messages stacked in front of it.",
  "the addressee's reply, when it comes, arrives with a median of eleven other messages stacked in front of it, and about four minutes."),
]
for a, b in E:
    if a not in t:
        if b in t:
            continue
        sys.exit("[ch20] NOT FOUND: %r" % a[:110])
    t = t.replace(a, b)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("patched chapter20")

p = R / "chapters/_v3-draft/chapter26-mixed-methods.qmd"
t = io.open(p, encoding="utf-8").read()
old = ("Chapter 20's finding that only 6.5 percent of addressed messages get an adjacent reply "
       "offers a mechanism, and interviews would be needed to confirm it.")
new = ("Chapter 20's finding that only 10 percent of addressed messages get an adjacent reply "
       "offers a mechanism, and interviews would be needed to confirm it.")
if old in t:
    t = t.replace(old, new)
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("patched chapter26")
elif new in t:
    print("chapter26 already current")
else:
    sys.exit("[ch26] NOT FOUND")
