import io, pathlib, sys

p = pathlib.Path("/Volumes/One Touch/20-research/aura-lab/v2v/chapters/"
                 "_v3-draft/chapter22-rhetorical-criticism.qmd")
t = io.open(p, encoding="utf-8").read()

bitzer = ("Bitzer, L. F. (1968). The rhetorical situation. *Philosophy & Rhetoric*, *1*(1), "
          "1-14.\n\n")
aristotle = ("Aristotle. (2007). *On rhetoric: A theory of civic discourse* (G. A. Kennedy, "
             "Trans.; 2nd ed.). Oxford University Press.\n\n")

if bitzer + aristotle in t:
    t = t.replace(bitzer + aristotle, aristotle + bitzer)
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("ch22 reference order fixed: Aristotle now precedes Bitzer")
elif aristotle + bitzer in t:
    print("already in order")
else:
    sys.exit("reference pair not found")
