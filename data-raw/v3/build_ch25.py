"""Assemble v4 Chapter 25, Inference and Effect.

The body is the owner's existing Chapter 13 (Making the call), whose prose is
86 percent free of R already. Paragraphs are extracted by anchor rather than
retyped; verify_ch25_lift.py proves they arrived byte-identical.

What the consolidation changes:

1. Cross-references: the descriptive material was Chapter 12 and is now 24; the
   measurement levels were Chapter 8 and are now 9; the modal category was built
   in Chapter 11 and is now built in 24.
2. Two sentences referred to the old title, "Making the call". The v4 title is
   Inference and Effect, so they are rewritten to say what they meant.
3. Figures are corrected upstream in chapter13.qmd rather than repaired here,
   because they were wrong in the 3rd edition too. Four messages are true NA,
   so R drops them from every na.rm summary, t.test and lm; the published t
   (-4.95), n (34,766), coefficient (-5.22), regression t (-7.08) and
   intercept t (48.16) were all computed as though they carried a length.
4. Every "run this function" passage drops to the tool supplement; the results
   themselves stay, because the results are the lesson.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path("/Volumes/One Touch/20-research/aura-lab/v2v")
OUT = ROOT / "chapters/_v3-draft/chapter25-inference-and-effect.qmd"
src = (ROOT / "chapters/chapter13.qmd").read_text(encoding="utf-8")


MANIFEST = []


def para(anchor, *subs):
    MANIFEST.append({"anchor": anchor, "repaired": bool(subs)})
    body = re.sub(r"^```.*?^```", "", src, flags=re.S | re.M)
    hits = [p.strip() for p in body.split("\n\n") if anchor in p]
    if len(hits) != 1:
        sys.exit("anchor matched %d paragraphs, refusing to guess: %r" % (len(hits), anchor[:60]))
    p = hits[0]
    for old, new in subs:
        if old not in p:
            sys.exit("repair anchor not found in %r: %r" % (anchor[:40], old[:70]))
        p = p.replace(old, new, 1)
    return p


P = []
def add(*b):
    P.extend(b)


add('---\ntitle: "Chapter 25: Inference and Effect"\n---')

add(para("ended on a number and a doubt", ("Chapter 12 ended", "Chapter 24 ended")))
add(para("The doubt is not idle."))
add(para("Settling that doubt is the job of **inferential statistics**",
         ("The chapter's title names what is at stake. After describing a sample",
          "After describing a sample")))

add("## What a test actually asks")
add(para("Start with what the question really is."))
add(para("So the honest question is not"))
add(para("The test does not start from the difference you suspect is real"))
add(para("The logic is the logic of a skeptic."))

add("## Choosing the test")
add(para("There is not one hypothesis test.",
         ("the measurement levels from Chapter 8", "the measurement levels from Chapter 9")))
add(para("The chat study's question pairs one continuous variable with one categorical split."))

add("""A short map of the common cases, so the choice is a lookup rather than a guess:

| Outcome | Comparison | Test |
|---|---|---|
| continuous | two independent groups | independent-samples t-test |
| continuous | one group, two occasions | paired t-test |
| continuous | three or more groups | ANOVA |
| continuous | against a continuous predictor | correlation, or regression |
| categorical | against another categorical | chi-square |

Chapter 7's warning governs all of them. Every test in that table assumes the observations are independent, and messages from the same sender in the same channel are not. The corpus violates the assumption in a way that makes the test below optimistic about its own precision, which is stated here rather than discovered later.""")

add("## Running it, and reading the output")

add("""Every tool produces the same numbers here in a slightly different layout. What follows is the result, and the result is what matters.

```
Welch Two Sample t-test

t = -4.94, df = 3768.7, p-value = 8.1e-07

mean in group gaming      28.49
mean in group non-gaming  33.70
```""")

add(para("The test is named in the first line as a **Welch** two-sample t-test",
         ("Chapter 12 showed plainly", "Chapter 24 showed plainly")))
add(para("The rest of the output is the result, and it has three parts worth reading slowly."))

add("## Reading the p-value")
add(para("The **p-value** reported here is"))
add(para("It means this: if gaming and non-gaming chat truly had"))
add(para("That convention deserves a note of its own."))
add(para("What matters more is being precise about what the p-value does not say."))

add("""> "Scientific conclusions and business or policy decisions should not be based only on whether a p-value passes a specific threshold."
>
> Wasserstein & Lazar (2016, p. 131)""")

add("## How big is the difference")
add(para("For that, the p-value has to hand the question to a different number"))
add(para('A p-value answers "is there a difference."'))
add(para("To read that number, it needs a yardstick"))
add(para("This is worth dwelling on, because it sounds like a contradiction"))
add(para("That leaves one question: how did a negligible difference come back"))

add("## Seeing the difference")
add(para("The two facts, a real gap and a negligible one",
         ("puts both on the same axis:", "puts both on the same axis.")))
add(para("The intervals are so short they nearly vanish behind the points"))

add("## Statistical significance is not practical importance")
add(para("Putting the two numbers together is the call the chapter is named for",
         ("is the call the chapter is named for", "is the call this chapter has been building toward")))
add(para("The finding is this."))
add(para("This is the difference between **statistical significance** and **practical significance**"))
add(para("In practice that means a result is written up with the full set of numbers"))
add(para("> Gaming channels produced shorter chat messages on average"))
add(para("And then, because a string of statistics is not an interpretation"))

add("## More than two groups: ANOVA")
add(para("The t-test settled a question with exactly two sides",
         ("the modal category built in Chapter 11", "the modal category built in Chapter 24"),
         ("and four means appear rather than two:", "and four means appear rather than two:")))

add("""| Game category | n | mean length |
|---|---|---|
| Fortnite | 4,000 | 33.23 |
| Hearthstone | 3,004 | 36.82 |
| Just Chatting | 2,429 | 39.03 |
| League of Legends | 4,000 | 22.63 |

A t-test cannot settle this, because a t-test compares two means and there are four. Comparing them two at a time takes six separate tests, each carrying its own chance of a false positive, and those chances pile up. The test built for the whole comparison at once is the **analysis of variance**, or **ANOVA**, and it asks a single question of all the groups together: is any of these means different enough from the rest that chance is an unconvincing explanation?

```
           Df    Sum Sq  Mean Sq  F value   Pr(>F)
game        3    547281   182427    92.26   < 2e-16
Residuals 13429 26552407    1977
```""")

add(para("The logic is the t-test's logic, widened."))
add(para("And, exactly as with the t-test, significance is not size."))

add("## From difference to model: regression")
add(para("The t-test and ANOVA both compare group means."))

add("""Fit the original two-group question as a **linear model** of message length on gaming status, and the output is two numbers:

```
              Estimate  Std. Error  t value  Pr(>|t|)
(Intercept)     33.70       0.70      48.08   < .001
is_gamingTRUE   -5.21       0.74      -7.06   < .001
```""")

add(para("Read the two numbers."))
add(para("That the regression reproduces the t-test is not a coincidence."))

add("""## How much the finding depends on one decision

A test tells you whether a gap is larger than sampling noise. It cannot tell you whether the gap survives a different but equally defensible definition of the groups being compared. Here it does not, and that turns out to matter more than the test.

`is_gaming` was built as a property of the **channel**: each channel's modal category across the week, applied to every message that channel sent. The same data supports a second operationalization. Label each **message** by the category the channel was actually streaming when it was sent, read from the nearest earlier stream snapshot.

| How the label is defined | gaming | non-gaming | gap |
|---|---|---|---|
| the channel's modal category | 28.49 (n = 31,305) | 33.70 (n = 3,457) | +5.21 |
| the category on screen at the time | 29.11 (n = 30,707) | 28.13 (n = 4,044) | -0.98 |

Under the second definition the gap reverses direction, falls to about one character, and is no longer statistically significant: Welch's *t*(4993.6) = 1.34, *p* = .18.

Neither calculation is wrong, and they are not in competition. They answer different questions, and the distance between them is concentrated in one fact worth seeing plainly: **the non-gaming group is five channels.** `bobross`, `hitch`, `xqcow`, `tjsmith` and `darksydephil`, three of them at the corpus's 1,000-message cap, 3,457 messages between them. `xqcow` alone is 29 percent of the group, and that channel is filed under Just Chatting for most of the week while spending a good deal of it playing games. Under the channel-level label every one of its messages is non-gaming. Under the message-level label most of them are not.

Two things follow, and both belong in the write-up.

The **unit of analysis** problem is doing real work here. The label varies across 48 channels, five of which are non-gaming, while the test is computed over 34,762 messages. The p-value answers "could 34,762 independent draws have produced this gap by chance". The question that matters is "could five channels", and the answer to that one is much less comfortable.

And the **finding has to be stated at the level it was actually measured**. Not "gaming chat is shorter", but "chat on the five predominantly non-gaming channels in this sample is longer on average, by an amount too small to matter, and the difference does not survive relabelling messages by what was on screen at the time".

That is a duller sentence, and it is the one the data supports.""")

add("## What this chapter cannot do for you")

add("""Three limits, each of which has ended a paper in peer review.

**A test cannot repair a design.** Chapter 14 is where causal claims are earned, and no p-value computed on observational data converts a difference into a cause. Gaming channels have shorter messages; nothing here says the game caused it, and channel size, audience, and moderation all differ alongside it.

**A test cannot rescue a violated assumption.** The independence problem stated above does not go away because the output printed a number. Chapter 7 gives the naive standard error for these data as 0.036 against a clustered 0.355, a factor of roughly ten, which is the sort of gap that turns a confident finding into a shrug.

**A test cannot choose your threshold after the fact.** Deciding what counts as significant once you have seen the p-value, running several tests and reporting the one that worked, or splitting the sample until a difference appears, are all versions of the same error. Fix the analysis before you run it, and report what you ran, including what failed.

None of that makes the test worthless. It makes it one input to a judgment, which is the reading this chapter has asked for throughout.""")

add("## Looking ahead")

add("""The study now has a tested finding, honestly interpreted: a real difference, a negligible effect, and an assumption it is knowingly straining.

It also has a shape of question it cannot answer. The test says gaming and non-gaming chat differ by five characters; it does not say what those five characters are made of, or why anyone would type differently in a painting stream. Chapter 26 is about designs that go after both at once, and about the fact that combining methods is considerably harder than running two studies and stapling them together.""")

add("""## References

Cohen, J. (1988). *Statistical power analysis for the behavioral sciences* (2nd ed.). Lawrence Erlbaum Associates.

Lakens, D. (2013). Calculating and reporting effect sizes to facilitate cumulative science: A practical primer for *t*-tests and ANOVAs. *Frontiers in Psychology*, *4*, 863. https://doi.org/10.3389/fpsyg.2013.00863

Wasserstein, R. L., & Lazar, N. A. (2016). The ASA statement on p-values: Context, process, and purpose. *The American Statistician*, *70*(2), 129-133. https://doi.org/10.1080/00031305.2016.1154108""")

OUT.write_text("\n\n".join(P) + "\n", encoding="utf-8")
print("wrote %s (%d words)" % (OUT, len(OUT.read_text(encoding='utf-8').split())))

(ROOT / "data-raw/v3/ch25_lift_manifest.json").write_text(
    json.dumps({"source": "chapters/chapter13.qmd",
                "output": "chapters/_v3-draft/chapter25-inference-and-effect.qmd",
                "lifted": MANIFEST}, indent=2), encoding="utf-8")
