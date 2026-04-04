# From Vibes to Variables

*A Field Guide to Open Media Science — Second Edition*

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Quarto Book](https://img.shields.io/badge/Built_with-Quarto-blue)](https://quarto.org)

An open educational resource (OER) that guides students through the complete arc of a research project — from the first spark of curiosity to a published, reproducible study. Written for undergraduates and graduate students in communication and media studies, it uses a real music industry dataset of 1,792 songs to teach research methods as structured storytelling.

**Read online:** <https://sim-lab-siue.github.io/vibes-to-variables/>

**Author:** Alex P. Leith, Southern Illinois University Edwardsville

**Course:** MC-451 Research Methods in Mass Media

---

## Table of Contents

The book is organized into five parts across 22 chapters:

### Part I: Foundations
1. The Architecture of Curiosity
2. The Infrastructure of Trust
3. The Reading Journal Protocol

### Part II: Design
4. The Archivist
5. Choosing Your Lens
6. The Roadmap
7. The Research Question
8. The Ethics of Inquiry

### Part III: Methods
9. The Methodologist's Toolkit
10. Qualitative Methods
11. Designing Surveys
12. Designing Experiments
13. Music Immersion
14. Vibes to Variables
15. The Rulebook
16. The Sampling Plan and Pilot Test

### Part IV: Analysis
17. Wrangling the Chaos
18. Seeing Patterns
19. The Surprise Detector
20. Interpreting the Call

### Part V: Publishing
21. The Portfolio
22. Going Live

### Appendices
- Data Dictionary — Complete variable reference for the unified music dataset

---

## What's New in the Second Edition

The second edition expands from 17 to 22 chapters, adding:

- **Research ethics** (Ch 8) — Belmont Report, IRB, ethics of analyzing public digital content
- **Methods landscape** (Ch 9) — where content analysis fits alongside surveys, experiments, and qualitative research
- **Qualitative methods** (Ch 10) — interviews, focus groups, thematic analysis as standalone approaches
- **Survey design** (Ch 11) — questionnaire construction, sampling theory, and validity
- **Experimental design** (Ch 12) — causation, control groups, and threats to validity

Every chapter now includes graduate extensions with assigned readings and advanced prompts, non-music examples from news, social media, and political communication, and verified citations throughout.

---

## How to Read

### Online (recommended)

Visit <https://sim-lab-siue.github.io/vibes-to-variables/> for the full HTML book with search, navigation, and interactive code examples.

### Offline via coursepackR

If you have the [`coursepackR`](https://github.com/SIM-Lab-SIUE/coursepackR) R package installed, all 22 chapters are bundled for offline access:

```r
# Path to a specific chapter
system.file("textbook", "chapter01.md", package = "coursepackR")
```

### PDF

A PDF version can be generated locally (see "Building Locally" below).

---

## Building Locally

### Prerequisites

- [Quarto](https://quarto.org/docs/get-started/) (v1.3 or later)
- [R](https://cran.r-project.org/) (>= 4.1) — required for chapters with R code examples
- R packages: `knitr`, `rmarkdown`, `tidyverse`, `kableExtra`, `rcompanion`

### Render the HTML book

```bash
quarto render
```

Output goes to `docs/`. Open `docs/index.html` in your browser.

### Render a PDF

```bash
quarto render --to pdf
```

This requires a LaTeX distribution (TinyTeX recommended: `quarto install tinytex`).

---

## The Dataset

Throughout the book, examples use the `unified_music` dataset — 1,792 songs combining Billboard chart performance, Spotify audio features, and Genius metadata. The dataset is bundled in the [coursepackR](https://github.com/SIM-Lab-SIUE/coursepackR) package:

```r
library(coursepackR)
data(unified_music)
```

See the [Data Dictionary appendix](https://sim-lab-siue.github.io/vibes-to-variables/appendices/data-dictionary.html) for the full variable reference.

---

## Related Projects

| Project | Description | Link |
|---------|-------------|------|
| **Open Methods Hub** | Course website — syllabus, R workbook (with videos), Methods Vault, setup guides | [Visit Site](https://sim-lab-siue.github.io/liaison-program/) \| [GitHub](https://github.com/SIM-Lab-SIUE/liaison-program) |
| **coursepackR** | R package — helper functions, `unified_music` dataset, weekly templates | [Docs](https://sim-lab-siue.github.io/coursepackR/) \| [GitHub](https://github.com/SIM-Lab-SIUE/coursepackR) |

---

## License

This work is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).

## Citation

> Leith, A. P. (2026). *From Vibes to Variables: A Field Guide to Open Media Science* (2nd ed.). Southern Illinois University Edwardsville. <https://sim-lab-siue.github.io/vibes-to-variables/>
