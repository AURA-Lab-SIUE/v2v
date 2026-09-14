import io, pathlib, re, sys
V = pathlib.Path("/Volumes/One Touch/20-research/aura-lab/v2v")

# ---- chapter 21: the cross-source section
p = V/"chapters/_v3-draft/chapter21-qualitative-data-analysis.qmd"
t = io.open(p, encoding="utf-8").read()
old_start = "That question has an answer you can compute"
i = t.index(old_start)
j = t.index("This is a mechanical check standing in for an interpretive judgement") if "judgement" in t else t.index("This is a mechanical check standing in for an interpretive judgment")
new = """That question has an answer you can compute, and the corpus shows what the two outcomes look like. Chapter 12's coded messages carry three manifest codes across 228 channels, and two of them behave in opposite ways.

The code `directed`, for a message aimed at a named participant, appears in **204 of the 228 channels**. Its single largest channel supplies **1.7 percent** of it, and its three largest supply **4.7 percent** between them. Whatever it is measuring is a property of the setting rather than of any one room.

The code `command`, for a message beginning with an exclamation mark, appears in **182 of 228 channels**, which is nearly as many. On the count that matters it is a different animal: one channel supplies **12.6 percent** of every command in the corpus, and three channels supply **27 percent**.

Both codes are real and both were applied by the same kind of rule. But a claim of the form "chat is full of bot commands" would be describing a handful of channels that run music-request bots, while a claim about directed address would be describing the corpus.

**Notice what the count of sources alone would have told you: almost nothing.** 204 against 182 looks like a small difference. The concentration is where the two separate, by a factor of seven, and a study that reported only how many participants mentioned a theme would have missed it entirely.

So the test is not how often a code occurs, nor even how many sources it occurs in, but **how much of it comes from its largest sources**. Spread thinly across many, it is a candidate theme. Piled up in two or three, it is a finding about those participants, which may well be worth reporting as long as you report it as that.

"""
t = t[:i] + new + t[j:]
io.open(p,"w",encoding="utf-8",newline="\n").write(t)
print("patched chapter21 chapter")

# ---- chapter 21 supplement
p = V/"supplements/excel/chapter21-qualitative-data-analysis.qmd"
t = io.open(p, encoding="utf-8").read()
reps = [
 ("`coded_messages.csv` is the file Chapter 12 coded: 35,256 messages with three columns, "
  "`channel`, `target` and `context`.",
  "`coded_messages.csv` is the file Chapter 12 coded: 156,992 messages with four columns, "
  "`channel`, `target`, `context` and `form`."),
 ("`target` is `directed` or `broadcast`, `context` is `gaming` or `nongame`.",
  "`target` is `directed` or `broadcast`, `context` is `gaming` or `nongame`, and `form` is "
  "`command` or `talk`."),
 ("You should have 35,257 rows including the header.", "You should have 156,993 rows including the header."),
 ("Fifty sources.", "228 sources."),
 ("=COUNTIF($A$2:$A$35257,$F2)", "=COUNTIF($A$2:$A$156993,$F2)"),
 ("=COUNTIFS($A$2:$A$35257,$F2,$B$2:$B$35257,H$1)", "=COUNTIFS($A$2:$A$156993,$F2,$B$2:$B$156993,H$1)"),
 ("=COUNTIFS($A$2:$A$35257,$F2,$C$2:$C$35257,J$1)", "=COUNTIFS($A$2:$A$156993,$F2,$C$2:$C$156993,J$1)"),
 ("fill **H2:I2** down to row 51", "fill **H2:I2** down to row 229"),
 ("| total | `=SUM(H2:H51)` | 3,350 |", "| total | `=SUM(H2:H229)` | 13,884 |"),
 ("| sources carrying it | `=COUNTIF(H2:H51,\">0\")` | 42 |",
  "| sources carrying it | `=COUNTIF(H2:H229,\">0\")` | 204 |"),
 ("| largest single source | `=MAX(H2:H51)` | 194 |", "| largest single source | `=MAX(H2:H229)` | 233 |"),
 ("| concentration | `=MAX(H2:H51)/SUM(H2:H51)` | 5.8% |",
  "| concentration | `=MAX(H2:H229)/SUM(H2:H229)` | 1.7% |"),
 ("| total | 4,044 |", "| total | 5,524 |"),
 ("| sources carrying it | 13 |", "| sources carrying it | 182 |"),
 ("| largest single source | 1,000 |", "| largest single source | 694 |"),
 ("| concentration | 24.7% |", "| concentration | 12.6% |"),
 ("`COUNTIF(H2:H51,\">0\")`", "`COUNTIF(H2:H229,\">0\")`"),
 ("=INDEX($F$2:$F$51,MATCH(MAX(K2:K51),K2:K51,0))", "=INDEX($F$2:$F$229,MATCH(MAX(L2:L229),L2:L229,0))"),
 ("=COUNTIF(K2:K51,MAX(K2:K51))", "=COUNTIF(L2:L229,MAX(L2:L229))"),
 ("=COUNTIFS($G$2:$G$51,\">=100\",$H$2:$H$51,\">0\")", "=COUNTIFS($G$2:$G$229,\">=100\",$H$2:$H$229,\">0\")"),
 ("=(LARGE(K2:K51,1)+LARGE(K2:K51,2)+LARGE(K2:K51,3))/SUM(K2:K51)",
  "=(LARGE(L2:L229,1)+LARGE(L2:L229,2)+LARGE(L2:L229,3))/SUM(L2:L229)"),
 ("=SUMPRODUCT(--(K2:K51=G2:G51),--(G2:G51>0))", "=SUMPRODUCT(--(L2:L229=G2:G229),--(G2:G229>0))"),
 ("Select **H2:K51**", "Select **H2:L229**"),
 ("`=H2/$G2`", "`=H2/$G2`"),
]
for a,b in reps:
    if a not in t:
        if b in t: continue
        print("  ch21 supp skip: %r" % a[:70]); continue
    t = t.replace(a,b)
io.open(p,"w",encoding="utf-8",newline="\n").write(t)
print("patched chapter21 supplement (ranges and counts)")
