# Regenerate the four Part VI figures from the v0.3.0 fixture.
#
# The 3rd edition's figures (fig12-1, fig12-2, fig12-3, ch13-means-ci) are still
# on disk and still depict the 50-channel corpus: fig12-2 peaks at 13:00 with
# 2,200 messages where the 4th edition reports 22:00 with 10,967. Wiring the old
# images into the new chapters would have put figures on the page that contradict
# the prose beside them, which is worse than the chapters having no figures.
#
# Palette is Okabe-Ito, which is colourblind-safe, and every figure also carries
# a redundant non-colour encoding, because Chapter 24 tells the reader to do that.

suppressPackageStartupMessages({library(ggplot2); library(dplyr); library(scales)})

D   <- "/Volumes/One Touch/20-research/aura-lab/v2v/data-raw/v3/"
OUT <- "/Volumes/One Touch/20-research/aura-lab/v2v/images/"

# na.strings = "" ONLY. Five messages are the literal text "NA" and R's default
# na.strings would turn them into missing values, which makes the gaming group's
# mean come back NA. That is the trap the appendix documents, and it caught this
# script on its first run.
chat    <- read.csv(paste0(D, "twitch_chat_sample.csv"),
                    stringsAsFactors = FALSE, na.strings = "")
streams <- read.csv(paste0(D, "twitch_streams_sample.csv"),
                    stringsAsFactors = FALSE, na.strings = "")

OK <- c("#0072B2", "#D55E00", "#009E73", "#CC79A7", "#E69F00", "#56B4E9", "#999999")
base <- theme_minimal(base_size = 11) +
  theme(panel.grid.minor = element_blank(),
        plot.title.position = "plot",
        legend.position = "bottom")

# ---------------------------------------------------------------- fig24-1
# Total concurrent viewers by game category, in six-hour UTC buckets.
streams$ts  <- as.POSIXct(streams$date / 1000, origin = "1970-01-01", tz = "UTC")
streams$bin <- as.POSIXct(round(as.numeric(streams$ts) / 21600) * 21600,
                          origin = "1970-01-01", tz = "UTC")
top <- streams |> count(game, sort = TRUE) |> filter(game != "") |> head(5) |> pull(game)
streams$cat <- ifelse(streams$game %in% top, streams$game, "All other categories")

v1 <- streams |> group_by(bin, cat) |> summarise(viewers = sum(viewers), .groups = "drop")
p1 <- ggplot(v1, aes(bin, viewers, colour = cat, linetype = cat)) +
  geom_line(linewidth = 0.7) +
  scale_colour_manual(values = OK, name = NULL) +
  scale_linetype_manual(values = c(1, 2, 3, 4, 5, 6), name = NULL) +
  scale_y_continuous(labels = label_comma()) +
  labs(x = NULL, y = "Total concurrent viewers") + base
ggsave(paste0(OUT, "fig24-1-viewers-by-game.png"), p1, width = 7.5, height = 4.2, dpi = 200)

cat("fig24-1 top categories:", paste(top, collapse = " | "), "\n")
cat("  peak bucket total:", format(max(v1$viewers), big.mark = ","), "\n")

# ---------------------------------------------------------------- fig24-2
chat$ts   <- as.POSIXct(chat$date / 1000, origin = "1970-01-01", tz = "UTC")
chat$hour <- as.integer(format(chat$ts, "%H"))
h <- chat |> count(hour)
p2 <- ggplot(h, aes(factor(hour), n)) +
  geom_col(fill = OK[1]) +
  scale_y_continuous(labels = label_comma()) +
  labs(x = "Hour of day (UTC)", y = "Chat messages") + base
ggsave(paste0(OUT, "fig24-2-chat-by-hour.png"), p2, width = 7.5, height = 3.8, dpi = 200)

cat("fig24-2 peak:", h$hour[which.max(h$n)], "=", format(max(h$n), big.mark = ","),
    "| trough:", h$hour[which.min(h$n)], "=", format(min(h$n), big.mark = ","), "\n")

# ---------------------------------------------------------------- fig24-3
NONGAME <- c("just chatting","art","music & performing arts","asmr",
             "talk shows & podcasts","irl","food & drink","travel & outdoors",
             "science & technology","sports & fitness","makers & crafting")
modal <- streams |> filter(game != "") |> count(channel, game) |>
  group_by(channel) |> slice_max(n, n = 1, with_ties = FALSE) |> ungroup() |>
  mutate(is_gaming = !(tolower(game) %in% NONGAME)) |> select(channel, is_gaming)

m <- chat |> inner_join(modal, by = "channel") |>
  mutate(len = nchar(message),
         grp = ifelse(is_gaming, "Gaming channels", "Non-gaming channels"))
mc <- m |> mutate(len = pmin(len, 120))

p3 <- ggplot(mc, aes(len, fill = grp)) +
  geom_histogram(binwidth = 5, position = "identity", alpha = 0.55) +
  scale_fill_manual(values = OK[c(2, 1)], name = NULL) +
  scale_y_continuous(labels = label_comma()) +
  facet_wrap(~grp, ncol = 1, scales = "free_y") +
  labs(x = "Message length in characters (capped at 120)", y = "Messages") +
  base + theme(legend.position = "none")
ggsave(paste0(OUT, "fig24-3-msglen-by-context.png"), p3, width = 7.5, height = 4.6, dpi = 200)

s <- m |> group_by(grp) |> summarise(n = n(), mean = mean(len), sd = sd(len), .groups = "drop")
print(as.data.frame(s))
cat("over cap:", sum(m$len > 120), sprintf("(%.1f%%)", 100 * sum(m$len > 120) / nrow(m)), "\n")

# ---------------------------------------------------------------- fig25-1
ci <- s |> mutate(se = sd / sqrt(n), lo = mean - 1.96 * se, hi = mean + 1.96 * se)
p4 <- ggplot(ci, aes(grp, mean)) +
  geom_errorbar(aes(ymin = lo, ymax = hi), width = 0.08, linewidth = 0.6) +
  geom_point(size = 3, colour = OK[1]) +
  scale_y_continuous(limits = c(0, NA)) +
  labs(x = NULL, y = "Mean message length in characters") + base
ggsave(paste0(OUT, "fig25-1-means-ci.png"), p4, width = 6, height = 4, dpi = 200)
print(as.data.frame(ci))
