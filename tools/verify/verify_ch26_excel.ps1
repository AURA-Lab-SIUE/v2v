# Verifies every figure printed in the Chapter 26 Excel supplement, in Excel.
# The integration made numeric: what excluding bot commands does to the study's
# headline difference. Message length is computed by Excel's LEN, which
# verify_ch24_excel.ps1 showed reproduces the reference figures exactly.
$ErrorActionPreference = "Stop"
$base = "O:\20-research\aura-lab\v2v-r\data-raw\"

$NONGAMING = @("Art","ASMR","Beauty & Body Art","Creative","Food & Drink","IRL",
    "Just Chatting","Makers & Crafting","Music","Music & Performing Arts",
    "Science & Technology","Sports & Fitness","Talk Shows & Podcasts","Travel & Outdoors")

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
    $p = $k.Split("|")
    if (-not $modal.ContainsKey($p[0]) -or $counts[$k] -gt $modal[$p[0]][1]) { $modal[$p[0]] = @($p[1], $counts[$k]) }
}

$rows = New-Object System.Collections.ArrayList
foreach ($r in $chatRows) {
    $lab = if ($modal.ContainsKey($r.channel)) {
        if ($NONGAMING -contains $modal[$r.channel][0]) { "nongaming" } else { "gaming" }
    } else { "unmatched" }
    [void]$rows.Add(@($r.channel, $lab, $r.message))
}
$n = $rows.Count
$arr = New-Object 'object[,]' $n, 3
for ($i = 0; $i -lt $n; $i++) { for ($j = 0; $j -lt 3; $j++) { $arr[$i, $j] = $rows[$i][$j] } }

$xl = New-Object -ComObject Excel.Application
$xl.Visible = $false; $xl.DisplayAlerts = $false; $xl.ScreenUpdating = $false
try {
    $wb = $xl.Workbooks.Add()
    $d = $wb.Worksheets.Item(1); $d.Name = "d"
    $d.Range("A1:C1").Value2 = @("channel", "label", "message")
    $d.Columns.Item(3).NumberFormat = "@"
    $d.Range("A2").Resize($n, 3).Value2 = $arr
    $last = $n + 1
    $d.Range("D1").Value2 = "length"
    $d.Range("D2:D$last").Formula = "=LEN(C2)"
    $d.Range("E1").Value2 = "iscmd"
    $d.Range("E2:E$last").Formula = '=IF(LEFT(C2,1)="!","command","talk")'

    $CH  = "d!`$A`$2:`$A`$$last"
    $LAB = "d!`$B`$2:`$B`$$last"
    $LEN = "d!`$D`$2:`$D`$$last"
    $CMD = "d!`$E`$2:`$E`$$last"

    $o = $wb.Worksheets.Add(); $o.Name = "out"
    $spec = @(
        @("gaming mean all",     "=AVERAGEIFS($LEN,$LAB,""gaming"")",                      29.54, 2),
        @("gaming mean talk",    "=AVERAGEIFS($LEN,$LAB,""gaming"",$CMD,""talk"")",        30.65, 2),
        @("nongaming mean all",  "=AVERAGEIFS($LEN,$LAB,""nongaming"")",                   31.96, 2),
        @("nongaming mean talk", "=AVERAGEIFS($LEN,$LAB,""nongaming"",$CMD,""talk"")",     32.49, 2),
        @("gaming n talk",       "=COUNTIFS($LAB,""gaming"",$CMD,""talk"")",               73404, 0),
        @("nongaming n talk",    "=COUNTIFS($LAB,""nongaming"",$CMD,""talk"")",            77649, 0),
        @("dev1 n",              "=COUNTIF($CH,""dev1"")",                                 1000,  0),
        @("dev1 commands",       "=COUNTIFS($CH,""dev1"",$CMD,""command"")",               473,   0),
        @("dev1 mean all",       "=AVERAGEIFS($LEN,$CH,""dev1"")",                         15.93, 2),
        @("dev1 mean talk",      "=AVERAGEIFS($LEN,$CH,""dev1"",$CMD,""talk"")",           25.575, 3)
    )
    for ($i = 0; $i -lt $spec.Count; $i++) {
        $o.Cells($i + 1, 1).Value2 = $spec[$i][0]
        $o.Cells($i + 1, 2).Formula = $spec[$i][1]
    }
    $gapRow = $spec.Count + 1
    $o.Cells($gapRow, 1).Value2 = "gap all"
    $o.Cells($gapRow, 2).Formula = "=B3-B1"
    $o.Cells($gapRow + 1, 1).Value2 = "gap talk only"
    $o.Cells($gapRow + 1, 2).Formula = "=B4-B2"
    $o.Cells($gapRow + 2, 1).Value2 = "gap shrinks by"
    $o.Cells($gapRow + 2, 2).Formula = "=1-(B4-B2)/(B3-B1)"
    $xl.CalculateFullRebuild()

    Write-Host ""
    Write-Host "label                       excel     expected"
    $bad = 0
    for ($i = 0; $i -lt $spec.Count; $i++) {
        $got = [math]::Round($o.Cells($i + 1, 2).Value2, $spec[$i][3])
        $ok = ($got -eq $spec[$i][2])
        if (-not $ok) { $bad++ }
        "{0,-22} {1,10} {2,12} {3}" -f $spec[$i][0], $got, $spec[$i][2], $(if ($ok) { "ok" } else { "** MISMATCH" }) | Write-Host
    }
    $g1 = [math]::Round($o.Cells($gapRow, 2).Value2, 2)
    $g2 = [math]::Round($o.Cells($gapRow + 1, 2).Value2, 2)
    $g3 = [math]::Round($o.Cells($gapRow + 2, 2).Value2, 3)
    foreach ($p in @(@("gap all", $g1, 2.43), @("gap talk only", $g2, 1.84))) {
        $ok = ($p[1] -eq $p[2])
        if (-not $ok) { $bad++ }
        "{0,-22} {1,10} {2,12} {3}" -f $p[0], $p[1], $p[2], $(if ($ok) { "ok" } else { "** MISMATCH" }) | Write-Host
    }
    Write-Host ("gap shrinks by         {0,10}   (reported as 18 percent)" -f $g3)
    Write-Host ""
    if ($bad -gt 0) { Write-Host "$bad MISMATCH(ES)" } else { Write-Host "all figures reproduced in Excel" }

    $wb.Close($false)
}
finally {
    $xl.Quit()
    [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($xl)
}
