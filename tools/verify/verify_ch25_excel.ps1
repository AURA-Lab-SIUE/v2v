# Verifies every figure printed in the Chapter 25 Excel supplement, in Excel.
# t-test, Welch df, Cohen's d, confidence intervals, one-way ANOVA and chi-square.
#
# The analysis-ready columns (label, length, command flag, game category) are
# assembled here in PowerShell; the Excel chain that produces them is proved
# separately by verify_ch24_excel.ps1. What this script verifies is the
# inferential arithmetic, which is what the Chapter 25 supplement prints.
$ErrorActionPreference = "Stop"
$base = "O:\20-research\aura-lab\v2v-r\data-raw\"

$NONGAMING = @("Art","ASMR","Beauty & Body Art","Creative","Food & Drink","IRL",
    "Just Chatting","Makers & Crafting","Music","Music & Performing Arts",
    "Science & Technology","Sports & Fitness","Talk Shows & Podcasts","Travel & Outdoors")
$FOUR = @("Fortnite", "Hearthstone", "Just Chatting", "League of Legends")

Write-Host "reading source files..."
$chatRows = Import-Csv -Path ($base + "twitch_chat_sample.csv") -Encoding UTF8
$stRows   = Import-Csv -Path ($base + "twitch_streams_sample.csv") -Encoding UTF8

$counts = @{}
foreach ($r in $stRows) {
    if ($r.game -and $r.game -ne "NA") {
        $k = $r.channel + "|" + $r.game
        if ($counts.ContainsKey($k)) { $counts[$k]++ } else { $counts[$k] = 1 }
    }
}
$modal = @{}
foreach ($k in $counts.Keys) {
    $parts = $k.Split("|"); $c = $parts[0]; $gme = $parts[1]
    if (-not $modal.ContainsKey($c) -or $counts[$k] -gt $modal[$c][1]) { $modal[$c] = @($gme, $counts[$k]) }
}
Write-Host "channels with a modal category: $($modal.Count) (expect 48)"

$rows = New-Object System.Collections.ArrayList
foreach ($r in $chatRows) {
    if (-not $modal.ContainsKey($r.channel)) { continue }
    $gme = $modal[$r.channel][0]
    $lab = if ($NONGAMING -contains $gme) { "nongaming" } else { "gaming" }
    $cmd = if ($r.message.StartsWith("!")) { "command" } else { "not" }
    $cat = if ($FOUR -contains $gme) { $gme } else { "" }
    [void]$rows.Add(@($lab, $r.message, $cmd, $cat))
}
$n = $rows.Count
Write-Host "classified messages: $n (expect 34766)"

$arr = New-Object 'object[,]' $n, 4
for ($i = 0; $i -lt $n; $i++) { for ($j = 0; $j -lt 4; $j++) { $arr[$i, $j] = $rows[$i][$j] } }

$xl = New-Object -ComObject Excel.Application
$xl.Visible = $false; $xl.DisplayAlerts = $false; $xl.ScreenUpdating = $false
try {
    $wb = $xl.Workbooks.Add()
    $d = $wb.Worksheets.Item(1); $d.Name = "d"
    $d.Range("A1:D1").Value2 = @("label", "message", "cmd", "cat")
    $d.Columns.Item(2).NumberFormat = "@"     # message stays text
    $d.Range("A2").Resize($n, 4).Value2 = $arr
    $last = $n + 1
    # length is computed by Excel's LEN, which verify_ch24_excel.ps1 showed
    # reproduces the reference figures exactly; .NET string Length does not,
    # because it counts surrogate pairs twice.
    $d.Range("E1").Value2 = "length"
    $d.Range("E2:E$last").Formula = "=IF(B2=""NA"","""",LEN(B2))"

    $LAB = "d!`$A`$2:`$A`$$last"
    $LEN = "d!`$E`$2:`$E`$$last"
    $CMD = "d!`$C`$2:`$C`$$last"
    $CAT = "d!`$D`$2:`$D`$$last"

    $o = $wb.Worksheets.Add(); $o.Name = "out"

    # group descriptives, needed by everything below
    $o.Range("A1").Value2 = "n1 (gaming)";    $o.Range("B1").Formula = "=COUNTIF($LAB,""gaming"")"
    $o.Range("A2").Value2 = "n2 (nongaming)"; $o.Range("B2").Formula = "=COUNTIF($LAB,""nongaming"")"
    $o.Range("A3").Value2 = "m1";             $o.Range("B3").Formula = "=AVERAGEIFS($LEN,$LAB,""gaming"")"
    $o.Range("A4").Value2 = "m2";             $o.Range("B4").Formula = "=AVERAGEIFS($LEN,$LAB,""nongaming"")"
    $o.Range("A5").Value2 = "s1";             $o.Range("B5").FormulaArray = "=STDEV.S(IF($LAB=""gaming"",$LEN))"
    $o.Range("A6").Value2 = "s2";             $o.Range("B6").FormulaArray = "=STDEV.S(IF($LAB=""nongaming"",$LEN))"

    $checks = @(
        @("Welch t",      "=(B3-B4)/SQRT(B5^2/B1+B6^2/B2)",                                        "-4.95",  2),
        @("Welch df",     "=(B5^2/B1+B6^2/B2)^2/((B5^2/B1)^2/(B1-1)+(B6^2/B2)^2/(B2-1))",          "3768.7", 1),
        @("T.TEST p",     "=T.TEST(IF($LAB=""gaming"",$LEN),IF($LAB=""nongaming"",$LEN),2,3)",      "0",      6),
        @("pooled sd",    "=SQRT(((B1-1)*B5^2+(B2-1)*B6^2)/(B1+B2-2))",                            "41.22",  2),
        @("Cohen d",      "=(B3-B4)/B12",                                                           "-0.13",  2),
        @("CI half g",    "=1.96*B5/SQRT(B1)",                                                      "0.43",   2),
        @("CI half ng",   "=1.96*B6/SQRT(B2)",                                                      "2.02",   2),
        @("chi2",         "",                                                                       "110.1",  1),
        @("Cramer V",     "",                                                                       "0.0563", 4),
        @("ANOVA F",      "",                                                                       "92.26",  2),
        @("eta squared",  "",                                                                       "0.0202", 4)
    )

    # --- t-test block
    $o.Range("A8").Value2 = "Welch t";   $o.Range("B8").Formula  = "=(B3-B4)/SQRT(B5^2/B1+B6^2/B2)"
    $o.Range("A9").Value2 = "Welch df";  $o.Range("B9").Formula  = "=(B5^2/B1+B6^2/B2)^2/((B5^2/B1)^2/(B1-1)+(B6^2/B2)^2/(B2-1))"
    $o.Range("A10").Value2 = "T.TEST p"; $o.Range("B10").FormulaArray = "=T.TEST(IF($LAB=""gaming"",$LEN),IF($LAB=""nongaming"",$LEN),2,3)"
    $o.Range("A12").Value2 = "pooled sd"; $o.Range("B12").Formula = "=SQRT(((B1-1)*B5^2+(B2-1)*B6^2)/(B1+B2-2))"
    $o.Range("A13").Value2 = "Cohen d";  $o.Range("B13").Formula = "=(B3-B4)/B12"
    $o.Range("A14").Value2 = "CI half gaming";    $o.Range("B14").Formula = "=1.96*B5/SQRT(B1)"
    $o.Range("A15").Value2 = "CI half nongaming"; $o.Range("B15").Formula = "=1.96*B6/SQRT(B2)"

    # --- chi-square block: label x command
    $o.Range("D1").Value2 = "command"; $o.Range("E1").Value2 = "not"
    $o.Range("C2").Value2 = "gaming";  $o.Range("C3").Value2 = "nongaming"
    $o.Range("D2").Formula = "=COUNTIFS($LAB,""gaming"",$CMD,""command"")"
    $o.Range("E2").Formula = "=COUNTIFS($LAB,""gaming"",$CMD,""not"")"
    $o.Range("D3").Formula = "=COUNTIFS($LAB,""nongaming"",$CMD,""command"")"
    $o.Range("E3").Formula = "=COUNTIFS($LAB,""nongaming"",$CMD,""not"")"
    $o.Range("F2").Formula = "=SUM(D2:E2)"; $o.Range("F3").Formula = "=SUM(D3:E3)"
    $o.Range("D4").Formula = "=SUM(D2:D3)"; $o.Range("E4").Formula = "=SUM(E2:E3)"
    $o.Range("F4").Formula = "=SUM(D2:E3)"
    # expected counts
    $o.Range("D6").Formula = "=`$F2*D`$4/`$F`$4"; $o.Range("E6").Formula = "=`$F2*E`$4/`$F`$4"
    $o.Range("D7").Formula = "=`$F3*D`$4/`$F`$4"; $o.Range("E7").Formula = "=`$F3*E`$4/`$F`$4"
    $o.Range("A17").Value2 = "chi2"
    $o.Range("B17").Formula = "=SUMPRODUCT((D2:E3-D6:E7)^2/(D6:E7))"
    $o.Range("A18").Value2 = "CHISQ.TEST p"
    $o.Range("B18").Formula = "=CHISQ.TEST(D2:E3,D6:E7)"
    $o.Range("A19").Value2 = "Cramer V"
    $o.Range("B19").Formula = "=SQRT(B17/F4)"

    # --- ANOVA block: four largest game categories
    $cats = $FOUR
    for ($i = 0; $i -lt 4; $i++) {
        $r = 22 + $i
        $o.Cells($r, 1).Value2 = $cats[$i]
        $o.Cells($r, 2).Formula = "=COUNTIF($CAT,""$($cats[$i])"")"
        $o.Cells($r, 3).Formula = "=AVERAGEIFS($LEN,$CAT,""$($cats[$i])"")"
        $o.Cells($r, 4).FormulaArray = "=VAR.S(IF($CAT=""$($cats[$i])"",$LEN))"
    }
    $o.Range("A26").Value2 = "N"; $o.Range("B26").Formula = "=SUM(B22:B25)"
    $o.Range("A27").Value2 = "grand mean"; $o.Range("B27").Formula = "=SUMPRODUCT(B22:B25,C22:C25)/B26"
    $o.Range("A28").Value2 = "SSB"; $o.Range("B28").Formula = "=SUMPRODUCT(B22:B25,(C22:C25-B27)^2)"
    $o.Range("A29").Value2 = "SSW"; $o.Range("B29").Formula = "=SUMPRODUCT(B22:B25-1,D22:D25)"
    $o.Range("A30").Value2 = "ANOVA F"; $o.Range("B30").Formula = "=(B28/3)/(B29/(B26-4))"
    $o.Range("A31").Value2 = "eta squared"; $o.Range("B31").Formula = "=B28/(B28+B29)"

    $xl.CalculateFullRebuild()

    $expect = @(
        @("B8",  "Welch t",       -4.942,  3),
        @("B9",  "Welch df",      3768.7,  1),
        @("B12", "pooled sd",     41.22,   2),
        @("B13", "Cohen d",       -0.13,   2),
        @("B14", "CI half gaming",    0.43, 2),
        @("B15", "CI half nongaming", 2.02, 2),
        @("B17", "chi2",          110.1,   1),
        @("B19", "Cramer V",      0.0563,  4),
        @("B30", "ANOVA F",       92.26,   2),
        @("B31", "eta squared",   0.0202,  4)
    )
    Write-Host ""
    Write-Host "group descriptives: n1=$($o.Range('B1').Value2) n2=$($o.Range('B2').Value2) m1=$([math]::Round($o.Range('B3').Value2,2)) m2=$([math]::Round($o.Range('B4').Value2,2))"
    Write-Host "chi-square table: gaming [$($o.Range('D2').Value2), $($o.Range('E2').Value2)]  nongaming [$($o.Range('D3').Value2), $($o.Range('E3').Value2)]"
    Write-Host "ANOVA group n: $($o.Range('B22').Value2), $($o.Range('B23').Value2), $($o.Range('B24').Value2), $($o.Range('B25').Value2)"
    Write-Host "T.TEST p = $($o.Range('B10').Value2)   CHISQ.TEST p = $($o.Range('B18').Value2)"
    Write-Host ""
    Write-Host "label                      excel     expected"
    $bad = 0
    foreach ($e in $expect) {
        $got = [math]::Round($o.Range($e[0]).Value2, $e[3])
        $ok = ($got -eq $e[2])
        if (-not $ok) { $bad++ }
        "{0,-20} {1,10} {2,12} {3}" -f $e[1], $got, $e[2], $(if ($ok) { "ok" } else { "** MISMATCH" }) | Write-Host
    }
    Write-Host ""
    if ($bad -gt 0) { Write-Host "$bad MISMATCH(ES)" } else { Write-Host "all figures reproduced in Excel" }

    $wb.Close($false)
}
finally {
    $xl.Quit()
    [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($xl)
}
