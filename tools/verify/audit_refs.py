"""Both directions of the citation-claim gate, for the three v3 draft chapters.

Direction 1: every entry in a References list is cited somewhere in the body.
Direction 2: every author cited in the body has an entry in the References list.
Graduate-readings blocks are further reading, not an APA reference list, so they
are excluded from direction 1 (chapter 10 on main sets that precedent).
"""
import pathlib
import re

base = pathlib.Path("/Volumes/One Touch/20-research/aura-lab/v2v/chapters/_v3-draft")
ok = True
for f in sorted(base.glob("*.qmd")):
    s = f.read_text(encoding="utf-8")
    if "## References" not in s:
        print(f"{f.name}: NO REFERENCES SECTION"); ok = False; continue
    body, reflist = s.split("## References", 1)
    # drop the graduate-extension block from the APA list
    apa = re.split(r":::\s*\{\.graduate-extension\}", reflist)[0]

    listed = set()
    for line in apa.splitlines():
        m = re.match(r"^([A-Z][A-Za-z'\-]+)(?:,| )", line.strip())
        if m and "(" in line:
            listed.add(m.group(1))

    # surnames appearing in narrative or parenthetical citations in the body
    cited = set()
    for m in re.finditer(r"\b([A-Z][a-z]{2,})\b(?=[^.]{0,40}\(\d{4}\))", body):
        cited.add(m.group(1))
    for m in re.finditer(r"\(([^)]*?\d{4}[^)]*)\)", body):
        for name in re.findall(r"\b([A-Z][a-z]{2,})\b", m.group(1)):
            cited.add(name)

    uncited = {n for n in listed if n not in body}
    missing = {n for n in cited if n not in apa and n not in
               {"Chapter", "Part", "Twitch", "Excel", "November", "Just", "Chatting"}}

    print(f"--- {f.name}")
    print(f"    listed: {len(listed)}  {sorted(listed)}")
    if uncited:
        print(f"    ** LISTED BUT NEVER CITED: {sorted(uncited)}"); ok = False
    if missing:
        print(f"    ** CITED BUT NOT LISTED: {sorted(missing)}"); ok = False
    if not uncited and not missing:
        print("    both directions clean")
print("\nAUDIT", "PASSED" if ok else "FOUND PROBLEMS")
