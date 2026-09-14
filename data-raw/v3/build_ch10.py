"""Assemble v4 Chapter 10, Reliability and Validity.

Promoted out of two places: the "Reliability and validity" section of the
owner's existing Chapter 8, which introduced the concepts and deferred the
statistics, and the pilot-test and agreement material from his existing
Chapter 10 (The sample), which supplied them. In v3 the concept and its
measurement were four chapters apart. Here they are one chapter.

Existing Chapter 10 keeps the sampling material and becomes v4 Chapter 11.

Cross-reference repairs: the codebook was finalized in old Chapter 9 and is now
built in Chapter 12; the statistics were promised to old Chapter 10 and are now
in this chapter; the wrangling chapter was 11 and is now 24.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path("/Volumes/One Touch/20-research/aura-lab/v2v")
OUT = ROOT / "chapters/_v3-draft/chapter10-reliability-and-validity.qmd"
SRC = {
    "ch08": (ROOT / "chapters/chapter08.qmd").read_text(encoding="utf-8"),
    "ch10": (ROOT / "chapters/chapter10.qmd").read_text(encoding="utf-8"),
}

MANIFEST = []


def para(where, anchor, *subs):
    MANIFEST.append({"anchor": anchor, "repaired": bool(subs), "source": where})
    body = re.sub(r"^```.*?^```", "", SRC[where], flags=re.S | re.M)
    hits = [p.strip() for p in body.split("\n\n") if anchor in p]
    if len(hits) != 1:
        sys.exit("[%s] anchor matched %d paragraphs: %r" % (where, len(hits), anchor[:60]))
    p = hits[0]
    for old, new in subs:
        if old not in p:
            sys.exit("[%s] repair anchor not found in %r: %r" % (where, anchor[:40], old[:70]))
        p = p.replace(old, new, 1)
    return p


P = []
def add(*b):
    P.extend(b)


add('---\ntitle: "Chapter 10: Reliability and Validity"\n---')

add(para("ch08", "An operational definition can be perfectly precise and still be bad measurement."))

add("""These are the two questions every measure has to answer, and a study that cannot answer them has not established that it measured anything. They are worth a chapter rather than a section, because the concepts are easy and the practice is not.""")

add("## Reliability")

add(para("ch08", "**Reliability** is consistency.",
         ("Chapter 10 covers those statistics and how to act on them; for now, the point is conceptual.",
          "The rest of this chapter covers those statistics and how to act on them.")))

add("""Inter-coder agreement is one of three forms, and which one applies depends on what your measure is.

**Inter-coder or inter-rater reliability** applies when humans classify material: content analysis, observational coding, any variable that exists because a person read something and made a judgment. It is the form the rest of this chapter works through.

**Internal consistency** applies when several items are combined into a scale, in Chapter 9's sense of indicators caused by a common construct. It asks whether the items behave as though they are measuring one thing, and it is reported as **Cronbach's alpha** or, increasingly, McDonald's omega. Conventionally alpha above about .70 is considered adequate and above .80 good, with the same caution that attaches to every threshold in this book.

Two things about alpha are routinely misunderstood. It rises as you add items, so a long scale of mediocre items can post a high alpha, and a very high alpha, above about .95, usually means the items are near-paraphrases rather than that the measure is excellent. And, as Chapter 9 says, it does not apply to an index at all, because the components of an index have no reason to correlate.

**Test-retest reliability** applies when a measure should be stable over time: administer it twice to the same people and correlate the results. It is only interpretable when the underlying thing genuinely is stable, which makes it right for a personality trait and wrong for a mood.""")

add("## Validity")

add(para("ch08", "**Validity** is accuracy."))

add("""A fourth form completes the set. **Criterion validity** asks whether the measure predicts or matches an external standard: concurrently, against something measured at the same time, or predictively, against a future outcome. It is the strongest evidence when a criterion exists, and for most communication constructs one does not, which is why construct validity carries the weight.

Two threats are worth naming because they are specific and common.

**Social desirability** is the tendency to answer as one ought rather than as one does, and it attacks validity without touching reliability: people are consistently flattering about themselves. Chapter 13 returns to this with the gap between reported and actual behavior.

**Construct underrepresentation** is measuring a narrow slice and naming it after the whole thing. A measure of community built entirely from posting frequency captures one aspect and calls it the concept, so the study's conclusions will be about posting while its abstract is about belonging.""")

add(para("ch08", "One principle ties the two together"))

add("## The pilot test")

add(para("ch10", "A pilot test is a trial run of the codebook before the real coding begins."))
add(para("ch10", "That word, independently, carries the whole logic."))

add("## Why raw agreement is not enough")

add(para("ch10", "The obvious way to turn the pilot into a number is to count how often the two coders matched."))
add(para("ch10", "It is also misleading, and seeing why is the key idea of the chapter."))
add(para("ch10", "Cohen's 1960 paper that introduced the standard fix made the point with a sharp example."))
add(para("ch10", "Raw agreement cannot tell that empty agreement apart from the real kind."))
add(para("ch10", "What you need is a measure that starts from the agreement actually observed"))

add("## Cohen's kappa and Krippendorff's alpha")

add(para("ch10", "**Cohen's kappa** is the first, introduced in the 1960 paper just mentioned"))
add(para("ch10", "When the coders do no better than chance, the numerator is zero"))

add("""**Krippendorff's alpha** is the second and the more general instrument (Krippendorff, 2018). Where kappa assumes exactly two coders and nominal categories, alpha accommodates any number of coders, handles ordinal, interval and ratio data, and tolerates missing values. For anything beyond the simplest two-coder nominal case it is the safer choice, and it is increasingly expected in content analysis.

Note that this alpha and Chapter 9's Cronbach's alpha share a name and nothing else. One measures agreement among coders; the other measures consistency among items. Reporting the wrong one is a small error that tells a reviewer a lot.""")

add(para("ch10", "Either way the result is a number between roughly zero and one"))

add("""One caution on thresholds. Landis and Koch's labels were proposed for a different literature and have hardened into a rule they were never meant to be. The working expectation in published content analysis is at least .70, with .80 preferred, and the harder point is that an acceptable coefficient on a trivial variable proves very little. Reporting agreement per variable rather than one figure for the whole codebook is the honest practice, because the variable that matters is usually the one that agrees worst.""")

add("## A worked reliability check")

add(para("ch10", "To see what a failed check looks like, and why codebooks fail it"))
add(para("ch10", "Imagine the codebook included a loosely worded variable."))
add(para("ch10", "The two coders agreed on 80 of the 100 messages"))
add(para("ch10", "By the Landis and Koch labels, 0.015 is slight agreement"))

add("## When reliability fails")

add(para("ch10", "A kappa of 0.015 is not a result to report."))
add(para("ch10", "The fix begins with diagnosis."))
add(para("ch10", "Then the codebook, now revised, is piloted again."))
add(para("ch10", "This is why Chapter 9 finalized only the codebook's status",
        ("This is why Chapter 9 finalized only the codebook's status and not its content.",
         "This is why Chapter 12 finalizes only the codebook's status and not its content.")))

add("""One rule governs the whole cycle, and breaking it is the most common integrity failure in content analysis. **The coefficient you report must come from a fresh sample coded after the last revision.** Revising the codebook to fix the disagreements and then recomputing agreement on the same messages measures how well you patched those messages, not whether the instrument works. Chapter 8's protocol separates the training set from the reliability sample for exactly this reason.

And report the whole procedure: how many units, drawn how, coded by whom, which statistic, per variable, and how many revision rounds it took. A kappa with no procedure behind it is a number a reader has no way to evaluate.""")

add("## Reliability in qualitative work")

add("""Everything above belongs to the social scientific paradigm from Chapter 2, and it does not transfer to Part IV. That is not a lowering of standards but a different kind of claim: where an interpretive reading depends on judgment a second coder is not meant to reproduce mechanically, agreement measures the wrong thing.

Chapter 21 sets out what replaces it, Lincoln and Guba's credibility, transferability, dependability and confirmability, and Chapter 19 makes the specific point that a qualitative content analysis reporting a kappa has usually misunderstood what it was doing.

The dividing line is not the material but the claim. Coding this book's corpus for whether a message contains an at-mention is a manifest judgment that two people should agree on, and a kappa is exactly right. Coding the same messages for whether they are welcoming is not.""")

add("## Looking ahead")

add("""You have a measure, and evidence that it is consistent and that it captures what it claims to. What you do not have is anything to apply it to.

Chapter 11 is about sampling: which cases to study, how to choose them, and what the choice licenses you to say about everyone you did not study.""")

add("""## References

Cohen, J. (1960). A coefficient of agreement for nominal scales. *Educational and Psychological Measurement*, *20*(1), 37-46. https://doi.org/10.1177/001316446002000104

Hayes, A. F., & Krippendorff, K. (2007). Answering the call for a standard reliability measure for coding data. *Communication Methods and Measures*, *1*(1), 77-89. https://doi.org/10.1080/19312450709336664

Krippendorff, K. (2018). *Content analysis: An introduction to its methodology* (4th ed.). SAGE Publications.

Landis, J. R., & Koch, G. G. (1977). The measurement of observer agreement for categorical data. *Biometrics*, *33*(1), 159-174. https://doi.org/10.2307/2529310

Lombard, M., Snyder-Duch, J., & Bracken, C. C. (2002). Content analysis in mass communication: Assessment and reporting of intercoder reliability. *Human Communication Research*, *28*(4), 587-604. https://doi.org/10.1111/j.1468-2958.2002.tb00826.x""")

OUT.write_text("\n\n".join(P) + "\n", encoding="utf-8")
(ROOT / "data-raw/v3/ch10_lift_manifest.json").write_text(
    json.dumps({"sources": {"ch08": "chapters/chapter08.qmd", "ch10": "chapters/chapter10.qmd"},
                "output": str(OUT.relative_to(ROOT)), "lifted": MANIFEST}, indent=2), encoding="utf-8")
print("wrote %s (%d words)" % (OUT, len(OUT.read_text(encoding='utf-8').split())))
