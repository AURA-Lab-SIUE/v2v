"""The pilot coding behind Chapter 10's reliability check.

The 3rd edition quoted a kappa of 0.236 from two coder rules that were described
but never written down, so the number could not be reproduced. This builds the
pilot from stated rules against the shipped fixture and writes pilot_coding.csv,
so the chapter's figures can be checked.

The two rules deliberately target the same loose idea, "high-energy messages",
in two different ways, which is the failure the chapter is about.

    data(twitch_chat_sample, package = "v2v")  ->  twitch_chat_sample.csv
"""
import csv
import re

EMOTES = ["LUL", "LULW", "OMEGALUL", "4Head", "Pog", "PogChamp",
          "monkaS", "Kappa", "cmonBruh", "BibleThump"]
ALLCAPS = re.compile(r"(?:^|[^A-Za-z])[A-Z]{4,}(?:[^A-Za-z]|$)")
N = 100

rows = []
with open("twitch_chat_sample.csv", encoding="utf-8", errors="replace") as f:
    for r in csv.DictReader(f):
        rows.append(r)
        if len(rows) == N:
            break

out = []
for r in rows:
    m = r["message"]
    a = any(e in m for e in EMOTES)            # coder A: contains a known emote token
    b = bool(ALLCAPS.search(m))                # coder B: contains an all-caps word of 4+
    out.append({"id": r["id"], "channel": r["channel"],
                "coder_a": int(a), "coder_b": int(b)})

with open("pilot_coding.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["id", "channel", "coder_a", "coder_b"])
    w.writeheader()
    w.writerows(out)

a_yes = sum(o["coder_a"] for o in out)
b_yes = sum(o["coder_b"] for o in out)
agree = sum(1 for o in out if o["coder_a"] == o["coder_b"])
both_yes = sum(1 for o in out if o["coder_a"] and o["coder_b"])
both_no = sum(1 for o in out if not o["coder_a"] and not o["coder_b"])
po = agree / N
pa, pb = a_yes / N, b_yes / N
pe = pa * pb + (1 - pa) * (1 - pb)
kappa = (po - pe) / (1 - pe)

print("wrote pilot_coding.csv, %d rows" % N)
print("  coder A flagged %d   coder B flagged %d" % (a_yes, b_yes))
print("  both yes %d   both no %d   agreed %d" % (both_yes, both_no, agree))
print("  observed agreement %.2f" % po)
print("  expected agreement %.4f" % pe)
print("  Cohen's kappa      %.4f" % kappa)
