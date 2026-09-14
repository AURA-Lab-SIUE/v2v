"""Wire the 4th edition together.

Three jobs:
  1. Lift v3's Chapter 7, "Structured listening", into a supplement, with its
     repairs declared here rather than made by hand. The Open Workspace moved
     the same way; both are hands-on material that dates faster than the
     reasoning around it, and neither is a chapter in the 4th edition.
  2. Repoint every cross-reference in the seven carried-over chapters, which
     were written when chapters 2, 7, 9, 10, 12, 13 and 14 held completely
     different content.
  3. Rewrite chapter 1's roadmap, which still describes a five-part,
     fourteen-chapter book.
"""
import io
import pathlib
import sys

R = pathlib.Path("/Volumes/One Touch/20-research/aura-lab/v2v")

# --------------------------------------------------------------- the lift
src = R / "chapters/chapter07.qmd"
dst = R / "supplements/structured-listening.qmd"
t = io.open(src, encoding="utf-8").read()

# drop the chapter-audio block: supplements do not carry one
a = t.index("::: {.chapter-audio")
b = t.index(":::\n", t.index("```\n", a)) + 4
t = t[:a] + t[b:]

LIFT = [
 ('title: "Chapter 7: Structured listening"',
  'title: "Supplement: Structured Listening"'),
 ("In Chapter 2 you looked at ten rows of the `stream_log` and watched Sodapoppin's audience climb:",
  "The Open Workspace supplement prints ten rows of the `stream_log`, in which Sodapoppin's audience climbs:"),
 ("This chapter is about that looking.",
  "This supplement is about that looking."),
 ("Watching them is the work of this chapter.",
  "Watching them is the work of this supplement."),
 ("You arrived at this chapter with a prospectus.",
  "You arrive here with a prospectus."),
 ("it is the same principle that will govern statistical sampling in Chapter 10",
  "it is the same principle that governs statistical sampling in Chapter 13"),
 ("## Looking ahead\n\nChapter 8 is where vibes become variables",
  "## Where this goes\n\nChapter 8 is where vibes become variables"),
]
for old, new in LIFT:
    if old not in t:
        sys.exit("[lift] NOT FOUND: %r" % old[:90])
    t = t.replace(old, new)

HEAD = """<!-- Lifted from the 3rd edition's Chapter 7, "Structured listening", with the
repairs declared in tools/verify/corrections/v4_wire.py. It is a supplement in
the 4th edition rather than a chapter because immersion is hands-on practice
rather than a method the book owes an account of; Chapter 18 is where
observation is treated as a method. Chapter 8 depends on the field notes this
produces, so work through it before operationalizing anything. -->

"""
t = t.replace("---\n\n", "---\n\n" + HEAD, 1)
io.open(dst, "w", encoding="utf-8", newline="\n").write(t)
print("lifted %s -> %s" % (src.name, dst.name))

# ------------------------------------------------- the carried-over chapters
CH01_ROADMAP_OLD = """The book is organized around the research process itself, divided into five parts that mirror the narrative arc this chapter has been describing.

**Part I: Foundations (Chapters 1 to 3)** sets up the intellectual and technical infrastructure. You will build habits of mind and workflow, plus the reproducibility principles that distinguish rigorous research from improvised analysis. Chapter 3 takes up research ethics, the constraint that all subsequent work has to honor.

**Part II: Planning (Chapters 4 to 6)** is where you design the study. Literature review, theoretical framework, research questions, and a project prospectus that maps what you will study, why it matters, and how you will proceed.

**Part III: Operationalization (Chapters 7 to 9)** is where you turn vague constructs into measurable variables. Sustained observation of the data, the move from qualitative noticing to quantitative coding, the construction of a codebook, and a first hands-on session with R. The book teaches content analysis end to end because depth in one method serves you better than shallow coverage of four, but it does not pretend the other major social-science methods (surveys, experiments, qualitative interviews and focus groups) do not exist. Chapter 5 introduces them as a coherent set when it discusses how theory selection shapes method choice. Chapter 9 stays focused on the first-R-contact work that the rest of the lab depends on. The V2V Hub holds the deeper hands-on material for any of these methods you want to pursue.

**Part IV: Execution (Chapters 10 to 12)** is the work itself. Sampling, inter-coder reliability, data wrangling, descriptive statistics, visualization. The chapters where you spend the most time in the IDE.

**Part V: Inference and publication (Chapters 13 to 14)** is the closing arc. You run inferential tests, interpret what they mean, and publish a portfolio that integrates the whole project into a single reproducible document.

A small note on tooling, taken up properly in Chapter 2. This book teaches the canonical version of each task."""

CH01_ROADMAP_NEW = """The book is organized around the research process itself, divided into six parts that mirror the narrative arc this chapter has been describing.

**Part I: Foundation (Chapters 1 to 3)** sets up how to think about research before doing any. Chapter 2 is on the three paradigms that divide the field, what each treats as an answer, and how the social scientific one accounts for its own failures. Chapter 3 takes up research ethics, the constraint that all subsequent work has to honor.

**Part II: Planning (Chapters 4 to 6)** is where you design the study. Literature review, theoretical framework, research questions, and a project prospectus that maps what you will study, why it matters, and how you will proceed.

**Part III: Quantitative Methods (Chapters 7 to 15)** turns a question into evidence you can count. Research design, the move from qualitative noticing to quantitative coding, measurement and scales, reliability and validity, data wrangling, and then the four designs themselves: content analysis, surveys, experiments, and working with data somebody else collected. Content analysis is taught end to end, because depth in one method serves you better than shallow coverage of four, and the other three get a chapter each.

**Part IV: Qualitative Methods (Chapters 16 to 21)** is the other half of the field rather than an appendix to this one. Interviewing, focus groups, ethnography, qualitative content analysis, discourse and conversation analysis, and then the chapter all of them point at: how language becomes a finding through coding.

**Part V: Rhetorical and Critical Analysis (Chapters 22 and 23)** changes the question again. Neither chapter codes or counts. They read closely, one to evaluate how a text attempts to persuade and one to ask whose interests an arrangement serves.

**Part VI: Analysis and Publication (Chapters 24 to 27)** is the closing arc. Preparing, describing and visualizing data, inferential tests and what they do and do not license, mixed methods, and finally the report itself and the business of publishing it.

Two supplements sit outside that arc because they are hands-on practice rather than method. *The Open Workspace* installs the tools and opens the dataset for the first time; *Structured Listening* is the immersion in the live medium that Chapter 8 assumes you have done. There is also an Excel supplement for most chapters in Parts III through VI, which does that chapter's analysis in a spreadsheet for readers who are not yet working in R.

A small note on tooling, taken up properly in *The Open Workspace*. This book teaches the canonical version of each task."""

F = {
"chapters/chapter01.qmd": [
  (CH01_ROADMAP_OLD, CH01_ROADMAP_NEW),
  ("Chapter 5 explores these paradigms in more depth.",
   "Chapter 2 explores these paradigms in more depth."),
],
"chapters/chapter06.qmd": [
  ("Chapter 7 begins Part III, where planning becomes practice. Before you can code a single chat message, you have to know the data the way a researcher knows it: not as an abstraction described in a prospectus, but as a texture you have spent real time inside. Chapter 7 is about that immersion, the structured listening that turns a dataset into something you understand well enough to operationalize.",
   "Chapter 7 begins Part III, where planning becomes practice. It is on research design: the plan that connects the question you just wrote to evidence that could actually answer it, and the four decisions every design has to make about cases, measures, timing and comparison.\n\nBefore Chapter 8 asks you to operationalize anything, work through the *Structured Listening* supplement. You cannot code a medium you have not watched, and the field notes it produces are what Chapter 8 turns into a codebook."),
],
"chapters/chapter08.qmd": [
  ("Somewhere in the field-notes document you built in Chapter 7 is an entry like this one:",
   "Somewhere in the field-notes document you built working through the *Structured Listening* supplement is an entry like this one:"),
  ("Chapter 7's observation complicated the simple two-way split,",
   "That observation complicated the simple two-way split,"),
  ("Recall the preview from Chapter 2: channel, title, game, viewers, date.",
   "Recall the preview in *The Open Workspace*: channel, title, game, viewers, date."),
  ("A ratio variable can be averaged, correlated, and entered into the kind of test Chapter 13 runs.",
   "A ratio variable can be averaged, correlated, and entered into the kind of test Chapter 25 runs."),
  ("Chapter 10 covers those statistics and how to act on them; for now, the point is conceptual.",
   "Chapter 10 covers those statistics and how to act on them; for now, the point is conceptual."),
  ("This is where the edge cases from your Chapter 7 observation log earn their keep.",
   "This is where the edge cases from your observation log earn their keep."),
  ("It is usually empty in a first draft and fills in as you pilot the codebook, which is Chapter 10's work.",
   "It is usually empty in a first draft and fills in as you pilot the codebook, which is Chapter 10's work."),
  ("the study the prospectus in Chapter 6 committed to and the observation in Chapter 7 sharpened",
   "the study the prospectus in Chapter 6 committed to and the observation supplement sharpened"),
  ("Chapter 9 is first contact with the data inside R. You have a research question, a theoretical frame, a prospectus, a field-notes document, and now a draft codebook. What you have not yet done is open the dataset in the tool you will analyze it with. Chapter 9 is where the planning stops and the code begins: you will load `chat_log` and `stream_log`, look at their structure, and confirm that the data you have designed a study around is the data you actually have.",
   "Chapter 9 is on measurement: scales, items, and the levels of measurement this chapter has been using informally. You have a research question, a theoretical frame, a prospectus, a field-notes document, and now a draft codebook. Chapter 9 asks the harder question about all of it, which is whether the thing you are about to count is the thing you meant, and Chapter 10 asks whether two people applying your codebook would count it the same way."),
],
"chapters/chapter11.qmd": [
  ("The chat table you loaded in Chapter 9 cannot answer your research question.",
   "The chat table as it ships cannot answer your research question."),
  ("Start with the timestamps, because Chapter 9 already flagged them.",
   "Start with the timestamps, because *The Open Workspace* already flagged them."),
  ("Chapter 12 will use exactly that to chart how chat volume rises and falls across the hours of the day.",
   "Chapter 24 will use exactly that to chart how chat volume rises and falls across the hours of the day."),
  ("That spread is the raw material of the study, and Chapter 12 will look hard at its shape.",
   "That spread is the raw material of the study, and Chapter 24 will look hard at its shape."),
  ("a dashed line at 120 characters marks where Chapter 12 will cap its axis",
   "a dashed line at 120 characters marks where Chapter 24 will cap its axis"),
  ("every figure in Chapter 12 and every test in Chapter 13, will be computed from this table",
   "every figure in Chapter 24 and every test in Chapter 25, will be computed from this table"),
  ("The next move is to look at them. Chapter 12 turns the analysis-ready table into figures: how chat volume moves across the hours of the day, how viewership splits across game categories, and how the distribution of message length compares between gaming and non-gaming channels. It is the chapter where the study's central question finally meets a picture of the answer.",
   "The next move is to put them to work. Chapter 12 is on quantitative content analysis, the design this book teaches end to end, and it is where the codebook from Chapter 8 finally meets the table you just built. Chapter 24 is where that table becomes figures: how chat volume moves across the hours of the day, how viewership splits across game categories, and how the distribution of message length compares between gaming and non-gaming channels."),
],
"chapters/_v3-draft/chapter07-research-design.qmd": [
  ('not "Twitch chat" but "chat messages posted in the 50 sampled channels between 18 and 24 November 2018."',
   'not "Twitch chat" but "chat messages posted in the 228 sampled channels between 18 and 24 November 2018."'),
],
}

for name, edits in F.items():
    p = R / name
    t = io.open(p, encoding="utf-8").read()
    orig = t
    for old, new in edits:
        if old not in t:
            if new in t:
                continue
            sys.exit("[%s] NOT FOUND: %r" % (name, old[:110]))
        t = t.replace(old, new)
    if t != orig:
        io.open(p, "w", encoding="utf-8", newline="\n").write(t)
        print("patched %s" % name.split("/")[-1])
