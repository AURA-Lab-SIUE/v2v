# Verifies every figure printed in the Chapter 23 Excel supplement, in Excel.
# UTF-8 import via OpenText Origin 65001 - never Workbooks.Open.
$ErrorActionPreference = "Stop"
$csv = "O:\20-research\aura-lab\v2v-r\data-raw\twitch_chat_sample.csv"

$xl = New-Object -ComObject Excel.Application
$xl.Visible = $false
$xl.DisplayAlerts = $false
try {
    $xl.Workbooks.OpenText($csv, 65001, 1, 1, 1, $false, $false, $false, $true, $false, $false)
    $wb = $xl.ActiveWorkbook
    $src = $wb.Worksheets.Item(1)
    $lastRow = $src.Cells($src.Rows.Count, 1).End(-4162).Row
    Write-Host "source rows: $lastRow  (expect 157081)"
    Write-Host "headers: $($src.Range('A1').Text),$($src.Range('B1').Text),$($src.Range('C1').Text)"

    # --- PivotTable: count of messages per sender
    $pSheet = $wb.Worksheets.Add()
    $pSheet.Name = "pivot"
    $srcRange = $src.Range("A1:E$lastRow")
    $cache = $wb.PivotCaches().Create(1, $srcRange)          # 1 = xlDatabase
    $pt = $cache.CreatePivotTable($pSheet.Range("A3"), "pt1")
    $pf = $pt.PivotFields("sender")
    $pf.Orientation = 1                                       # xlRowField
    $df = $pt.AddDataField($pt.PivotFields("id"), "n", -4112)      # -4112 = xlCount; must NOT be the row field
    $pt.RowAxisLayout(1) | Out-Null

    $pLast = $pSheet.Cells($pSheet.Rows.Count, 1).End(-4162).Row
    Write-Host "pivot rows (incl header + grand total): $pLast"

    # --- copy pivot values out to a plain sheet so we can sort
    $calc = $wb.Worksheets.Add()
    $calc.Name = "calc"
    $pSheet.Range("A4:B$($pLast-1)").Copy() | Out-Null        # drop the Grand Total row
    $calc.Range("A1").PasteSpecial(-4163) | Out-Null
    $xl.CutCopyMode = 0
    $n = $calc.Cells($calc.Rows.Count, 1).End(-4162).Row
    Write-Host "distinct senders: $n  (expect 61320)"

    # --- sort by count, descending
    $calc.Range("A1:B$n").Sort($calc.Range("B1"), 2, $null, $null, 1, $null, 1, 0) | Out-Null

    $R = "`$B`$1:`$B`$$n"
    $calc.Range("D1").Value2 = "senders"   ; $calc.Range("E1").Formula = "=COUNT($R)"
    $calc.Range("D2").Value2 = "messages"  ; $calc.Range("E2").Formula = "=SUM($R)"
    $calc.Range("D3").Value2 = "posted once"; $calc.Range("E3").Formula = "=COUNTIF($R,1)"
    $calc.Range("D4").Value2 = "pct once"  ; $calc.Range("E4").Formula = "=E3/E1"
    $calc.Range("D5").Value2 = "max"       ; $calc.Range("E5").Formula = "=MAX($R)"
    $calc.Range("D6").Value2 = "median"    ; $calc.Range("E6").Formula = "=MEDIAN($R)"

    $row = 7
    foreach ($p in 1, 5, 10, 25, 50) {
        $k = [math]::Round($n * $p / 100)
        $calc.Range("D$row").Value2 = "top $p% (k=$k)"
        $calc.Range("E$row").Formula = "=SUM(`$B`$1:`$B`$$k)/`$E`$2"
        $row++
    }
    $calc.Range("D$row").Value2 = "bottom 50% share"
    $half = [math]::Floor($n / 2)
    $calc.Range("E$row").Formula = "=SUM(`$B`$$($n-$half+1):`$B`$$n)/`$E`$2"
    $botRow = $row; $row++

    # Gini over a descending-sorted column: sum((n+1-2i)*x_i) / (n * total)
    $calc.Range("D$row").Value2 = "gini"
    $calc.Range("E$row").Formula = "=SUMPRODUCT(($n+1-2*ROW($R))*$R)/($n*`$E`$2)"
    $giniRow = $row

    $xl.CalculateFullRebuild()

    Write-Host ""
    foreach ($r in 1..$giniRow) {
        $lbl = $calc.Range("D$r").Text
        $val = $calc.Range("E$r").Value2
        if ($lbl) { "{0,-22} {1}" -f $lbl, $val | Write-Host }
    }
    Write-Host ""
    Write-Host "expect: senders 61320 | once 38158 (62.2%) | max 1773 | median 1"
    Write-Host "expect: top1 16.6% top5 35.6% top10 47.4% top25 65.7% top50 80.5% | bottom50 19.5% | gini 0.514"

    $wb.Close($false)
}
finally {
    $xl.Quit()
    [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($xl)
}
