# Figures — registry, coverage, and identified gaps

Audited 2026-07-23 against `redesign/unify-2026-07`.

## How figures are made

**One command, from the book root:**

```
Rscript figures/render-all.R          # every figure
Rscript figures/render-all.R ch12     # one chapter
```

`figures/render-all.R` is the single source of every data figure. It builds the ch11
`analysis` table once, asserts the counts the prose quotes (`is_gaming` FALSE 3457 /
TRUE 31309 / NA 501) so figures and text cannot silently diverge, renders from the
registry, and finishes with an alt-text coverage check.

Before this existed, figures were rendered by ad-hoc scripts on the ThinkBook that
loaded the package with `devtools::load_all()` from a **temp scratchpad directory that
no longer exists**, then hand-copied the PNGs in. No figure in the book was reproducible.

## Accessibility contract

Every figure must satisfy all four, and the render script is written to enforce them:

1. Colour comes only from `scale_colour_v2v()` / `scale_fill_v2v()` (Okabe-Ito,
   colourblind-safe). Never hardcode a hex.
2. Colour is never the sole encoding (WCAG 2.1 SC 1.4.1). Pair it with linetype, shape,
   facets, or direct labels.
3. Filled marks carry a thin `colour = "grey20"` outline so adjacent fills clear 3:1
   (SC 1.4.11).
4. Every image carries `fig-alt` describing **what the data shows**, not the chart type.

## Current coverage

| Chapter | Title | Data figures | Assessment |
|---|---|---|---|
| 1 | The Science of Storytelling | 0 | Conceptual. No data figure warranted. |
| 2 | The Open Workspace | 0 | Tooling walkthrough. None warranted. |
| 3 | Knowing and Knowing Well | 0 | Ethics. None warranted. |
| 4 | Intelligence Gathering | 0 | **Gap — see G1.** |
| 5 | Theory as a Lens | 0 | Conceptual. None warranted. |
| 6 | The Prospectus | 0 | Conceptual. None warranted. |
| 7 | Structured listening | 0 | **Gap — see G2.** |
| 8 | From vibes to variables | 0 | **Gap — see G3, G4. Highest priority.** |
| 9 | The rulebook and first workspace | 0 | **Gap — see G5.** |
| 10 | The sample | 0 | **Gap — see G6. Highest priority.** |
| 11 | Wrangling the data | 0 | **Gap — see G7.** |
| 12 | Visualizing the narrative | 3 | Complete. |
| 13 | Making the call | 1 | **Gap — see G8.** |
| 14 | The one-click report | 0 | Workflow. None warranted. |

Four data figures across fourteen chapters, all in the last three. Parts I to III carry
none, which is exactly where students are being asked to absorb the most abstract
material.

## Identified gaps, in priority order

Priority reflects teaching value: how much the figure does work that the prose cannot.

**G6 — Ch10, stratified vs simple random coverage. (highest)**
The chapter argues a simple random sample is not enough and that stratification fixes it,
then asks the reader to take it on faith. The dataset's own design is the proof: 8 anchor
channels plus 42 stratified additions. Plot channel viewership on a log axis, mark which
channels an SRS would likely miss, and the argument becomes visible in one glance.
Redundant encoding: shape for anchor vs stratified, not colour alone.

**G3 — Ch8, levels of measurement on one real variable. (highest)**
Nominal/ordinal/interval/ratio is the chapter's core and the most commonly muddled idea in
the course. Take one Twitch variable and show it rendered at each level, so the reader sees
what information each level keeps and discards. This is a small-multiple, not a chart type.

**G4 — Ch8, reliability vs validity.**
The four-quadrant target diagram is canonical for a reason. It is a schematic rather than a
data figure, so it does not belong in `render-all.R`; author it as a tagged SVG or a
ggplot-drawn schematic and register it separately.

**G7 — Ch11, raw message-length distribution.**
Ch12's histogram caps length at 120 characters. Nothing shows the reader *why*. The
uncapped distribution makes the long tail obvious and justifies the capping decision
instead of asserting it. Cheap to build: the data is already in `build_analysis()`.

**G8 — Ch13, effect size and overlap.**
The chapter has means with confidence intervals but stops there. "How big is the
difference" deserves a figure showing the overlap between the two distributions, since a
significant difference between heavily overlapping distributions is the single most
misread result in student work.

**G1 — Ch4, saturation curve.**
"Recognizing saturation" is described narratively. A curve of new-sources-found against
sources-read makes the flattening concrete. Illustrative data is acceptable here provided
the alt text and caption say so plainly.

**G2 — Ch7, sampling your observation.**
A timeline strip showing which windows a structured observation actually covers versus the
full collection week. Low cost, moderate payoff.

**G5 — Ch9, the shape of the data.**
"Looking at the data" would benefit from a compact view of the table's structure: rows,
columns, types, missingness. Missingness in particular pays off later, since the 501 NA
rows in `is_gaming` are a live teaching point.

## Notes

- G4 is a schematic, not a data figure. Everything else belongs in `render-all.R`.
- Adding a figure means three coordinated edits: a registry entry in `render-all.R`, the
  `![](){fig-alt=}` embed in the chapter, and a row in the coverage table above.
- The undergrad and grad editions share this figure set. If a figure should appear in only
  one edition, gate it in the profile config, not by rendering two variants.
