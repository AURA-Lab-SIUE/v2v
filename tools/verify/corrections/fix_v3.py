"""Correct figures in the 3rd edition that do not survive recomputation.

Every replacement below was recomputed from the shipped fixtures with R, the
book's own tool, by /tmp/v2v_recompute.R. The cause of the numeric ones is a
single fact: four messages in twitch_chat_sample are true NA, so nchar() and
str_length() return NA for them and every na.rm summary, t.test and lm drops
them. The published statistics were computed as though those four rows carried
a length, which moves the third significant digit of the test statistics and
the reported n.

Nothing here changes a finding. The means, medians, standard deviations,
Cohen's d, F, eta squared, the hour counts and the histogram figures all
reproduce exactly.
"""
import io
import pathlib
import sys

ROOT = pathlib.Path("/Volumes/One Touch/20-research/aura-lab/v2v/chapters")

EDITS = {
    "chapter01.qmd": [
        # 5.850648 days, which is five days and twenty hours, not five and a half
        ("collected by an automated process during five and a half days of public broadcasting",
         "collected by an automated process during five days and twenty hours of public broadcasting"),
        ("A caveat the data itself enforces: five and a half days is not a long time.",
         "A caveat the data itself enforces: five days and twenty hours is not a long time."),
    ],
    "chapter12.qmd": [
        # n() counted rows; the statistics beside it drop the four NA lengths
        ("    n      = n(),",
         "    n      = sum(!is.na(message_length)),"),
        ("| TRUE      | 31,309 | 28.49 | 17     | 38.47 |",
         "| TRUE      | 31,305 | 28.49 | 17     | 38.47 |"),
        ("Read the `mean` column and a story jumps out:",
         "The gaming row counts 31,305 rather than the 31,309 messages that came from "
         "gaming channels, because four messages in the corpus have no text at all and "
         "therefore no length. Counting rows where the statistics skip four of them "
         "would make the `n` column describe a different set of messages from the "
         "columns beside it.\n\nRead the `mean` column and a story jumps out:"),
    ],
    "chapter13.qmd": [
        ("The study did not measure those 34,766 messages",
         "The study did not measure those 34,762 messages"),
        ("  Difference           -5.22 characters",
         "  Difference           -5.21 characters"),
        ("  t                    -4.95",
         "  t                    -4.94"),
        ("The `t` value, -4.95, measures the gap between the means",
         "The `t` value, -4.94, measures the gap between the means"),
        ("The test ran on 34,766 messages,",
         "The test ran on 34,762 messages,"),
        ("Welch's _t_(3768.7) = -4.95, _p_ < .001, Cohen's _d_ = -0.13.",
         "Welch's _t_(3768.7) = -4.94, _p_ < .001, Cohen's _d_ = -0.13."),
        ("(Intercept)     33.70       0.70      48.16   < .001",
         "(Intercept)     33.70       0.70      48.08   < .001"),
        ("is_gamingTRUE   -5.22       0.74      -7.08   < .001",
         "is_gamingTRUE   -5.21       0.74      -7.06   < .001"),
        ("The coefficient on `is_gamingTRUE`, -5.22, is exactly the gap the t-test found: "
         "gaming channels average 5.22 characters fewer.",
         "The coefficient on `is_gamingTRUE`, -5.21, is exactly the gap the t-test found: "
         "gaming channels average 5.21 characters fewer."),
        ("(Its `t` of -7.08 differs a little from the Welch test's -4.95",
         "(Its `t` of -7.06 differs a little from the Welch test's -4.94"),
    ],
}

changed = 0
for name, subs in EDITS.items():
    p = ROOT / name
    t = io.open(p, encoding="utf-8").read()
    for old, new in subs:
        if old not in t:
            sys.exit("NOT FOUND in %s, refusing to guess:\n  %r" % (name, old[:90]))
        if t.count(old) != 1:
            sys.exit("NOT UNIQUE in %s (%d times):\n  %r" % (name, t.count(old), old[:90]))
        t = t.replace(old, new)
        changed += 1
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("patched %s (%d edits)" % (name, len(subs)))
print("total edits: %d" % changed)
