import os, re, glob

img_dir = "../images"
ch_dir = "."

# Alt text descriptions for each chapter's images
alt_text = {
    "01": {
        "brain": "Abstract visualization of neural networks and brain science",
        "curiosity": "Person exploring with curiosity and wonder"
    },
    "02": {
        "code": "Programming code displayed on a computer screen",
        "infrastructure": "Server room representing research infrastructure"
    },
    "03": {
        "journal": "Person writing in a research journal",
        "library": "Library stacks filled with academic books"
    },
    "04": {
        "archive": "Research documents and archival materials",
        "search": "Searching a database on a computer"
    },
    "05": {
        "lens": "Camera lens representing theoretical focus",
        "microscope": "Microscope in a science laboratory"
    },
    "06": {
        "blueprint": "Architectural blueprint representing research planning",
        "map": "Navigation map representing research roadmap"
    },
    "07": {
        "crossroads": "Crossroads representing research decision points",
        "question": "Question mark representing inquiry"
    },
    "08": {
        "justice": "Scales of justice representing research ethics",
        "protection": "Shield representing participant protection"
    },
    "09": {
        "toolkit": "Collection of tools representing research methods",
        "versatile": "Swiss army knife representing methodological versatility"
    },
    "10": {
        "focus-group": "Group discussion representing focus group research",
        "interview": "Two people in conversation representing in-depth interview"
    },
    "11": {
        "checklist": "Clipboard with checklist representing survey design",
        "survey": "Person completing a survey questionnaire"
    },
    "12": {
        "cause-effect": "Visual representation of cause and effect relationships",
        "laboratory": "Scientific laboratory representing controlled experiments"
    },
    "13": {
        "concert": "Live music concert representing media immersion",
        "headphones": "Person listening to music with headphones",
        "vinyl": "Vinyl record on a turntable"
    },
    "14": {
        "measuring": "Measuring tools representing operationalization",
        "spectrum": "Color spectrum representing measurement scales",
        "transform": "Abstract transformation representing concept to variable"
    },
    "15": {
        "checklist": "Organized checklist representing codebook structure",
        "rulebook": "Reference manual representing coding rules"
    },
    "16": {
        "dice": "Dice representing probability and random sampling",
        "random": "Random selection representing sampling methods",
        "selection": "Selection process representing choosing a sample"
    },
    "17": {
        "clean": "Neatly organized cables representing clean data",
        "tangled": "Tangled messy cables representing raw data"
    },
    "18": {
        "chart": "Data visualization chart on a screen",
        "dashboard": "Analytics dashboard displaying data patterns",
        "natural-pattern": "Natural pattern representing pattern recognition"
    },
    "19": {
        "magnifying": "Magnifying glass representing statistical detection",
        "surprise": "Surprised expression representing unexpected findings"
    },
    "20": {
        "gavel": "Judge gavel representing making a research call",
        "thinking": "Person thinking deeply about interpretation"
    },
    "21": {
        "portfolio": "Professional portfolio document",
        "website": "Laptop displaying a website design"
    },
    "22": {
        "rocket": "Rocket launch representing going live with research",
        "sharing": "People collaborating and sharing work"
    }
}

for ch_num in range(1, 23):
    ch = f"{ch_num:02d}"
    qmd = os.path.join(ch_dir, f"chapter{ch}.qmd")
    if not os.path.exists(qmd):
        continue

    imgs = sorted(glob.glob(os.path.join("../images", f"ch{ch}-*.jpg")))
    if not imgs:
        continue

    with open(qmd, "r", encoding="utf-8") as f:
        content = f.read()

    # Find the first image and insert after the first "---" separator after learning objectives
    first_img = imgs[0]
    img_basename = os.path.basename(first_img)

    # Extract the descriptor from filename (e.g., "brain" from "ch01-brain_2.jpg")
    descriptor = re.search(r"ch\d+-(.+?)_", img_basename)
    if descriptor:
        desc_key = descriptor.group(1)
    else:
        desc_key = "image"

    # Get alt text
    chapter_alts = alt_text.get(ch, {})
    alt = chapter_alts.get(desc_key, f"Chapter {ch_num} illustration")

    # Build the image markdown
    img_md = f'\n![{alt}](../images/{img_basename}){{fig-alt="{alt}" width="100%"}}\n'

    # Insert after the first "---" that follows "Learning Objectives"
    lo_match = re.search(r"(## Learning Objectives.*?)(---)", content, re.DOTALL)
    if lo_match:
        insert_pos = lo_match.end()
        content = content[:insert_pos] + img_md + content[insert_pos:]
        print(f"  Ch {ch}: Inserted {img_basename} after Learning Objectives")
    else:
        # Fallback: insert after first ---
        first_sep = content.find("---", content.find("---") + 3)
        if first_sep > 0:
            content = content[:first_sep + 3] + img_md + content[first_sep + 3:]
            print(f"  Ch {ch}: Inserted {img_basename} after first separator")

    with open(qmd, "w", encoding="utf-8") as f:
        f.write(content)

print("Done!")
