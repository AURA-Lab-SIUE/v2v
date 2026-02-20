# From Vibes to Variables

*A Field Guide to Open Media Science*

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Quarto Book](https://img.shields.io/badge/Built_with-Quarto-blue)](https://quarto.org)

An open educational resource (OER) that guides students through the complete arc of a research project — from the first spark of curiosity to a published, reproducible study. Written for undergraduates in communication and media studies, it uses a real music industry dataset of 1,792 songs to teach research methods as structured storytelling.

**Read online:** <https://sim-lab-siue.github.io/vibes-to-variables/>

**Author:** Alex P. Leith, Southern Illinois University Edwardsville

**Course:** MC-451 Research Methods

---

## Table of Contents

The book is organized into five parts that mirror the phases of a research project:

### Part I: Foundations
1. The Architecture of Curiosity
2. The Infrastructure of Trust
3. The Reading Journal Protocol
4. The Archivist

### Part II: Design
5. Choosing Your Lens
6. The Roadmap
7. The Research Question

### Part III: Measurement
8. The Music Immersion
9. Vibes to Variables
10. The Rulebook
11. The Pilot Test

### Part IV: Analysis
12. Wrangling the Chaos
13. Seeing Patterns
14. The Surprise Detector
15. Interpreting the Call

### Part V: Communication
16. The Portfolio
17. Going Live

### Appendices
- Data Dictionary — Complete variable reference for the unified music dataset

---

## How to Read

### Online (recommended)

Visit <https://sim-lab-siue.github.io/vibes-to-variables/> for the full HTML book with search, navigation, and interactive code examples.

### Offline via coursepackR

If you have the [`coursepackR`](https://github.com/SIM-Lab-SIUE/coursepackR) R package installed, all 17 chapters are bundled for offline access:

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

This requires a LaTeX distribution (TinyTeX recommended: `quarto install tinytex`). The PDF is written to `docs/From-Vibes-to-Variables.pdf`.

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
| **coursepackR** | R package with helper functions, dataset, and weekly templates | [GitHub](https://github.com/SIM-Lab-SIUE/coursepackR) |
| **liaison-program** | Course support website with syllabus, setup guides, and resources | [GitHub](https://github.com/SIM-Lab-SIUE/liaison-program) |

---

## License

This work is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).

You are free to share and adapt this material for any purpose, including commercially, as long as you give appropriate credit.

## Citation

> Leith, A. P. (2026). *From Vibes to Variables: A Field Guide to Open Media Science*. Southern Illinois University Edwardsville. <https://sim-lab-siue.github.io/vibes-to-variables/>
