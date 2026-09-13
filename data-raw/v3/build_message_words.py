"""Message-level file for the Chapter 7 Excel supplement.

The supplement's lesson is aggregation: the same rows, rolled up to a sender or
a channel, answer different questions. That needs message-level rows, and it
needs the word count already computed, because Excel's only native word count
splits on spaces and would disagree with the chapter's figures. The chapter
counts word-like tokens, which is the same rule Chapters 13 and 14 use.

Input is the book fixture exported to CSV from the v2v R package:

    data(twitch_chat_sample, package = "v2v")  ->  twitch_chat_sample.csv
"""
import csv
import re

words = lambda m: len(re.findall(r"[A-Za-z']+", m or ""))

rows = []
with open("twitch_chat_sample.csv", encoding="utf-8", errors="replace") as f:
    for r in csv.DictReader(f):
        rows.append({"channel": r["channel"], "sender": r["sender"],
                     "words": words(r["message"])})

with open("message_words.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["channel", "sender", "words"])
    w.writeheader()
    w.writerows(rows)
print(f"wrote message_words.csv, {len(rows)} rows")
