suppressMessages({library(dplyr)})
d <- "/Volumes/One Touch/20-research/aura-lab/v2v-r/data/"
load(paste0(d,"twitch_chat_sample.rda")); load(paste0(d,"twitch_streams_sample.rda"))
chat <- twitch_chat_sample; streams <- twitch_streams_sample

nongaming <- c("Art","ASMR","Beauty & Body Art","Creative","Food & Drink","IRL",
  "Just Chatting","Makers & Crafting","Music","Music & Performing Arts",
  "Science & Technology","Sports & Fitness","Talk Shows & Podcasts","Travel & Outdoors")

ctype <- streams %>% filter(!is.na(game)) %>% count(channel, game) %>%
  group_by(channel) %>% slice_max(n, n=1, with_ties=FALSE) %>% ungroup() %>%
  mutate(is_gaming = !(game %in% nongaming)) %>% select(channel, is_gaming, game)

a <- chat %>% mutate(message_length = nchar(message)) %>%
  left_join(ctype %>% select(channel,is_gaming), by="channel")

cat("== count(is_gaming) ==\n"); print(a %>% count(is_gaming))
cat("\n== group stats (na.rm) ==\n")
print(a %>% filter(!is.na(is_gaming)) %>% group_by(is_gaming) %>%
  summarise(n_rows=n(), n_len=sum(!is.na(message_length)),
            mean=mean(message_length,na.rm=TRUE), median=median(message_length,na.rm=TRUE),
            sd=sd(message_length,na.rm=TRUE), .groups="drop"))

g <- a %>% filter(!is.na(is_gaming), !is.na(message_length))
tt <- t.test(message_length ~ is_gaming, data=g)
cat("\n== Welch t-test ==\n"); print(tt)
cat("n used:", sum(!is.na(g$message_length)), "\n")
s <- g %>% group_by(is_gaming) %>% summarise(n=n(), m=mean(message_length), v=var(message_length))
sp <- sqrt(sum((s$n-1)*s$v)/(sum(s$n)-2))
cat("pooled sd:", sp, " Cohen d:", (s$m[2]-s$m[1])/sp, "\n")

cat("\n== regression ==\n")
print(round(summary(lm(message_length ~ is_gaming, data=g))$coefficients, 4))
cat("R2:", summary(lm(message_length ~ is_gaming, data=g))$r.squared, "\n")

four <- c("Fortnite","Hearthstone","Just Chatting","League of Legends")
fg <- a %>% left_join(ctype %>% select(channel,game), by="channel") %>%
  filter(game %in% four, !is.na(message_length))
cat("\n== four categories ==\n")
print(fg %>% group_by(game) %>% summarise(n=n(), mean=round(mean(message_length),2)))
av <- aov(message_length ~ game, data=fg); print(summary(av))
ss <- summary(av)[[1]][["Sum Sq"]]; cat("eta2:", ss[1]/sum(ss), "\n")

cat("\n== hour counts ==\n")
h <- as.POSIXct(chat$date/1000, origin="1970-01-01", tz="UTC")
tb <- table(format(h, "%H")); print(c(peak13=tb["13"], quiet03=tb["03"]))
cat("span days:", as.numeric(difftime(max(h), min(h), units="days")), "\n")
cat("len>120:", sum(nchar(chat$message)>120, na.rm=TRUE), " max:", max(nchar(chat$message), na.rm=TRUE), "\n")
