"""The setting's rhythm by hour, for the Chapter 18 supplement.

Chapter 18 warns that observation concentrated in one window is a study of that
window. That is checkable rather than merely sensible: if you know when the setting
is actually busy, you can measure what share of its activity your sessions spanned.

This produces the real half of that exercise. Every figure comes from the stream
snapshots: how many channels were live in each hour, and the mean total viewers.
The observation schedule a student logs against it is theirs to write, and is a
plan rather than data, which is why none is shipped here.

Hours are UTC, stated explicitly because a coverage matrix in the wrong timezone
is confidently wrong rather than obviously wrong.

Input is the book fixture exported from the v2v R package:
    data(twitch_streams_sample, package = "v2v")  ->  twitch_streams_sample.csv
"""
import csv
import datetime as dt
from collections import defaultdict

rows = list(csv.DictReader(open("twitch_streams_sample.csv", encoding="utf-8", errors="replace")))

live = defaultdict(set)
viewers = defaultdict(list)
for r in rows:
    h = dt.datetime.utcfromtimestamp(int(r["date"]) / 1000).hour
    live[h].add(r["channel"])
    viewers[h].append(int(r["viewers"]))

out = []
for h in range(24):
    v = viewers.get(h, [])
    out.append({
        "hour_utc": h,
        "channels_live": len(live.get(h, ())),
        "mean_viewers": round(sum(v) / len(v)) if v else 0,
    })

with open("coverage.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["hour_utc", "channels_live", "mean_viewers"])
    w.writeheader()
    w.writerows(out)

total = sum(r["mean_viewers"] for r in out)
busiest = max(out, key=lambda r: r["mean_viewers"])
quietest = min(out, key=lambda r: r["mean_viewers"])

print(f"wrote coverage.csv, 24 rows")
print(f"busiest hour : {busiest['hour_utc']:02d} UTC, mean {busiest['mean_viewers']:,} viewers")
print(f"quietest hour: {quietest['hour_utc']:02d} UTC, mean {quietest['mean_viewers']:,} viewers")
print(f"ratio: {busiest['mean_viewers']/quietest['mean_viewers']:.1f}x")
print(f"sum of mean_viewers across all 24 hours: {total:,}")

# Two illustrative schedules, to show what the diagnostic does.
def share(hours):
    return 100 * sum(r["mean_viewers"] for r in out if r["hour_utc"] in hours) / total

evenings = {22, 23, 0}
spread = {2, 7, 11, 15, 19, 23}
print(f"\nthree evening hours {sorted(evenings)}: {len(evenings)}/24 hours = "
      f"{100*len(evenings)/24:.0f}% of the clock, but {share(evenings):.1f}% of the activity")
print(f"six spread hours {sorted(spread)}: {len(spread)}/24 hours = "
      f"{100*len(spread)/24:.0f}% of the clock, and {share(spread):.1f}% of the activity")
