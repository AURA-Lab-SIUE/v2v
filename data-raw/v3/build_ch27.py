"""Assemble v4 Chapter 27, Writing and Publishing Research.

The body is the owner's existing Chapter 14 (The one-click report). That chapter
was 25 percent R-shaped prose, because it taught Quarto: the mechanics drop to
the tool supplement and what stays is IMRaD, the reflection and the closing,
which are tool-agnostic already. Paragraphs are lifted by anchor; the manifest
lets verify_lift_manifest.py prove they arrived byte-identical.

What the consolidation changes:

1. Cross-references: the codebook moved from Chapter 8 to 12, sampling to 11,
   reliability to 10, the figures from Chapter 12 to 24, the test from 13 to 25.
2. The old chapter opened by declaring the study "done" because it was the last
   chapter of a 14-chapter book. It is still the last chapter, but Parts IV to VI
   now sit between, so the recap names what actually accumulated.
3. Sections on authorship, preregistration, peer review and open materials are
   added. The 3rd edition ended at publishing a site, which is where a course
   portfolio ends and not where research does.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path("/Volumes/One Touch/20-research/aura-lab/v2v")
OUT = ROOT / "chapters/_v3-draft/chapter27-writing-and-publishing.qmd"
src = (ROOT / "chapters/chapter14.qmd").read_text(encoding="utf-8")

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


add('---\ntitle: "Chapter 27: Writing and Publishing Research"\n---')

add("""A study that nobody can read is not research yet. It is work that was done.

This chapter is about the form the work takes when it leaves your hands: the report, the materials that travel with it, the names on it, and the process it goes through before anyone else believes it.""")

add(para("This last chapter gives the work a form.",
         ("It assembles every piece into one report, makes that report reproducible, gathers it with the study's other documents into a single site, and publishes that site where anyone can find it.",
          "It assembles every piece into one report, makes that report reproducible, and gathers it with the study's other documents into something another researcher can check.")))

add("## The shape of a report: IMRaD")

add(para("A document that rebuilds itself still needs a structure"))
add(para("The **Introduction** states the question and why it is worth asking."))

add(para("The **Methods** section says exactly what was done",
         ("This is the home of the codebook from Chapter 8, the sampling procedure and the inter-coder reliability check from Chapter 10",
          "This is the home of the codebook from Chapter 12, the sampling procedure from Chapter 11 and the inter-coder reliability check from Chapter 10")))

add(para("The **Results** section reports what was found",
         ("The three figures from Chapter 12 and the t-test from Chapter 13 belong here.",
          "The three figures from Chapter 24 and the t-test from Chapter 25 belong here.")))

add(para("The **Discussion** says what the results mean.",
         ("This is where the interpretation from Chapter 13 belongs",
          "This is where the interpretation from Chapter 25 belongs")))

add("""Two things belong in the Discussion that student papers routinely omit.

**Limitations, stated as specifics.** "This study has limitations" is not a limitation. This study's are nameable: the messages are not independent observations, so the reported precision is optimistic by roughly a factor of ten; one channel's chat is 46 percent bot commands, which the message-level measures could not distinguish from talk; the corpus dates from 2018 and its vocabulary has moved on. A reader trusts a paper that finds its own problems more than one that does not appear to have looked.

**What would come next.** Not a gesture at "future research" but the actual next study: what you would collect, and what it would settle.""")

add("## A report is not only for a qualitative or quantitative study")

add("""IMRaD fits an experiment perfectly and fits an ethnography badly, and forcing the second into the first is a common way to make good qualitative work read as thin.

Qualitative reports keep the same obligations and rearrange them. Methods becomes a fuller account of setting, access, participants, and the researcher's own position, because those determine what could be seen. Results and Discussion are frequently interleaved rather than separated, since an extract and its interpretation belong together and splitting them makes both unreadable. Sections are often named for themes rather than numbered.

What does not change is the traceability. Whatever the shape, a reader must be able to see how you got from material to claim. Chapter 21's list of what to report is the qualitative equivalent of the Methods section, and it is not shorter.

Mixed methods reports need a decision about sequence: both strands in full and then the integration, or organized by finding with both strands inside each. Chapter 26's joint display goes wherever the integration is, and the paper should be legible to a reader who is expert in only one of the two halves.""")

add("## Authorship")

add("""Authorship is a professional and ethical matter, not a courtesy, and the norms are specific.

An author is someone who made a substantial intellectual contribution to the work and can take public responsibility for it. Collecting the data is not automatically authorship; neither is funding the project, chairing the department, or supervising in general terms. Conversely, a student who designed and ran a study is an author of it, and commonly the first one.

**Order carries meaning and the meaning varies by field.** In much of communication, first author is the principal contributor and last is the senior or supervising author, with the middle ordered by contribution. Some fields alphabetize. Some journals now publish a contributor statement naming who did what, which is the clearest solution and worth proposing.

**Agree the order in writing, early, and revisit it when the work changes.** Disputes are common, they are unpleasant, and nearly all of them come from a conversation nobody had at the start. If you are a student working with a supervisor, ask the question directly; it is a normal question and being uncomfortable asking it is not a reason to leave it open.""")

add("## Preregistration and open materials")

add("""Chapter 25 warned against deciding the analysis after seeing the data. **Preregistration** is the structural fix: you deposit the hypotheses, the design and the analysis plan in a timestamped public record before collecting, so that the distinction between what you predicted and what you noticed is preserved.""")

add(para("> \"Preregistration distinguishes analyses and outcomes"))

add("""It is not a cage. You may depart from the plan; you report that you did and why, and the reader can weigh it. And the exploratory half of a study remains entirely legitimate, labeled as exploratory.

Alongside it, **open materials**: the data where ethics and licences allow, the analysis code, the codebook, the instrument. Chapter 3's obligations govern what can be shared. Human-subjects data usually cannot be posted as collected; a de-identified version, or a synthetic one, plus the full instrument and code, is normally both possible and sufficient for a reader to check the analysis.

The standard to aim at is that someone else, given your materials, would arrive at your numbers. That is a higher bar than most published work in communication currently meets, and it is the direction the field is moving.""")

add("## Getting it published")

add("""**Choose the venue before you write.** Journals differ in length, in what they consider a contribution, and in whether they publish qualitative work at all. Reading the aims and scope, plus three recent articles, tells you more about fit than any ranking does.

**The review process.** An editor screens for fit and may desk-reject, which is fast and not a judgment on quality. Surviving that, the paper goes to two or three peer reviewers, and the usual outcome is revise and resubmit, often with a response that reads as brutal. A rejection with substantive reviews is more valuable than a desk rejection, because it comes with a free and detailed critique.

**Responding to reviewers.** Answer every point, in a numbered letter, saying what you changed and where. Where you disagree, say so with a reason rather than complying against your judgment; reviewers are frequently wrong and are usually reasonable when answered directly. The tone to aim for is a colleague's, not a defendant's.

**Conferences first.** For most student work the sensible route is a conference paper, which gets the work read and criticized quickly, and then a journal version. Communication's associations run division-based review with published deadlines, and a divisional paper is a realistic target for good coursework.

**Predatory venues.** A journal that solicits you by flattering email, promises review in days, charges a fee to publish, and is not in the databases your library indexes is not a journal. Publishing there costs money and does damage that is hard to undo. When unsure, ask a librarian, who will know in about a minute.""")

add("## The reflection")

add(para("One short piece remains, and the portfolio is not complete without it"))
add(para("A good reflection is specific."))

add("## Looking ahead")

add(para("This is the last chapter, and looking ahead now means looking past the book."))

add(para("The chat study is finished.",
         ("The whole of it became a reproducible site with a public address, a study another person can read, check, and extend.",
          "The whole of it became something another person can read, check, and extend.")))

add(para("That sequence is what the book's title has been describing all along."))

add("""## References

Knuth, D. E. (1984). Literate programming. *The Computer Journal*, *27*(2), 97-111. https://doi.org/10.1093/comjnl/27.2.97

Nosek, B. A., Ebersole, C. R., DeHaven, A. C., & Mellor, D. T. (2018). The preregistration revolution. *Proceedings of the National Academy of Sciences*, *115*(11), 2600-2606. https://doi.org/10.1073/pnas.1708274114""")

OUT.write_text("\n\n".join(P) + "\n", encoding="utf-8")
(ROOT / "data-raw/v3/ch27_lift_manifest.json").write_text(
    json.dumps({"source": "chapters/chapter14.qmd",
                "output": "chapters/_v3-draft/chapter27-writing-and-publishing.qmd",
                "lifted": MANIFEST}, indent=2), encoding="utf-8")
print("wrote %s (%d words)" % (OUT, len(OUT.read_text(encoding='utf-8').split())))
