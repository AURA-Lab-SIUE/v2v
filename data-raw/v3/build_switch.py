"""A natural experiment in the corpus: what happens to chat when a streamer
switches category?

The experimental-design chapter has to teach manipulation and random assignment,
and archival data supports neither. What it DOES support is a quasi-experiment:
the streamer performs a real intervention at a known moment (switching into or
out of Just Chatting), and chat before and after can be compared. That is a
genuine design with genuine inferential limits, and naming those limits is the
teaching point.

Measures per message: word count, whether it asks a question, whether it is
shouted. Windows are symmetric around the switch so exposure time is equal.

Inputs are the two book fixtures exported to CSV from the v2v R package, which is
where the corpus is documented:

    data(twitch_chat_sample,    package = "v2v")   ->  twitch_chat_sample.csv
    data(twitch_streams_sample, package = "v2v")   ->  twitch_streams_sample.csv

Run from a directory holding both exports. Output switch_events.csv is committed
beside this script so the chapter's numbers can be checked without re-exporting.
"""
import csv
import re
import statistics as st
from collections import defaultdict

WINDOW_MIN = 45
NONGAME = "Just Chatting"

chat = list(csv.DictReader(open("twitch_chat_sample.csv", encoding="utf-8", errors="replace")))
streams = list(csv.DictReader(open("twitch_streams_sample.csv", encoding="utf-8", errors="replace")))

by_chan_chat = defaultdict(list)
for r in chat:
    by_chan_chat[r["channel"]].append((int(r["date"]), r["message"] or ""))
for v in by_chan_chat.values():
    v.sort()

snaps = defaultdict(list)
for r in streams:
    snaps[r["channel"]].append((int(r["date"]), r["game"]))
for v in snaps.values():
    v.sort()

def measures(msgs):
    if not msgs:
        return None
    words, q, shout = [], 0, 0
    for _, m in msgs:
        w = re.findall(r"[A-Za-z']+", m)
        words.append(len(w))
        q += "?" in m
        letters = [ch for ch in m if ch.isalpha()]
        shout += bool(letters) and sum(ch.isupper() for ch in letters) / len(letters) > .5
    return dict(n=len(msgs), words=st.mean(words),
                q=100 * q / len(msgs), shout=100 * shout / len(msgs))

events = []
for chan, sn in snaps.items():
    prev = None
    for ts, game in sn:
        if prev is not None and game != prev[1]:
            into = (game == NONGAME)
            out = (prev[1] == NONGAME)
            if into or out:
                events.append((chan, ts, prev[1], game, "into" if into else "out"))
        prev = (ts, game)

print(f"switch events involving {NONGAME}: {len(events)}")

rows = []
w = WINDOW_MIN * 60 * 1000
for chan, ts, g_before, g_after, direction in events:
    msgs = by_chan_chat.get(chan, [])
    before = [m for m in msgs if ts - w <= m[0] < ts]
    after = [m for m in msgs if ts <= m[0] < ts + w]
    b, a = measures(before), measures(after)
    if b and a and b["n"] >= 15 and a["n"] >= 15:
        rows.append(dict(channel=chan, direction=direction,
                         before_n=b["n"], after_n=a["n"],
                         d_words=a["words"] - b["words"],
                         d_q=a["q"] - b["q"], d_shout=a["shout"] - b["shout"]))

print(f"events with >=15 messages on BOTH sides of a {WINDOW_MIN}-minute window: {len(rows)}")
for r in rows:
    print(f"  {r['channel']:<16}{r['direction']:<6}n {r['before_n']:>3}/{r['after_n']:<3}"
          f" dwords {r['d_words']:+6.2f}  dq {r['d_q']:+6.1f}  dshout {r['d_shout']:+6.1f}")

if rows:
    for k in ("d_words", "d_q", "d_shout"):
        v = [r[k] for r in rows]
        print(f"{k:>9}: mean {st.mean(v):+.2f}  sd {st.pstdev(v):.2f}  n {len(v)}")
    with open("switch_events.csv", "w", newline="", encoding="utf-8") as f:
        wtr = csv.DictWriter(f, fieldnames=list(rows[0]))
        wtr.writeheader(); wtr.writerows(rows)
    print("wrote switch_events.csv")
