# Verifies every figure printed in the Chapter 24 Excel supplement, in Excel.
# Reproduces the whole chain: epoch conversion, LEN, the modal-category join,
# the unmatched rows, the descriptives and the histogram cap.
#
# The message column is written into a Text-formatted column before any formula
# touches it. That is what Data > From Text/CSV with the column typed as Text
# gives you in the UI, and it is not optional: left to itself Excel retypes 212
# messages as numbers and 5 as formula errors, which moves the mean and the
# long-message count. The supplement says so; this proves it.
$ErrorActionPreference = "Stop"
$chatCsv    = "O:\20-research\aura-lab\v2v-r\data-raw\twitch_chat_sample.csv"
$streamsCsv = "O:\20-research\aura-lab\v2v-r\data-raw\twitch_streams_sample.csv"

$NONGAMING = @("Art","ASMR","Beauty & Body Art","Creative","Food & Drink","IRL",
    "Just Chatting","Makers & Crafting","Music","Music & Performing Arts",
    "Science & Technology","Sports & Fitness","Talk Shows & Podcasts","Travel & Outdoors")

Write-Host "reading source files..."
$chatRows = Import-Csv -Path $chatCsv -Encoding UTF8
$stRows   = Import-Csv -Path $streamsCsv -Encoding UTF8
Write-Host "chat records: $($chatRows.Count) (expect 35267)   stream records: $($stRows.Count) (expect 32276)"

$nc = $chatRows.Count
$chatArr = New-Object 'object[,]' $nc, 5
for ($i = 0; $i -lt $nc; $i++) {
    $r = $chatRows[$i]
    $chatArr[$i, 0] = $r.id; $chatArr[$i, 1] = $r.channel; $chatArr[$i, 2] = $r.sender
    $chatArr[$i, 3] = $r.message; $chatArr[$i, 4] = $r.date
}
$ns = $stRows.Count
$stArr = New-Object 'object[,]' $ns, 2
for ($i = 0; $i -lt $ns; $i++) {
    $stArr[$i, 0] = $stRows[$i].channel; $stArr[$i, 1] = $stRows[$i].game
}

$xl = New-Object -ComObject Excel.Application
$xl.Visible = $false
$xl.DisplayAlerts = $false
$xl.ScreenUpdating = $false
try {
    $wb = $xl.Workbooks.Add()
    $chat = $wb.Worksheets.Item(1)
    $chat.Name = "chat"
    $chat.Columns.Item(4).NumberFormat = "@"      # message stays text, always
    $chat.Range("A1:E1").Value2 = @("id", "channel", "sender", "message", "date")
    $chat.Range("A2").Resize($nc, 5).Value2 = $chatArr
    $cLast = $nc + 1

    $st = $wb.Worksheets.Add()
    $st.Name = "streams"
    $st.Range("A1:B1").Value2 = @("channel", "game")
    $st.Range("A2").Resize($ns, 2).Value2 = $stArr
    $sLast = $ns + 1

    for ($i = 0; $i -lt $NONGAMING.Count; $i++) { $st.Cells($i + 1, 20).Value2 = $NONGAMING[$i] }

    # ---- channel|game key for every snapshot that recorded a category
    $st.Range("D1").Value2 = "key"
    $st.Range("D2:D$sLast").Formula = '=IF(OR($B2="",$B2="NA"),"",$A2&"|"&$B2)'

    $st.Range("D2:D$sLast").Copy() | Out-Null
    $st.Range("F2").PasteSpecial(-4163) | Out-Null
    $xl.CutCopyMode = 0
    $st.Range("F1").Value2 = "pair"
    $st.Range("F1:F$sLast").RemoveDuplicates(1, 1) | Out-Null
    $pLast = $st.Cells($st.Rows.Count, 6).End(-4162).Row
    Write-Host "unique channel|game pairs (one row is blank): $($pLast - 1) (expect 104)"

    $st.Range("G1").Value2 = "n"
    $st.Range("G2:G$pLast").Formula = "=COUNTIF(`$D`$2:`$D`$$sLast,`$F2)"
    $st.Range("H1").Value2 = "channel"
    $st.Range("H2:H$pLast").Formula = '=IFERROR(LEFT($F2,FIND("|",$F2)-1),"")'
    $st.Range("I1").Value2 = "game"
    $st.Range("I2:I$pLast").Formula = '=IFERROR(MID($F2,FIND("|",$F2)+1,999),"")'
    $st.Range("J1").Value2 = "chan|n"
    $st.Range("J2:J$pLast").Formula = '=IF($H2="","",$H2&"|"&$G2)'

    $st.Range("H2:H$pLast").Copy() | Out-Null
    $st.Range("L2").PasteSpecial(-4163) | Out-Null
    $xl.CutCopyMode = 0
    $st.Range("L1").Value2 = "channel"
    $st.Range("L1:L$pLast").RemoveDuplicates(1, 1) | Out-Null
    $chLast = $st.Cells($st.Rows.Count, 12).End(-4162).Row
    Write-Host "channel list rows (one blank): $($chLast - 1) (expect 49)"

    $st.Range("M1").Value2 = "top_n"
    $st.Range("M2:M$chLast").Formula = "=IF(`$L2=`"`",`"`",MAXIFS(`$G`$2:`$G`$$pLast,`$H`$2:`$H`$$pLast,`$L2))"
    $st.Range("N1").Value2 = "modal_game"
    $st.Range("N2:N$chLast").Formula = "=IFERROR(INDEX(`$I`$2:`$I`$$pLast,MATCH(`$L2&`"|`"&`$M2,`$J`$2:`$J`$$pLast,0)),`"`")"
    $st.Range("O1").Value2 = "label"
    $st.Range("O2:O$chLast").Formula = "=IF(`$N2=`"`",`"`",IF(COUNTIF(`$T`$1:`$T`$14,`$N2)>0,`"nongaming`",`"gaming`"))"

    # ---- derive on the chat sheet. ROUNDDOWN to whole seconds first: the raw
    # millisecond value lands 19 messages within a second of an hour boundary,
    # and the float date serial rounds them into the next hour.
    $chat.Range("G1").Value2 = "timestamp"
    $chat.Range("G2:G$cLast").Formula = '=ROUNDDOWN(E2/1000,0)/86400+DATE(1970,1,1)'
    $chat.Range("G2:G$cLast").NumberFormat = "yyyy-mm-dd hh:mm:ss"
    $chat.Range("H1").Value2 = "message_length"
    $chat.Range("H2:H$cLast").Formula = '=LEN(D2)'
    $chat.Range("I1").Value2 = "label"
    $chat.Range("I2:I$cLast").Formula = "=IFERROR(INDEX(streams!`$O`$2:`$O`$$chLast,MATCH(`$B2,streams!`$L`$2:`$L`$$chLast,0)),`"unmatched`")"

    $xl.CalculateFullRebuild()

    Write-Host ""
    Write-Host "message column: text cells = $($xl.WorksheetFunction.CountA($chat.Range("D2:D$cLast")))"
    Write-Host "first timestamp: $($chat.Range('G2').Text)   (expect 2018-11-18 21:55:27)"
    Write-Host "first three lengths: $($chat.Range('H2').Value2), $($chat.Range('H3').Value2), $($chat.Range('H4').Value2)  (expect 23, 441, 8)"

    $R = "`$I`$2:`$I`$$cLast"
    $L = "`$H`$2:`$H`$$cLast"
    $G = "`$G`$2:`$G`$$cLast"
    $o = $wb.Worksheets.Add()
    $o.Name = "out"
    $rows = @(
        @("gaming n",        "=COUNTIF(chat!$R,""gaming"")",               "31309"),
        @("nongaming n",     "=COUNTIF(chat!$R,""nongaming"")",            "3457"),
        @("unmatched n",     "=COUNTIF(chat!$R,""unmatched"")",            "501"),
        @("gaming mean",     "=AVERAGEIFS(chat!$L,chat!$R,""gaming"")",    "28.49"),
        @("nongaming mean",  "=AVERAGEIFS(chat!$L,chat!$R,""nongaming"")", "33.7"),
        @("len > 120",       "=COUNTIF(chat!$L,"">120"")",                 "1047"),
        @("max length",      "=MAX(chat!$L)",                              "501"),
        @("peak hour 13",    "=SUMPRODUCT(--(HOUR(chat!$G)=13))",          "2201"),
        @("quiet hour 03",   "=SUMPRODUCT(--(HOUR(chat!$G)=3))",           "833")
    )
    for ($i = 0; $i -lt $rows.Count; $i++) {
        $o.Cells($i + 1, 1).Value2 = $rows[$i][0]
        $o.Cells($i + 1, 2).Formula = $rows[$i][1]
        $o.Cells($i + 1, 4).Value2 = $rows[$i][2]
    }
    $arr = @(
        @("gaming median",   "=MEDIAN(IF(chat!$R=""gaming"",chat!$L))",     "17"),
        @("nongaming median","=MEDIAN(IF(chat!$R=""nongaming"",chat!$L))",  "16"),
        @("gaming sd",       "=STDEV.S(IF(chat!$R=""gaming"",chat!$L))",    "38.47"),
        @("nongaming sd",    "=STDEV.S(IF(chat!$R=""nongaming"",chat!$L))", "60.68")
    )
    for ($i = 0; $i -lt $arr.Count; $i++) {
        $r = $rows.Count + $i + 1
        $o.Cells($r, 1).Value2 = $arr[$i][0]
        $o.Cells($r, 2).FormulaArray = $arr[$i][1]
        $o.Cells($r, 4).Value2 = $arr[$i][2]
    }
    $xl.CalculateFullRebuild()

    Write-Host ""
    Write-Host "label                     excel     expected"
    $bad = 0
    foreach ($r in 1..($rows.Count + $arr.Count)) {
        $lbl = $o.Cells($r, 1).Text
        $got = $o.Cells($r, 2).Value2
        $exp = $o.Cells($r, 4).Text
        $g2 = if ($got -is [double]) { [math]::Round($got, 2) } else { $got }
        $ok = ("$g2" -eq $exp)
        if (-not $ok) { $bad++ }
        "{0,-22} {1,9} {2,12} {3}" -f $lbl, $g2, $exp, $(if ($ok) { "ok" } else { "** MISMATCH" }) | Write-Host
    }
    Write-Host ""
    if ($bad -gt 0) { Write-Host "$bad MISMATCH(ES)" } else { Write-Host "all figures reproduced in Excel" }

    $wb.Close($false)
}
finally {
    $xl.Quit()
    [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($xl)
}
