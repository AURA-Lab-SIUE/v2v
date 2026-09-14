# Verify the Chapter 16 supplement's saturation procedure in Excel: the expanding
# COUNTIFS that flags a category's first appearance, the per-case new count, and the
# decision statistic (new categories in the last 10 cases).
# Expected from Python: 382 rows, 226 cases, 117 categories, 7 new in the last 10,
# halfway (case 114) 70 of 117.
$ErrorActionPreference = 'Stop'
$csv = 'O:\20-research\aura-lab\v2v\data-raw\v3\accumulation.csv'
$xl = New-Object -ComObject Excel.Application
$xl.Visible = $false; $xl.DisplayAlerts = $false
try {
    $xl.Workbooks.OpenText($csv, 65001, 1, 1, 1, $false, $false, $false, $true, $false, $false)
    $wb = $xl.ActiveWorkbook; $ws = $wb.Worksheets.Item(1)
    $last = $ws.Cells($ws.Rows.Count, 1).End(-4162).Row
    Write-Output "rows incl header: $last"

    # D: is this the first time this category has appeared anywhere above?
    $ws.Cells(1,4).Value2 = 'first_appearance'
    $ws.Range("D2:D$last").Formula = '=IF(COUNTIFS($C$2:C2,C2)=1,1,0)'
    $xl.Calculate()
    Write-Output ("distinct categories (sum of first_appearance): {0}" -f $xl.WorksheetFunction.Sum($ws.Range("D2:D$last")))
    Write-Output ("distinct cases: {0}" -f $xl.WorksheetFunction.Max($ws.Range("A2:A$last")))

    # Per-case summary on a second sheet: new categories at each case, and cumulative.
    $sh = $wb.Worksheets.Add(); $sh.Name = 'curve'
    $sh.Cells(1,1).Value2='case'; $sh.Cells(1,2).Value2='new'; $sh.Cells(1,3).Value2='cumulative'
    $n = [int]$xl.WorksheetFunction.Max($ws.Range("A2:A$last"))
    for ($i=1; $i -le $n; $i++) {
        $sh.Cells($i+1,1).Value2 = $i
        $sh.Cells($i+1,2).Formula = "=SUMIFS('$($ws.Name)'!`$D`$2:`$D`$$last,'$($ws.Name)'!`$A`$2:`$A`$$last,A$($i+1))"
        $sh.Cells($i+1,3).Formula = "=SUM(`$B`$2:B$($i+1))"
    }
    $xl.Calculate()
    Write-Output ("cumulative at final case: {0}" -f $sh.Cells($n+1,3).Value2)
    Write-Output ("cumulative at case 25   : {0}" -f $sh.Cells(26,3).Value2)
    Write-Output ("cumulative at case 114  : {0}  (halfway; expect 70)" -f $sh.Cells(115,3).Value2)
    Write-Output ("cumulative at case 10   : {0}  (expect 14)" -f $sh.Cells(11,3).Value2)

    # Decision statistic: new categories contributed by the last 10 cases.
    $sh.Cells(1,5).Value2 = 'new_in_last_10'
    $sh.Cells(2,5).Formula = "=SUM(B$($n+1-9):B$($n+1))"
    $xl.Calculate()
    Write-Output ("new categories in the last 10 cases: {0}" -f $sh.Cells(2,5).Value2)

    Write-Output "`nfirst six cases (case, new, cumulative):"
    for ($i=1; $i -le 6; $i++) {
        Write-Output ("  {0,3} {1,4} {2,5}" -f $sh.Cells($i+1,1).Value2, $sh.Cells($i+1,2).Value2, $sh.Cells($i+1,3).Value2)
    }
    $wb.Close($false)
} finally {
    $xl.Quit(); [System.Runtime.InteropServices.Marshal]::ReleaseComObject($xl) | Out-Null
}
