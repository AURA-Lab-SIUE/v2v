#!/usr/bin/env Rscript
# =====================================================================
# v2v-book — reproducible figure render for the whole book.
#
# WHY THIS EXISTS
#   Before 2026-07-23 the book's data figures were rendered by ad-hoc
#   scripts on the ThinkBook (C:\pythia\work\mc451-501-accessibility\
#   render_ch12.R / render_ch13.R), which loaded the v2v package with
#   devtools::load_all() from a *temp scratchpad directory*. That
#   directory no longer exists, so no figure in this book could be
#   reproduced. The PNGs were then hand-scp'd into images/.
#
#   This script replaces that. Every data figure in the book is defined
#   here, rendered from the shipped v2v sample data, and written to
#   images/. One command re-renders the book's entire figure set.
#
# ACCESSIBILITY CONTRACT (WCAG 2.1 AA — this is a remediated OER)
#   * Colour comes ONLY from scale_colour_v2v()/scale_fill_v2v()
#     (Okabe-Ito, colourblind-safe). Never hardcode a hex.
#   * Colour is never the sole encoding — pair it with direct labels,
#     facets, shape, or linetype (SC 1.4.1).
#   * Filled marks carry a thin dark outline so adjacent fills clear
#     3:1 against each other and the background (SC 1.4.11).
#   * Every figure here MUST have a matching fig-alt in the .qmd that
#     embeds it. The alt text describes WHAT THE DATA SHOWS, not the
#     chart type. Run check_alt_coverage() below to verify.
#
# USAGE
#   Rscript figures/render-all.R            # render everything
#   Rscript figures/render-all.R ch12       # render one chapter's set
# =====================================================================

suppressMessages({
  library(ggplot2); library(dplyr); library(tidyr)
  library(stringr); library(lubridate); library(forcats)
})

# Locate the book root: run from the book dir OR from figures/. Identify it by
# its own marker files rather than by script path, which Rscript does not expose.
find_book <- function() {
  for (cand in c(".", "..", "../..")) {
    p <- normalizePath(cand, mustWork = FALSE)
    if (dir.exists(file.path(p, "images")) && file.exists(file.path(p, "_quarto.yml"))) return(p)
  }
  stop("Cannot locate the v2v-book root (looked for images/ + _quarto.yml in . .. ../..)")
}

BOOK   <- find_book()
IMAGES <- file.path(BOOK, "images")
PKGDIR <- file.path(dirname(BOOK), "v2v")   # sibling AURA-Lab repo

# --- load v2v: installed package preferred, sibling source as fallback ---
if (requireNamespace("v2v", quietly = TRUE)) {
  suppressMessages(library(v2v))
  message("v2v: using installed package ", utils::packageVersion("v2v"))
} else if (dir.exists(PKGDIR)) {
  if (!requireNamespace("devtools", quietly = TRUE))
    stop("v2v is not installed and devtools is unavailable to load ", PKGDIR)
  message("v2v: not installed — devtools::load_all('", PKGDIR, "')")
  suppressMessages(devtools::load_all(PKGDIR, quiet = TRUE))
} else {
  stop("Cannot find the v2v package: neither installed nor at ", PKGDIR)
}

W <- 8; H <- 4.6; DPI <- 150      # book figure geometry — keep consistent

save_fig <- function(plot, name) {
  path <- file.path(IMAGES, name)
  ggsave(path, plot, width = W, height = H, dpi = DPI, bg = "white")
  message(sprintf("  wrote %-34s %6.0f KB", name, file.size(path) / 1024))
  invisible(path)
}

# =====================================================================
# Shared data prep — the ch11 "analysis" table the whole book builds on.
# Kept in ONE place so every chapter's figure agrees with the prose.
# =====================================================================
build_analysis <- function() {
  streams <- v2v::twitch_streams()
  chat0   <- v2v::twitch_chat()

  nongaming_categories <- c(
    "Art", "ASMR", "Beauty & Body Art", "Creative", "Food & Drink",
    "IRL", "Just Chatting", "Makers & Crafting", "Music",
    "Music & Performing Arts", "Science & Technology",
    "Sports & Fitness", "Talk Shows & Podcasts", "Travel & Outdoors")

  channel_type <- streams |>
    filter(!is.na(game)) |>
    count(channel, game) |>
    group_by(channel) |>
    slice_max(n, n = 1, with_ties = FALSE) |>
    ungroup() |>
    mutate(is_gaming = !(game %in% nongaming_categories)) |>
    select(channel, is_gaming)

  analysis <- chat0 |>
    mutate(timestamp      = as.POSIXct(date / 1000, origin = "1970-01-01", tz = "UTC"),
           message_length = str_length(message)) |>
    left_join(channel_type, by = "channel")

  list(streams = streams, chat = chat0, analysis = analysis)
}

# --- validation gate: the prose quotes these numbers, so assert them ---
validate <- function(d) {
  counts <- d$analysis |> count(is_gaming)
  # NA must be keyed as the literal string "NA": as.character(NA) is NA, not "NA",
  # which silently produced an unmatchable key and a false "DIVERGED" warning.
  keys <- ifelse(is.na(counts$is_gaming), "NA", as.character(counts$is_gaming))
  got  <- setNames(as.numeric(counts$n), keys)
  expected <- c("FALSE" = 3457, "TRUE" = 31309, "NA" = 501)
  bad <- 0L
  for (k in names(expected)) {
    # compare as plain numerics: integer-vs-double made identical() always FALSE,
    # so this validator used to warn even when the counts matched exactly.
    if (!(k %in% names(got)) || !isTRUE(all.equal(got[[k]], expected[[k]]))) {
      bad <- bad + 1L
      warning(sprintf("is_gaming[%s] = %s but the prose says %s - figures and text have DIVERGED",
                      k, if (k %in% names(got)) got[[k]] else "absent", expected[[k]]),
              call. = FALSE)
    }
  }
  if (bad == 0L) message("validation: is_gaming counts match the prose (3457 / 31309 / 501). PASS")
}

# =====================================================================
# FIGURE REGISTRY
# Each entry renders one figure. To add a figure: append an entry, give
# it a chapter tag, and add the matching ![](){fig-alt=} in the .qmd.
# =====================================================================

fig_ch12_1 <- function(d) {
  viewers_over_time <- d$streams |>
    filter(!is.na(game)) |>
    mutate(timestamp = as.POSIXct(date / 1000, origin = "1970-01-01", tz = "UTC"),
           six_hour  = floor_date(timestamp, "6 hours"),
           category  = fct_lump_n(game, n = 5)) |>
    group_by(six_hour, category) |>
    summarise(total_viewers = sum(viewers), .groups = "drop")

  p <- ggplot(viewers_over_time,
              aes(six_hour, total_viewers, colour = category, linetype = category)) +
    geom_line(linewidth = 0.9) +
    scale_colour_v2v() +
    labs(title = "Concurrent viewers by game category",
         x = "Date (UTC, six-hour buckets)", y = "Total viewers in bucket",
         colour = "Category", linetype = "Category") +
    theme_v2v()
  save_fig(p, "fig12-1-viewers-by-game.png")
}

fig_ch12_2 <- function(d) {
  chat_by_hour <- d$analysis |> mutate(hour = hour(timestamp)) |> count(hour, name = "messages")
  # Single series: use the palette's highest-contrast hue (blue, 5.2:1 vs
  # white) rather than a hardcoded hex, so the book has ONE colour source.
  p <- ggplot(chat_by_hour, aes(hour, messages)) +
    geom_col(fill = unname(v2v_colours["blue"]), colour = "grey20", linewidth = 0.2) +
    labs(title = "Chat messages by hour of day",
         x = "Hour of day (UTC)", y = "Messages") +
    theme_v2v()
  save_fig(p, "fig12-2-chat-by-hour.png")
}

fig_ch12_3 <- function(d) {
  msglen <- d$analysis |> filter(!is.na(is_gaming)) |>
    mutate(length_shown = pmin(message_length, 120))
  p <- ggplot(msglen, aes(length_shown, fill = is_gaming)) +
    geom_histogram(binwidth = 5, position = "identity", alpha = 0.55,
                   colour = "grey20", linewidth = 0.15) +
    scale_fill_v2v() +
    labs(title = "Message length by channel context",
         x = "Message length (characters, capped at 120)", y = "Messages",
         fill = "Gaming channel") +
    theme_v2v()
  save_fig(p, "fig12-3-msglen-by-context.png")
}

fig_ch13_means <- function(d) {
  summ <- d$analysis |> filter(!is.na(is_gaming)) |>
    group_by(group = ifelse(is_gaming, "Gaming", "Non-gaming")) |>
    summarise(n = n(), mean = mean(message_length),
              se = sd(message_length) / sqrt(n()), .groups = "drop") |>
    mutate(ci_lo = mean - 1.96 * se, ci_hi = mean + 1.96 * se)

  p <- ggplot(summ, aes(group, mean, colour = group)) +
    geom_errorbar(aes(ymin = ci_lo, ymax = ci_hi), width = 0.14, linewidth = 0.9) +
    geom_point(size = 3) +
    geom_text(aes(y = ci_hi, label = sprintf("%.1f", mean)),
              vjust = -0.7, size = 4, colour = "grey20") +
    scale_colour_v2v() +
    scale_y_continuous(limits = c(0, NA), expand = expansion(mult = c(0, 0.08))) +
    labs(title = "Mean message length with 95% confidence intervals",
         x = NULL, y = "Mean message length (characters)") +
    theme_v2v() + theme(legend.position = "none")
  save_fig(p, "ch13-means-ci.png")
}

fig_ch08_levels <- function(d) {
  # G3 — one column, measured at different levels (ch8 "Notice what happened
  # with stream title"). Three panels re-measure the SAME column (title);
  # the fourth shows the level a string cannot reach — interval — using the
  # chapter's own example, the timestamp. Single-hue fills with direct labels:
  # colour never carries information here, so SC 1.4.1 is satisfied by design.
  library(patchwork)
  blue <- unname(v2v_colours["blue"])

  titles <- d$streams |> filter(!is.na(title), title != "") |>
    distinct(channel, title) |>
    mutate(nchar_title = str_length(title))

  n_titles <- nrow(titles)
  n_unique <- n_distinct(titles$title)
  ex5 <- titles |> count(title, sort = TRUE) |> slice_head(n = 5) |>
    mutate(title_short = str_trunc(title, 18))
  pA <- ggplot(ex5, aes(n, fct_reorder(title_short, n))) +
    geom_col(fill = blue, colour = "grey20", linewidth = 0.2, width = 0.7) +
    scale_x_continuous(breaks = c(0, 1), expand = expansion(mult = c(0, 0.12))) +
    labs(title = "Nominal: the raw string",
         subtitle = sprintf("Counting is all you can do, and %d of %d
titles are unique: it tells you nothing", n_unique, n_titles),
         x = "Streams using this exact title", y = NULL) +
    theme_v2v()

  bins <- titles |>
    mutate(bin = cut(nchar_title, c(-Inf, 20, 60, Inf),
                     labels = c("≤20", "21–60", ">60"))) |>
    count(bin)
  med_bin <- bins$bin[which(cumsum(bins$n) >= sum(bins$n) / 2)[1]]
  pB <- ggplot(bins, aes(bin, n)) +
    geom_col(fill = blue, colour = "grey20", linewidth = 0.2) +
    geom_text(aes(label = ifelse(bin == med_bin, paste0(n, " (median bin)"), n)),
              vjust = -0.35, size = 3.2, colour = "grey20") +
    scale_y_continuous(expand = expansion(mult = c(0, 0.14))) +
    labs(title = "Ordinal: binned by length",
         subtitle = "Ranks and medians, but unequal gaps",
         x = "Title length (characters)", y = "Stream titles") +
    theme_v2v()

  mean_len <- mean(titles$nchar_title)
  pC <- ggplot(titles, aes(nchar_title)) +
    geom_histogram(binwidth = 5, fill = blue, colour = "grey20", linewidth = 0.15) +
    geom_vline(xintercept = mean_len, linetype = "dashed", colour = "grey20") +
    annotate("text", x = mean_len, y = Inf, hjust = -0.08, vjust = 1.6, size = 3.2,
             colour = "grey20", label = sprintf("mean = %.0f chars", mean_len)) +
    labs(title = "Ratio: length in characters",
         subtitle = "True zero; every statistic is available",
         x = "Title length (characters)", y = "Stream titles") +
    theme_v2v()

  per_day <- d$analysis |> mutate(day = as.Date(timestamp)) |> count(day)
  pD <- ggplot(per_day, aes(day, n)) +
    geom_col(fill = blue, colour = "grey20", linewidth = 0.2) +
    labs(title = "Interval: the timestamp",
         subtitle = "Equal spacing; zero (1970) is arbitrary",
         x = "Date (UTC)", y = "Chat messages") +
    theme_v2v()

  p <- (pA | pB) / (pC | pD) +
    plot_annotation(
      title = "Level of measurement is a decision, not a property of the data",
      subtitle = "The stream-title column measured three ways, plus the one level a string can never take",
      theme = theme_v2v())
  path <- file.path(IMAGES, "fig08-1-levels-of-measurement.png")
  ggsave(path, p, width = W, height = 6.4, dpi = DPI, bg = "white")
  message(sprintf("  wrote %-34s %6.0f KB", basename(path), file.size(path) / 1024))
}

fig_ch10_sampling <- function(d) {
  # G6 — the fixture's own stratified design as the argument for stratification.
  # Redundant encoding per the accessibility contract: anchor vs stratified is
  # carried by BOTH shape and colour, and the SRS-miss region by a labeled line.
  anchors <- c("xqcow", "forsen", "sodapoppin", "asmongold", "loltyler1",
               "disguisedtoast", "giantwaffle", "bobross")
  by_channel <- d$chat |>
    count(channel, name = "messages") |>
    arrange(desc(messages)) |>
    mutate(rank   = row_number(),
           design = ifelse(channel %in% anchors, "Anchor (fixed)", "Stratified draw"))
  srs_n     <- 1000
  threshold <- sum(by_channel$messages) / srs_n
  n_missed  <- sum(by_channel$messages < threshold)

  p <- ggplot(by_channel, aes(rank, messages, colour = design, shape = design)) +
    geom_hline(yintercept = threshold, linetype = "dashed", colour = "grey40") +
    geom_point(size = 2.6, stroke = 0.7) +
    annotate("text", x = 1, y = threshold, hjust = 0, vjust = -0.7, size = 3.3, colour = "grey20",
             label = sprintf(
               "Below the dashed line, a 1,000-message simple random sample expects under one message per channel:\n%d of the 50 channels would likely vanish. The stratified design keeps every one.",
               n_missed)) +
    scale_y_log10(labels = scales::comma) +
    scale_colour_v2v() +
    scale_shape_manual(values = c("Anchor (fixed)" = 17, "Stratified draw" = 16)) +
    labs(title = "The skew got sampled across, not sampled away",
         subtitle = "All 50 fixture channels; the flat top is the 1,000-message-per-channel cap",
         x = "Channel, ranked by chat volume", y = "Messages in the window (log scale)",
         colour = "Sampling design", shape = "Sampling design") +
    theme_v2v()
  save_fig(p, "fig10-1-stratified-coverage.png")
}

REGISTRY <- list(
  ch08 = list(fig_ch08_levels),
  ch10 = list(fig_ch10_sampling),
  ch12 = list(fig_ch12_1, fig_ch12_2, fig_ch12_3),
  ch13 = list(fig_ch13_means)
)

# =====================================================================
# Alt-text coverage check — an image without fig-alt is an Ally failure.
# =====================================================================
check_alt_coverage <- function() {
  qmds <- c(list.files(file.path(BOOK, "chapters"),    "\\.qmd$", full.names = TRUE),
            list.files(file.path(BOOK, "appendices"),  "\\.qmd$", full.names = TRUE),
            file.path(BOOK, "index.qmd"))
  qmds <- qmds[file.exists(qmds)]
  missing <- character()
  for (f in qmds) {
    src <- paste(readLines(f, warn = FALSE), collapse = "\n")
    for (m in regmatches(src, gregexpr("!\\[[^]]*\\]\\([^)]+\\)(\\{[^}]*\\})?", src))[[1]]) {
      if (!grepl("fig-alt", m, fixed = TRUE))
        missing <- c(missing, sprintf("%s :: %s", basename(f), substr(m, 1, 70)))
    }
  }
  if (length(missing)) {
    message("\nALT-TEXT GAPS (", length(missing), ") — these will score red in Ally:")
    for (x in missing) message("  ", x)
  } else {
    message("\nalt-text: every image in the book carries fig-alt. PASS")
  }
  invisible(missing)
}

# =====================================================================
main <- function() {
  args <- commandArgs(trailingOnly = TRUE)
  which <- if (length(args)) args else names(REGISTRY)
  if (!dir.exists(IMAGES)) stop("images/ not found under ", BOOK)

  message("book:   ", BOOK)
  message("images: ", IMAGES)
  d <- build_analysis()
  validate(d)

  for (ch in which) {
    if (is.null(REGISTRY[[ch]])) { warning("no figures registered for ", ch); next }
    message("\n", ch, ":")
    for (fn in REGISTRY[[ch]]) fn(d)
  }
  check_alt_coverage()
  message("\ndone.")
}

if (!interactive()) main()
