# Verify the Chapter 7 Excel supplement by doing what it tells the reader to do:
# build a PivotTable that averages words by sender, Grand Totals off, and another by channel, then
# average the pivot's own output. Expected from Python: 4.81 at message level,
# 4.22 at sender level, 4.97 at channel level.
$ErrorActionPreference = 'Stop'
$csv = 'O:\20-research\aura-lab\v2v\data-raw\v3\message_words.csv'
$xl = New-Object -ComObject Excel.Application
$xl.Visible = $false; $xl.DisplayAlerts = $false
try {
    $xl.Workbooks.OpenText($csv, 65001, 1, 1, 1, $false, $false, $false, $true, $false, $false)
    $wb = $xl.ActiveWorkbook
    $ws = $wb.Worksheets.Item(1)
    $last = $ws.Cells($ws.Rows.Count, 1).End(-4162).Row
    Write-Output "rows incl header: $last"
    Write-Output ("message-level mean: {0}" -f $xl.WorksheetFunction.Average($ws.Range("C2:C$last")))

    $src = $ws.Range("A1:C$last")
    foreach ($field in @('sender','channel')) {
        $sheet = $wb.Worksheets.Add()
        $sheet.Name = "pv_$field"
        $cache = $wb.PivotCaches().Create(1, $src)          # 1 = xlDatabase
        $pt = $cache.CreatePivotTable($sheet.Range("A3"), "pt_$field")
        # ColumnGrand controls the Grand Total ROW at the bottom (RowGrand is the
        # total COLUMN at the right). That row sits inside DataBodyRange and
        # silently biases an average of the averages.
        $pt.ColumnGrand = $false
        $pt.RowGrand = $false
        $pt.PivotFields($field).Orientation = 1             # 1 = xlRowField
        $df = $pt.AddDataField($pt.PivotFields('words'), "avg words", -4106)  # -4106 = xlAverage
        $xl.Calculate()
        $body = $pt.DataBodyRange
        $n = $body.Rows.Count
        $mean = $xl.WorksheetFunction.Average($body)
        Write-Output ("unit = {0,-8} pivot rows = {1,6}   average of the averages = {2}" -f $field, $n, $mean)
    }
    $wb.Close($false)
} finally {
    $xl.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($xl) | Out-Null
}
