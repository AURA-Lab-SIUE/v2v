import io, pathlib, sys
p = pathlib.Path("/Volumes/One Touch/20-research/aura-lab/v2v/supplements/excel/chapter16-qualitative-interviewing.qmd")
t = io.open(p, encoding="utf-8").read()
E = [
 ("`accumulation.csv` holds 102 rows, one per channel-and-category pair, with 48 channels standing in as cases and the stream categories standing in as the categories you would be discovering.",
  "`accumulation.csv` holds 381 rows, one per channel-and-category pair, with 226 channels standing in as cases and the stream categories standing in as the categories you would be discovering."),
 ("You should have 103 rows and three columns: `case_order`, `channel`, `category`.",
  "You should have 382 rows and three columns: `case_order`, `channel`, `category`."),
 ("Fill it down to row 103.", "Fill it down to row 382."),
 ("```\n=SUM(D2:D103)\n```\n\nIt returns **59**.", "```\n=SUM(D2:D382)\n```\n\nIt returns **117**."),
 ("Fill A2:A49 with 1 through 48.", "Fill A2:A227 with 1 through 226."),
 ("=SUMIFS(accumulation!$D$2:$D$103,accumulation!$A$2:$A$103,A2)",
  "=SUMIFS(accumulation!$D$2:$D$382,accumulation!$A$2:$A$382,A2)"),
 ("Fill both down to row 49.", "Fill both down to row 227."),
 ("| 1 | 3 | 3 |\n| 2 | 1 | 4 |\n| 3 | 1 | 5 |\n| 4 | 1 | 6 |\n| 5 | 0 | 6 |\n| 6 | 2 | 8 |",
  "| 1 | 1 | 1 |\n| 2 | 2 | 3 |\n| 3 | 0 | 3 |\n| 4 | 3 | 6 |\n| 5 | 1 | 7 |\n| 6 | 3 | 10 |"),
 ("and the final cumulative value, in C49, is **59**.", "and the final cumulative value, in C227, is **117**."),
 ("Select A1:C49 and insert a line chart", "Select A1:C227 and insert a line chart"),
 ("```\n=SUM(B40:B49)\n```\n\nIt returns **24**. Of 59 categories, 24 arrived in the final ten cases, and the halfway point had seen only 33.\n\n**This curve has not flattened.** That is the correct reading and it is the useful one. If these were interviews, the honest sentence would be that the study had not reached saturation at 48 cases, and the honest next step would be more cases or a narrower question. What you must not write is \"saturation was reached\", because the evidence on the screen says it was not.",
  "```\n=SUM(B218:B227)\n```\n\nIt returns **7**. Of 117 categories, 7 arrived in the final ten cases, and the halfway point, case 114, had seen 70 of them, sixty percent.\n\nSo the curve has flattened a great deal. The first ten cases produced 14 new categories and the last ten produced 7, half the rate over twenty times the accumulated total. **It has not stopped, though, and the shape is less tidy than the textbook picture.** Cases 101 to 110 brought only 2 new categories, and the final ten brought more than three times that. A curve that appears to have levelled off can start climbing again, which is the reason the rule has to be fixed before you look rather than declared at the point the line happens to look flat.\n\nIf these were interviews, the honest sentence would be that new categories were still arriving at 226 cases, at a much reduced rate, and that saturation in the strict sense was not reached. What you must not write is \"saturation was reached\", because the evidence on the screen says it was not."),
 ("**Heterogeneous cases saturate slowly, or never.** These 48 channels have little in common",
  "**Heterogeneous cases saturate slowly, or never.** These 226 channels have little in common"),
 ("While preparing this supplement, Excel and a case-sensitive tool disagreed about the number of categories: 59 against 60.",
  "While preparing this supplement, Excel and a case-sensitive tool disagreed about the number of categories: 117 against 123."),
 ("The cause was in the raw data, which carries both `minecraft` and `Minecraft` as category strings. They are one category recorded two ways. **Excel's `COUNTIFS` is case-insensitive**, so it merged them without comment and returned 59. The case-sensitive count returned 60.",
  "The cause was in the raw data, which carries both `minecraft` and `Minecraft` as category strings, and five more pairs like it: `Just Chatting`, `League of Legends`, `Hearthstone`, `Town of Salem` and `HaxBall` all appear in two spellings. Each is one category recorded two ways. **Excel's `COUNTIFS` is case-insensitive**, so it merged all six without comment and returned 117. The case-sensitive count returned 123."),
]
for a,b in E:
    if a not in t:
        if b in t: continue
        sys.exit("NOT FOUND: %r" % a[:110])
    t = t.replace(a,b)
io.open(p,"w",encoding="utf-8",newline="\n").write(t)
print("patched ch16 supplement")
