import io, pathlib
p = pathlib.Path("/Volumes/One Touch/20-research/aura-lab/v2v/supplements/excel/chapter21-qualitative-data-analysis.qmd")
t = io.open(p, encoding="utf-8").read()
t = t.replace("using the corpus because it has fifty sources and a ready answer, and because the two codes in it behave in opposite ways.",
              "using the corpus because it has 228 sources and a ready answer, and because two of the codes in it behave in opposite ways.")
t = t.replace("because a file with fifty sources shows you both outcomes in one screen. Treat `channel` as your `source` column and the two code columns as two of your codes.",
              "because a file with 228 sources shows you both outcomes in one workbook. Treat `channel` as your `source` column and the three code columns as three of your codes.")

i = t.index("### The source list")
j = t.index("## What Excel will not do for you")
new = '''### The source list

Copy column A, paste it into **F2**, type `source` in **F1**, then select **F1:F** and use **Data**, **Remove Duplicates**. 228 sources.

Then their sizes, in **G2**:

```
=COUNTIF($A$2:$A$156993,$F2)
```

filled down. Look at the result before going on. The largest source has 1,000 messages and the smallest has one, and 32 of the 228 have fewer than fifty. That range is the reason the next section cannot stop at raw counts.

### The matrix

Put the six code names in **H1:M1**: `directed`, `broadcast`, `gaming`, `nongame`, `command`, `talk`. In **H2**:

```
=COUNTIFS($A$2:$A$156993,$F2,$B$2:$B$156993,H$1)
```

Fill it across to **I2**, then fill **H2:I2** down to row 229. Columns J and K read the context column instead, so in **J2**:

```
=COUNTIFS($A$2:$A$156993,$F2,$C$2:$C$156993,J$1)
```

filled across to K and down, and columns L and M read the form column, so in **L2**:

```
=COUNTIFS($A$2:$A$156993,$F2,$D$2:$D$156993,L$1)
```

filled across to M and down.

**The dollar signs are the entire trick, so read them before filling anything.** `$F2` locks the column and lets the row move, so every formula in a row looks at that row's source. `H$1` locks the row and lets the column move, so every formula in a column looks at that column's code. One formula, written once, correctly fills fourteen hundred cells.

Get them wrong and nothing announces it. Chapter 18's supplement met the same problem from the other side: there, the same formula string was assigned to every cell instead of being filled, the references never shifted, and every row came back with an identical value that looked entirely reasonable. Here the failure is quieter still, because a half-anchored matrix returns a different number in every cell and none of them are wrong-looking. Check one cell by hand against a `COUNTIFS` you write separately.

### The diagnostics

Four numbers per code. For `directed`, in column H:

| Label | Formula | Result |
|---|---|---|
| total | `=SUM(H2:H229)` | 13,884 |
| sources carrying it | `=COUNTIF(H2:H229,">0")` | 204 |
| largest single source | `=MAX(H2:H229)` | 233 |
| concentration | `=MAX(H2:H229)/SUM(H2:H229)` | 1.7% |

And the same four on column L, for `command`:

| Label | Formula | Result |
|---|---|---|
| total | `=SUM(L2:L229)` | 5,524 |
| sources carrying it | `=COUNTIF(L2:L229,">0")` | 182 |
| largest single source | `=MAX(L2:L229)` | 694 |
| concentration | `=MAX(L2:L229)/SUM(L2:L229)` | 12.6% |

The second row of each table is the one that does the work. `COUNTIF(H2:H229,">0")` is not counting messages, it is counting sources that have at least one. That single change, from volume to presence, is the whole cross-source check, and it is one formula.

To name the biggest source, use Chapter 18's pairing:

```
=INDEX($F$2:$F$229,MATCH(MAX(L2:L229),L2:L229,0))
```

which returns `jbishere`. **And here is the same trap in its most dangerous form, on data you can check.** Run that pairing on column G instead, the source sizes, and it returns one channel name. But 115 of the 228 sources sit on exactly 1,000 messages, because the sample was drawn with a cap, and `MATCH` returns the position of the first match only. The tie is invisible: you get one name, with nothing to suggest that half the corpus is exactly as large. Whenever you report a maximum, count how many sources reach it:

```
=COUNTIF(G2:G229,MAX(G2:G229))
```

which returns 115.

## What it says

Set the two codes beside each other.

`directed` appears in **204 of 228** sources, and in **185 of the 187** sources with at least a hundred messages, which you can check without filtering:

```
=COUNTIFS($G$2:$G$229,">=100",$H$2:$H$229,">0")
```

No source supplies more than **1.7 percent** of it, and its three largest supply **4.7 percent** between them.

`command` appears in **182 of 228** sources, which is nearly as many. Its three largest supply **27 percent** of it:

```
=(LARGE(L2:L229,1)+LARGE(L2:L229,2)+LARGE(L2:L229,3))/SUM(L2:L229)
```

**Stop at the source counts and the two codes look alike: 204 against 182.** Go on to the concentration and they separate by a factor of seven. A qualitative write-up that reported only how many participants mentioned a theme, which is the usual way it is reported, would have shown you nothing here.

Both codes were applied the same way, and both are real. But `command` occurring 5,524 times is substantially a description of the handful of channels running music-request bots, while `directed` occurring 13,884 times is a description of the corpus. Nothing in a frequency table separates them, and both would read as a solid finding.

That is what phase four is for, and it is why Chapter 21 tells you to test a candidate theme against the whole dataset rather than against the extracts that produced it.

**Neither answer disqualifies a code.** A concentrated code can be the most important thing in a study, and Chapter 21 says so: the two participants who carry a theme may be the only two who experienced the thing you are studying. What the check buys you is knowing which kind of claim you are making before you write it down.

## Reading the matrix as a matrix

One more thing the grid is good for, and it does not need a formula.

Select **H2:M229** and apply **Home**, **Conditional Formatting**, **Color Scales**. The `command` column runs mostly white with a few dark cells near the top; the `directed` column shades evenly all the way down. The shape of a cross-source pattern and the shape of one participant's preoccupation look different, and that is the fastest read of the check you will get.

Do not report the picture. Color scales compare raw counts, and your sources are different sizes, so a dark cell may only mean a long interview. Add a share column, `=H2/$G2`, before drawing any conclusion from the shading, and use the count of sources rather than the colors when you write.

'''
t = t[:i] + new + t[j:]
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("rewrote part two")
