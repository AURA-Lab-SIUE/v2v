import os, re, glob

alt_text = {
    "01": "Abstract visualization of neural networks and brain science",
    "02": "Programming code displayed on a computer screen",
    "03": "Person writing in a research journal",
    "04": "Research documents and archival materials",
    "05": "Camera lens representing theoretical focus",
    "06": "Architectural blueprint representing research planning",
    "07": "Crossroads representing research decision points",
    "08": "Scales of justice representing research ethics",
    "09": "Collection of tools representing research methods",
    "10": "Group discussion representing focus group research",
    "11": "Clipboard with checklist representing survey design",
    "12": "Visual representation of cause and effect relationships",
    "13": "Live music concert representing media immersion",
    "14": "Measuring tools representing operationalization",
    "15": "Organized checklist representing codebook structure",
    "16": "Dice representing probability and random sampling",
    "17": "Neatly organized cables representing clean data",
    "18": "Data visualization chart on a screen",
    "19": "Magnifying glass representing statistical detection",
    "20": "Judge gavel representing making a research call",
    "21": "Professional portfolio document",
    "22": "Rocket launch representing going live with research",
}

for ch_num in range(1, 23):
    ch = f"{ch_num:02d}"
    qmd = f"chapter{ch}.qmd"
    if not os.path.exists(qmd):
        continue

    imgs = sorted(glob.glob(f"../images/ch{ch}-*.jpg"))
    if not imgs:
        continue

    with open(qmd, "r", encoding="utf-8") as f:
        lines = f.readlines()

    img_path = f"../images/{os.path.basename(imgs[0])}"
    alt = alt_text.get(ch, f"Chapter {ch_num} illustration")
    img_line = f'\n![{alt}]({img_path}){{fig-alt="{alt}"}}\n\n'

    # Strategy: find "## Learning Objectives", then find the next "---" after it,
    # and insert the image after that "---"
    in_lo = False
    found_lo = False
    inserted = False
    new_lines = []

    # First pass: find line numbers
    lo_start = -1
    separator_after_lo = -1

    for i, line in enumerate(lines):
        if "## Learning Objectives" in line:
            lo_start = i
        elif lo_start >= 0 and separator_after_lo < 0 and line.strip() == "---":
            separator_after_lo = i

    if separator_after_lo >= 0:
        # Insert after the separator
        for i, line in enumerate(lines):
            new_lines.append(line)
            if i == separator_after_lo and not inserted:
                new_lines.append(img_line)
                inserted = True
                print(f"  Ch {ch}: Inserted after line {i+1} (--- after Learning Objectives)")
    else:
        # Fallback: find first blank line after Learning Objectives list ends
        past_lo = False
        for i, line in enumerate(lines):
            new_lines.append(line)
            if "## Learning Objectives" in line:
                past_lo = True
            elif past_lo and not inserted and line.strip() == "" and i > lo_start + 3:
                # Find next non-list line
                if i + 1 < len(lines) and not lines[i+1].strip().startswith("-"):
                    new_lines.append(img_line)
                    inserted = True
                    print(f"  Ch {ch}: Inserted after line {i+1} (fallback)")

    if not inserted:
        print(f"  Ch {ch}: FAILED to find insertion point")
        new_lines = lines  # Don't modify

    with open(qmd, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

print("Done!")
