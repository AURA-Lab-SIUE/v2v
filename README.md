# V2V (Vibes to Variables)

*A Methods Package for Students New to Research, Stats, and Code. Third Edition.*

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Quarto Book](https://img.shields.io/badge/Built_with-Quarto-blue)](https://quarto.org)

V2V is an open educational resource that teaches communication and media research methods as a complete arc, from the first spark of curiosity to a published, reproducible study. V2V is a methods package, not a textbook with bonuses: the book in this repository is one of several co-equal components alongside the V2V Hub (course site), the `v2v` R package (friction-reducing helpers), and the *Beyond Vibes* graduate supplement.

**Read online:** <https://aura-lab-siue.github.io/v2v/>

**Author:** Alex P. Leith, Southern Illinois University Edwardsville

**Courses:** MC 451 Social Media Analytics (undergraduate); MC 500 + MC 501 Research Methods (graduate, via *Beyond Vibes*)

---

## Table of Contents

The 3rd Edition is organized into 14 chapters across five parts. (Chapters 1 through 6 are drafted; chapters 7 through 14 are stubs at this release and land progressively through Summer and Fall 2026.)

### Part I: Foundation
1. The Science of Storytelling
2. The Open Workspace
3. Knowing and Knowing Well

### Part II: Planning
4. Intelligence Gathering
5. Theory as a Lens
6. The Prospectus

### Part III: Operationalization
7. Structured Listening *(in development)*
8. From Vibes to Variables *(in development)*
9. The Rulebook and First Workspace *(in development)*

### Part IV: Execution
10. The Sample *(in development)*
11. Wrangling the Data *(in development)*
12. Visualizing the Narrative *(in development)*

### Part V: Inference and Publication
13. Making the Call *(in development)*
14. The One-Click Report *(in development)*

### Appendices
- Data Dictionary: variable reference for the V2V working datasets

### V2V 2nd Edition (archived)

The 2nd Edition's 22-chapter structure (music dataset, R introduced in Chapter 2) is preserved in `chapters/_archive-v2/` as a transitional reference and remains available for instructors transitioning from the 2nd Edition.

---

## What's New in the Third Edition (V2V)

The third edition consolidates the prior *From Vibes to Variables* textbook with the surrounding course infrastructure under one unified V2V brand. Major v2 to v3 changes:

- **V2V umbrella branding** across the book, course site, R package, and graduate supplement. The textbook is one co-equal component of a methods package, not a textbook with bonuses.
- **Dual-profile build** producing distinct undergraduate and graduate editions from one source. Render with `quarto render --profile undergrad` or `--profile grad`; outputs land in `docs/undergrad/` and `docs/grad/` respectively. Audience-level profile names keep V2V adoptable as an OER outside SIUE.
- **Beyond Vibes graduate supplement** (in progress): the MC 501 edition adds power analysis, pre-registration discipline, two-coder reliability planning, and an audit-trail layer on top of the undergraduate foundation, satisfying the SIUE 33 percent cross-listing differential.
- **`coursepackR` rebrand to `v2v`** (in progress): the R package is being renamed to match the umbrella brand.
- **Open Methods Hub fold-in to V2V Hub** (in progress): the prior `liaison-program` course site is being consolidated under the V2V Hub identifier.
- **Planned dataset migration**: chapter examples will move from the music dataset to a Twitch chat and stream-metadata corpus, better serving the MC 451 Social Media Analytics course. The migration ships chapter by chapter; the music dataset remains canonical until each chapter is updated.

The 2nd Edition's 22-chapter content (research ethics, the methods landscape, qualitative methods, survey design, experimental design, the music dataset throughout) is preserved at `chapters/_archive-v2/` as a transitional reference. Pedagogical material from the 2nd Edition's expansion will be re-integrated into the 3rd Edition's 14-chapter structure as chapters 7 through 14 are drafted through Summer and Fall 2026.

---

## How to Read

### Online (recommended)

Visit <https://aura-lab-siue.github.io/v2v/> for the full HTML book with search, navigation, and interactive code examples.

### Offline via the v2v R package

If you have the [`v2v`](https://github.com/AURA-Lab-SIUE/v2v-r) R package installed, the bundled chapters (3rd Edition drafted + 2nd Edition archive) are available for offline access:

```r
# Path to a specific chapter
system.file("textbook", "chapter01.md", package = "v2v")
```

### PDF

A PDF version can be generated locally (see "Building Locally" below).

---

## Building Locally

### Prerequisites

- [Quarto](https://quarto.org/docs/get-started/) (v1.3 or later)
- [R](https://cran.r-project.org/) (>= 4.1): required for chapters with R code examples
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

Throughout the book, examples currently use the `unified_music` dataset, 1,792 songs combining Billboard chart performance, Spotify audio features, and Genius metadata. The dataset is bundled in the [v2v](https://github.com/AURA-Lab-SIUE/v2v) R package:

```r
library(v2v)
data(unified_music)
```

See the [Data Dictionary appendix](https://aura-lab-siue.github.io/v2v/appendices/data-dictionary.html) for the full variable reference.

The third-edition migration will move chapter examples to a Twitch chat and stream-metadata corpus to better serve the MC 451 Social Media Analytics course. That migration ships chapter by chapter through Summer and Fall 2026; the music dataset remains canonical until each chapter is updated.

---

## V2V Package Components

V2V is a methods package; the book is one of several co-equal components.

| Component | Description | Link |
|---------|-------------|------|
| **V2V Hub** | Course site wrapping the book: syllabus, R workbook (with videos), course workspace, setup guides, cheat sheets, datasets, references, instructor materials. Currently hosted under the legacy `liaison-program` identifier; consolidation under the V2V Hub identifier is in progress. | [Visit Site](https://aura-lab-siue.github.io/v2v-hub/) \| [GitHub](https://github.com/AURA-Lab-SIUE/v2v-hub) |
| **`v2v` R package** | R helpers, the `unified_music` dataset, weekly templates, and the planned Twitch corpus. Rebrand from `coursepackR` is in progress. | [Docs](https://github.com/AURA-Lab-SIUE/v2v-r/) \| [GitHub](https://github.com/AURA-Lab-SIUE/v2v-r) |
| **Beyond Vibes** (in progress) | Graduate supplement; produces a publishable white paper and conference poster. SIUE deployment pairs it with MC 500 in the MC 501 cohort. | Renders from this repository via `quarto render --profile grad`. |

---

## License

This work is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).

## Citation

> Leith, A. P. (2026). *Vibes to Variables: A Methods Package for Students New to Research, Stats, and Code* (3rd ed.). Southern Illinois University Edwardsville. <https://aura-lab-siue.github.io/v2v/>
