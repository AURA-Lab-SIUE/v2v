import io, pathlib, sys

p = pathlib.Path("/Volumes/One Touch/20-research/aura-lab/v2v/chapters/"
                 "_v3-draft/chapter19-qualitative-content-analysis.qmd")
t = io.open(p, encoding="utf-8").read()

old = ("The single most common thing a person types in this corpus is not a word. Across all "
       "157,080 messages, **31.7 percent contain exactly one word**, **56.6 percent contain "
       "three or fewer**, and **6.3 percent contain no alphabetic characters at all**. Just "
       "under a third of all messages, **31.7 percent**, are a single token with no spaces in "
       "them.")
new = ("The single most common thing a person types in this corpus is not a word. Across all "
       "157,080 messages, **31.7 percent contain exactly one word** and **56.6 percent contain "
       "three or fewer**. Just under a third of all messages are a single token with no spaces "
       "in them.\n\n"
       "A fourth figure is worth walking into slowly, because the obvious version of it is "
       "wrong. Ask how many messages contain no letters, write the rule as `[A-Za-z]`, and the "
       "answer is **6.3 percent**, which reads as a striking fact about emote-only speech. Ask "
       "the same question of letters in *any* alphabet and it falls to **2.5 percent**. The gap "
       "is **5,957 messages written in Cyrillic, Hangul, Thai and Greek**, which the first rule "
       "counted as having no letters in them. They are words. They are simply not in the "
       "alphabet the rule was written in.\n\n"
       "Nothing in the output announces that. Both numbers are the correct answer to the "
       "question each rule actually asked, and only one of them is the answer to the question "
       "that was meant. This is Chapter 9's validity problem arriving in a single regular "
       "expression, and it is the reason this chapter exists: a count is a reading, and the "
       "reading was done when the rule was written.")
if old in t:
    t = t.replace(old, new)
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("patched chapter19")
elif "5,957 messages written in Cyrillic" in t:
    print("chapter19 already current")
else:
    sys.exit("[ch19] NOT FOUND")
