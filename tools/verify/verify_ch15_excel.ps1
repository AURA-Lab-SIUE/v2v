# Verifies every figure printed in the Chapter 15 Excel supplement, in Excel.
# The documentation audit: row and channel counts, duplicate ids, blank
# messages, the documented 509-character maximum, the date span, and the
# undocumented per-channel cap at 1,000 messages.
#
# The message column is written into a Text-formatted column before any formula
# touches it, for the reason verify_ch24_excel.ps1 documents at length.
$ErrorActionPreference = "Stop"
$csv = "O:\20-research\aura-lab\v2v-r\data-raw\twitch_chat_sample.csv"

$ANCHORS = @("xqcow","forsen","sodapoppin","asmongold","loltyler1","disguisedtoast","giantwaffle","bobross")

$rows = Import-Csv -Path $csv -Encoding UTF8
$n = $rows.Count
$arr = New-Object 'object[,]' $n, 5
for ($i = 0; $i -lt $n; $i++) {
    $r = $rows[$i]
    $arr[$i, 0] = $r.id; $arr[$i, 1] = $r.channel; $arr[$i, 2] = $r.sender
    $arr[$i, 3] = $r.message; $arr[$i, 4] = $r.date
}

$xl = New-Object -ComObject Excel.Application
$xl.Visible = $false; $xl.DisplayAlerts = $false; $xl.ScreenUpdating = $false
try {
    $wb = $xl.Workbooks.Add()
    $d = $wb.Worksheets.Item(1); $d.Name = "chat"
    $d.Columns.Item(4).NumberFormat = "@"
    $d.Range("A1:E1").Value2 = @("id", "channel", "sender", "message", "date")
    $d.Range("A2").Resize($n, 5).Value2 = $arr
    $last = $n + 1

    $d.Range("G1").Value2 = "length"
    $d.Range("G2:G$last").Formula = "=LEN(D2)"
    $d.Range("H1").Value2 = "ts"
    $d.Range("H2:H$last").Formula = "=ROUNDDOWN(E2/1000,0)/86400+DATE(1970,1,1)"

    # one row per channel
    $d.Range("B2:B$last").Copy() | Out-Null
    $d.Range("J2").PasteSpecial(-4163) | Out-Null
    $xl.CutCopyMode = 0
    $d.Range("J1").Value2 = "channel"
    $d.Range("J1:J$last").RemoveDuplicates(1, 1) | Out-Null
    $cLast = $d.Cells($d.Rows.Count, 10).End(-4162).Row
    $d.Range("K1").Value2 = "n"
    $d.Range("K2:K$cLast").Formula = "=COUNTIF(`$B`$2:`$B`$$last,`$J2)"

    $o = $wb.Worksheets.Add(); $o.Name = "audit"
    $spec = @(
        @("rows",                "=COUNTA(chat!`$A`$2:`$A`$$last)",                          35267),
        @("distinct ids",        "=SUMPRODUCT(1/COUNTIF(chat!`$A`$2:`$A`$$last,chat!`$A`$2:`$A`$$last))", 35267),
        @("blank messages",      "=COUNTBLANK(chat!`$D`$2:`$D`$$last)",                      0),
        @("missing (text NA)",   "=COUNTIF(chat!`$D`$2:`$D`$$last,""NA"")",                  4),
        @("channels",            "=COUNTA(chat!`$J`$2:`$J`$$cLast)",                         50),
        @("anchors present",     "",                                                          8),
        @("max length",          "=MAX(chat!`$G`$2:`$G`$$last)",                             501),
        @("messages over 500",   "=COUNTIF(chat!`$G`$2:`$G`$$last,"">500"")",                1),
        @("messages over 509",   "=COUNTIF(chat!`$G`$2:`$G`$$last,"">509"")",                0),
        @("channels at exactly 1000", "=COUNTIF(chat!`$K`$2:`$K`$$cLast,1000)",              31),
        @("channels over 1000",  "=COUNTIF(chat!`$K`$2:`$K`$$cLast,"">1000"")",              0),
        @("channels under 100",  "=COUNTIF(chat!`$K`$2:`$K`$$cLast,""<100"")",               9),
        @("smallest channel",    "=MIN(chat!`$K`$2:`$K`$$cLast)",                            1)
    )
    for ($i = 0; $i -lt $spec.Count; $i++) {
        $o.Cells($i + 1, 1).Value2 = $spec[$i][0]
        if ($spec[$i][1]) { $o.Cells($i + 1, 2).Formula = $spec[$i][1] }
        $o.Cells($i + 1, 4).Value2 = $spec[$i][2]
    }
    # anchors present: one COUNTIF per anchor, summed
    for ($i = 0; $i -lt $ANCHORS.Count; $i++) {
        $o.Cells($i + 1, 6).Value2 = $ANCHORS[$i]
        $o.Cells($i + 1, 7).Formula = "=COUNTIF(chat!`$B`$2:`$B`$$last,`$F$($i+1))"
    }
    # write the anchors-present total into whichever row that check occupies,
    # so inserting a check above it cannot silently overwrite a different row
    $apRow = 1 + [array]::IndexOf(($spec | ForEach-Object { $_[0] }), "anchors present")
    $o.Cells($apRow, 2).Formula = "=COUNTIF(G1:G8,"">0"")"
    $o.Range("A14").Value2 = "first message"
    $o.Range("B14").Formula = "=MIN(chat!`$H`$2:`$H`$$last)"
    $o.Range("A15").Value2 = "last message"
    $o.Range("B15").Formula = "=MAX(chat!`$H`$2:`$H`$$last)"
    $o.Range("A16").Value2 = "span in days"
    $o.Range("B16").Formula = "=B15-B14"
    $o.Range("B14:B15").NumberFormat = "yyyy-mm-dd hh:mm"
    $xl.CalculateFullRebuild()

    Write-Host ""
    Write-Host "check                          excel     documented/expected"
    $bad = 0
    for ($i = 0; $i -lt $spec.Count; $i++) {
        $got = $o.Cells($i + 1, 2).Value2
        if ($got -is [double]) { $got = [math]::Round($got, 0) }
        $ok = ("$got" -eq "$($spec[$i][2])")
        if (-not $ok) { $bad++ }
        "{0,-28} {1,8} {2,12} {3}" -f $spec[$i][0], $got, $spec[$i][2], $(if ($ok) { "ok" } else { "** MISMATCH" }) | Write-Host
    }
    Write-Host ""
    Write-Host "anchor counts: $(($ANCHORS | ForEach-Object -Begin {$k=1} -Process { "$_=$($o.Cells($k,7).Value2)"; $k++ }) -join ', ')"
    Write-Host "first message: $($o.Range('B14').Text)   last: $($o.Range('B15').Text)   span: $([math]::Round($o.Range('B16').Value2,2)) days"
    Write-Host ""
    if ($bad -gt 0) { Write-Host "$bad MISMATCH(ES)" } else { Write-Host "all figures reproduced in Excel" }

    $wb.Close($false)
}
finally {
    $xl.Quit()
    [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($xl)
}
