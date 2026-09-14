"""Propagate the NA correction into the v4 supplements and their verifiers.

Four messages in twitch_chat_sample are true NA. R drops them from every length
statistic. write.csv writes them into the CSV as the two-character string NA, so
Excel reads them as text and LEN returns 2, which silently turns four missing
messages into four two-character ones. Every figure below is recomputed in R
with the missing values excluded.
"""
import io
import pathlib
import sys

ROOT = pathlib.Path("/Volumes/One Touch/20-research/aura-lab/v2v")

EDITS = {
    "chapters/_v3-draft/chapter26-mixed-methods.qmd": [
        ("a real difference and a negligible one, computed over 34,766 messages.",
         "a real difference and a negligible one, computed over the 34,762 of them that carry a length."),
    ],

    "supplements/excel/chapter24-preparing-describing-visualizing.qmd": [
        # the length column has to exclude the four missing messages
        ("```\n=LEN(D2)\n```\n\nThe first three come back 23, 441 and 8.",
         "```\n=IF(D2=\"NA\",\"\",LEN(D2))\n```\n\nThe first three come back 23, 441 and 8."),
        ("If you skipped the Text step above, some of these are the length of a date serial number instead.",
         "If you skipped the Text step above, some of these are the length of a date serial number instead.\n\n"
         "### Trap five: `NA` is a word in a CSV\n\n"
         "The `IF` is not decoration. **Four messages in this corpus have no text at all**, and R writes a "
         "missing value into a CSV as the two bare characters `NA`. Excel has no way to know that is not "
         "a message, so `LEN` returns **2** and four missing messages quietly become four two-character ones.\n\n"
         "Four rows in 35,267 move the mean by less than a hundredth of a character, so nothing in the "
         "descriptives below changes. They move the third digit of Chapter 25's test statistics, and they "
         "change an `n` you would report. The general point is the one worth keeping: **a CSV cannot "
         "distinguish a missing value from the text that spells it**, and every tool guesses differently. "
         "Check what your file uses for missing before you compute anything over it, because `NA`, `N/A`, "
         "`NULL`, `-99` and an empty cell all arrive as something, and only one of them is nothing."),
        ("| n | `=COUNTIF($I$2:$I$35268,\"gaming\")` | 31,309 | 3,457 |",
         "| n | `=COUNTIFS($I$2:$I$35268,\"gaming\",$H$2:$H$35268,\">=0\")` | 31,305 | 3,457 |"),
        ("Now read the table, which is the point of building it.",
         "The gaming `n` is 31,305 rather than the 31,309 messages that came from gaming channels, because "
         "of the four with no text. `COUNTIFS` with a second condition of `\">=0\"` counts only the rows that "
         "actually have a length, so the `n` describes the same messages as the mean beside it.\n\n"
         "Now read the table, which is the point of building it."),
    ],

    "supplements/excel/chapter25-inference-and-effect.qmd": [
        ("The 501 unmatched messages sit out everything below, leaving **34,766**.",
         "The 501 unmatched messages sit out everything below, leaving **34,766** classified messages, "
         "**34,762** of which carry a length. Chapter 24's supplement explains the four that do not: they "
         "are missing, and the CSV spells that `NA`. Counts of messages below use 34,766; anything "
         "computed from message length uses 34,762."),
        ("| n | `=COUNTIF($A$2:$A$34767,\"gaming\")` | 31,309 | 3,457 |",
         "| n | `=COUNTIFS($A$2:$A$34767,\"gaming\",$E$2:$E$34767,\">=0\")` | 31,305 | 3,457 |"),
        ("giving **-4.945**.", "giving **-4.942**."),
        ("returning **7.95E-07**, which you report as *p* < .001.",
         "returning **8.08E-07**, which you report as *p* < .001."),
        ("Welch's *t*(3768.7) = -4.95, *p* < .001, Cohen's *d* = -0.13.",
         "Welch's *t*(3768.7) = -4.94, *p* < .001, Cohen's *d* = -0.13."),
        ("Every p-value above is computed as though each of the 34,766 messages were an independent draw,",
         "Every p-value above is computed as though each of the 34,762 messages were an independent draw,"),
        ("It will not tell you that a significant result on 34,766 observations",
         "It will not tell you that a significant result on 34,762 observations"),
        ("| total | 1,977 | 32,789 | 34,766 |",
         "| total | 1,977 | 32,789 | 34,766 |\n\nThose are counts of messages rather than of lengths, so all "
         "34,766 classified messages appear here, including the four with no text."),
    ],

    "supplements/excel/chapter26-mixed-methods.qmd": [
        ("| gaming | 28.49 | 29.87 |", "| gaming | 28.49 | 29.88 |"),
        ("| **gap** | **5.22** | **4.26** |", "| **gap** | **5.21** | **4.25** |"),
        ("**The gap the whole study is about shrinks from 5.22 characters to 4.26, a reduction of 18 percent, "
         "on a decision about what counts as a message.**",
         "**The gap the whole study is about shrinks from 5.21 characters to 4.25, a reduction of 18 percent, "
         "on a decision about what counts as a message.**"),
        ("| Message-level measures overstate how much talk is happening | gap of 5.22 characters, *t*(3768.7) "
         "= -4.95, *p* < .001, *d* = -0.13, n = 34,766 |",
         "| Message-level measures overstate how much talk is happening | gap of 5.21 characters, *t*(3768.7) "
         "= -4.94, *p* < .001, *d* = -0.13, n = 34,762 |"),
        ("excluding commands cuts the gap to 4.26, so roughly a fifth of the headline effect",
         "excluding commands cuts the gap to 4.25, so roughly a fifth of the headline effect"),
    ],
}

for name, subs in EDITS.items():
    p = ROOT / name
    t = io.open(p, encoding="utf-8").read()
    for old, new in subs:
        if old not in t:
            sys.exit("NOT FOUND in %s:\n  %r" % (name, old[:100]))
        if t.count(old) != 1:
            sys.exit("NOT UNIQUE in %s (%d):\n  %r" % (name, t.count(old), old[:100]))
        t = t.replace(old, new)
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("patched %s (%d edits)" % (name, len(subs)))
