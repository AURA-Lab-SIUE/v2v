# Final verification for the Chapter 19 supplement.
#
# Two Excel behaviours drive the whole supplement and both are demonstrated here:
#   1. COUNTIF is case-INsensitive, so it cannot separate LUL from lul.
#      FIND is case-sensitive, so SUMPRODUCT(--ISNUMBER(FIND(...))) can.
#   2. Messages beginning with = + or - are EVALUATED AS FORMULAS on a plain
#      import, yielding #NAME? cells that poison any SUM or SUMPRODUCT over the
#      column. COUNTIF survives them; SUMPRODUCT does not. Hence IFERROR.
#
# Expected from Python (case-sensitive, whole space-delimited token):
#   LUL 6449, LULW 1326, OMEGALUL 1041, 4Head 426, Pog 2008, PogChamp 1242
#   LUL substring (case-insensitive) 9716
#   !play 855 exact; !-prefixed 5529; dev1 1000 messages, 449 !play
# NOTE on the 1-2 message gaps below. This script uses OpenText, which EVALUATES
# 18 messages as formulas and turns them into errors; one of them carries a LUL
# token, one an OMEGALUL, and two a lowercase lul. The supplement tells the reader
# to import through Data > From Text/CSV (Power Query), which imports them as text
# and so returns the Python figures above. Both behaviours are the point of Ch 24.
$ErrorActionPreference = 'Stop'
$dir = 'O:\20-research\aura-lab\v2v\data-raw\v3'
$xl = New-Object -ComObject Excel.Application
$xl.Visible = $false; $xl.DisplayAlerts = $false
try {
    $fmt = @(@(1,2),@(2,2),@(3,2),@(4,2),@(5,2))
    $xl.Workbooks.OpenText((Join-Path $dir 'twitch_chat_sample.csv'), 65001, 1, 1, 1, $false, $false, $false, $true, $false, $false, $fmt)
    $wb = $xl.ActiveWorkbook; $ws = $wb.Worksheets.Item(1)
    $last = $ws.Cells($ws.Rows.Count,1).End(-4162).Row

    $ws.Cells(1,6).Value2 = 'padded'
    $ws.Range("F2:F$last").Formula = '=IFERROR(" "&D2&" ","")'
    $ws.Cells(1,7).Value2 = 'is_play'
    $ws.Range("G2:G$last").Formula = '=IFERROR(--EXACT(TRIM(D2),"!play"),0)'
    $ws.Cells(1,8).Value2 = 'is_error'
    $ws.Range("H2:H$last").Formula = '=--ISERROR(D2)'
    $xl.Calculate()

    $out = @(
      @('cells that became formula errors', "=SUM(H2:H$last)"),
      @('LUL   case-sensitive token',  "=SUMPRODUCT(--ISNUMBER(FIND("" LUL "",F2:F$last)))"),
      @('LULW  case-sensitive token',  "=SUMPRODUCT(--ISNUMBER(FIND("" LULW "",F2:F$last)))"),
      @('OMEGALUL case-sensitive',     "=SUMPRODUCT(--ISNUMBER(FIND("" OMEGALUL "",F2:F$last)))"),
      @('4Head case-sensitive',        "=SUMPRODUCT(--ISNUMBER(FIND("" 4Head "",F2:F$last)))"),
      @('Pog   case-sensitive token',  "=SUMPRODUCT(--ISNUMBER(FIND("" Pog "",F2:F$last)))"),
      @('PogChamp case-sensitive',     "=SUMPRODUCT(--ISNUMBER(FIND("" PogChamp "",F2:F$last)))"),
      @('LUL substring COUNTIF (ci)',  "=COUNTIF(D2:D$last,""*LUL*"")"),
      @('!play exact case-sensitive',  "=SUM(G2:G$last)"),
      @('!play COUNTIF (ci)',          "=COUNTIF(D2:D$last,""!play"")"),
      @('messages starting with !',    "=COUNTIF(D2:D$last,""!*"")"),
      @('dev1 messages',               "=COUNTIF(B2:B$last,""dev1"")"),
      @('dev1 !play',                  "=SUMIFS(G2:G$last,B2:B$last,""dev1"")")
    )
    for ($i=0; $i -lt $out.Count; $i++) {
        $ws.Cells($i+1,11).Value2  = $out[$i][0]
        $ws.Cells($i+1,12).Formula = $out[$i][1]
    }
    $xl.Calculate()
    Write-Output ""
    for ($i=1; $i -le $out.Count; $i++) {
        Write-Output ("{0,-34}{1,9}" -f $ws.Cells($i,11).Value2, $ws.Cells($i,12).Value2)
    }
    $wb.Close($false)
} finally { $xl.Quit(); [System.Runtime.InteropServices.Marshal]::ReleaseComObject($xl) | Out-Null }
