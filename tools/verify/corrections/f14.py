import io, pathlib, sys
p = pathlib.Path("/Volumes/One Touch/20-research/aura-lab/v2v/supplements/excel/chapter14-experimental-design.qmd")
t = io.open(p, encoding="utf-8").read()
E = [
 ("one row per switch event that had enough chat on both sides to measure, seventeen of them.",
  "one row per switch event that had enough chat on both sides to measure, seventy-six of them."),
 ("You should land on a sheet of 18 rows, one header plus 17 events, with columns A through G:",
  "You should land on a sheet of 77 rows, one header plus 76 events, with columns A through G:"),
 ("Put labels in column I and formulas in column J, starting at row 1. The data range is `E2:E18`.",
  "Put labels in column I and formulas in column J, starting at row 1. The data range is `E2:E77`."),
 ("| J1 | n | `=COUNT(E2:E18)` |\n| J2 | mean difference | `=AVERAGE(E2:E18)` |\n| J3 | SD | `=STDEV.S(E2:E18)` |",
  "| J1 | n | `=COUNT(E2:E77)` |\n| J2 | mean difference | `=AVERAGE(E2:E77)` |\n| J3 | SD | `=STDEV.S(E2:E77)` |"),
 ("You should see n = 17, a mean of -1.080, SD = 1.541, SE = 0.374, t = -2.889, df = 16, p = 0.0107, and d = -0.701.\n\nRead the three middle cells together, because they are the whole logic of a t-test in one line. The mean difference is about one word. The standard error is the amount the mean would be expected to bounce around from sample to sample, here about a third of a word. Dividing one by the other asks how many standard errors the observed mean sits from zero, and the answer is nearly three, which is far enough to be unlikely by chance.",
  "You should see n = 76, a mean of 0.213, SD = 1.988, SE = 0.228, t = 0.934, df = 75, p = 0.353, and d = 0.107.\n\nRead the three middle cells together, because they are the whole logic of a t-test in one line. The mean difference is about a fifth of a word, in the direction of slightly longer messages after a switch. The standard error is the amount the mean would be expected to bounce around from sample to sample, here about a quarter of a word. Dividing one by the other asks how many standard errors the observed mean sits from zero, and the answer is under one, which is well inside what chance produces routinely."),
 ("It returns 0.0107, matching cell J7 exactly.", "It returns 0.353, matching cell J7 exactly."),
 ("Put zeros in `L2:L18`, then:\n\n```\n=T.TEST(E2:E18,L2:L18,2,1)\n```",
  "Put zeros in `L2:L77`, then:\n\n```\n=T.TEST(E2:E77,L2:L77,2,1)\n```"),
 ("Look at column A. Seventeen events, but not seventeen streamers. Sort by channel and count: forsen appears five times, uberhaxornova three, four channels twice each, and giantwaffle once. Seven channels in total.",
  "Look at column A. Seventy-six events, but not seventy-six streamers. Sort by channel and count: `pokelawls` appears eleven times, `nymn` and `jahrein` six each, `alinity` five, `uberhaxornova` four, and sixteen channels appear exactly once. Thirty-three channels in total."),
 ("That matters because the t-test above assumed seventeen independent observations. They are not independent. Five of those rows describe the same streamer with largely the same audience, and if that audience has a habit, the habit gets counted five times. The test cannot tell the difference between seventeen facts and seven facts recorded seventeen times, so it reports a precision the data do not have.",
  "That matters because the t-test above assumed seventy-six independent observations. They are not independent. Eleven of those rows describe the same streamer with largely the same audience, and if that audience has a habit, the habit gets counted eleven times. The test cannot tell the difference between seventy-six facts and thirty-three facts recorded seventy-six times, so it reports a precision the data do not have."),
 ("So average each channel's events into a single number first, then test those seven numbers.",
  "So average each channel's events into a single number first, then test those thirty-three numbers."),
 ("1. In **N1** through **N7**, type the seven channel names: `chemicaldragoon`, `forsen`, `giantwaffle`, `leonblack`, `skiddlerrs`, `sodapoppin`, `uberhaxornova`.",
  "1. In **N1** through **N33**, put the 33 distinct channel names. Copy column A into N, then **Data**, **Remove Duplicates**, which is quicker and less error-prone than typing them out."),
 ("=AVERAGEIF($A$2:$A$18,N1,$E$2:$E$18)", "=AVERAGEIF($A$2:$A$77,N1,$E$2:$E$77)"),
 ("3. Select O1, copy, and paste into O2 down to O7.", "3. Select O1, copy, and paste into O2 down to O33."),
 ("You should see these seven channel means:\n\n| Channel | Mean change in words |\n|---|---|\n| chemicaldragoon | -1.93 |\n| forsen | -1.73 |\n| giantwaffle | -0.95 |\n| leonblack | -1.22 |\n| skiddlerrs | -0.52 |\n| sodapoppin | -2.04 |\n| uberhaxornova | +0.89 |\n\nSix of the seven are negative. Read that row of numbers before you run anything on them, because it is more informative than the test will be: the pattern is consistent but not universal, and one channel went the other way.",
  "Thirty-three numbers is too many to read at once, so here are the six channels contributing the most events, plus the two extremes:\n\n| Channel | Events | Mean change in words |\n|---|---|---|\n| pokelawls | 11 | +0.49 |\n| nymn | 6 | -0.77 |\n| jahrein | 6 | +0.85 |\n| alinity | 5 | +0.58 |\n| uberhaxornova | 4 | +0.69 |\n| forsen | 3 | +1.30 |\n| xqcow | 2 | +4.93 |\n| trainwreckstv | 1 | -2.74 |\n\nSixteen of the thirty-three are negative and seventeen are positive. Read that before you run anything on it, because it is more informative than the test will be: the channels are not agreeing with each other about anything, and the two extremes come from a channel with two events and a channel with one."),
 ("Now the same eight formulas as before, in columns Q and R, pointed at `O1:O7`:",
  "Now the same eight formulas as before, in columns Q and R, pointed at `O1:O33`:"),
 ("| R1 | n | `=COUNT(O1:O7)` |\n| R2 | mean difference | `=AVERAGE(O1:O7)` |\n| R3 | SD | `=STDEV.S(O1:O7)` |",
  "| R1 | n | `=COUNT(O1:O33)` |\n| R2 | mean difference | `=AVERAGE(O1:O33)` |\n| R3 | SD | `=STDEV.S(O1:O33)` |"),
 ("Expect n = 7, a mean of -1.071, SD = 1.024, SE = 0.387, t = -2.769, df = 6, p = 0.0325, and **d = -1.047**.",
  "Expect n = 33, a mean of 0.151, SD = 1.504, SE = 0.262, t = 0.578, df = 32, p = 0.567, and **d = 0.101**."),
 ("| n | 17 events | 7 channels |\n| mean | -1.080 | -1.071 |\n| SD | 1.541 | 1.024 |\n| t | -2.889 | -2.769 |\n| df | 16 | 6 |\n| p | .011 | .032 |\n| d | -0.701 | -1.047 |",
  "| n | 76 events | 33 channels |\n| mean | 0.213 | 0.151 |\n| SD | 1.988 | 1.504 |\n| t | 0.934 | 0.578 |\n| df | 75 | 32 |\n| p | .353 | .567 |\n| d | 0.107 | 0.101 |"),
 ("The **mean barely moved**, from -1.080 to -1.071. Averaging within channel did not change what the data say is happening.",
  "The **mean barely moved**, from 0.213 to 0.151. Averaging within channel did not change what the data say is happening."),
 ("The **degrees of freedom collapsed**, from 16 to 6. This is the honest cost of admitting you have seven independent units and not seventeen, and it is why the p-value tripled.",
  "The **degrees of freedom collapsed**, from 75 to 32. This is the honest cost of admitting you have thirty-three independent units and not seventy-six, and it is why the p-value rose by more than half."),
 ("The **effect size got larger**, from -0.70 to -1.05, which surprises most people. Averaging within a channel removes the variation between that channel's own events, so the standard deviation shrank from 1.54 to 1.02 while the mean stayed put. A standardized effect is the mean divided by that standard deviation, so it grew. Larger is not better here; it is simply a different and more appropriate question, about how much channels differ from each other rather than how much events do.\n\nAnd the **conclusion survived**. The effect is still there at p = .032. It does not always work out that way, and when clustering destroys a result, the result was never there.",
  "The **effect size hardly moved**, from 0.107 to 0.101. Averaging within a channel removes the variation between that channel's own events, so the standard deviation shrank from 1.99 to 1.50, but the mean shrank in step with it and the ratio came out almost unchanged. It does not always work that way: when the within-channel variation is large relative to the variation between channels, clustering makes the standardized effect noticeably bigger.\n\nAnd the **verdict did not change**, because there was no verdict to change. Neither test found anything. That is worth dwelling on rather than skipping past, because a null that survives clustering is a stronger null than one that does not: the naive analysis had 76 observations and all the overstated precision that goes with them, and it still could not distinguish this mean from zero.\n\nThe reverse case is the dangerous one. A naive p of .04 on clustered data can become .3 the moment the units are counted honestly, and the result vanishes. You cannot tell which case you are in without running both, which is the argument for making the clustered analysis your default rather than your robustness check."),
 ("> Across seven channels, chat messages were shorter after a category switch than before it (M = -1.07 words, SD = 1.02), t(6) = -2.77, p = .032, d = -1.05. Events were averaged within channel before testing, because five of the seventeen events came from a single channel.",
  "> Across 33 channels, mean message length did not differ reliably before and after a category switch (M = +0.15 words, SD = 1.50), t(32) = 0.58, p = .567, d = 0.10. Events were averaged within channel before testing, because 11 of the 76 events came from a single channel."),
 ("That last sentence is not optional padding. A reader who does not know you clustered cannot judge the degrees of freedom, and a reviewer who spots seventeen events reported with six degrees of freedom will want the explanation you just gave them.",
  "That last sentence is not optional padding. A reader who does not know you clustered cannot judge the degrees of freedom, and a reviewer who spots 76 events reported with 32 degrees of freedom will want the explanation you just gave them.\n\nNotice also what the sentence does not say. It does not say the switch had no effect. It says this analysis could not detect one, which is a claim about the study rather than about the world, and with an effect size of 0.10 it is the only claim available."),
]
for a, b in E:
    if a not in t:
        if b in t:
            continue
        sys.exit("NOT FOUND: %r" % a[:110])
    t = t.replace(a, b)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("patched ch14 supplement")
