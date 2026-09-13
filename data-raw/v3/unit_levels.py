"""The three answers in Chapter 7's unit-of-analysis section.

The chapter's claim is that one corpus, one measure and three defensible units
give three different numbers, and that the spread is not an error. This produces
those numbers, plus the standard errors that show why nesting matters before the
analysis stage rather than after it.

Inputs are the two book fixtures exported to CSV from the v2v R package:

    data(twitch_chat_sample, package = "v2v")  ->  twitch_chat_sample.csv

Run from a directory holding the export.
"""
import csv
import re
import statistics as st
from collections import defaultdict

words = lambda m: len(re.findall(r"[A-Za-z']+", m or ""))

chat = list(csv.DictReader(open("twitch_chat_sample.csv", encoding="utf-8", errors="replace")))

by_sender, by_channel = defaultdict(list), defaultdict(list)
for r in chat:
    w = words(r["message"])
    by_sender[r["sender"]].append(w)
    by_channel[r["channel"]].append(w)

message = [words(r["message"]) for r in chat]
sender = [st.mean(v) for v in by_sender.values()]
channel = [st.mean(v) for v in by_channel.values()]

for label, v in (("message", message), ("sender", sender), ("channel", channel)):
    sd = st.stdev(v)
    print(f"unit = {label:<8} n = {len(v):>6}  mean = {st.mean(v):.2f}  "
          f"SD = {sd:.2f}  SE = {sd / len(v) ** 0.5:.4f}")

once = sum(1 for v in by_sender.values() if len(v) == 1)
print(f"\nsenders posting exactly once: {once} of {len(by_sender)}")
print(f"median messages per sender: {st.median(len(v) for v in by_sender.values()):.0f}")
