"""Assemble v4 Chapter 2, Three Paradigms.

Promoted out of the "Three paradigms" section of the owner's existing Chapter 5
(Theory as a Lens), which is where it has been living as four paragraphs. In v4
it becomes a chapter, because Parts IV and V need it: a reader arriving at
ethnography or critical analysis has to already know that those chapters answer
to a different standard, and a section inside the theory chapter cannot carry
that weight.

The four source paragraphs lift whole. What is added is what a section could not
hold: what a paradigm actually commits you to, how the commitment reaches all
the way down to what counts as evidence, the incommensurability argument, and
where each part of this book sits.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path("/Volumes/One Touch/20-research/aura-lab/v2v")
OUT = ROOT / "chapters/_v3-draft/chapter02-three-paradigms.qmd"
src = (ROOT / "chapters/chapter05.qmd").read_text(encoding="utf-8")

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


add('---\ntitle: "Chapter 2: Three Paradigms"\n---')

add("""Chapter 1 said that research is a disciplined way of answering a question. This chapter says that researchers disagree, deeply and in good faith, about what an answer is.

That disagreement is not a defect to be resolved before work can start. It is the reason this book has a quantitative half and a qualitative half that do not simply take turns, and it is why a reader who arrives at Chapter 18 expecting the standards of Chapter 14 will conclude that the ethnographers are being careless. They are not. They are answering to something else.

Get this chapter now and the rest of the book stops looking like a list of techniques.""")

add(para("The way researchers use theory depends on their broader philosophical commitments",
         ("Three major paradigms dominate communication research, and each treats theory differently.",
          "Three major paradigms dominate communication research. They differ over what exists to be studied, what would count as knowing it, and what the researcher's relationship to it should be, and each treats theory differently as a consequence.")))

add("""Three questions separate them, and it is worth naming the questions before the answers.

**What is there to be known?** Is there a social world that exists independently of how we describe it, or is the world partly made by the descriptions?

**What would count as knowing it?** Measurement that another researcher could repeat, or an interpretation that a reader finds convincing and well evidenced?

**What is the researcher for?** To describe the world accurately while staying out of it, or to be visibly part of what is produced, or to change the thing being studied?

Each paradigm answers all three, and the answers hang together. That is what makes them paradigms rather than preferences.""")

add("## The social scientific paradigm")
add(para("The **social scientific paradigm** assumes there is an objective reality"))

add("""What follows from those commitments runs all the way down. Concepts must be operationalized before they can be studied, because a concept that cannot be measured cannot be tested. Measures must be reliable, because an inconsistent instrument cannot approximate anything. Samples must be drawn so that they license a claim beyond themselves. The researcher's own views are a source of error to be controlled.

Chapters 7 through 15 and Part VI work inside this paradigm. Its characteristic failure is measuring something adjacent to what you care about and reporting it as though it were the thing itself, which is why Chapters 9 and 10 exist.""")

add("## The interpretive paradigm")
add(para("The **interpretive paradigm** assumes reality is socially constructed"))

add("""Its commitments run down just as far, and in the opposite direction. Categories should emerge from the material rather than being fixed in advance, because imposing them prejudges what you are trying to find. Two researchers agreeing is not the standard, since the reading depends on judgment that a second reader is not meant to reproduce mechanically. What replaces it is evidence: showing enough material that a reader can evaluate the reading, and saying where it does not hold. The researcher's position is not error to be controlled but a condition of the work, to be stated so a reader can weigh it.

Part IV works inside this paradigm. Its characteristic failure is an interpretation that arrived before the material and was never tested against it.""")

add("## The critical and cultural paradigm")
add(para("The **critical and cultural paradigm** assumes that power structures shape what counts as knowledge"))

add("""Its distinguishing commitment is the third question. Critical work holds that no research is free of a standpoint, and that work which does not examine its own is not neutral but unexamined. It therefore declines the ambition of describing without judging, and takes the ordinary and unremarkable as its object, on the grounds that assumptions do their most effective work when nobody notices them.

Part V works inside this paradigm. Its characteristic failure is a framework that predicts its own findings, so that the analysis could not have come out any other way.""")

add("## How far down it goes")

add("""It is tempting to treat a paradigm as a preference about method: quantitative people count, qualitative people read. That understates it, and the understatement causes real confusion when students read across the halves of this book.

Take one question, and watch what each paradigm turns it into.

*Are livestream communities welcoming to newcomers?*

The **social scientific** version operationalizes welcoming, perhaps as the proportion of first-time posters who receive a reply within some window, measures it across many channels, and asks what predicts variation. Its answer is a number with an interval around it, and it can say how confident you should be that the number generalizes.

The **interpretive** version asks what welcome means to the people in the room, and finds that it is not one thing: being replied to, being ignored in a way that signals you have passed as a regular, being corrected gently rather than mocked. Its answer is an account of how membership is recognized and conferred, and it cannot tell you how common any of it is.

The **critical** version asks who the room is welcoming *to*, what a newcomer has to already know to be legible as one, and whose comfort the norms protect. Its answer is an argument about whose interests the arrangement serves.

**None of those is a worse version of the others.** The first cannot tell you what welcome means, the second cannot tell you how common it is, and the third is not trying to do either. And notice that the same data, this book's corpus, could feed all three, which is exactly what Chapters 19 through 25 do to it.""")

add("## Can they be combined?")

add("""The strong position is **incommensurability**: the paradigms rest on contradictory assumptions about what exists, so combining them is incoherent rather than merely difficult. You cannot hold that message length measures an underlying reality and that the reality is constituted by how participants talk about it.

The usual working answer is **pragmatism**: what justifies a method is whether it answers the question, and a question can have parts that need different tools. Most mixed methods research adopts it, and Chapter 26 sets out what it requires.

It is worth knowing the objection has force. The failure it predicts is real and common: a study that treats interview accounts as imperfect measurements of something the survey measured better has not combined paradigms, it has subordinated one, and the qualitative half will read as quotes decorating a result. The defense is to keep each strand answerable to its own standard, and Chapter 26 is specific about how.

For now, one practical instruction. **You do not have to pick a paradigm for life.** You have to know which one a given study is working in, because that determines what the study must do to be any good, and a reader who cannot tell will apply the wrong test to half of what they read.""")

add("## Locating yourself, and the study")

add("""Three questions to ask of your own project, and of everything you read.

**What kind of answer would satisfy the question?** A rate, a meaning, or a critique. This usually settles the paradigm before any method is chosen, and Chapter 7 makes the same argument about design.

**What would count as being wrong?** In social scientific work, a hypothesis fails a test. In interpretive work, the material resists the reading and the negative cases will not fit. In critical work, the argument does not hold up against the text or the material conditions. A study with no answer to this question is not yet a study.

**Where does the researcher stand?** Outside, controlling for their own influence; inside, accounting for it; or committed, and saying so.

Read the answers in published papers, not just in method sections. A paper that reports a kappa on interpretive codes, or one that generalizes from six interviews to a population, has usually mixed up which game it is playing, and knowing that is most of what this chapter is for.""")

add("## Looking ahead")

add("""Chapter 3 is on research ethics, which every paradigm shares and which none of them relaxes. Whatever you think knowledge is, the people you study are owed the same things.

After that, Chapter 4 on reading the literature, Chapter 5 on theory, and Chapter 6 on turning all of it into a question you can actually answer.""")

add("""## References

Braun, V., & Clarke, V. (2006). Using thematic analysis in psychology. *Qualitative Research in Psychology*, *3*(2), 77-101. https://doi.org/10.1191/1478088706qp063oa

Gerbner, G., & Gross, L. (1976). Living with television: The violence profile. *Journal of Communication*, *26*(2), 172-199. https://doi.org/10.1111/j.1460-2466.1976.tb01397.x""")

OUT.write_text("\n\n".join(P) + "\n", encoding="utf-8")
(ROOT / "data-raw/v3/ch02_lift_manifest.json").write_text(
    json.dumps({"source": "chapters/chapter05.qmd", "output": str(OUT.relative_to(ROOT)),
                "lifted": MANIFEST}, indent=2), encoding="utf-8")
print("wrote %s (%d words)" % (OUT, len(OUT.read_text(encoding='utf-8').split())))
