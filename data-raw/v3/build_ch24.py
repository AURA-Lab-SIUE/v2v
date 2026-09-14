"""Assemble v4 Chapter 24, Preparing, Describing, and Visualizing Data.

This is a merge of the owner's existing Chapter 11 (Wrangling the data) and
Chapter 12 (Visualizing the narrative), plus a describing section the old book
taught only in passing. Both sources carry R, so this builder lifts only the
paragraphs that are already tool-agnostic and writes replacements for the rest.
Paragraphs are extracted by anchor rather than retyped, so his prose arrives
exactly as written, and verify_ch24_lift.py proves it.

What the consolidation changes:

1. Old Ch11 opened by pointing at a table "loaded in Chapter 9". Chapter 9 in
   the v4 TOC is Measurement, Scales and Items, and the loading material has
   moved to the tool supplement, so the hook is made self-contained.
2. The levels-of-measurement reference moved from Chapter 8 to Chapter 9.
3. Forward pointers to "Chapter 12" (figures) now resolve inside this chapter,
   and pointers to "Chapter 13" (tests) become Chapter 25.
4. The dplyr verbs are taught as operations rather than as function names, and
   every worked transformation drops to the supplement.
5. A describing section is added between wrangling and visualizing, because the
   mean-versus-median material was the strongest thing in old Ch12 and was
   buried inside a figure discussion.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path("/Volumes/One Touch/20-research/aura-lab/v2v")
OUT = ROOT / "chapters/_v3-draft/chapter24-preparing-describing-visualizing.qmd"

src11 = (ROOT / "chapters/chapter11.qmd").read_text(encoding="utf-8")
src12 = (ROOT / "chapters/chapter12.qmd").read_text(encoding="utf-8")


def para(src, anchor, *subs):
    """Return the single paragraph containing anchor, with declared repairs applied."""
    body = re.sub(r"^```.*?^```", "", src, flags=re.S | re.M)
    hits = [p.strip() for p in body.split("\n\n") if anchor in p]
    if len(hits) != 1:
        sys.exit("anchor matched %d paragraphs, refusing to guess: %r" % (len(hits), anchor[:60]))
    p = hits[0]
    for old, new in subs:
        if old not in p:
            sys.exit("repair anchor not found in %r: %r" % (anchor[:40], old[:60]))
        p = p.replace(old, new, 1)
    return p


P = []
def add(*blocks):
    P.extend(blocks)


add('---\ntitle: "Chapter 24: Preparing, Describing, and Visualizing Data"\n---')

# ---------------------------------------------------------------- opening
add(para(src11, "The chat table you loaded in Chapter 9 cannot answer",
         ("The chat table you loaded in Chapter 9 cannot answer your research question.",
          "The chat table you collected cannot answer your research question.")))
add(para(src11, "This is the ordinary situation at this stage of a study"))

add("""Part VI is where a project stops being a design and becomes a result. This chapter covers the three things that happen to a dataset before anything is tested: getting it into shape, describing what is in it, and looking at it. Chapter 25 does the testing.

The order matters and it is routinely inverted. A great deal of bad analysis comes from running a test on a table nobody described and nobody looked at.""")

# ---------------------------------------------------------------- verbs
add("## The operations")

add("""Whatever tool you use, data preparation is built from a small number of operations, and they are the same operations in a spreadsheet, in R, in Python and in SPSS. Learning them as operations rather than as commands is what makes the next tool easy.

**Filtering** keeps the rows that meet a condition and drops the rest. **Selecting** keeps or drops columns. **Deriving** adds a new column computed from the ones already there, which is how a variable your codebook named but your data lacks comes into existence. **Sorting** reorders rows by a column's values. **Grouping and summarizing** collapses many rows into one per group, which is how you get a per-channel or per-condition figure out of a table of individual observations.

**Joining** brings columns from one table onto another by matching on a shared key. It is the one operation that is genuinely harder than it looks, and it gets its own section below.""")

add(para(src11, "The reason these verbs combine so well is a shared design",
         ("each one takes a data frame and returns a data frame. That is what lets the pipe string them into a sequence, the output of one verb flowing in as the input of the next.",
          "each one takes a table and returns a table. That is what lets them be strung into a sequence, the output of one operation flowing in as the input of the next.")))

add("""Every one of those steps is a decision, and the decisions are methodology rather than housekeeping. Which cases you excluded, how you treated missing values, where you drew a category boundary: each will be asked about, and each should be recorded where it can be found. In a script that record is a comment. In a spreadsheet it is a documentation sheet, because a spreadsheet otherwise keeps no history of what you did to it. The supplement to this chapter is mostly about that problem.""")

# ---------------------------------------------------------------- deriving
add("## Deriving the variables the study needs")

add("""Three variables in this book's running study do not exist in the raw data and have to be built.

**A readable time.** The raw `date` column is a run of very large numbers, and Chapter 9 classified it as interval data with a catch: the number is not a date in any form a person can read. What it holds is a count of milliseconds elapsed since midnight on the first of January, 1970, a reference moment called the **Unix epoch** that nearly every computer uses to keep time. Counting from it turns any instant into a single integer, which is precise and entirely unreadable.

Converting it back is the most error-prone small step in this chapter, and the reason is a factor of a thousand. Most date functions expect a count of **seconds**, and this column holds **milliseconds**. Hand the raw number to a function expecting seconds and every message lands tens of thousands of years in the future, which at least announces itself. The quieter failure is a tool that silently succeeds on a value it should have rejected.

The first message in the corpus carries the timestamp `1542578127023`, which is the evening of the 18th of November, 2018. If your conversion gives you a date in the year 50,000, you forgot to divide.

**Message length.** The character count of each message, which the codebook named and the file does not contain. It is a ratio variable in the Chapter 9 sense: a true zero, equal intervals, a count you can average.

The first three messages in the corpus run 23, 441 and 8 characters: a row of punctuation, a block of copy-pasted emotes, and a single word. All three are ordinary Twitch chat, and the distance between them is the raw material of the study.

**A gaming label.** This is the one the research question turns on, and it takes real work, so it gets its own section.""")

# ---------------------------------------------------------------- joining
add("## Joining, and the label that needed it")

add(para(src11, "The third transformation is the one the central research question turns on"))
add(para(src11, "Gaming or non-gaming is best understood as a property of the channel"))
add(para(src11, "The first step reaches into the stream table"))
add(para(src11, "The second step is a judgment, and it should be visible rather than buried"))

add("""The list the study used names fourteen Twitch categories as non-gaming: Art, ASMR, Beauty & Body Art, Creative, Food & Drink, IRL, Just Chatting, Makers & Crafting, Music, Music & Performing Arts, Science & Technology, Sports & Fitness, Talk Shows & Podcasts, and Travel & Outdoors. Any channel whose dominant category is not on that list is treated as gaming.

Write the list out, in the paper or its appendix. A reader who disagrees with one entry can then see exactly what it would change, and "we classified channels as gaming or non-gaming" gives them nothing to disagree with.

The third step is the **join**: attach that one-row-per-channel lookup to every message, matching on the channel name. A join that keeps every row of the message table and adds the matching label is the one you want here, because losing messages to a failed match is the thing you are trying to avoid.""")

add(para(src11, "A join is only as good as the match between its keys"))

add("""Inspect the derived column immediately, before doing anything else with it. Counting the messages in each category gives 3,457 non-gaming, 31,309 gaming, and **501 with no label at all**.

That last group is the part worth understanding. Two channels in the corpus streamed without ever having a category recorded, so they have no dominant category, so the join found nothing to attach. The result is correct rather than broken: the data genuinely does not say whether those 501 messages came from gaming channels, and an honest missing value records that the study cannot classify them. They sit out the comparison rather than being guessed into one side of it.

A tool that had quietly dropped those rows, or quietly assigned them to the larger group, would have produced a tidier table and a worse study.""")

# ---------------------------------------------------------------- tidy
add("## The analysis-ready table")

add(para(src11, "This is what wrangling was for. The table is now **tidy**"))

add(para(src11, "None of this was analysis. Not a single result has been computed.",
         ("every figure in Chapter 12 and every test in Chapter 13",
          "every figure in this chapter and every test in Chapter 25")))

# ---------------------------------------------------------------- describing
add("## Describing before testing")

add("""With a tidy table you can finally say what is in it, and the temptation is to say it with one number per group and move on.

Three numbers describe a single numeric variable, and you need all three.

**The mean** is the arithmetic average, and it uses every value. **The median** is the value of the middle observation when they are sorted, and it does not care how extreme the extremes are. **The standard deviation** summarizes how far values typically sit from the mean.

Here they are for the study's central variable, message length, split by the label built above. The gaming row counts 31,305 rather than 31,309 because four messages in the corpus have no text at all, so they have no length and sit out every statistic in the row:

| Group | n | mean | median | sd |
|---|---|---|---|---|
| non-gaming | 3,457 | 33.70 | 16 | 60.68 |
| gaming | 31,305 | 28.49 | 17 | 38.47 |

Read the `mean` column and a story jumps out. Read the `median` column and it collapses.""")

add(para(src12, "Read the `mean` column and a story jumps out"))

add("""Note the standard deviations too, because they are the loudest signal in the table and the easiest to skip. Non-gaming messages vary far more than gaming ones, 60.68 against 38.47, and a standard deviation nearly twice a group's own mean is a warning that the mean is describing a shape it does not fit.

Chapter 23's supplement made the same point with the same corpus from a different angle: the mean participant posted 2.09 messages and the median posted one. **Whenever a mean and a median disagree, the distribution is telling you something, and the way to hear it is to look.**""")

# ---------------------------------------------------------------- visualizing
add("## Looking at it")

add(para(src12, "A figure is the instrument that makes the pattern visible",
         ("This chapter builds three", "This section builds three")))

add("""A figure does not merely display data. A well-made figure carries an argument: it shows a reader what the analyst found and why it matters. Visualization is part of the analysis rather than decoration applied after it.""")

add("### The grammar")

add(para(src12, "Three parts do most of the work. The first is the **data**"))

add("""Named that way, the choice of chart stops being a menu of pictures and becomes a question with an answer: what is being mapped to position, and what geometry suits the kind of variable doing the mapping? Three questions from the running study, three answers.""")

add("### A line for change over time")

add(para(src12, "The first question is about viewership"))
add(para(src12, "When the horizontal axis is time and the vertical axis is a quantity that rises and falls"))

add("""The figure has an obvious headline: the line that dominates it is "Other", the catch-all holding every game outside the top five, which spikes far above any named category.

That fact can be read two ways and a careful analyst holds both. One reading is substantive, that viewership here is spread across a long tail of smaller games rather than concentrated in the big ones. The other is an artifact of the analyst's own choice, since "Other" is large precisely because the top five was set at five. A category you created is not a finding about the world, and a figure whose headline is your own binning decision needs that said out loud.""")

add("### A bar for counts")

add(para(src12, "The second question is about timing"))
add(para(src12, "Hour of day is not a continuous sweep the way a date is"))
add(para(src12, "The figure shows a clear daily pulse"))

add("### A histogram for shape")

add(para(src12, "The third question is the study's central one"))
add(para(src12, "This question is not about a total or a trend. It is about a **distribution**"))

add("""Two choices shape a histogram and both have to be disclosed. **Bin width** sets how wide each bar is: wider bins smooth the shape, narrower bins roughen it, and the number is a judgment you make and report. **Capping the axis** hides the far tail so the bulk of the data is visible, and it is legitimate only if you say what it hid. Here the display caps at 120 characters, which puts 1,047 messages, three percent of the corpus, out of view, stretched thinly all the way out to 501 characters.

A cap that removes three percent to make the other ninety-seven legible is a good trade. A cap that removes a third of the data is a different figure entirely.""")

add(para(src12, "The figure shows, first, a shape both groups share"))
add(para(src12, "The histogram explains how both things can be true at once"))
add(para(src12, "This is what it means to treat descriptive statistics as a visual setup rather than a verdict"))

# ---------------------------------------------------------------- readable
add("## Figures other people can read")

add(para(src12, "Three figures are built. Before they are finished"))
add(para(src12, "The first duty is **color**"))
add(para(src12, "The second duty is the **alt text**"))
add(para(src12, "A figure that is honest about its choices"))

# ---------------------------------------------------------------- ahead
add("## Looking ahead")

add(para(src12, "The histogram left a precise question on the table"))

add("""Chapter 25 answers it. It is the chapter where a difference you can see becomes a difference you can defend, and where the size of that difference finally gets reported alongside the question of whether it is real.""")

add("""## References

Wickham, H. (2014). Tidy data. *Journal of Statistical Software*, *59*(10), 1-23. https://doi.org/10.18637/jss.v059.i10

Wilkinson, L. (2005). *The grammar of graphics* (2nd ed.). Springer. https://doi.org/10.1007/0-387-28695-0""")

OUT.write_text("\n\n".join(P) + "\n", encoding="utf-8")
words = len(OUT.read_text(encoding="utf-8").split())
print("wrote %s (%d words)" % (OUT, words))
