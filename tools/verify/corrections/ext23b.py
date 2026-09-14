"""The worked reading in Chapter 23 attributed a finding to Chapter 25 that
Chapter 25 does not contain. Neither Chapter 25 nor Chapter 7 mentions Just
Chatting at all. The claim is true, and measurably so, so it is stated here with
its own numbers instead of borrowed from a chapter that never made it.

Verified against the fixture on 2026-09-14, grouping channels by modal category:
  gaming    n = 77,218  mean 29.55  sd 39.70
  Just Chatting  n = 57,085  mean 30.62  sd 54.04   d = 0.023 against gaming
  other non-gaming n = 22,276  mean 35.39  sd 55.56  d = 0.133 against gaming
"""
import io
import pathlib
import sys

p = pathlib.Path("/Volumes/One Touch/20-research/aura-lab/v2v/chapters/"
                 "_v3-draft/chapter23-critical-cultural-analysis.qmd")
t = io.open(p, encoding="utf-8").read()

old = ("Two thirds of the non-gaming stratum is Just Chatting, and Chapter 25 reports that Just "
       "Chatting behaves almost exactly like gaming on the measure the study cares about. A "
       "comparison whose treatment group is mostly the residual bin is a comparison partly about "
       "the bin.")

new = ("Two thirds of the non-gaming stratum is Just Chatting, and it is worth splitting the "
       "stratum to see what that costs. Messages from channels whose modal category is Just "
       "Chatting average **30.62 characters** against **29.55** on gaming channels, a "
       "standardized difference of **0.02**, which is nothing. Messages from the other "
       "non-gaming channels, the art and music and talk-show ones, average **35.39**, a "
       "standardized difference of **0.13** against gaming: still small, and roughly six times "
       "larger. **The residual bin behaves like gaming and the named non-game categories do "
       "not**, so the study's headline comparison is substantially diluted by a category that "
       "exists because the platform had nowhere else to put those channels.")

if old in t:
    t = t.replace(old, new)
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("ch23: claim now stands on its own numbers")
elif "The residual bin behaves like gaming" in t:
    print("already corrected")
else:
    sys.exit("[ch23] passage not found")
