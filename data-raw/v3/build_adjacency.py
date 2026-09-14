"""Turn positions for one channel, for the Chapter 20 supplement.

Chapter 20 measures how far apart an addressed message and its addressee's reply
actually are, which is Herring's interactional coherence problem made countable.
This produces the table that measurement runs on.

No message text is shipped. The analysis needs only who spoke, who they addressed,
and when, so the file carries exactly that. The at-mention is extracted here because
pulling it out of free text in Excel is a MID and FIND exercise that teaches nothing
about discourse.

One channel, ordered by timestamp, with a 1-based turn index so "how many turns
later" is a subtraction.

Input is the book fixture exported from the v2v R package:
    data(twitch_chat_sample, package = "v2v")  ->  twitch_chat_sample.csv
"""
import csv
import re
from collections import Counter

CHANNEL = "rdulive"

rows = [r for r in csv.DictReader(open("twitch_chat_sample.csv", encoding="utf-8", errors="replace"))
        if r["channel"] == CHANNEL]
rows.sort(key=lambda r: int(r["date"]))

senders = {r["sender"].lower() for r in rows}

out = []
for i, r in enumerate(rows, start=1):
    mentions = [m.lower() for m in re.findall(r"@(\w+)", r["message"] or "")]
    # Only mentions of someone who also speaks in this channel can be followed up.
    addressed = next((m for m in mentions if m in senders and m != r["sender"].lower()), "")
    out.append({
        "turn": i,
        "sender": r["sender"].lower(),
        "addressed": addressed,
        "ts_ms": r["date"],
    })

with open("adjacency.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["turn", "sender", "addressed", "ts_ms"])
    w.writeheader()
    w.writerows(out)

# Reference answers the Excel version must reproduce.
by_sender = {}
for o in out:
    by_sender.setdefault(o["sender"], []).append(o["turn"])

gaps, secs, none = [], [], 0
addressed_rows = [o for o in out if o["addressed"]]
for o in addressed_rows:
    later = [t for t in by_sender.get(o["addressed"], []) if t > o["turn"]]
    if not later:
        none += 1
        continue
    nxt = min(later)
    gaps.append(nxt - o["turn"])
    secs.append((int(out[nxt - 1]["ts_ms"]) - int(o["ts_ms"])) / 1000)

import statistics as st
print(f"channel {CHANNEL}: {len(out)} turns, {len(senders)} senders")
print(f"messages addressing another sender: {len(addressed_rows)}")
print(f"  addressee never speaks again: {none}")
print(f"  addressee does speak again   : {len(gaps)}")
print(f"\ngap in turns: median {st.median(gaps):.0f}  mean {st.mean(gaps):.1f}  min {min(gaps)}  max {max(gaps)}")
print(f"  reply is the very next turn: {sum(1 for g in gaps if g == 1)} "
      f"({100*sum(1 for g in gaps if g == 1)/len(gaps):.1f}%)")
print(f"  within 5 turns: {100*sum(1 for g in gaps if g <= 5)/len(gaps):.1f}%")
print(f"\nseconds to reply: median {st.median(secs):.0f}  mean {st.mean(secs):.0f}")
