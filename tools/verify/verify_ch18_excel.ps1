# Verify the Chapter 18 supplement: the coverage diagnostics over the real hourly
# rhythm. Expected from Python: total 178,792; evening schedule {0,22,23} = 12.5% of
# the clock but 20.4% of activity; spread {2,7,11,15,19,23} = 25% of clock, 24.6%.
$ErrorActionPreference = 'Stop'
$dir = 'C:\Users\alexl\AppData\Local\Temp\claude\C--pythia\911c8096-d1d3-4b3f-ab5c-0faea3c53a43\scratchpad'
$xl = New-Object -ComObject Excel.Application
$xl.Visible = $false; $xl.DisplayAlerts = $false
try {
    $wb = $xl.Workbooks.Open((Join-Path $dir 'coverage.csv'))
    $ws = $wb.Worksheets.Item(1)
    $last = $ws.Cells($ws.Rows.Count, 1).End(-4162).Row
    Write-Output "rows incl header: $last"

    $ws.Cells(1,4).Value2 = 'observed'
    $ws.Cells(1,6).Value2 = 'metric'; $ws.Cells(1,7).Value2 = 'value'
    $ws.Cells(2,6).Value2 = 'hours_observed'; $ws.Cells(2,7).Formula = "=SUM(D2:D$last)"
    $ws.Cells(3,6).Value2 = 'share_of_clock'; $ws.Cells(3,7).Formula = "=SUM(D2:D$last)/24"
    $ws.Cells(4,6).Value2 = 'share_of_activity'
    $ws.Cells(4,7).Formula = "=SUMPRODUCT(C2:C$last,D2:D$last)/SUM(C2:C$last)"
    $ws.Cells(5,6).Value2 = 'total_activity'; $ws.Cells(5,7).Formula = "=SUM(C2:C$last)"
    $ws.Cells(6,6).Value2 = 'busiest_hour'
    $ws.Cells(6,7).Formula = "=INDEX(A2:A$last,MATCH(MAX(C2:C$last),C2:C$last,0))"
    $ws.Cells(7,6).Value2 = 'quietest_hour'
    $ws.Cells(7,7).Formula = "=INDEX(A2:A$last,MATCH(MIN(C2:C$last),C2:C$last,0))"
    $ws.Cells(8,6).Value2 = 'peak_trough_ratio'
    $ws.Cells(8,7).Formula = "=MAX(C2:C$last)/MIN(C2:C$last)"
    $xl.Calculate()
    Write-Output ("total activity   : {0}" -f $ws.Cells(5,7).Value2)
    Write-Output ("busiest hour UTC : {0}" -f $ws.Cells(6,7).Value2)
    Write-Output ("quietest hour UTC: {0}" -f $ws.Cells(7,7).Value2)
    Write-Output ("peak/trough ratio: {0:N2}" -f $ws.Cells(8,7).Value2)

    function Test-Schedule($hours, $label) {
        $ws.Range("D2:D$last").Value2 = 0
        foreach ($h in $hours) { $ws.Cells($h + 2, 4).Value2 = 1 }   # hour 0 sits in row 2
        $xl.Calculate()
        Write-Output ("`n{0}: hours={1}  clock={2:P1}  activity={3:P1}" -f `
            $label, $ws.Cells(2,7).Value2, $ws.Cells(3,7).Value2, $ws.Cells(4,7).Value2)
    }
    Test-Schedule @(0,22,23) 'evenings only {0,22,23}'
    Test-Schedule @(2,7,11,15,19,23) 'spread {2,7,11,15,19,23}'
    $wb.Close($false)
} finally {
    $xl.Quit(); [System.Runtime.InteropServices.Marshal]::ReleaseComObject($xl) | Out-Null
}
