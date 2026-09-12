"""Turn chat logs into respondent-level rows: the bridge the survey chapter needs.

Each SENDER becomes a case, each derived measure a variable, exactly the shape a
questionnaire produces. The data is real and traceable; what it is NOT is survey
data, and the chapter has to say so. Dictionaries are hand-built and printed in
full so a student can see every word that drives a score, which a proprietary
lexicon would hide.
"""
import csv
import re
import statistics
from collections import Counter, defaultdict

chat = list(csv.DictReader(open("twitch_chat_sample.csv", encoding="utf-8", errors="replace")))
streams = list(csv.DictReader(open("twitch_streams_sample.csv", encoding="utf-8", errors="replace")))

NONGAME = {"Art", "Just Chatting", "Music & Performing Arts", "Talk Shows & Podcasts",
           "Food & Drink", "Science & Technology", "Creative", "Makers & Crafting",
           "Sports & Fitness", "Travel & Outdoors", "ASMR", "Beauty & Body Art"}
chan_games = defaultdict(Counter)
for s in streams:
    chan_games[s["channel"]][s["game"]] += 1
chan_nongame = {c: (g.most_common(1)[0][0] in NONGAME) for c, g in chan_games.items()}

POS = {"love", "great", "good", "nice", "awesome", "amazing", "best", "happy", "lol",
       "lmao", "haha", "thanks", "thank", "beautiful", "wow", "cool", "yes", "win"}
NEG = {"bad", "worst", "hate", "awful", "terrible", "boring", "trash", "stupid",
       "sucks", "cringe", "no", "wrong", "fail", "sad", "angry"}

rows = defaultdict(list)
for m in chat:
    rows[m["sender"]].append(m)

def build(minmsg):
    out = []
    for sender, msgs in rows.items():
        if len(msgs) < minmsg:
            continue
        lens, pos, neg, q, caps, ng = [], 0, 0, 0, 0, 0
        for m in msgs:
            t = m["message"] or ""
            words = re.findall(r"[a-z']+", t.lower())
            lens.append(len(words))
            pos += sum(w in POS for w in words)
            neg += sum(w in NEG for w in words)
            q += "?" in t
            letters = [c for c in t if c.isalpha()]
            caps += bool(letters) and sum(c.isupper() for c in letters) / len(letters) > .5
            ng += chan_nongame.get(m["channel"], False)
        tot = max(sum(lens), 1)
        out.append({
            "sender": sender,
            "messages": len(msgs),
            "mean_words": round(statistics.mean(lens), 2),
            "pos_rate": round(1000 * pos / tot, 2),
            "neg_rate": round(1000 * neg / tot, 2),
            "question_pct": round(100 * q / len(msgs), 1),
            "shouting_pct": round(100 * caps / len(msgs), 1),
            "nongame_pct": round(100 * ng / len(msgs), 1),
            "channels": len({m["channel"] for m in msgs}),
        })
    return out

for t in (2, 3, 5, 8, 10):
    print(f"  threshold >={t} messages -> {len(build(t)):>6} respondents")

data = build(5)
with open("respondents.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(data[0]))
    w.writeheader(); w.writerows(data)

print(f"\nwrote respondents.csv, n={len(data)}")
for v in ("messages", "mean_words", "pos_rate", "neg_rate", "question_pct", "shouting_pct", "nongame_pct"):
    vals = [r[v] for r in data]
    print(f"  {v:<14} mean {statistics.mean(vals):7.2f}  sd {statistics.pstdev(vals):6.2f}  "
          f"min {min(vals):6.2f}  max {max(vals):7.2f}")
ng = [r for r in data if r["nongame_pct"] >= 50]
g = [r for r in data if r["nongame_pct"] < 50]
print(f"\n  mostly non-gaming respondents: {len(ng)}   mostly gaming: {len(g)}")
for v in ("mean_words", "question_pct", "pos_rate"):
    print(f"    {v:<14} non-gaming {statistics.mean([r[v] for r in ng]):6.2f}   "
          f"gaming {statistics.mean([r[v] for r in g]):6.2f}")
