# Verify every figure the Chapter 14 Excel supplement will print, in Excel itself.
# Two analyses per measure: the naive one-sample t-test over all 76 events, and the
# clustered one over the 33 channel means. Run for d_words (column E) and d_shout (G).
# Expected from R:
#   d_words  naive t(75) =  0.934 p=.3532 d= 0.107 | clustered t(32) =  0.578 p=.5675 d= 0.101
#   d_q      naive t(75) =  0.018 p=.9860 d= 0.002 | clustered t(32) =  0.333 p=.7411 d= 0.058
#   d_shout  naive t(75) = -2.745 p=.0076 d=-0.315 | clustered t(32) = -2.219 p=.0337 d=-0.386
$ErrorActionPreference = 'Stop'
$csv = 'O:\20-research\aura-lab\v2v\data-raw\v3\switch_events.csv'
$xl = New-Object -ComObject Excel.Application
$xl.Visible = $false; $xl.DisplayAlerts = $false
try {
    $xl.Workbooks.OpenText($csv, 65001, 1, 1, 1, $false, $false, $false, $true, $false, $false)
    $wb = $xl.ActiveWorkbook; $ws = $wb.Worksheets.Item(1)
    $last = $ws.Cells($ws.Rows.Count, 1).End(-4162).Row
    Write-Output "last data row: $last  (expect 77)"

    # zeros column for the T.TEST cross-check the supplement teaches
    $ws.Range("L2:L$last").Value2 = 0

    # the distinct channels, in a stable order
    $chans = @{}
    for ($i = 2; $i -le $last; $i++) { $chans[$ws.Cells($i,1).Value2] = $true }
    $names = $chans.Keys | Sort-Object
    Write-Output ("distinct channels: {0}  (expect 33)" -f $names.Count)
    $r = 1
    foreach ($n in $names) { $ws.Cells($r, 14).Value2 = $n; $r++ }
    $lastN = $r - 1

    # each measure gets its own pair of scratch columns so nothing is overwritten
    $measures = @(
        @{ name = 'd_words'; col = 'E'; means = 'P'; lbl = 'R'; val = 'S' },
        @{ name = 'd_q';     col = 'F'; means = 'T'; lbl = 'U'; val = 'V' },
        @{ name = 'd_shout'; col = 'G'; means = 'W'; lbl = 'X'; val = 'Y' }
    )

    foreach ($m in $measures) {
        $c = $m.col; $mc = $m.means; $vc = $m.val
        $ws.Range("$mc`1:$mc$lastN").Formula =
            "=AVERAGEIF(`$A`$2:`$A`$$last,`$N1,`$$c`$2:`$$c`$$last)"
        $rows = @(
          @('n_naive',   "=COUNT($c`2:$c$last)"),
          @('M_naive',   "=AVERAGE($c`2:$c$last)"),
          @('SD_naive',  "=STDEV.S($c`2:$c$last)"),
          @('SE_naive',  "=$vc`3/SQRT($vc`1)"),
          @('t_naive',   "=$vc`2/$vc`4"),
          @('df_naive',  "=$vc`1-1"),
          @('p_naive',   "=T.DIST.2T(ABS($vc`5),$vc`6)"),
          @('d_naive',   "=$vc`2/$vc`3"),
          @('p_T.TEST',  "=T.TEST($c`2:$c$last,L2:L$last,2,1)"),
          @('n_clust',   "=COUNT($mc`1:$mc$lastN)"),
          @('M_clust',   "=AVERAGE($mc`1:$mc$lastN)"),
          @('SD_clust',  "=STDEV.S($mc`1:$mc$lastN)"),
          @('SE_clust',  "=$vc`12/SQRT($vc`10)"),
          @('t_clust',   "=$vc`11/$vc`13"),
          @('df_clust',  "=$vc`10-1"),
          @('p_clust',   "=T.DIST.2T(ABS($vc`14),$vc`15)"),
          @('d_clust',   "=$vc`11/$vc`12")
        )
        for ($i = 0; $i -lt $rows.Count; $i++) {
            $ws.Range("$($m.lbl)$($i+1)").Value2  = $rows[$i][0]
            $ws.Range("$vc$($i+1)").Formula = $rows[$i][1]
        }
    }
    $xl.CalculateFullRebuild()

    foreach ($m in $measures) {
        $vc = $m.val
        Write-Output ""
        Write-Output ("--- {0} ---" -f $m.name)
        foreach ($i in 1..17) {
            Write-Output ("{0,-10} {1}" -f $ws.Range("$($m.lbl)$i").Value2, $ws.Range("$vc$i").Value2)
        }
    }

    Write-Output ""
    Write-Output "--- the eight channel means the supplement tables (d_words) ---"
    foreach ($want in 'pokelawls','nymn','jahrein','alinity','uberhaxornova','forsen','xqcow','trainwreckstv') {
        for ($i = 1; $i -le $lastN; $i++) {
            if ($ws.Cells($i,14).Value2 -eq $want) {
                Write-Output ("{0,-16} {1}" -f $want, $ws.Range("P$i").Value2)
            }
        }
    }
    $wb.Close($false)
} finally {
    $xl.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($xl) | Out-Null
}
