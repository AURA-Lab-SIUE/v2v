# Verify the Chapter 12 Excel supplement by doing what it tells the reader to do:
# build the crosstab from coded_messages.csv with a PivotTable, compute expected
# counts, then chi-square by hand and with CHISQ.TEST. Expected from Python:
# chi-square = 24.1684, df = 1, p = 0.000001, Cramer's V = 0.0262.
$ErrorActionPreference = 'Stop'
$csv = 'C:\Users\alexl\AppData\Local\Temp\claude\C--pythia\911c8096-d1d3-4b3f-ab5c-0faea3c53a43\scratchpad\coded_messages.csv'
$xl = New-Object -ComObject Excel.Application
$xl.Visible = $false; $xl.DisplayAlerts = $false
try {
    $wb = $xl.Workbooks.Open($csv); $ws = $wb.Worksheets.Item(1)
    $last = $ws.Cells($ws.Rows.Count, 1).End(-4162).Row
    Write-Output "rows incl header: $last"

    # Crosstab with COUNTIFS, which is what the supplement teaches first because it
    # makes the four cells explicit rather than hiding them in a pivot.
    $sh = $wb.Worksheets.Add(); $sh.Name = 'work'
    $B = "'$($ws.Name)'!`$B`$2:`$B`$$last"   # target
    $C = "'$($ws.Name)'!`$C`$2:`$C`$$last"   # context
    $cells = @(
      @(2,2,"=COUNTIFS($C,`"gaming`",$B,`"directed`")"),
      @(2,3,"=COUNTIFS($C,`"gaming`",$B,`"broadcast`")"),
      @(3,2,"=COUNTIFS($C,`"nongame`",$B,`"directed`")"),
      @(3,3,"=COUNTIFS($C,`"nongame`",$B,`"broadcast`")")
    )
    foreach ($c in $cells) { $sh.Cells($c[0], $c[1]).Formula = $c[2] }
    $sh.Range("D2").Formula = '=SUM(B2:C2)'; $sh.Range("D3").Formula = '=SUM(B3:C3)'
    $sh.Range("B4").Formula = '=SUM(B2:B3)'; $sh.Range("C4").Formula = '=SUM(C2:C3)'
    $sh.Range("D4").Formula = '=SUM(B2:C3)'
    # expected counts
    $sh.Range("B6").Formula = '=$D2*B$4/$D$4'; $sh.Range("C6").Formula = '=$D2*C$4/$D$4'
    $sh.Range("B7").Formula = '=$D3*B$4/$D$4'; $sh.Range("C7").Formula = '=$D3*C$4/$D$4'
    # chi-square by hand, then the built-in
    $sh.Range("B9").Formula  = '=SUMPRODUCT((B2:C3-B6:C7)^2/B6:C7)'
    $sh.Range("B10").Formula = '=CHISQ.TEST(B2:C3,B6:C7)'
    $sh.Range("B11").Formula = '=CHISQ.DIST.RT(B9,1)'
    $sh.Range("B12").Formula = '=SQRT(B9/D4)'
    $sh.Range("B13").Formula = '=B2/D2'
    $sh.Range("B14").Formula = '=B3/D3'
    $xl.Calculate()

    Write-Output ("observed  gaming : directed {0}  broadcast {1}  total {2}" -f $sh.Range("B2").Value2, $sh.Range("C2").Value2, $sh.Range("D2").Value2)
    Write-Output ("observed  nongame: directed {0}  broadcast {1}  total {2}" -f $sh.Range("B3").Value2, $sh.Range("C3").Value2, $sh.Range("D3").Value2)
    Write-Output ("grand total: {0}" -f $sh.Range("D4").Value2)
    Write-Output ("expected  gaming : {0}  {1}" -f $sh.Range("B6").Value2, $sh.Range("C6").Value2)
    Write-Output ("expected  nongame: {0}  {1}" -f $sh.Range("B7").Value2, $sh.Range("C7").Value2)
    Write-Output ("chi-square (hand)     : {0}" -f $sh.Range("B9").Value2)
    Write-Output ("p (CHISQ.TEST)        : {0}" -f $sh.Range("B10").Value2)
    Write-Output ("p (CHISQ.DIST.RT)     : {0}" -f $sh.Range("B11").Value2)
    Write-Output ("Cramer's V            : {0}" -f $sh.Range("B12").Value2)
    Write-Output ("% directed, gaming    : {0}" -f $sh.Range("B13").Value2)
    Write-Output ("% directed, nongame   : {0}" -f $sh.Range("B14").Value2)
    $wb.Close($false)
} finally {
    $xl.Quit(); [System.Runtime.InteropServices.Marshal]::ReleaseComObject($xl) | Out-Null
}
