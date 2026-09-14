import io, pathlib, sys

p = pathlib.Path("/Volumes/One Touch/20-research/aura-lab/v2v/chapters/chapter01.qmd")
t = io.open(p, encoding="utf-8").read()

old = ("Chapter 2 turns to the technical infrastructure that makes research reproducible. VSCode, "
       "R, Quarto, Git. Those tools can look intimidating from a distance. Their purpose is "
       "simple: they let you document every step of an analysis so others, including your future "
       "self, can verify and build on it. Chapter 2 also brings you face to face with the dataset "
       "for the first time. Ten rows of a real collection from a single minute in November 2018, "
       "before any cleaning, before any code. The questions you ask of those ten rows are the "
       "questions the rest of the book will help you answer at scale.")
new = ("Chapter 2 turns to a disagreement this chapter has been quietly standing on one side of. "
       "Researchers do not agree about what an answer is, and the three paradigms that divide "
       "them differ over what exists to be studied, what would count as knowing it, and what the "
       "researcher is for. It is also where the replication crisis arrives, along with the reason "
       "an analysis nobody can retrace is an analysis nobody can check.\n\n"
       "Alongside it, work through *The Open Workspace*, the first of the book's two practice "
       "supplements. It installs the tools that make retracing possible, VSCode, R, Quarto and "
       "Git, which can look intimidating from a distance and exist for one simple purpose: to "
       "document every step of an analysis so that others, including your future self, can "
       "verify it and build on it. It also brings you face to face with the dataset. Ten rows of "
       "a real collection from a single minute in November 2018, before any cleaning, before any "
       "code. The questions you ask of those ten rows are the questions the rest of the book will "
       "help you answer at scale.")

if old in t:
    io.open(p, "w", encoding="utf-8", newline="\n").write(t.replace(old, new))
    print("patched chapter01 looking-ahead")
elif "the first of the book's two practice" in t:
    print("chapter01 already current")
else:
    sys.exit("[ch01] NOT FOUND")
