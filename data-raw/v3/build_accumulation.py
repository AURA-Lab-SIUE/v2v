"""Real data with the shape of a saturation curve, for the Chapter 16 supplement.

Chapter 16 argues that "saturation" is only worth anything with a stated procedure
behind it. The procedure is an accumulation curve: order your cases, and after each
one count how many categories you have seen that you had not seen before. When new
categories stop arriving, that is the evidence.

Interview transcripts do not exist for this book, and inventing them would teach
students to code something no human said. So the supplement demonstrates the
PROCEDURE on real data with the identical structure: channels are the cases, in a
fixed order, and the stream categories each one broadcasts are the "new categories".
The Excel technique is the same one you would run over interviews.

Input is the book fixture exported from the v2v R package:
    data(twitch_streams_sample, package = "v2v")  ->  twitch_streams_sample.csv
"""
import csv
from collections import OrderedDict

rows = list(csv.DictReader(open("twitch_streams_sample.csv", encoding="utf-8", errors="replace")))

# One row per (channel, game) pair, channels in a fixed alphabetical order so the
# exercise is reproducible and does not depend on however the file happened to sort.
# The raw data carries BOTH "minecraft" and "Minecraft" as category strings. They are
# one category, so they are normalized to a single canonical spelling here rather than
# counted twice. Worth knowing: Excel's COUNTIFS is case-insensitive and would silently
# merge them anyway, which means a student comparing Excel against a case-sensitive tool
# gets two different category counts and no warning from either.
canon = {}
seen = OrderedDict()
collisions = set()
for r in rows:
    game = (r["game"] or "").strip()
    if not game:
        continue                      # 1% of snapshots carry no category; excluded and reported
    key = game.casefold()
    if key in canon and canon[key] != game:
        collisions.add((canon[key], game))
    canon.setdefault(key, game)
    seen.setdefault(r["channel"], set()).add(canon[key])

out = []
for order, channel in enumerate(sorted(seen), start=1):
    for game in sorted(seen[channel]):
        out.append({"case_order": order, "channel": channel, "category": game})

with open("accumulation.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["case_order", "channel", "category"])
    w.writeheader()
    w.writerows(out)

# The reference answer the supplement must reproduce in Excel.
first_seen, cumulative, per_case = set(), [], []
for order, channel in enumerate(sorted(seen), start=1):
    new = [g for g in sorted(seen[channel]) if g not in first_seen]
    first_seen.update(new)
    per_case.append((order, channel, len(new), len(first_seen)))
    cumulative.append(len(first_seen))

print(f"rows: {len(out)}  cases (channels): {len(seen)}  distinct categories: {len(first_seen)}")
if collisions:
    print(f"case-variant spellings normalized: {sorted(collisions)}")
print("\norder  channel              new  cumulative")
for o, c, n, cum in per_case[:6]:
    print(f"{o:>5}  {c:<20}{n:>4}{cum:>12}")
print("  ...")
for o, c, n, cum in per_case[-4:]:
    print(f"{o:>5}  {c:<20}{n:>4}{cum:>12}")
half = per_case[len(per_case)//2]
print(f"\nhalfway (case {half[0]}): {half[3]} of {len(first_seen)} categories seen "
      f"({100*half[3]/len(first_seen):.0f}%)")
last10 = per_case[-1][3] - per_case[-11][3]
print(f"new categories from the last 10 cases: {last10}")
