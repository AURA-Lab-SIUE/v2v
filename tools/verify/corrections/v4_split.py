"""Move the seven carried-over chapters into the v4 draft directory.

They were edited in place for the 4th edition: a six-part roadmap, references to
the two practice supplements, forward pointers to chapters 24 and 25. All of
that is wrong for the 3rd edition, which still renders from chapters/*.qmd on
main, so leaving the edits there means a merge silently breaks the published
book.

After this, every v4 chapter lives in chapters/_v3-draft/ and every 3rd edition
chapter lives in chapters/, and the two editions cannot corrupt each other.

Relative paths move one level deeper, so ../images/ and ../audio/ become
../../images/ and ../../audio/.
"""
import io
import pathlib
import subprocess
import sys

R = pathlib.Path("/Volumes/One Touch/20-research/aura-lab/v2v")

MOVES = {
    "chapter01.qmd": "chapter01-the-science-of-storytelling.qmd",
    "chapter03.qmd": "chapter03-knowing-and-knowing-well.qmd",
    "chapter04.qmd": "chapter04-intelligence-gathering.qmd",
    "chapter05.qmd": "chapter05-theory-as-a-lens.qmd",
    "chapter06.qmd": "chapter06-the-prospectus.qmd",
    "chapter08.qmd": "chapter08-from-vibes-to-variables.qmd",
    "chapter11.qmd": "chapter11-wrangling-the-data.qmd",
}

for src_name, dst_name in MOVES.items():
    src = R / "chapters" / src_name
    dst = R / "chapters" / "_v3-draft" / dst_name
    if dst.exists():
        print("  already moved: %s" % dst_name)
        continue
    t = io.open(src, encoding="utf-8").read()
    before = t
    t = t.replace("](../images/", "](../../images/")
    t = t.replace('src="../audio/', 'src="../../audio/')
    io.open(dst, "w", encoding="utf-8", newline="\n").write(t)
    depth_fixes = sum(
        before.count(x) for x in ("](../images/", 'src="../audio/')
    )
    print("  %-18s -> _v3-draft/%s  (%d relative paths deepened)"
          % (src_name, dst_name, depth_fixes))

# restore the 3rd edition's copies to exactly what is committed on this branch's
# parent state: these files must not carry any v4 edit
subprocess.run(
    ["git", "checkout", "HEAD", "--"] + ["chapters/" + n for n in MOVES],
    cwd=str(R), check=True,
)
print("restored chapters/*.qmd to HEAD (3rd edition untouched)")

# point the v4 table of contents at the moved files
cfg = R / "_quarto-v4.yml"
t = io.open(cfg, encoding="utf-8").read()
for src_name, dst_name in MOVES.items():
    old = "        - chapters/%s\n" % src_name
    new = "        - chapters/_v3-draft/%s\n" % dst_name
    if old not in t:
        if new in t:
            continue
        sys.exit("TOC entry not found: %s" % src_name)
    t = t.replace(old, new)
io.open(cfg, "w", encoding="utf-8", newline="\n").write(t)
print("v4 table of contents repointed")
