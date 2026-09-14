# Verify the Chapter 20 supplement: find each addressee's next turn with MINIFS,
# then the gap in turns and in seconds.
# Expected from Python (channel rdulive, 1000 turns):
#   174 addressed; 57 never speak again; 117 do
#   gap median 35, mean 111.7, next-turn 9 (7.7%), within 5 = 23.1%
#   seconds median 954
$ErrorActionPreference = 'Stop'
$dir = 'C:\Users\alexl\AppData\Local\Temp\claude\C--pythia\911c8096-d1d3-4b3f-ab5c-0faea3c53a43\scratchpad'
$xl = New-Object -ComObject Excel.Application
$xl.Visible = $false; $xl.DisplayAlerts = $false
try {
    $fmt = @(@(1,1),@(2,2),@(3,2),@(4,1))   # turn numeric, sender/addressed TEXT, ts numeric
    $xl.Workbooks.OpenText((Join-Path $dir 'adjacency.csv'), 65001, 1, 1, 1, $false, $false, $false, $true, $false, $false, $fmt)
    $wb = $xl.ActiveWorkbook; $ws = $wb.Worksheets.Item(1)
    $last = $ws.Cells($ws.Rows.Count,1).End(-4162).Row
    Write-Output "rows incl header: $last"

    $ws.Cells(1,6).Value2 = 'next_turn'
    $ws.Cells(1,7).Value2 = 'gap_turns'
    $ws.Cells(1,8).Value2 = 'gap_secs'
    # MINIFS returns 0 when nothing matches, NOT an error, so IFERROR never fires and
    # the zero flows into the arithmetic as a negative gap. Test for 0 explicitly.
    $ws.Range("F2:F$last").Formula = "=IF(C2="""","""",IF(MINIFS(`$A`$2:`$A`$$last,`$B`$2:`$B`$$last,C2,`$A`$2:`$A`$$last,"">""&A2)=0,""none"",MINIFS(`$A`$2:`$A`$$last,`$B`$2:`$B`$$last,C2,`$A`$2:`$A`$$last,"">""&A2)))"
    $ws.Range("G2:G$last").Formula = '=IF(OR(F2="",F2="none"),"",F2-A2)'
    $ws.Range("H2:H$last").Formula = "=IF(OR(F2="""",F2=""none""),"""",(INDEX(`$D`$2:`$D`$$last,MATCH(F2,`$A`$2:`$A`$$last,0))-D2)/1000)"
    $xl.Calculate()

    $out = @(
      @('turns',                  "=COUNT(A2:A$last)"),
      @('addressed messages',     "=COUNTIF(C2:C$last,""?*"")"),
      @('addressee never returns',"=COUNTIF(F2:F$last,""none"")"),
      @('gaps measured',          "=COUNT(G2:G$last)"),
      @('gap median',             "=MEDIAN(G2:G$last)"),
      @('gap mean',               "=AVERAGE(G2:G$last)"),
      @('gap max',                "=MAX(G2:G$last)"),
      @('reply is next turn',     "=COUNTIF(G2:G$last,1)"),
      @('within 5 turns',         "=COUNTIF(G2:G$last,""<=5"")"),
      @('seconds median',         "=MEDIAN(H2:H$last)")
    )
    for ($i=0; $i -lt $out.Count; $i++) {
        $ws.Cells($i+1,10).Value2  = $out[$i][0]
        $ws.Cells($i+1,11).Formula = $out[$i][1]
    }
    $xl.Calculate()
    Write-Output ""
    for ($i=1; $i -le $out.Count; $i++) {
        Write-Output ("{0,-26}{1,10}" -f $ws.Cells($i,10).Value2, $ws.Cells($i,11).Value2)
    }
    $wb.Close($false)
} finally { $xl.Quit(); [System.Runtime.InteropServices.Marshal]::ReleaseComObject($xl) | Out-Null }
