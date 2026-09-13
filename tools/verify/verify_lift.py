"""Confirm the merge preserved the owner's prose exactly.

Every paragraph lifted from chapter07.qmd must appear byte-identical in the new
chapter 12, except the handful of cross-reference repairs the builder declares.
Anything else that changed is drift introduced by the merge, which is the thing
this check exists to catch.
"""
import pathlib
import re

root = pathlib.Path("/Volumes/One Touch/20-research/aura-lab/v2v")
src = (root / "chapters/chapter07.qmd").read_text(encoding="utf-8")
new = (root / "chapters/_v3-draft/chapter12-quantitative-content-analysis.qmd").read_text(encoding="utf-8")

# The declared repairs: paragraphs containing these are expected to differ.
declared = [
    "will be assembled almost entirely",
    "naming it now will make",
    "A distinction discovered now becomes a category",
    "statistical sampling in Chapter",
    "intercoder reliability protocol",
    "Assembling them into one is",
]

lifted_sections = ["Why structured observation matters", "Three modes of attention", "Field notes",
                   "Manifest and latent content", "From observation to sharper questions",
                   "Sampling your observation", "Documenting edge cases", "Knowing when to stop"]

parts = re.split(r"^## ", src, flags=re.M)
sections = {}
for chunk in parts[1:]:
    name, _, body = chunk.partition("\n")
    sections[name.strip()] = body

missing, repaired, identical = [], [], 0
for name in lifted_sections:
    for para in [p.strip() for p in sections[name].split("\n\n") if p.strip()]:
        if para in new:
            identical += 1
        elif any(d in para for d in declared):
            repaired.append((name, para[:55]))
        else:
            missing.append((name, para[:90]))

print(f"paragraphs preserved byte-identical : {identical}")
print(f"paragraphs changed by declared repair: {len(repaired)}")
for n, p in repaired:
    print(f"   [{n}] {p}...")
if missing:
    print(f"\n** UNDECLARED DRIFT, {len(missing)} paragraph(s):")
    for n, p in missing:
        print(f"   [{n}] {p}")
else:
    print("\nNo undeclared drift. Every other paragraph is exactly as he wrote it.")
