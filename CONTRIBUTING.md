# Contributing to From Vibes to Variables

Thank you for helping improve this open textbook! This document explains
how to report errors, suggest improvements, and contribute content.

## Reporting Typos and Errors

If you spot a typo, broken link, or factual error, please
[open an issue](https://github.com/SIM-Lab-SIUE/vibes-to-variables/issues/new)
on GitHub. Include:

- The chapter number and section where you found the error
- What the text currently says
- What it should say (if you know)

## Suggesting Content Improvements

Ideas for new examples, better explanations, or additional exercises
are welcome. Open a
[GitHub issue](https://github.com/SIM-Lab-SIUE/vibes-to-variables/issues/new)
describing your suggestion and which chapter it relates to.

## Contributing Edits

### Building Locally

To preview your changes before submitting:

1. **Clone** the repository:
   ```bash
   git clone https://github.com/SIM-Lab-SIUE/vibes-to-variables.git
   cd vibes-to-variables
   ```

2. **Install prerequisites**:
   - [Quarto](https://quarto.org/docs/get-started/) (v1.3 or later)
   - [R](https://cran.r-project.org/) (>= 4.1)
   - R packages:
     ```r
     install.packages(c("knitr", "rmarkdown", "tidyverse",
                        "kableExtra", "rcompanion"))
     ```

3. **Render the book**:
   ```bash
   quarto render
   ```
   Open `docs/index.html` to preview.

### Style Guide

When editing or writing content, follow these conventions:

**Chapter structure:**
- Each chapter is a single `.qmd` file in `chapters/`
- Chapters begin with a level-1 heading (`#`) that serves as the title
- Use level-2 headings (`##`) for major sections and level-3 (`###`)
  for subsections

**Callout boxes:**
Use Quarto callout blocks for tips, warnings, and key concepts:
```markdown
::: {.callout-tip}
## Tip Title
Content here.
:::

::: {.callout-warning}
## Warning Title
Content here.
:::

::: {.callout-note}
## Note Title
Content here.
:::
```

**Code blocks:**
- Use ```` ```r ```` for R code that readers should run
- Use ```` ```{{r}} ```` (double curly braces) for R code that is shown
  as a display example only and should **not** be executed during rendering
- Include comments in code blocks to explain each step

**Cross-references:**
- Link to other chapters with relative paths:
  `[Chapter 5](chapter05.qmd)`
- Link to the data dictionary appendix:
  `[Data Dictionary](../appendices/data-dictionary.qmd)`

**Images:**
- Place images in a chapter-specific subfolder if needed
- Include alt text for accessibility: `![Alt text](path/to/image.png)`

### Submitting Changes

1. **Fork** the repository on GitHub.
2. **Create a branch**: `git checkout -b fix/chapter-03-typo`
3. **Make your edits**.
4. **Render locally** to verify: `quarto render`
5. **Commit and push**:
   ```bash
   git add -A
   git commit -m "Fix typo in chapter 3"
   git push origin fix/chapter-03-typo
   ```
6. **Open a pull request** against the `main` branch.

## License

By contributing, you agree that your contributions will be licensed
under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/),
the same license as the rest of the book.

## Questions?

Open an issue or contact the author at aleith@siue.edu.
