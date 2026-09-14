import io, pathlib, sys

p = pathlib.Path("/Volumes/One Touch/20-research/aura-lab/v2v/planning/v4-read-through-review.md")
t = io.open(p, encoding="utf-8").read()

anchor = "## DEFERRED to Fall 2027: the graduate layer"
NOTE = """## RESOLVED: six live chapters were carrying 4th-edition data

Found while separating the editions, and worth recording because it had been
sitting in the branch since the re-sample. Commit `d5a18d5` updated chapters 8,
9, 10, 11, 12 and 13 **in `chapters/`**, the 3rd edition's own files, to the
228-channel census: 157,080 rows where the published book says 35,267, a peak
hour of 22:00 where it says 13:00, a gap of 29.54 against 31.96 where it says
28.49 against 33.70.

That was invisible because this branch never renders the live book. It would
have become visible the moment `v3-draft` merged to main, and it is the same
inconsistency the package hold exists to prevent: 4th-edition figures on a site
whose readers hold the 50-channel fixture.

All six are restored to `origin/main`, and every file in `chapters/` on this
branch is now byte-identical to what is published. Chapters 8 and 11 keep their
census figures in the 4th edition, in their `_v3-draft` copies, where they
belong. Chapters 9, 10, 12 and 13 are superseded by new drafts, so their census
versions were not needed anywhere.

One thing to lift back out of history. The reverted `chapters/chapter10.qmd`
carried the **reproducible** version of the kappa example, wired to
`data-raw/v3/build_reliability.py` and `pilot_coding.csv`, with the coder counts
and `v2v::reliability()` call written out. It is at `d5a18d5:chapters/chapter10.qmd`.
That is the passage to adapt when reconnecting the 4th edition's chapter 10,
which currently has the right numbers and no fixture behind them.

"""
if "six live chapters were carrying" in t:
    print("already noted")
else:
    if anchor not in t:
        sys.exit("anchor not found")
    t = t.replace(anchor, NOTE + anchor, 1)
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("review updated")
