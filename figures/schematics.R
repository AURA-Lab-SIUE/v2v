#!/usr/bin/env Rscript
# =====================================================================
# v2v-book — SCHEMATIC figures (not data figures; see figures/FIGURES.md).
# Registered here, separately from render-all.R, because nothing in them
# derives from the v2v data: they are drawn illustrations. Same
# accessibility contract as render-all.R (palette scales, redundant
# encoding, thin outlines, fig-alt in the embedding .qmd).
#
# USAGE:  Rscript figures/schematics.R
# =====================================================================
suppressMessages({ library(ggplot2); library(dplyr) })

find_book <- function() {
  for (cand in c(".", "..", "../..")) {
    p <- normalizePath(cand, mustWork = FALSE)
    if (dir.exists(file.path(p, "images")) && file.exists(file.path(p, "_quarto.yml"))) return(p)
  }
  stop("Cannot locate the v2v-book root")
}
BOOK <- find_book()
if (requireNamespace("v2v", quietly = TRUE)) suppressMessages(library(v2v)) else
  suppressMessages(devtools::load_all(file.path(dirname(BOOK), "v2v"), quiet = TRUE))

# --- G4: the reliability-vs-validity target diagram -------------------
# Four targets; shots are FIXED coordinates (a schematic, not a simulation).
ring <- function(r) {
  th <- seq(0, 2 * pi, length.out = 120)
  data.frame(x = r * cos(th), y = r * sin(th), r = r)
}
rings <- do.call(rbind, lapply(c(1, 2, 3), ring))

tight  <- data.frame(dx = c(-0.25, 0.2, 0.05, -0.1, 0.3, -0.3, 0.15, -0.05),
                     dy = c(0.2, -0.15, 0.3, -0.3, 0.05, 0.1, -0.25, 0.15))
spread <- data.frame(dx = c(-1.7, 1.5, 0.3, -0.9, 1.9, -1.4, 0.8, -0.2),
                     dy = c(1.3, -1.6, 1.9, -1.1, 0.4, -0.5, 1.5, -1.9))
quads <- rbind(
  transform(tight,  cx = 0,   cy = 0,   panel = "Reliable and valid:
consistent, and on target"),
  transform(tight,  cx = 1.6, cy = 1.6, panel = "Reliable, not valid:
consistent, and consistently wrong"),
  transform(spread, cx = 0,   cy = 0,   panel = "Valid on average, not reliable:
right on average, unusable one at a time"),
  transform(spread, cx = 1.4, cy = 1.4, panel = "Neither:
inconsistent and off target"))
quads <- quads %>% mutate(x = cx + dx * 0.9, y = cy + dy * 0.9)
quads$panel <- factor(quads$panel, levels = unique(quads$panel))

p <- ggplot() +
  geom_path(data = merge(rings, data.frame(panel = factor(levels(quads$panel), levels = levels(quads$panel)))),
            aes(x, y, group = r), colour = "grey60", linewidth = 0.4) +
  geom_point(data = data.frame(panel = factor(levels(quads$panel), levels = levels(quads$panel))),
             aes(x = 0, y = 0), shape = 3, size = 2.5, colour = "grey40") +
  geom_point(data = quads, aes(x, y), shape = 21, size = 2.6,
             fill = unname(v2v_colours["blue"]), colour = "grey20", stroke = 0.5) +
  facet_wrap(~ panel, ncol = 2) +
  coord_equal(xlim = c(-3.4, 3.4), ylim = c(-3.4, 3.4)) +
  labs(title = "Reliability is consistency; validity is accuracy",
       subtitle = "Each target's centre is the concept being measured; each dot is one measurement") +
  theme_v2v() +
  theme(axis.title = element_blank(), axis.text = element_blank(),
        axis.ticks = element_blank(), panel.grid = element_blank())

path <- file.path(BOOK, "images", "fig08-2-reliability-validity.png")
ggsave(path, p, width = 8, height = 7.4, dpi = 150, bg = "white")
message(sprintf("wrote %s  %.0f KB", basename(path), file.size(path) / 1024))
