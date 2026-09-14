"""Assemble v4 Chapter 9, Measurement, Scales, and Items.

Absorbs the levels-of-measurement and kinds-of-variable material from the
owner's existing Chapter 8 (From vibes to variables), which keeps
operationalization and the codebook. Splitting them lets Chapter 8 stay about
the gap between a concept and a measure, and gives measurement structure a
chapter of its own before Chapters 10 and 13 need it.

Deliberately does NOT cover item wording or response formats: Chapter 13
(Survey Research) owns those, and duplicating them would leave two chapters
half-teaching the same thing. This chapter covers what a measure IS.

Cross-reference repairs: the stream_log preview was Chapter 2 and is now in the
tool supplement; the wrangling chapter was 11 and is now 24; the test chapter
was 13 and is now 25.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path("/Volumes/One Touch/20-research/aura-lab/v2v")
OUT = ROOT / "chapters/_v3-draft/chapter09-measurement-scales-items.qmd"
src = (ROOT / "chapters/chapter08.qmd").read_text(encoding="utf-8")

MANIFEST = []


def para(anchor, *subs):
    MANIFEST.append({"anchor": anchor, "repaired": bool(subs)})
    body = re.sub(r"^```.*?^```", "", src, flags=re.S | re.M)
    hits = [p.strip() for p in body.split("\n\n") if anchor in p]
    if len(hits) != 1:
        sys.exit("anchor matched %d paragraphs: %r" % (len(hits), anchor[:60]))
    p = hits[0]
    for old, new in subs:
        if old not in p:
            sys.exit("repair anchor not found in %r: %r" % (anchor[:40], old[:70]))
        p = p.replace(old, new, 1)
    return p


P = []
def add(*b):
    P.extend(b)


add('---\ntitle: "Chapter 9: Measurement, Scales, and Items"\n---')

add("""Chapter 8 closed the gap between a concept and something you can observe. This chapter is about what you are left holding once you have.

A measure has a structure. It sits at a level that governs what arithmetic is legitimate on it, it is either handed to you or built by you, and it consists of one indicator or of several combined. Those three facts decide, before any data is collected, what the study will be able to conclude. Getting them wrong is not recoverable later, which is why they come before sampling rather than after.""")

add("## Levels of measurement")

add(para("Once a variable is operationalized, it has a **level of measurement**"))
add(para("is a convenient place to see all four",
         ("Recall the preview from Chapter 2: channel, title, game, viewers, date.",
          "Its columns are channel, title, game, viewers and date.")))

add(para("A **nominal** variable sorts cases into categories that have no inherent order."))
add(para("An **ordinal** variable sorts cases into categories that do have an order"))
add(para("An **interval** variable has equal, constant distances between values",
         ("Chapter 11 will spend real effort on it", "Chapter 24 will spend real effort on it")))
add(para("A **ratio** variable has equal intervals and a true zero"))
add(para("Notice what happened with stream title."))
add(para("Levels matter because they govern the statistics available to you later.",
         ("entered into the kind of test Chapter 13 runs", "entered into the kind of test Chapter 25 runs")))

add("""One warning about the hierarchy. You can always move **down** it, binning a ratio variable into ordinal categories, and you can never move up. Message length in characters can become short, medium and long at any point; once collected as short, medium and long it can never become characters again.

So collect at the highest level the phenomenon allows, and bin later if you want to. Asking a survey respondent for their exact age rather than an age band costs nothing and preserves every option; the reverse decision is permanent and is made by people who were thinking about the table rather than the analysis.""")

add("## Where variables come from")

add(para("Some variables arrive in the dataset ready-made."))
add(para("Other variables do not exist until you build them."))

add("""There is a third case this book's corpus makes unavoidable: variables that are **derived** rather than coded. Message length is not in the file and requires no human judgment either; it is computed. Chapter 24 builds three of them.

The distinction matters for reliability. A coded variable needs two coders to agree, because a human is making a judgment. A derived variable needs its definition checked, because a machine is applying a rule perfectly and the only question is whether the rule was right. Chapter 24's supplement shows a derived variable going wrong in exactly that way: the rule was applied flawlessly to text the tool had silently retyped.""")

add("## Single items and composite measures")

add("""Some concepts are adequately captured by one observation. Age, message length, whether a message contains an at-mention: one indicator, and asking for a second would be strange.

Most interesting concepts are not like that. Parasocial attachment, perceived community, media trust, willingness to self-censor: no single question captures them, and any single question you pick will capture something narrower alongside a good deal of noise. These need a **composite measure**, several indicators combined into one score.

The reason is worth stating properly, because it is not a convention. Every indicator carries some of the concept and some error peculiar to itself. Combine several and the concept accumulates while the idiosyncratic errors partly cancel, so a composite is both a broader and a more stable measure of the construct than any of its parts. That is also why Chapter 10 can compute a reliability coefficient for a composite and cannot compute one for a single item.

Two kinds of composite are often confused, and the difference changes what you may do with the score.

**A scale** treats the indicators as *effects* of an underlying construct. Someone's level of parasocial attachment causes their answers to all the items, which is why the items should correlate with one another, and why an item that does not correlate with the others is evidence that it is not measuring the same thing. Internal consistency is meaningful here, and Chapter 10 is where it is computed.

**An index** combines indicators that are *causes* or components of the thing, and they have no reason to correlate. A measure of platform activity built from hours watched, messages sent, subscriptions held and clips created is an index: a person can be high on any one and low on the others, and the components do not need to hang together because the construct is their sum rather than their common cause.

Computing an internal-consistency coefficient for an index is a category error, and it is a common one. A low alpha on an index is not a defect to be fixed by deleting items; it is what an index looks like. Ask which kind you have built before you report a coefficient for it.""")

add("## Common response structures")

add("""Three structures cover most composite measures in communication research. Chapter 13 covers how to word the items and lay them out; what matters here is what each structure produces.

**Likert-type items** present a statement and ask for agreement on an ordered set of options. Strictly the responses are ordinal, since there is no guarantee that the distance from "disagree" to "neutral" equals the distance from "neutral" to "agree". In practice, summed or averaged across several items, they are analyzed as interval, and that is a defensible convention rather than a theorem. Where it matters, say what you did.

**Semantic differential items** anchor a scale between opposed adjectives, warm and cold, honest and dishonest, and ask the respondent to place the object between them. They work well for evaluations of a person or a thing and badly for behaviors.

**Behavioral frequency items** ask how often something was done. They are ratio-level if answered as a count, and ordinal if answered in bands, and Chapter 13 explains at length why the answers are less accurate than they look.

A practical note on number of options. Too few loses variation you cannot recover, and too many invites distinctions people cannot actually make. Five to seven points is the usual working range. And decide deliberately whether to include a midpoint: including one lets people sit in the middle, which is sometimes an honest answer and sometimes an escape from thinking.""")

add("## Borrowed measures")

add("""Most constructs you care about have been measured before, and using an established measure is usually right. It has known properties, it makes your results comparable, and the reviewers will not argue about it.

Three conditions before you do.

**Find the original.** Scales get copied from paper to paper, shedding items and changing wording. Cite and use the source, not a secondary reproduction of it.

**Check what it was validated on.** A measure developed on undergraduates in 1994 has evidence about undergraduates in 1994. It may transfer; that is an assumption, and if your population differs meaningfully the assumption belongs in the limitations.

**Do not quietly edit it.** Dropping items, rewording them for your context, or changing the response options produces a different instrument whose established properties no longer apply. Adapting is legitimate and common; reporting the adaptation, and re-establishing reliability on your own data, is the price.

Chapter 26's exploratory sequential design exists largely for the case where no borrowed measure fits: qualitative work first, to find out what the construct is and how people talk about it, then measurement built from that.""")

add("## Looking ahead")

add("""A measure with the right level, the right structure and the right provenance can still be worthless, because none of those properties says whether it is consistent or whether it captures what it claims to.

Chapter 10 is about those two questions, reliability and validity, and about the statistics that answer the first of them.""")

add("""## References

Wickham, H. (2014). Tidy data. *Journal of Statistical Software*, *59*(10), 1-23. https://doi.org/10.18637/jss.v059.i10""")

OUT.write_text("\n\n".join(P) + "\n", encoding="utf-8")
(ROOT / "data-raw/v3/ch09_lift_manifest.json").write_text(
    json.dumps({"source": "chapters/chapter08.qmd", "output": str(OUT.relative_to(ROOT)),
                "lifted": MANIFEST}, indent=2), encoding="utf-8")
print("wrote %s (%d words)" % (OUT, len(OUT.read_text(encoding='utf-8').split())))
