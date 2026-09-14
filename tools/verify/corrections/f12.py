import io, pathlib, sys
p = pathlib.Path("/Volumes/One Touch/20-research/aura-lab/v2v/supplements/excel/chapter12-quantitative-content-analysis.qmd")
t = io.open(p, encoding="utf-8").read()
E = [
 ("one row per chat message, 35,256 of them, with three columns.",
  "one row per chat message, 156,992 of them, with four columns."),
 ("You should land on 35,257 rows, one header plus 35,256 messages: `channel`, `target`, `context`.",
  "You should land on 156,993 rows, one header plus 156,992 messages: `channel`, `target`, `context`, `form`."),
 ("`context` is `gaming` or `nongame`, taken from the stream's category at the moment the message was sent rather than from the channel's usual habit, so a channel that switched partway through an evening is counted correctly on both sides of the switch.",
  "`context` is `gaming` or `nongame`, taken from the stream's category at the moment the message was sent rather than from the channel's usual habit, so a channel that switched partway through an evening is counted correctly on both sides of the switch. `form` is `command` if the message begins with an exclamation mark and `talk` otherwise; Chapter 21's supplement uses it and this one does not."),
 ("which is what makes 35,256 coded units possible at all",
  "which is what makes 156,992 coded units possible at all"),
 ("Eleven messages are missing from the file.",
  "Eighty-eight messages are missing from the file."),
 ("There are nearly eight times as many gaming messages as non-gaming ones, so of course there are more directed messages in the gaming row.",
  "There are about nineteen percent more gaming messages than non-gaming ones, and even that is enough to make the raw counts misleading."),
 ("| **gaming** | 3,052 | 28,160 | 31,212 |", "| **gaming** | 8,087 | 77,099 | 85,186 |"),
 ("| **nongame** | 298 | 3,746 | 4,044 |", "| **nongame** | 5,797 | 66,009 | 71,806 |"),
 ("| **total** | 3,350 | 31,906 | 35,256 |", "| **total** | 13,884 | 143,108 | 156,992 |"),
 ("If the grand total is not 35,256,", "If the grand total is not 156,992,"),
 ("That gives **9.78 percent** of gaming messages directed at the streamer, against **7.37 percent** of non-gaming messages.",
  "That gives **9.49 percent** of gaming messages directed at the streamer, against **8.07 percent** of non-gaming messages."),
 ("every row should show the same overall rate of directed messages, 3,350 out of 35,256, or 9.50 percent.",
  "every row should show the same overall rate of directed messages, 13,884 out of 156,992, or 8.84 percent."),
 ("| **gaming** | 2,965.74 | 28,246.26 |", "| **gaming** | 7,533.65 | 77,652.35 |"),
 ("| **nongame** | 384.26 | 3,659.74 |", "| **nongame** | 6,350.35 | 65,455.65 |"),
 ("The gaming row has about 86 more directed messages than independence predicts, and the non-gaming row has about 86 fewer.",
  "The gaming row has about 553 more directed messages than independence predicts, and the non-gaming row has about 553 fewer."),
 ("It returns **24.168**.", "It returns **97.48**."),
 ("returns **0.00000088**. Excel's built-in shortcut gives the same p-value from the two tables directly:",
  "returns **5.4E-23**. Excel's built-in shortcut gives the same p-value from the two tables directly:"),
 ("Both return 8.83 times ten to the negative seventh. Report it as p < .001.",
  "Both return about 5.4 times ten to the negative twenty-third. Report it as p < .001."),
 ("So there it is: a highly significant relationship, p less than one in a million. Time to write it up.",
  "So there it is: a highly significant relationship, with twenty-two zeroes after the decimal point before the p-value starts. Time to write it up."),
 ("It returns **0.026**, on a scale where 0 is no relationship and 1 is perfect. That is, by any published benchmark, negligible. Both kinds of stream are overwhelmingly full of broadcast messages, and knowing which kind you are watching moves the directed rate by about two and a half percentage points.",
  "It returns **0.025**, on a scale where 0 is no relationship and 1 is perfect. That is, by any published benchmark, negligible. Both kinds of stream are overwhelmingly full of broadcast messages, and knowing which kind you are watching moves the directed rate by about one and a half percentage points."),
 ("With 35,256 cases, a test can detect a difference far too small to matter to anyone",
  "With 156,992 cases, a test can detect a difference far too small to matter to anyone"),
 ("The test just treated 35,256 messages as 35,256 independent observations. They are not. They come from 50 channels, and messages from one channel share a streamer, an audience, and a set of local habits. The effective number of independent units is very much closer to 50 than to 35,256, and a chi-square test has no way of knowing that.",
  "The test just treated 156,992 messages as 156,992 independent observations. They are not. They come from 228 channels, and messages from one channel share a streamer, an audience, and a set of local habits. The effective number of independent units is very much closer to 228 than to 156,992, and a chi-square test has no way of knowing that."),
 ("computes a directed-message rate per channel and compares 50 numbers rather than 35,256.",
  "computes a directed-message rate per channel and compares 228 numbers rather than 156,992."),
 ("> Messages sent during gaming streams were more often addressed directly to the streamer (9.8%) than messages sent during non-gaming streams (7.4%), a difference that was statistically significant, chi-square(1, N = 35,256) = 24.17, p < .001, but negligible in size, Cramér's V = .03. Messages are nested within 50 channels, so the test overstates the precision of this comparison.",
  "> Messages sent during gaming streams were more often addressed directly to the streamer (9.5%) than messages sent during non-gaming streams (8.1%), a difference that was statistically significant, chi-square(1, N = 156,992) = 97.48, p < .001, but negligible in size, Cramér's V = .02. Messages are nested within 228 channels, so the test overstates the precision of this comparison."),
]
for a,b in E:
    if a not in t:
        if b in t: continue
        sys.exit("NOT FOUND: %r" % a[:100])
    t = t.replace(a,b)
t = t.replace("$C$2:$C$35257","$C$2:$C$156993").replace("$B$2:$B$35257","$B$2:$B$156993")
io.open(p,"w",encoding="utf-8",newline="\n").write(t)
print("patched ch12 supplement")
