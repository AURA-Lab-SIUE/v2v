# Verifies every figure printed in the Chapter 21 Excel supplement, in Excel.
# UTF-8 import via OpenText Origin 65001 - never Workbooks.Open.
$ErrorActionPreference = "Stop"
$csv = "O:\20-research\aura-lab\v2v\data-raw\v3\coded_messages.csv"

$xl = New-Object -ComObject Excel.Application
$xl.Visible = $false
$xl.DisplayAlerts = $false
try {
    $xl.Workbooks.OpenText($csv, 65001, 1, 1, 1, $false, $false, $false, $true, $false, $false)
    $wb = $xl.ActiveWorkbook
    $ws = $wb.Worksheets.Item(1)

    $last = $ws.Cells($ws.Rows.Count, 1).End(-4162).Row
    Write-Host "last row: $last  (expect 35257)"
    Write-Host "A1/B1/C1: $($ws.Range('A1').Text) / $($ws.Range('B1').Text) / $($ws.Range('C1').Text)"

    $D = "`$A`$2:`$A`$$last"   # channel
    $T = "`$B`$2:`$B`$$last"   # target
    $X = "`$C`$2:`$C`$$last"   # context

    # --- build the unique source list with Remove Duplicates, as a student would
    $ws.Range("A2:A$last").Copy() | Out-Null
    $ws.Range("F2").PasteSpecial(-4163) | Out-Null
    $xl.CutCopyMode = 0
    $ws.Range("F1").Value2 = "source"
    $ws.Range("F1:F$last").RemoveDuplicates(1, 1) | Out-Null
    $nSrc = $ws.Cells($ws.Rows.Count, 6).End(-4162).Row - 1
    Write-Host "unique sources: $nSrc  (expect 50)"

    $srcLast = $nSrc + 1

    # --- source size
    $ws.Range("G1").Value2 = "n"
    $ws.Range("G2:G$srcLast").Formula = "=COUNTIF($D,`$F2)"

    # --- the code-by-source matrix
    $ws.Range("H1").Value2 = "directed"
    $ws.Range("I1").Value2 = "broadcast"
    $ws.Range("J1").Value2 = "gaming"
    $ws.Range("K1").Value2 = "nongame"
    $ws.Range("H2:H$srcLast").Formula = "=COUNTIFS($D,`$F2,$T,H`$1)"
    $ws.Range("I2:I$srcLast").Formula = "=COUNTIFS($D,`$F2,$T,I`$1)"
    $ws.Range("J2:J$srcLast").Formula = "=COUNTIFS($D,`$F2,$X,J`$1)"
    $ws.Range("K2:K$srcLast").Formula = "=COUNTIFS($D,`$F2,$X,K`$1)"

    # --- diagnostics per code
    $ws.Range("M1").Value2 = "total"
    $ws.Range("M2").Formula = "=SUM(H2:H$srcLast)"
    $ws.Range("M3").Formula = "=SUM(I2:I$srcLast)"
    $ws.Range("M4").Formula = "=SUM(J2:J$srcLast)"
    $ws.Range("M5").Formula = "=SUM(K2:K$srcLast)"
    $ws.Range("N1").Value2 = "sources"
    $ws.Range("N2").Formula = "=COUNTIF(H2:H$srcLast,`">0`")"
    $ws.Range("N3").Formula = "=COUNTIF(I2:I$srcLast,`">0`")"
    $ws.Range("N4").Formula = "=COUNTIF(J2:J$srcLast,`">0`")"
    $ws.Range("N5").Formula = "=COUNTIF(K2:K$srcLast,`">0`")"
    $ws.Range("O1").Value2 = "max"
    $ws.Range("O2").Formula = "=MAX(H2:H$srcLast)"
    $ws.Range("O3").Formula = "=MAX(I2:I$srcLast)"
    $ws.Range("O4").Formula = "=MAX(J2:J$srcLast)"
    $ws.Range("O5").Formula = "=MAX(K2:K$srcLast)"
    $ws.Range("P1").Value2 = "concentration"
    $ws.Range("P2").Formula = "=O2/M2"
    $ws.Range("P3").Formula = "=O3/M3"
    $ws.Range("P4").Formula = "=O4/M4"
    $ws.Range("P5").Formula = "=O5/M5"
    $ws.Range("Q1").Value2 = "topsource"
    $ws.Range("Q2").Formula = "=INDEX(`$F`$2:`$F`$$srcLast,MATCH(O2,H2:H$srcLast,0))"
    $ws.Range("Q5").Formula = "=INDEX(`$F`$2:`$F`$$srcLast,MATCH(O5,K2:K$srcLast,0))"

    # --- extra claims
    $ws.Range("S1").Value2 = "sources>=100"
    $ws.Range("S2").Formula = "=COUNTIF(G2:G$srcLast,`">=100`")"
    $ws.Range("S3").Value2 = "directed present among those"
    $ws.Range("S4").Formula = "=COUNTIFS(G2:G$srcLast,`">=100`",H2:H$srcLast,`">0`")"
    $ws.Range("S5").Value2 = "channels wholly nongame"
    $ws.Range("S6").Formula = "=SUMPRODUCT(--(K2:K$srcLast=G2:G$srcLast),--(G2:G$srcLast>0))"
    $ws.Range("S7").Value2 = "nongame top3 share"
    $ws.Range("S8").Formula = "=(LARGE(K2:K$srcLast,1)+LARGE(K2:K$srcLast,2)+LARGE(K2:K$srcLast,3))/M5"
    $ws.Range("S9").Value2 = "rows"
    $ws.Range("S10").Formula = "=COUNTA($D)"

    $xl.CalculateFullRebuild()

    Write-Host ""
    Write-Host "code        total   sources   max   concentration  top"
    foreach ($r in 2..5) {
        $lbl = @{2="directed";3="broadcast";4="gaming";5="nongame"}[$r]
        $tot = $ws.Range("M$r").Value2
        $src = $ws.Range("N$r").Value2
        $max = $ws.Range("O$r").Value2
        $con = $ws.Range("P$r").Value2
        $top = $ws.Range("Q$r").Text
        "{0,-10} {1,7} {2,7} {3,7}  {4,12:P1}  {5}" -f $lbl, $tot, $src, $max, $con, $top | Write-Host
    }
    Write-Host ""
    Write-Host "rows                       : $($ws.Range('S10').Value2)  (expect 35256)"
    Write-Host "sources with >=100 msgs    : $($ws.Range('S2').Value2)  (expect 41)"
    Write-Host "  of those carrying directed: $($ws.Range('S4').Value2)  (expect 41)"
    Write-Host "channels wholly nongame    : $($ws.Range('S6').Value2)  (expect 4)"
    Write-Host "nongame top-3 share        : $($ws.Range('S8').Value2)  (expect 0.6229)"

    $wb.Close($false)
}
finally {
    $xl.Quit()
    [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($xl)
}
