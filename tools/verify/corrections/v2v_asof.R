suppressMessages({library(dplyr)})
d <- "/Volumes/One Touch/20-research/aura-lab/v2v-r/data/"
load(paste0(d,"twitch_chat_sample.rda")); load(paste0(d,"twitch_streams_sample.rda"))
ng <- c("Art","ASMR","Beauty & Body Art","Creative","Food & Drink","IRL","Just Chatting",
 "Makers & Crafting","Music","Music & Performing Arts","Science & Technology",
 "Sports & Fitness","Talk Shows & Podcasts","Travel & Outdoors")
chat <- twitch_chat_sample %>% mutate(L = nchar(message)) %>% filter(!is.na(L))
st <- twitch_streams_sample %>% filter(!is.na(game)) %>%
  mutate(ctx = ifelse(game %in% ng, "nongaming", "gaming")) %>%
  select(channel, date, ctx) %>% arrange(channel, date)
# asof: most recent snapshot at or before each message
j <- chat %>% arrange(channel, date) %>%
  left_join(st, by = join_by(channel, closest(date >= date)))
cat("-- per-message context (asof) --\n")
print(j %>% filter(!is.na(ctx)) %>% group_by(ctx) %>%
      summarise(n=n(), mean=round(mean(L),4), median=median(L)))
cat("unmatched:", sum(is.na(j$ctx)), "\n")
a <- j %>% filter(!is.na(ctx))
cat(sprintf("gap (nongaming - gaming) = %+.4f\n",
  mean(a$L[a$ctx=="nongaming"]) - mean(a$L[a$ctx=="gaming"])))
print(t.test(L ~ ctx, data = a))
