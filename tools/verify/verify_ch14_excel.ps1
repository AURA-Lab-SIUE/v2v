# Verify every figure the Chapter 14 Excel supplement will print, in Excel itself.
# Two analyses: the naive one-sample t-test over all 17 events, and the clustered
# one over the 7 channel means. Expected from Python: naive t(16) = -2.89, d = -0.70;
# clustered t(6) = -2.77, d = -1.05.
$ErrorActionPreference = 'Stop'
$csv = 'C:\Users\alexl\AppData\Local\Temp\claude\C--pythia\911c8096-d1d3-4b3f-ab5c-0faea3c53a43\scratchpad\switch_events.csv'
$xl = New-Object -ComObject Excel.Application
$xl.Visible = $false; $xl.DisplayAlerts = $false
try {
    $wb = $xl.Workbooks.Open($csv); $ws = $wb.Worksheets.Item(1)
    $last = $ws.Cells($ws.Rows.Count, 1).End(-4162).Row
    Write-Output "last data row: $last"

    # d_words is column E, d_q F, d_shout G
    $E = "E2:E$last"
    $naive = @(
      @('n',   "=COUNT($E)"),
      @('M',   "=AVERAGE($E)"),
      @('SD',  "=STDEV.S($E)"),
      @('SE',  '=J3/SQRT(J1)'),
      @('t',   '=J2/J4'),
      @('df',  '=J1-1'),
      @('p',   '=T.DIST.2T(ABS(J5),J6)'),
      @('d',   '=J2/J3'),
      @('pchk',"=T.TEST($E,L2:L$last,2,1)")   # paired against a column of zeros
    )
    # zeros column for the T.TEST cross-check
    $ws.Range("L2:L$last").Value2 = 0
    for ($i = 0; $i -lt $naive.Count; $i++) {
        $ws.Cells($i + 1, 9).Value2  = $naive[$i][0]
        $ws.Cells($i + 1, 10).Formula = $naive[$i][1]
    }
    $xl.Calculate()
    Write-Output "--- naive, all 17 events ---"
    for ($i = 1; $i -le $naive.Count; $i++) {
        Write-Output ("{0,-5} {1}" -f $ws.Cells($i, 9).Value2, $ws.Cells($i, 10).Value2)
    }

    # --- clustered: AVERAGEIF over the distinct channels ---
    $chans = @{}
    for ($i = 2; $i -le $last; $i++) { $chans[$ws.Cells($i,1).Value2] = $true }
    $names = $chans.Keys | Sort-Object
    Write-Output ("--- channels: {0} ---" -f $names.Count)
    $r = 1
    foreach ($n in $names) {
        $ws.Cells($r, 14).Value2  = $n
        $ws.Cells($r, 15).Formula = "=AVERAGEIF(`$A`$2:`$A`$$last,N$r,`$E`$2:`$E`$$last)"
        $r++
    }
    $lastN = $r - 1
    $O = "O1:O$lastN"
    $clust = @(
      @('n',  "=COUNT($O)"),
      @('M',  "=AVERAGE($O)"),
      @('SD', "=STDEV.S($O)"),
      @('SE', '=R3/SQRT(R1)'),
      @('t',  '=R2/R4'),
      @('df', '=R1-1'),
      @('p',  '=T.DIST.2T(ABS(R5),R6)'),
      @('d',  '=R2/R3')
    )
    for ($i = 0; $i -lt $clust.Count; $i++) {
        $ws.Cells($i + 1, 17).Value2  = $clust[$i][0]
        $ws.Cells($i + 1, 18).Formula = $clust[$i][1]
    }
    $xl.Calculate()
    Write-Output "--- per-channel means (col O) ---"
    for ($i = 1; $i -le $lastN; $i++) {
        Write-Output ("{0,-18} {1}" -f $ws.Cells($i,14).Value2, $ws.Cells($i,15).Value2)
    }
    Write-Output "--- clustered, 7 channel means ---"
    for ($i = 1; $i -le $clust.Count; $i++) {
        Write-Output ("{0,-5} {1}" -f $ws.Cells($i, 17).Value2, $ws.Cells($i, 18).Value2)
    }
    $wb.Close($false)
} finally {
    $xl.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($xl) | Out-Null
}
