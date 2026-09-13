"""Code every chat message on two manifest variables, for Chapter 12's supplement.

Both variables are manifest in Krippendorff's sense: they are read off the surface
by an explicit rule, with no interpretation, which is exactly the kind of variable
a machine can apply the codebook to. The chapter's latent variables are not coded
here, because a rule cannot do that job and pretending otherwise would teach the
wrong lesson.

  target  : "directed" if the message contains an @mention, else "broadcast"
  context : the stream's category at the moment the message was sent, reduced to
            "gaming" or "nongame"

Context is the category in force at the message's timestamp, taken from the most
recent stream snapshot at or before it, so a channel that switches mid-session is
counted correctly on both sides rather than by its overall habit.

Inputs are the two book fixtures exported to CSV from the v2v R package.
"""
import bisect
import csv
import re
from collections import defaultdict

NONGAME = {"Art", "Just Chatting", "Music & Performing Arts", "Talk Shows & Podcasts",
           "Food & Drink", "Science & Technology", "Creative", "Makers & Crafting",
           "Sports & Fitness", "Travel & Outdoors", "ASMR", "Beauty & Body Art"}

MENTION = re.compile(r"@\w")

chat = list(csv.DictReader(open("twitch_chat_sample.csv", encoding="utf-8", errors="replace")))
streams = list(csv.DictReader(open("twitch_streams_sample.csv", encoding="utf-8", errors="replace")))

snaps = defaultdict(list)
for s in streams:
    snaps[s["channel"]].append((int(s["date"]), s["game"]))
for v in snaps.values():
    v.sort()
times = {c: [t for t, _ in v] for c, v in snaps.items()}

rows, unmatched = [], 0
for r in chat:
    ch, ts = r["channel"], int(r["date"])
    ts_list = times.get(ch, [])
    i = bisect.bisect_right(ts_list, ts) - 1
    if i < 0:
        unmatched += 1
        continue
    game = snaps[ch][i][1]
    rows.append({
        "channel": ch,
        "target": "directed" if MENTION.search(r["message"] or "") else "broadcast",
        "context": "nongame" if game in NONGAME else "gaming",
    })

with open("coded_messages.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["channel", "target", "context"])
    w.writeheader()
    w.writerows(rows)

print(f"coded {len(rows)} messages; {unmatched} dropped with no prior snapshot")
tab = defaultdict(int)
for r in rows:
    tab[(r["context"], r["target"])] += 1
print(f"\n{'':<10}{'directed':>10}{'broadcast':>11}{'total':>9}{'%directed':>11}")
for ctx in ("gaming", "nongame"):
    d, b = tab[(ctx, "directed")], tab[(ctx, "broadcast")]
    print(f"{ctx:<10}{d:>10}{b:>11}{d+b:>9}{100*d/(d+b):>10.2f}%")
gd = tab[("gaming", "directed")] + tab[("nongame", "directed")]
gb = tab[("gaming", "broadcast")] + tab[("nongame", "broadcast")]
print(f"{'total':<10}{gd:>10}{gb:>11}{gd+gb:>9}{100*gd/(gd+gb):>10.2f}%")
