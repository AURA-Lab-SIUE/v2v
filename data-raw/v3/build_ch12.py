"""Assemble v3 Chapter 12, Quantitative Content Analysis.

This is a merge, not a fresh draft. The body is the owner's existing Chapter 7
(Structured listening), which contains no R at all and therefore lifts whole,
plus the codebook material from the existing Chapter 9, which does contain R and
has to be rewritten tool-agnostic. Sections are extracted from the source file
programmatically rather than retyped, so his prose arrives exactly as written.

What the reorganization actually changes, beyond the merge:

1. The opening depended on "In Chapter 2 you looked at ten rows of the stream_log".
   In the v3 TOC, Chapter 2 is Three Paradigms, so the hook is made self-contained.
2. Chapter 7 forward-promised the codebook to a later chapter. In v3 this chapter
   builds it, so every "next chapter" pointer resolves inward.
3. In v3 the reader reaches this chapter having already had operationalization (8),
   measurement (9), reliability and validity (10) and sampling (11). Sections that
   taught those in passing now point to them instead of previewing them.
4. It is the first methods chapter of Part III, so it needs the definition of the
   method itself, which the old Chapter 7 never had to give.
"""
import pathlib
import re
import sys

SRC = pathlib.Path("/Volumes/One Touch/20-research/aura-lab/v2v/chapters/chapter07.qmd")
OUT = pathlib.Path("/Volumes/One Touch/20-research/aura-lab/v2v/chapters/_v3-draft/"
                   "chapter12-quantitative-content-analysis.qmd")

src = SRC.read_text(encoding="utf-8")

# Split the source into level-2 sections, keeping everything under each heading.
parts = re.split(r"^## ", src, flags=re.M)
sections = {}
for chunk in parts[1:]:
    name, _, body = chunk.partition("\n")
    sections[name.strip()] = body.rstrip("\n")

required = ["Why structured observation matters", "Three modes of attention", "Field notes",
            "Manifest and latent content", "From observation to sharper questions",
            "Sampling your observation", "Documenting edge cases", "Knowing when to stop"]
missing = [r for r in required if r not in sections]
if missing:
    sys.exit(f"source sections missing, refusing to build: {missing}")


def fix(name, *subs):
    """Lift a section verbatim, applying only the listed cross-reference repairs.

    Returns the heading with its body, so the caller splices one complete section.
    """
    body = sections[name]
    for old, new in subs:
        if old not in body:
            sys.exit(f"[{name}] anchor not found, refusing to guess: {old[:60]}")
        body = body.replace(old, new, 1)
    return name + "\n" + body


front = """---
title: "Chapter 12: Quantitative Content Analysis"
---

Here are three rows from the stream records, one minute apart, for a single large channel on a November evening: 27,934 concurrent viewers, then 28,076, then 28,203. Two hundred sixty-nine viewers in a hundred and twenty-two seconds. The data records that climb to the second. What the data cannot tell you is what the climb was.

It could have been a raid, another streamer ending a broadcast and sending their audience over. It could have been a clip going viral on Reddit, pulling in strangers. It could have been the streamer returning from a break, or a game update, or simply the slow accumulation of a good night. The row looks the same in every case: a number, then a larger number, then a larger number still.

The only way to know what a climb like that means is to have watched enough live Twitch to recognize the shapes these numbers make. Someone who has spent real time on the platform can look at a viewer curve and read it. A raid has a signature, a near-vertical jump, often with a wave of near-identical greetings in chat. A viral clip has a different signature, a slower swell of viewers who do not know the room's conventions. The data will not label these for you. You bring the labels, and you can only bring them if you have done the looking.

This chapter is the first of the book's method chapters, and it is the one the rest of the book leans on hardest. It covers quantitative content analysis from end to end: what the method is, how you come to understand a medium well enough to measure it, how a codebook gets built and tested, and what it takes to turn a pile of messages into numbers that mean something.
"""

what_it_is = """
## What content analysis is

**Content analysis** is the systematic, quantitative study of communication content. You take a body of material, messages, articles, images, transcripts, broadcasts, and you apply an explicit set of rules that turn it into data other people could reproduce.

Berelson (1952) gave the definition that shaped the field, describing content analysis as a research technique for the objective, systematic, and quantitative description of the manifest content of communication. Krippendorff (2018) states the purpose more usefully for our era: content analysis is a technique for making replicable and valid inferences from texts to the contexts of their use. Riffe, Lacy, Watson, and Fico (2019) is the standard modern treatment in mass communication, and Neuendorf (2017) is the standard practical guide.

Three words in those definitions carry most of the weight.

**Systematic** means the rules are fixed before you apply them, and applied the same way to every case. You do not decide what counts as hostile while you are reading the hostile messages. The rule exists first, and then the material meets it.

**Quantitative** means the output is counts and measurements that can be compared, tested and reported. This is what separates the method from a close reading, which may be more insightful about any single message and cannot tell you how often something occurs across ten thousand of them.

**Replicable** means another competent researcher, handed your codebook and your material, would produce substantially the same numbers. That is a strong claim and it is the one the method lives or dies by, which is why Chapter 10's reliability testing is not a formality bolted on at the end but the thing that makes the results admissible at all.

The method has a shape that does not vary much, whatever the material:

1. Define the population of content, and draw a sample from it, which is Chapter 11's subject.
2. Define the **unit of analysis**, the thing that becomes one row: a message, an article, a shot, a speaking turn.
3. Build a **codebook** that defines every variable, its possible values, and the rules for deciding hard cases.
4. Test the codebook by having two people apply it independently to the same units, and measure their agreement, which is Chapter 10's subject.
5. Revise, then code the full sample.
6. Analyze the resulting numbers.

This chapter covers steps 2 through 5, the parts specific to the method. Steps 1 and 6 are chapters of their own because they are not specific to content analysis at all.

What the numbered list conceals is that step 3 is impossible to do well without something that appears nowhere in it. Before you can write a rule that separates hostile messages from sarcastic ones, you have to know the room well enough to tell the difference yourself. That knowledge is not in the dataset. It comes from watching, and that is where the chapter starts.
"""

codebook = """
## The codebook

Everything so far has been preparation. The codebook is where it becomes an instrument.

In Chapter 8 you drafted a codebook on paper: a unit of analysis, operationalized variables, a set of decision rules. That draft was an argument about how a study would measure things. Now it becomes a real document, the project's **rulebook**, the reference every later step answers to.

A working codebook has five parts, and a codebook missing any of them will fail during coding rather than before it.

**The unit of analysis**, stated exactly. Not "chat" but "one chat message, as delivered, including messages consisting only of emotes." The unit decides what one row is, and Chapter 7 explains why getting it wrong is expensive.

**The variables**, each with a definition written so that someone who has not had your conversations can apply it. "Message target" is not a definition. "Message target: whether the message is addressed to the streamer, to another viewer, or to the room in general" is closer, and it is still not enough on its own.

**The values** each variable can take, exhaustive and mutually exclusive. Every unit must fit exactly one value. This is where the "unclassifiable" or "other" category earns its place: not as a dumping ground, but as the honest destination for units that genuinely do not fit, whose size you will report.

**The decision rules**, which are the part beginners leave out and experienced coders write first. A rule resolves a case the definition alone cannot. If a message contains an at-mention of the streamer and also a reply to another viewer, which is it? The rule does not have to be the only defensible answer. It has to be stated in advance and applied consistently.

**Worked examples**, ideally the real ones from your edge-case log, each showing a unit and the value it receives and why. Examples do more work than definitions do. A second coder learns your categories from your examples faster than from your prose, and the examples are what you will use to train them.

Give the document a version number and a date. This matters more than it sounds. A codebook changes during piloting, and a study where coding was done under three different versions of the rules, with no record of which coder used which, has a problem it cannot fix afterward. Version the file, note what changed and when, and keep the old versions.

Calling this "finalizing" the codebook is slightly optimistic, and it is worth being honest about that. Piloting the codebook, two coders applying it to the same messages, routinely sends you back to edit a category or sharpen a rule. What this step finalizes is not the content of the rulebook but its status: it stops being a sketch in your notes and becomes the official instrument of the project, versioned and ready to be tested. A draft you can revise is exactly what you want walking into a pilot.
"""

against_data = """
## Reading the data against the codebook

Before any coding starts, the codebook and the data should be laid side by side and asked a blunt question: does this material actually support the study the codebook describes?

Walk the variables one at a time and find the thing each one is read from. If message target is coded from the message text plus the sender, then the data needs a message field and a sender field. If message length is the count of characters in the message, the message field covers it. If a variable turns out to depend on something the data does not contain, and studies designed away from the data routinely do, you would rather discover it now than halfway through coding.

The same pass surfaces what the codebook will have to work harder at. Look at the first twenty messages in the corpus and the edge cases from your observation log are all there: a message of twenty-three question marks, with no obvious target, which is what the "unclassifiable" category exists to catch. A line of repeated "TriEasy Clap", which is copypasta and needs the rule you wrote for it. Short tokens that are emote-only messages. The codebook did not anticipate these in the abstract. It anticipated them because observation had you watch for them, and here they are, in the first screen of data.

One genuine wrinkle in this corpus is worth carrying forward as an example of the kind of thing this step is for. Among the early messages is one addressed to a streamer that begins "@xQcOW". The channel field for that same row reads "xqcow". The at-mention and the channel name are the same name in different casing: the display name as a viewer typed it, against the lowercase login name the data stores. A message-target rule that keys on "an at-mention of the streamer's channel name" will silently fail on every message like it unless the rule says what to do about case.

That is a small thing that would have cost a real study a real variable. It is exactly the kind of refinement that belongs in the codebook now, while the rulebook is still living and before a single message has been coded.
"""

coding_begins = """
## Piloting, and then coding

The codebook now goes on trial, and Chapter 10 is where the machinery for that trial was built.

Two coders take the codebook and apply it independently to the same set of units, drawn separately from the material that will be analyzed later. Then you measure how often they agreed, using a statistic that corrects for the agreement you would expect from chance alone, because raw percentage agreement flatters every codebook ever written. If agreement is adequate, coding proceeds. If it is not, you find the categories where the disagreement concentrated, repair the definitions or the decision rules that let it happen, and pilot again.

Two points about that loop are worth stating plainly, because both are routinely misunderstood.

Revising a codebook after a failed pilot is not cheating, and it is not a result you have to disclose apologetically. It is the method working. What would be cheating is revising the codebook partway through coding the real sample, without re-testing, and reporting a reliability figure obtained under rules that no longer apply.

And reliability is not validity. Two coders can agree almost perfectly while measuring something other than what you claim to be measuring, which is a possibility Chapter 10 takes seriously. High agreement means your rules are clear. It does not certify that your variable deserves its name.

Once the codebook clears its pilot, coding the full sample is the least intellectually demanding part of the entire study, and usually the longest. The thinking has already happened. What remains is applying the rules consistently and resisting the urge to improve them along the way.
"""

body = [
    front,
    what_it_is,
    "\n## " + fix(
        "Why structured observation matters",
    ),
    "\n## " + fix(
        "Three modes of attention",
    ),
    "\n## " + fix(
        "Field notes",
        ("because the codebook you build in the next chapter will be assembled almost entirely "
         "from what they contain.",
         "because the codebook you build later in this chapter will be assembled almost entirely "
         "from what they contain."),
    ),
    "\n## " + fix(
        "Manifest and latent content",
        ("Structured listening trains a particular kind of judgment, and naming it now will make "
         "the next chapter easier.",
         "Structured listening trains a particular kind of judgment, and naming it now will make "
         "the codebook easier to write."),
    ),
    "\n## " + fix(
        "From observation to sharper questions",
        ("A distinction discovered now becomes a category in the codebook you build next chapter.",
         "A distinction discovered now becomes a category in the codebook you build later in this "
         "chapter."),
    ),
    "\n## " + fix(
        "Sampling your observation",
        # Sampling is Chapter 11 in v3, and the reader has already had it.
        ("and it is the same principle that will govern statistical sampling in Chapter 10.",
         "and it is the same principle that governed statistical sampling in Chapter 11."),
    ),
    "\n## " + fix(
        "Documenting edge cases",
        # Reliability is Chapter 10 in v3.
        ("The formal intercoder reliability protocol (Chapter 8) requires",
         "The formal intercoder reliability protocol of Chapter 10 requires"),
    ),
    "\n## " + fix(
        "Knowing when to stop",
        ("Assembling them into one is the next chapter's work.",
         "Assembling them into one is the rest of this chapter's work."),
    ),
    codebook,
    against_data,
    coding_begins,
    """
## Looking ahead

Content analysis answers questions about what was said. It cannot ask anyone why they said it, or what they believed while saying it, because the people who produced the content are not available to be asked. Chapter 13 turns to the method that does ask them directly, with all the new problems that introduces: surveys, where the measurement instrument is a set of questions and the hard part is that people answer the question you actually asked rather than the one you meant.

## References

Berelson, B. (1952). *Content analysis in communication research*. Free Press.

Geertz, C. (1973). *The interpretation of cultures: Selected essays*. Basic Books.

Katz, E., Blumler, J. G., & Gurevitch, M. (1973). Uses and gratifications research. *Public Opinion Quarterly*, *37*(4), 509-523. https://doi.org/10.1086/268109

Krippendorff, K. (2018). *Content analysis: An introduction to its methodology* (4th ed.). SAGE Publications.

Neuendorf, K. A. (2017). *The content analysis guidebook* (2nd ed.). SAGE Publications.

Riffe, D., Lacy, S., Watson, B. R., & Fico, F. (2019). *Analyzing media messages: Using quantitative content analysis in research* (4th ed.). Routledge.

::: {.graduate-extension}
### Graduate readings

Hayes, A. F., & Krippendorff, K. (2007). Answering the call for a standard reliability measure for coding data. *Communication Methods and Measures*, *1*(1), 77-89. https://doi.org/10.1080/19312450709336664
:::
""",
]

OUT.write_text("\n".join(b.rstrip("\n") + "\n" for b in body), encoding="utf-8")
words = len(OUT.read_text(encoding="utf-8").split())
print(f"wrote {OUT.name}, {words} words")
