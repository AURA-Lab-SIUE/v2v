"""Build the v4 preview's _quarto.yml. Called only by tools/render-v4.sh.

Takes the 3rd edition's _quarto.yml and swaps four things: the output
directory, the downloads list, the edition and subtitle, and the entire
book.chapters block, which comes from _quarto-v4.yml. Everything else, the
theme, the citation setting, the read-time toggle script, is inherited so the
draft renders in the same shell the published book does.

Line surgery rather than a YAML round trip because m4's python3 has no PyYAML,
and because a round trip would reformat the whole file and lose its comments.
"""
import io
import sys

repo, build = sys.argv[1], sys.argv[2]

base = io.open(repo + "/_quarto.yml", encoding="utf-8").read().splitlines(True)
v4 = io.open(repo + "/_quarto-v4.yml", encoding="utf-8").read().splitlines(True)

# the v4 chapters block: from its "  chapters:" line to the end of the file
start = next(i for i, line in enumerate(v4) if line.rstrip() == "  chapters:")
v4_chapters = v4[start:]

out, i, replaced = [], 0, False
while i < len(base):
    line = base[i]
    if line.rstrip() == "  output-dir: docs":
        out.append("  output-dir: _preview-v4\n")
        i += 1
        continue
    if line.startswith("  downloads:"):
        out.append("  downloads: []\n")
        i += 1
        continue
    if line.startswith("  edition:"):
        out.append('  edition: "4th"\n')
        i += 1
        continue
    if line.startswith("  subtitle:"):
        out.append('  subtitle: "4th edition, working draft"\n')
        i += 1
        continue
    if line.rstrip() == "  chapters:":
        out.extend(v4_chapters)
        i += 1
        # skip the 3rd edition's chapter entries, which are more deeply indented
        while i < len(base) and (base[i].startswith("    ") or not base[i].strip()):
            i += 1
        replaced = True
        continue
    out.append(line)
    i += 1

if not replaced:
    sys.exit("splice failed: no '  chapters:' block found in _quarto.yml")

io.open(build + "/_quarto.yml", "w", encoding="utf-8", newline="\n").writelines(out)
