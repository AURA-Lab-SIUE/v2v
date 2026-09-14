suppressMessages({library(dplyr)})
d <- "/Volumes/One Touch/20-research/aura-lab/v2v-r/data/"
load(paste0(d,"twitch_chat_sample.rda")); load(paste0(d,"twitch_streams_sample.rda"))
ng <- c("Art","ASMR","Beauty & Body Art","Creative","Food & Drink","IRL","Just Chatting",
 "Makers & Crafting","Music","Music & Performing Arts","Science & Technology",
 "Sports & Fitness","Talk Shows & Podcasts","Travel & Outdoors")
ct <- twitch_streams_sample %>% filter(!is.na(game)) %>% count(channel,game) %>%
  group_by(channel) %>% slice_max(n,n=1,with_ties=FALSE) %>% ungroup() %>%
  mutate(is_gaming=!(game %in% ng))
a <- twitch_chat_sample %>% mutate(L=nchar(message),
       cmd=ifelse(!is.na(message) & startsWith(message,"!"),"command","talk")) %>%
     left_join(ct %>% select(channel,is_gaming,game), by="channel")

g <- a %>% filter(!is.na(is_gaming), !is.na(L))
s <- g %>% group_by(is_gaming) %>% summarise(n=n(), m=mean(L), sd=sd(L), md=median(L))
cat(sprintf("label n_len=%d mean=%.4f sd=%.4f median=%d  (is_gaming=%s)\n", s$n,s$m,s$sd,s$md,s$is_gaming))
n1<-s$n[2]; n2<-s$n[1]; m1<-s$m[2]; m2<-s$m[1]; s1<-s$sd[2]; s2<-s$sd[1]
v1<-s1^2/n1; v2<-s2^2/n2
cat(sprintf("Welch t=%.4f df=%.1f\n",(m1-m2)/sqrt(v1+v2),(v1+v2)^2/((v1^2)/(n1-1)+(v2^2)/(n2-1))))
sp<-sqrt(((n1-1)*s1^2+(n2-1)*s2^2)/(n1+n2-2))
cat(sprintf("pooled sd=%.4f  d=%.4f\n",sp,(m1-m2)/sp))
cat(sprintf("CI half gaming=%.4f nongaming=%.4f\n",1.96*s1/sqrt(n1),1.96*s2/sqrt(n2)))
cat(sprintf("T.TEST p=%.4g\n", t.test(L~is_gaming,data=g)$p.value))

cat("\n-- chi-square (label x command), all classified messages --\n")
cc <- a %>% filter(!is.na(is_gaming)) %>% count(is_gaming,cmd)
print(cc); tb<-xtabs(n~is_gaming+cmd,cc); print(addmargins(tb))
ch<-chisq.test(tb,correct=FALSE)
cat(sprintf("chi2=%.4f df=%d p=%.4g V=%.4f N=%d\n",ch$statistic,ch$parameter,ch$p.value,sqrt(ch$statistic/sum(tb)),sum(tb)))

cat("\n-- ch26: commands excluded --\n")
t2 <- g %>% group_by(is_gaming) %>% summarise(all=mean(L),n_all=n())
t3 <- g %>% filter(cmd=="talk") %>% group_by(is_gaming) %>% summarise(talk=mean(L),n_talk=n())
j <- left_join(t2,t3,by="is_gaming"); print(j)
cat(sprintf("gap all=%.4f  gap talk=%.4f  shrink=%.4f\n",
  j$all[1]-j$all[2], j$talk[1]-j$talk[2], 1-((j$talk[1]-j$talk[2])/(j$all[1]-j$all[2]))))
dv <- a %>% filter(channel=="dev1")
cat(sprintf("dev1 n=%d commands=%d mean_all=%.4f mean_talk=%.4f\n",
  nrow(dv), sum(dv$cmd=="command"), mean(dv$L,na.rm=TRUE), mean(dv$L[dv$cmd=="talk"],na.rm=TRUE)))
