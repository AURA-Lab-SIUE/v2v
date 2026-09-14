# Verify the Chapter 17 supplement: the who-addresses-whom matrix built with SUMIFS,
# then out-degree, in-degree, and the share of addressing aimed at the moderator.
# Expected from Python: 74 directed messages, HOST in=32 out=0, host share 43.2%.
#
# NOTE: each cell's formula is written with its OWN column letter. Assigning the same
# formula string to every cell does NOT shift relative references the way filling does,
# which silently pointed every column at the first participant on the first attempt.
$ErrorActionPreference = 'Stop'
$dir = 'O:\20-research\aura-lab\v2v\data-raw\v3'

function Col([int]$n) {  # 1 -> A
    $s = ''
    while ($n -gt 0) { $m = ($n - 1) % 26; $s = [char](65 + $m) + $s; $n = [int](($n - $m) / 26) }
    return $s
}

$xl = New-Object -ComObject Excel.Application
$xl.Visible = $false; $xl.DisplayAlerts = $false
try {
    $xl.Workbooks.OpenText((Join-Path $dir 'interaction.csv'), 65001, 1, 1, 1, $false, $false, $false, $true, $false, $false)
    $wb = $xl.ActiveWorkbook
    $ws = $wb.Worksheets.Item(1)
    $last = $ws.Cells($ws.Rows.Count, 1).End(-4162).Row
    Write-Output "edge rows incl header: $last"

    $names = @('HOST','P1','P2','P3','P4','P5','P6','P7')
    $n = $names.Count
    $sh = $wb.Worksheets.Add(); $sh.Name = 'matrix'

    for ($i = 0; $i -lt $n; $i++) {
        $sh.Cells($i+2, 1).Value2 = $names[$i]
        $sh.Cells(1, $i+2).Value2 = $names[$i]
    }
    for ($r = 0; $r -lt $n; $r++) {
        for ($c = 0; $c -lt $n; $c++) {
            $cl = Col ($c + 2)
            $sh.Cells($r+2, $c+2).Formula =
              "=SUMIFS('$($ws.Name)'!`$C`$2:`$C`$$last,'$($ws.Name)'!`$A`$2:`$A`$$last,`$A$($r+2),'$($ws.Name)'!`$B`$2:`$B`$$last,$cl`$1)"
        }
    }
    $firstCol = Col 2
    $lastCol  = Col ($n + 1)
    $degCol   = Col ($n + 3)

    $sh.Cells(1, $n+3).Value2 = 'addressed_others'
    for ($i = 0; $i -lt $n; $i++) {
        $sh.Cells($i+2, $n+3).Formula = "=SUM($firstCol$($i+2):$lastCol$($i+2))"
    }
    $sh.Cells($n+3, 1).Value2 = 'was_addressed'
    for ($c = 0; $c -lt $n; $c++) {
        $cl = Col ($c + 2)
        $sh.Cells($n+3, $c+2).Formula = "=SUM($cl`2:$cl$($n+1))"
    }
    $sh.Cells($n+5, 1).Value2 = 'total'
    $sh.Cells($n+5, 2).Formula = "=SUM($firstCol`2:$lastCol$($n+1))"
    $sh.Cells($n+6, 1).Value2 = 'host_share'
    $sh.Cells($n+6, 2).Formula = "=$firstCol$($n+3)/$firstCol$($n+5)"
    $xl.Calculate()

    Write-Output ""
    Write-Output ("{0,-12}{1,18}{2,15}" -f 'participant', 'addressed_others', 'was_addressed')
    for ($i = 0; $i -lt $n; $i++) {
        Write-Output ("{0,-12}{1,18}{2,15}" -f $sh.Cells($i+2,1).Value2, $sh.Cells($i+2,$n+3).Value2, $sh.Cells($n+3,$i+2).Value2)
    }
    Write-Output ("`ntotal directed messages: {0}" -f $sh.Cells($n+5,2).Value2)
    Write-Output ("share addressed to HOST : {0:N3}" -f $sh.Cells($n+6,2).Value2)
    $wb.Close($false)
} finally {
    $xl.Quit(); [System.Runtime.InteropServices.Marshal]::ReleaseComObject($xl) | Out-Null
}
