# Verify the Chapter 13 Excel supplement by doing exactly what it tells the reader:
# build the group column, sort so the groups are contiguous, then run Welch by hand
# and against T.TEST, plus Cohen's d from the pooled SD.
# Expected from R: n 3055 gaming / 3504 nongame; M 13.4401 / 21.2263;
#   SD 20.6562 / 24.0589; SE 0.5521; t -14.1019; df 6555.47; p 1.646e-44;
#   pooled SD 22.5381; d -0.3455.
$ErrorActionPreference = 'Stop'
$csv = 'O:\20-research\aura-lab\v2v\data-raw\v3\respondents.csv'
$xl = New-Object -ComObject Excel.Application
$xl.Visible = $false; $xl.DisplayAlerts = $false
try {
    $xl.Workbooks.OpenText($csv, 65001, 1, 1, 1, $false, $false, $false, $true, $false, $false)
    $wb = $xl.ActiveWorkbook; $ws = $wb.Worksheets.Item(1)
    $last = $ws.Cells($ws.Rows.Count, 1).End(-4162).Row
    Write-Output "rows incl header: $last  (expect 6560)"
    Write-Output ("headers A..I: {0}" -f (2..9 | ForEach-Object { $ws.Cells(1,$_).Text }) -join ',')

    # J: the grouping variable, then frozen to values so the sort cannot break it
    $ws.Cells(1,10).Value2 = 'group'
    $ws.Range("J2:J$last").Formula = '=IF(H2>=50,"nongame","gaming")'
    $xl.Calculate()
    $ws.Range("J2:J$last").Value2 = $ws.Range("J2:J$last").Value2

    # sort the whole table by group so each group is one contiguous block
    $ws.Range("A1:J$last").Sort($ws.Range("J1"), 1, $null, $null, 1, $null, 1, 1) | Out-Null

    # find the boundary the supplement tells the reader to look for
    $gLast = 1
    for ($i = 2; $i -le $last; $i++) {
        if ($ws.Cells($i,10).Value2 -eq 'gaming') { $gLast = $i } else { break }
    }
    Write-Output "gaming block: rows 2..$gLast   nongame block: rows $($gLast+1)..$last"

    $G1 = "G2:G$gLast"; $G2 = "G$($gLast+1):G$last"
    $rows = @(
      @('n gaming',     "=COUNT($G1)"),
      @('n nongame',    "=COUNT($G2)"),
      @('mean gaming',  "=AVERAGE($G1)"),
      @('mean nongame', "=AVERAGE($G2)"),
      @('SD gaming',    "=STDEV.S($G1)"),
      @('SD nongame',   "=STDEV.S($G2)"),
      @('SE',           '=SQRT(M5^2/M1+M6^2/M2)'),
      @('t',            '=(M3-M4)/M7'),
      @('df',           '=(M5^2/M1+M6^2/M2)^2/((M5^2/M1)^2/(M1-1)+(M6^2/M2)^2/(M2-1))'),
      @('p (long)',     '=T.DIST.2T(ABS(M8),M9)'),
      @('pooled SD',    '=SQRT(((M1-1)*M5^2+(M2-1)*M6^2)/(M1+M2-2))'),
      @("Cohen's d",    '=(M3-M4)/M11'),
      @('p (T.TEST)',   "=T.TEST($G1,$G2,2,3)")
    )
    for ($i = 0; $i -lt $rows.Count; $i++) {
        $ws.Cells($i+1, 12).Value2  = $rows[$i][0]
        $ws.Cells($i+1, 13).Formula = $rows[$i][1]
    }
    $xl.CalculateFullRebuild()
    Write-Output ""
    for ($i = 1; $i -le $rows.Count; $i++) {
        Write-Output ("{0,-14} {1}" -f $ws.Cells($i,12).Value2, $ws.Cells($i,13).Value2)
    }
    $wb.Close($false)
} finally {
    $xl.Quit(); [System.Runtime.InteropServices.Marshal]::ReleaseComObject($xl) | Out-Null
}
