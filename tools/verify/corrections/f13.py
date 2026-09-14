import io, pathlib, sys

p = pathlib.Path("/Volumes/One Touch/20-research/aura-lab/v2v/supplements/excel/chapter13-survey-research.qmd")
t = io.open(p, encoding="utf-8").read()
E = [
 ("one row per chat sender, 1,195 of them, each with the measures computed from their messages.",
  "one row per chat sender, 6,559 of them, each with the measures computed from their messages."),
 ("You should land on a sheet of 1,196 rows, one header plus 1,195 cases, with columns A through I:",
  "You should land on a sheet of 6,560 rows, one header plus 6,559 cases, with columns A through I:"),
 ("3. Select J2, copy, then select J3 down to J1196 and paste.",
  "3. Select J2, copy, then select J3 down to J6560 and paste."),
 ("Select **J2:J1196**, copy, then **Paste Special** and choose **Values**.",
  "Select **J2:J6560**, copy, then **Paste Special** and choose **Values**."),
 ("In this file the gaming block runs from row 2 to row 1105, and the non-gaming block from row 1106 to row 1196. Write those numbers down; every formula below uses them.",
  "In this file the gaming block runs from row 2 to row 3056, and the non-gaming block from row 3057 to row 6560. Write those numbers down; every formula below uses them."),
 ("So the two ranges are `G2:G1105` and `G1106:G1196`.",
  "So the two ranges are `G2:G3056` and `G3057:G6560`."),
 ("| M1 | n, gaming | `=COUNT(G2:G1105)` |\n| M2 | n, non-gaming | `=COUNT(G1106:G1196)` |\n"
  "| M3 | mean, gaming | `=AVERAGE(G2:G1105)` |\n| M4 | mean, non-gaming | `=AVERAGE(G1106:G1196)` |\n"
  "| M5 | SD, gaming | `=STDEV.S(G2:G1105)` |\n| M6 | SD, non-gaming | `=STDEV.S(G1106:G1196)` |",
  "| M1 | n, gaming | `=COUNT(G2:G3056)` |\n| M2 | n, non-gaming | `=COUNT(G3057:G6560)` |\n"
  "| M3 | mean, gaming | `=AVERAGE(G2:G3056)` |\n| M4 | mean, non-gaming | `=AVERAGE(G3057:G6560)` |\n"
  "| M5 | SD, gaming | `=STDEV.S(G2:G3056)` |\n| M6 | SD, non-gaming | `=STDEV.S(G3057:G6560)` |"),
 ("You should see 1104 and 91 for the counts, means of 13.92 and 9.77, and standard deviations of 21.28 and 13.74.",
  "You should see 3055 and 3504 for the counts, means of 13.44 and 21.23, and standard deviations of 20.66 and 24.06."),
 ("Given standard deviations of 21.28 and 13.74, that assumption would be uncomfortable here, so Welch is the right default.",
  "Given standard deviations of 20.66 and 24.06, that assumption would be uncomfortable here, so Welch is the right default."),
 ("Expect SE = 1.577, t = 2.633, df = 128.67, and p = 0.0095.",
  "Expect SE = 0.552, t = -14.102, df = 6555.47, and p = 1.6E-44.\n\nThe sign of t is negative because M3, the gaming mean, is the smaller of the two. Nothing about the test cares which group you subtract from which; the sign records the direction and you report it in words rather than leaving a reader to work it out from a minus sign."),
 ("```\n=T.TEST(G2:G1105,G1106:G1196,2,3)\n```",
  "```\n=T.TEST(G2:G3056,G3057:G6560,2,3)\n```"),
 ("It returns 0.0095, agreeing with the long route to four decimal places. The tiny remaining difference is rounding in the degrees of freedom and does not matter.",
  "It returns 1.6E-44, agreeing with the long route. `T.TEST` reports the p-value unsigned, which is another reason to build the long route as well."),
 ("Expect a pooled SD of 20.81 and **d = 0.200**. By the conventional benchmarks that is a small effect, which is exactly the point the chapter makes: the difference is detectable and it is also slight, and the two groups overlap heavily.",
  "Expect a pooled SD of 22.54 and **d = -0.346**. By the conventional benchmarks that is between a small and a medium effect, which is exactly the point the chapter makes: the p-value has forty-three zeroes after the decimal point and the two groups still overlap heavily. A *d* of 0.35 means the average non-gaming respondent shouts more than about 64 percent of gaming respondents, which leaves 36 percent of them shouting more than the average of the other group."),
 ("> Gaming-channel respondents typed in capitals more often (M = 13.92%, SD = 21.28) than non-gaming respondents (M = 9.77%, SD = 13.74), t(128.67) = 2.63, p = .009, d = 0.20.",
  "> Non-gaming respondents typed in capitals more often (M = 21.23%, SD = 24.06) than gaming-channel respondents (M = 13.44%, SD = 20.66), t(6555.47) = -14.10, p < .001, d = -0.35."),
]
for a, b in E:
    if a not in t:
        if b in t:
            continue
        sys.exit("NOT FOUND: %r" % a[:110])
    t = t.replace(a, b)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("patched ch13 supplement")
