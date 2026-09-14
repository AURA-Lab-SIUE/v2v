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
    Write-Host "last row: $last  (expect 156993)"
    Write-Host "A1..D1: $($ws.Range('A1').Text) / $($ws.Range('B1').Text) / $($ws.Range('C1').Text) / $($ws.Range('D1').Text)"

    $D = "`$A`$2:`$A`$$last"   # channel
    $T = "`$B`$2:`$B`$$last"   # target
    $X = "`$C`$2:`$C`$$last"   # context
    $M = "`$D`$2:`$D`$$last"   # form

    # --- build the unique source list with Remove Duplicates, as a student would
    $ws.Range("A2:A$last").Copy() | Out-Null
    $ws.Range("F2").PasteSpecial(-4163) | Out-Null
    $xl.CutCopyMode = 0
    $ws.Range("F1").Value2 = "source"
    $ws.Range("F1:F$last").RemoveDuplicates(1, 1) | Out-Null
    $nSrc = $ws.Cells($ws.Rows.Count, 6).End(-4162).Row - 1
    Write-Host "unique sources: $nSrc  (expect 228)"

    $srcLast = $nSrc + 1

    # --- source size
    $ws.Range("G1").Value2 = "n"
    $ws.Range("G2:G$srcLast").Formula = "=COUNTIF($D,`$F2)"

    # --- the code-by-source matrix, six codes across three columns of the CSV
    $names = @("directed","broadcast","gaming","nongame","command","talk")
    $cols  = @("H","I","J","K","L","M")
    $ranges= @($T,$T,$X,$X,$M,$M)
    for ($i = 0; $i -lt 6; $i++) {
        $c = $cols[$i]
        $ws.Range("$c`1").Value2 = $names[$i]
        $ws.Range("$c`2:$c$srcLast").Formula = "=COUNTIFS($D,`$F2,$($ranges[$i]),$c`$1)"
    }

    # --- diagnostics per code, one row each in O..S
    $ws.Range("O1").Value2 = "total"
    $ws.Range("P1").Value2 = "sources"
    $ws.Range("Q1").Value2 = "max"
    $ws.Range("R1").Value2 = "concentration"
    $ws.Range("S1").Value2 = "top3"
    $ws.Range("T1").Value2 = "topsource"
    for ($i = 0; $i -lt 6; $i++) {
        $c = $cols[$i]; $r = $i + 2
        $ws.Range("O$r").Formula = "=SUM($c`2:$c$srcLast)"
        $ws.Range("P$r").Formula = "=COUNTIF($c`2:$c$srcLast,`">0`")"
        $ws.Range("Q$r").Formula = "=MAX($c`2:$c$srcLast)"
        $ws.Range("R$r").Formula = "=Q$r/O$r"
        $ws.Range("S$r").Formula = "=(LARGE($c`2:$c$srcLast,1)+LARGE($c`2:$c$srcLast,2)+LARGE($c`2:$c$srcLast,3))/O$r"
        $ws.Range("T$r").Formula = "=INDEX(`$F`$2:`$F`$$srcLast,MATCH(Q$r,$c`2:$c$srcLast,0))"
    }

    # --- extra claims
    $ws.Range("V1").Value2  = "rows"
    $ws.Range("W1").Formula = "=COUNTA($D)"
    $ws.Range("V2").Value2  = "sources>=100"
    $ws.Range("W2").Formula = "=COUNTIF(G2:G$srcLast,`">=100`")"
    $ws.Range("V3").Value2  = "of those, directed present"
    $ws.Range("W3").Formula = "=COUNTIFS(G2:G$srcLast,`">=100`",H2:H$srcLast,`">0`")"
    $ws.Range("V4").Value2  = "smallest source"
    $ws.Range("W4").Formula = "=MIN(G2:G$srcLast)"
    $ws.Range("V5").Value2  = "sources under 50 msgs"
    $ws.Range("W5").Formula = "=COUNTIF(G2:G$srcLast,`"<50`")"
    $ws.Range("V6").Value2  = "sources tied at the max size"
    $ws.Range("W6").Formula = "=COUNTIF(G2:G$srcLast,MAX(G2:G$srcLast))"
    $ws.Range("V7").Value2  = "largest source"
    $ws.Range("W7").Formula = "=MAX(G2:G$srcLast)"

    $xl.CalculateFullRebuild()

    Write-Host ""
    Write-Host "code        total   sources   max   concentration   top3   top"
    for ($i = 0; $i -lt 6; $i++) {
        $r = $i + 2
        "{0,-10} {1,7} {2,7} {3,7}  {4,12:P1} {5,7:P1}   {6}" -f $names[$i],
            $ws.Range("O$r").Value2, $ws.Range("P$r").Value2, $ws.Range("Q$r").Value2,
            $ws.Range("R$r").Value2, $ws.Range("S$r").Value2, $ws.Range("T$r").Text | Write-Host
    }
    Write-Host ""
    $exp = @{1="156992"; 2="187"; 3="185"; 4="1"; 5="32"; 6="115"; 7="1000"}
    $lbl = @{1="rows"; 2="sources>=100"; 3="  of those carrying directed"; 4="smallest source";
             5="sources under 50 messages"; 6="sources tied at the max size"; 7="largest source"}
    foreach ($r in 1..7) {
        "{0,-30}: {1}  (expect {2})" -f $lbl[$r], $ws.Range("W$r").Value2, $exp[$r] | Write-Host
    }
    Write-Host ""
    Write-Host "supplement claims: directed 13,884 / 204 / 233 / 1.7% / 4.7%"
    Write-Host "                   command   5,524 / 182 / 694 / 12.6% / 27.3% / jbishere"

    $wb.Close($false)
}
finally {
    $xl.Quit()
    [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($xl)
}
