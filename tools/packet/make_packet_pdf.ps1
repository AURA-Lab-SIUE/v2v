# Render the Undrah packet to a tagged, accessible PDF.
#
# Same pipeline as the canonical convert-to-pdf.ps1 (pandoc md -> DOCX -> Word COM
# ExportAsFixedFormat with DocStructureTags): pandoc + xelatex produces an UNTAGGED
# PDF, which is the documented failure this pipeline exists to prevent. One document,
# one Word process.
$ErrorActionPreference = "Stop"

$dir  = "C:\Users\alexl\AppData\Local\Temp\claude\C--pythia\911c8096-d1d3-4b3f-ab5c-0faea3c53a43\scratchpad\packet"
$md   = Join-Path $dir "undrah-packet-full.md"
$docx = Join-Path $dir "undrah-packet-full.docx"
$pdf  = Join-Path $dir "v2v-fourth-edition-overview.pdf"

function Set-WordDocProperty {
    param($Properties, [string]$Name, $Value)
    $binding = [System.Reflection.BindingFlags]::GetProperty
    $prop = [System.__ComObject].InvokeMember("Item", $binding, $null, $Properties, @($Name))
    $bindingSet = [System.Reflection.BindingFlags]::SetProperty
    [System.__ComObject].InvokeMember("Value", $bindingSet, $null, $prop, @($Value)) | Out-Null
}

& pandoc $md -o $docx --from markdown --to docx -s
if ($LASTEXITCODE -ne 0) { throw "pandoc failed" }
Write-Output "docx built: $((Get-Item $docx).Length) bytes"

$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
    $doc = $word.Documents.Open($docx, $false, $false)

    # Atkinson Hyperlegible across every style, per the course-material standard.
    # If the per-user font install has gone orphaned this silently leaves Word's
    # default, so the verification step below checks the embedded fonts.
    $font = "Atkinson Hyperlegible"
    # Code styles are EXCLUDED from the sweep. Applying the body font to them turned
    # every Excel formula into italic proportional text, which is unusable in a
    # supplement whose formulas a student retypes character by character.
    # Match on a normalized name: pandoc's style IDs are "VerbatimChar" and "SourceCode"
    # but Word may report the display name with a space, so compare without spaces.
    $codeKeys = @("verbatimchar", "sourcecode", "htmlcode", "macrotext", "verbatimstringtok")
    foreach ($style in $doc.Styles) {
        try {
            $key = ($style.NameLocal -replace '\s', '').ToLower()
            if ($codeKeys -contains $key) { continue }
            if ($style.Font.Name -ne $font) {
                $style.Font.Name = $font
                $style.Font.NameAscii = $font
                $style.Font.NameOther = $font
            }
        } catch {}
    }
    # NOTE: no blanket $doc.Content.Font.Name sweep here. It applies DIRECT character
    # formatting to every run, which beats style-based formatting and silently repainted
    # the Excel formulas out of Consolas. Pandoc's docx output is style-based, so the
    # style sweep above is sufficient.

    # Now force the code styles to a real monospace face, upright, after the sweep
    # (Content.Font.Name above repaints everything, so this has to come last).
    $codeFixed = 0
    foreach ($style in $doc.Styles) {
        try {
            $key = ($style.NameLocal -replace '\s', '').ToLower()
            if ($codeKeys -contains $key) {
                $style.Font.Name = "Consolas"
                $style.Font.NameAscii = "Consolas"
                $style.Font.NameOther = "Consolas"
                $style.Font.Italic = $false
                $style.Font.Size = 11
                $codeFixed++
            }
        } catch {}
    }
    Write-Output "code styles set to Consolas: $codeFixed"

    # Flatten the heading hierarchy: bold and italic carry level, not size jumps.
    $spec = @{
        "Heading 1" = @{ Size = 14; Bold = $true;  Italic = $false }
        "Heading 2" = @{ Size = 13; Bold = $true;  Italic = $false }
        "Heading 3" = @{ Size = 12; Bold = $true;  Italic = $true  }
        "Heading 4" = @{ Size = 12; Bold = $true;  Italic = $true  }
        "Heading 5" = @{ Size = 12; Bold = $false; Italic = $true  }
        "Heading 6" = @{ Size = 12; Bold = $true;  Italic = $false }
    }
    foreach ($n in $spec.Keys) {
        try {
            $s = $doc.Styles.Item($n)
            $s.Font.Size = $spec[$n].Size; $s.Font.Bold = $spec[$n].Bold; $s.Font.Italic = $spec[$n].Italic
        } catch {}
    }
    # Two lines short of a single page. Buy the room from paragraph spacing rather
    # than from the type size or the content: 10pt after -> 6pt across ~12 paragraphs.
    try {
        $nrm = $doc.Styles.Item("Normal")
        $nrm.ParagraphFormat.SpaceAfter = 6
        $nrm.ParagraphFormat.SpaceBefore = 0
    } catch {}

    # One-pager: body at 13pt per the printed one-pager font floor.
    try { $doc.Styles.Item("Normal").Font.Size = 13 } catch {}

    # Word's auto multilevel numbering on headings reads as arbitrary; strip it.
    try {
        foreach ($para in $doc.Paragraphs) {
            $sn = $null
            try { $sn = $para.Style.NameLocal } catch {}
            if ($sn -and $sn -match '^Heading\s+\d+$') { try { $para.Range.ListFormat.RemoveNumbers() } catch {} }
        }
    } catch {}

    # Word sets KeepWithNext on heading styles by default, which chains a heading to
    # the block under it and shunts the whole group to the next page even when there
    # is most of a page free. That is what pushed the final section over, with 116pt
    # of page 1 still empty, so it is switched off here.
    # Setting this on the STYLE does not take, because pandoc writes the property
    # onto each paragraph directly, and direct formatting wins. Clear it per paragraph.
    $kept = 0
    foreach ($para in $doc.Paragraphs) {
        try {
            $pf = $para.Format
            if ($pf.KeepWithNext -ne 0) { $pf.KeepWithNext = $false; $kept++ }
            $pf.KeepTogether    = $false
            $pf.PageBreakBefore = $false
            # Paragraph spacing is written per-paragraph by pandoc too, so setting it
            # on the Normal style alone does nothing. Same trap as KeepWithNext above.
            $pf.SpaceAfter  = 6
            $pf.SpaceBefore = 0
        } catch {}
    }
    Write-Output "KeepWithNext cleared on $kept paragraph(s)"

    # Keep it to a single page without dropping below the one-pager font floor:
    # buy the room from the margins (0.8in) rather than from the type.
    try {
        $doc.PageSetup.TopMargin    = 0.8 * 72
        $doc.PageSetup.BottomMargin = 0.8 * 72
        $doc.PageSetup.LeftMargin   = 0.9 * 72
        $doc.PageSetup.RightMargin  = 0.9 * 72
    } catch {}

    $props = $doc.BuiltInDocumentProperties
    Set-WordDocProperty -Properties $props -Name "Title"   -Value "Vibes to Variables, fourth edition: an overview for MC 451"
    Set-WordDocProperty -Properties $props -Name "Author"  -Value "Dr. Alex P. Leith"
    Set-WordDocProperty -Properties $props -Name "Subject" -Value "Communication research methods textbook, fourth edition overview and samples"
    Set-WordDocProperty -Properties $props -Name "Company" -Value "Southern Illinois University Edwardsville"

    $doc.ExportAsFixedFormat($pdf, 17, $false, 1, 0, 1, 1, 0, $true, $true, 0, $true, $true, $false)
    $doc.Close($false)
    Write-Output "pdf built: $((Get-Item $pdf).Length) bytes"
} finally {
    $word.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
}
