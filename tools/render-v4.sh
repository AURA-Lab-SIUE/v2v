#!/bin/bash
# Render the 4th-edition working draft as a readable book.
#
# WHY THIS IS NOT A QUARTO PROFILE. A profile MERGES with _quarto.yml, and
# Quarto merges YAML arrays by concatenation, so putting book.chapters in a
# profile APPENDS the v4 table of contents to the 3rd edition's instead of
# replacing it. The first attempt rendered a sidebar with two Part IVs and two
# Part Vs. So this script builds the config itself, by splicing the v4 chapter
# list in _quarto-v4.yml into a copy of _quarto.yml, and runs the render in an
# isolated copy of the tree. The repo's own _quarto.yml is never touched.
#
# HARD: nothing here may write to docs/. docs/ is the published 3rd edition.
# The build copy excludes it, and the output lands in _preview-v4/.
#
# Usage, from anywhere on m4:   bash tools/render-v4.sh
set -euo pipefail

export PATH=/opt/homebrew/bin:/usr/local/bin:$PATH
REPO="$(cd "$(dirname "$0")/.." && pwd)"
BUILD="${TMPDIR:-/tmp}/v2v-v4-build"

command -v quarto  >/dev/null || { echo "quarto not on PATH"; exit 1; }
command -v Rscript >/dev/null || { echo "Rscript not on PATH"; exit 1; }

rm -rf "$BUILD"
mkdir -p "$BUILD"

# Everything the render needs, and nothing that is published output or history.
rsync -a --delete \
  --exclude '.git/' \
  --exclude 'docs/' \
  --exclude '_preview-v4/' \
  --exclude '_book/' \
  --exclude '.quarto/' \
  "$REPO"/ "$BUILD"/

rm -f "$BUILD/_quarto-grad.yml" "$BUILD/_quarto-undergrad.yml"

# index.qmd is in BOTH editions' tables of contents, so the 4th edition gets its
# own front matter in index-v4.qmd and the build copy swaps it into place. Editing
# index.qmd directly would rewrite the published 3rd edition's landing page.
cp "$REPO/index-v4.qmd" "$BUILD/index.qmd"
rm -f "$BUILD/index-v4.qmd"

# Splice: the base config, with output-dir, downloads, edition, subtitle and the
# whole book.chapters block replaced by the v4 ones. Line surgery rather than a
# YAML library because m4's python3 has no PyYAML. The result is not trusted on
# faith: the render is checked below against a 3rd-edition part name.
python3 "$REPO/tools/_splice_v4_config.py" "$REPO" "$BUILD"

rm -f "$BUILD/_quarto-v4.yml"
( cd "$BUILD" && quarto render --to html )

# Verify the splice replaced rather than appended: no 3rd-edition part name may
# survive into the v4 sidebar.
if grep -q "Part IV: Execution" "$BUILD/_preview-v4/index.html"; then
  echo "REFUSING to publish the preview: the 3rd edition TOC leaked into it." >&2
  exit 1
fi

rm -rf "$REPO/_preview-v4"
cp -R "$BUILD/_preview-v4" "$REPO/_preview-v4"

echo
echo "v4 preview written to $REPO/_preview-v4/index.html"
echo "docs/ was excluded from the build copy and is untouched."
