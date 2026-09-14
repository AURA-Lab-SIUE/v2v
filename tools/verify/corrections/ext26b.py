import io, pathlib, sys

p = pathlib.Path("/Volumes/One Touch/20-research/aura-lab/v2v/chapters/"
                 "_v3-draft/chapter26-mixed-methods.qmd")
t = io.open(p, encoding="utf-8").read()

oc = ("O'Cathain, A., Murphy, E., & Nicholl, J. (2008). The quality of mixed methods studies in "
      "health services research. *Journal of Health Services Research & Policy*, *13*(2), 92-98. "
      "https://doi.org/10.1258/jhsrp.2007.007074\n\n")
morse = ("Morse, J. M. (1991). Approaches to qualitative-quantitative methodological "
         "triangulation. *Nursing Research*, *40*(2), 120-123. "
         "https://doi.org/10.1097/00006199-199103000-00014\n\n")

if oc + morse in t:
    t = t.replace(oc + morse, morse + oc)
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("reference order fixed: Morse now precedes O'Cathain")
elif morse + oc in t:
    print("already in order")
else:
    sys.exit("reference pair not found")
