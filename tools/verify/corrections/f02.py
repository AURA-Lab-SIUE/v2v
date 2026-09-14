import io, pathlib, sys

p = pathlib.Path("/Volumes/One Touch/20-research/aura-lab/v2v/chapters/"
                 "_v3-draft/chapter02-three-paradigms.qmd")
t = io.open(p, encoding="utf-8").read()

NEW = '''## When the answers did not hold up

A paradigm is judged partly by how it handles its own failures, and the social scientific one has had a public reckoning worth knowing about before you work inside it.

In 2015 the Open Science Collaboration, a group of 270 researchers from around the world, set out to redo 100 published psychology studies. They followed the original methods as closely as the published papers described, recruited similar participants, and ran the same analyses. Only **36 percent** of the original results replicated at conventional thresholds of statistical significance, and among those that did, the effect sizes were on average about half the magnitude originally reported (Open Science Collaboration, 2015).

The number was striking. The cause was more so. The Collaboration was not finding fraud. It was finding ordinary friction. Published methods sections did not contain enough detail to re-run the original analysis. Researchers had to email the original authors for clarifications. Some authors had moved. Some had lost the data. Some had run their analysis in software whose menus had since changed. The replications were not blocked by malice but by the simple fact that the original research had never been built to be retraceable.

That episode acquired a name, the **replication crisis**, and it was less a sudden emergency than the slow recognition that published findings were not as durable as the field had assumed. The mechanisms were not exotic. Researchers had run many analyses and reported the ones that worked. Studies finding something had been likelier to get published than studies finding nothing, which inflated the visible base rate of real effects. Predictions had been adjusted after looking at the data, which is legitimate in some traditions and, done silently, manufactures significance out of noise.

The term for the underlying condition is **researcher degrees of freedom**: every analytical decision open to a researcher, which observations to keep, which controls to include, which test to run, is a chance to nudge a result toward publishable. The decisions are not wrong individually. Any one of them might be the right call. The problem is that a reader who cannot see them cannot tell a defensible choice from a convenient one, and neither, after six months, can you. Documented, they can be weighed. Undocumented, they vanish into the methods section as though they were never made. Chapter 3 takes this up as an ethical matter and Chapter 6 as a design one, where preregistration closes the degrees of freedom by making the plan inspectable before the data exists.

Notice that this is a failure the paradigm can name in its own terms, which is what distinguishes it from a paradigm that cannot be wrong. The interpretive and critical paradigms have their own versions, named at the end of each section above, and none of the three is exempt.

**The practical part of the answer is a habit rather than a doctrine.** Most legacy statistical software, SPSS and Excel and JMP among them, does its work through menus. You click Analyze, then Compare Means, then One-Way ANOVA. The result appears and the click history vanishes. To redo the analysis next month you must remember which menus you opened, in what order, with what options selected; to let a collaborator verify it you must describe every click in prose. Almost nobody does this well and almost nobody wants to.

Code does not have the problem. A script is a description of every step, written in a language the computer can re-run, and **the code is the methods section**. Chapter 1's Reinhart-Rogoff error was caught because the spreadsheet, eventually shared, had the broken formula on the page; written as code from the start, it would have been on the page from the start.

That is the whole of the argument. The supplement *The Open Workspace* is the other half: which tools produce that plain-text record, how to install them, and what this book's dataset looks like the first time you open it. It sits outside the chapters because installers and menus date faster than anything else here, and the reasoning above does not date at all.

'''

anchor = "## The interpretive paradigm"
if "## When the answers did not hold up" in t:
    print("chapter02 already current")
else:
    i = t.index(anchor)
    t = t[:i] + NEW + t[i:]
    # add the reference, keeping the list alphabetical
    ref_anchor = ("Gerbner, G., & Gross, L. (1976). Living with television: The violence "
                  "profile. *Journal of Communication*, *26*(2), 172-199. "
                  "https://doi.org/10.1111/j.1460-2466.1976.tb01397.x")
    if ref_anchor not in t:
        sys.exit("[ch02] reference anchor not found")
    t = t.replace(ref_anchor, ref_anchor + "\n\nOpen Science Collaboration. (2015). Estimating "
                  "the reproducibility of psychological science. *Science*, *349*(6251), "
                  "aac4716. https://doi.org/10.1126/science.aac4716")
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("patched chapter02")
