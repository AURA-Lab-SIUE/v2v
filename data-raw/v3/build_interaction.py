"""A who-addresses-whom dataset for the Chapter 17 supplement.

Chapter 17's central claim is Kitzinger's: in a focus group the data is what
participants say to EACH OTHER, and a session where everyone answers the moderator
in turn has produced parallel interviews instead. That claim is testable, and the
test is an interaction matrix.

Focus group transcripts do not exist for this book. This runs the same procedure on
real group talk with the same structure: one Twitch channel's chat, where an
at-mention is a message addressed to a named other participant. The host stands in
for the moderator. The Excel technique is identical to the one you would run over a
transcript whose turns you had attributed.

Participants are PSEUDONYMIZED, both because printing real usernames in a textbook
is wrong and because it is what Chapter 16's supplement just taught: the analysis
file carries ids, never identities.

Input is the book fixture exported from the v2v R package:
    data(twitch_chat_sample, package = "v2v")  ->  twitch_chat_sample.csv
"""
import csv
import re
from collections import Counter, defaultdict

CHANNEL = "bustaj"          # 1,000 messages across only 101 senders: small enough to matrix
N = 8                       # the size of a real focus group

chat = [r for r in csv.DictReader(open("twitch_chat_sample.csv", encoding="utf-8", errors="replace"))
        if r["channel"] == CHANNEL]

senders = {r["sender"].lower() for r in chat}
turns = Counter(r["sender"].lower() for r in chat)

edges = Counter()
for r in chat:
    s = r["sender"].lower()
    for m in re.findall(r"@(\w+)", r["message"] or ""):
        t = m.lower()
        if t in senders and t != s:
            edges[(s, t)] += 1

involvement = Counter()
for (a, b), n in edges.items():
    involvement[a] += n
    involvement[b] += n

top = [p for p, _ in involvement.most_common(N)]

# The channel owner is the host, and is the moderator analogue.
alias = {}
i = 0
for p in top:
    if p == CHANNEL:
        alias[p] = "HOST"
    else:
        i += 1
        alias[p] = f"P{i}"

with open("interaction.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["speaker", "addressee", "messages"])
    w.writeheader()
    for (a, b), n in sorted(edges.items()):
        if a in top and b in top:
            w.writerow({"speaker": alias[a], "addressee": alias[b], "messages": n})

with open("participants.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["participant", "turns"])
    w.writeheader()
    for p in top:
        w.writerow({"participant": alias[p], "turns": turns[p]})

# Reference answers the Excel version must reproduce.
out_deg, in_deg = Counter(), Counter()
total = 0
for (a, b), n in edges.items():
    if a in top and b in top:
        out_deg[alias[a]] += n
        in_deg[alias[b]] += n
        total += n

print(f"channel {CHANNEL}: {len(chat)} messages, {len(senders)} senders")
print(f"directed edges among the top {N}: {total}\n")
print(f"{'participant':<12}{'turns':>6}{'addressed others':>18}{'was addressed':>15}")
for p in sorted(alias.values(), key=lambda x: (x != "HOST", x)):
    real = [k for k, v in alias.items() if v == p][0]
    print(f"{p:<12}{turns[real]:>6}{out_deg[p]:>18}{in_deg[p]:>15}")
print(f"\nshare of all addressing that went to the HOST: "
      f"{100*in_deg['HOST']/total:.1f}%")
