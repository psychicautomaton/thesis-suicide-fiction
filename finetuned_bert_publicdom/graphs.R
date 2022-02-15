library(tidyverse)
library(ggrepel)
library(hrbrthemes)
hrbrthemes::import_roboto_condensed()
setwd('/Users/umadwivedi/Documents/Projects/YALE/senior/s1/LING 380 — neural network language models/final_project')

f <- read.csv('finetuned.csv')
g <- read.csv('generic.csv')


names(g) <- c("g_X", "g_pc1", "g_pc2", "g_word")

embeds <- cbind(f, g)


ggplot(embeds, aes(x=pc1, y=pc2)) + 
  geom_point() + 
  geom_text_repel(aes(label=word), col="white") +
  theme_ft_rc() 


ggplot(embeds, aes(x=g_pc1, y=g_pc2)) + 
  geom_point() + 
  geom_text_repel(aes(label=word), col="white") +
  theme_ft_rc() 

library(reshape2)

fin_sim <- read.csv('fin_sim.csv')
gen_sim <- read.csv('gen_sim.csv')

fs <- melt(fin_sim)
gs <- melt(gen_sim)

fs <- fs %>% group_by(X) %>%
  arrange(variable, .by_group=T)
gs <- gs %>% group_by(variable) %>%
  arrange(X, .by_group=T)

ggplot(filter(fs, X != variable), aes(X, variable)) + geom_tile(aes(fill = value)) +
  theme_ft_rc() +
  theme(axis.text.x = element_text(angle = 90),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank()) +
  scale_y_discrete(limits = sort(fin_sim$X),labels=sort(fin_sim$X))


ggplot(filter(gs, X != 0 & X != variable), aes(X, variable)) + 
  geom_tile(aes(fill = value),
            color = "white",
            lwd = .1,
            linetype = 1) +
  theme_ft_rc() +
  theme(axis.text.x.top = element_text(hjust=0),
        axis.text.x = element_text(angle = 45,
                                   margin = margin(t = .01, unit = "cm"),
                                   hjust = .9,
                                   size=rel(1)),
        axis.text.y = element_text(size=rel(1)),
        plot.title=element_text(size=rel(1.7)),
        plot.subtitle = element_text(size=rel(1.2), color="plum1"),
        axis.title.x = element_blank(),
        axis.title.y = element_blank(),
        legend.title = element_text(size=rel(1.25), color = "white"),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank()) +
  scale_y_discrete(limits = sort(fin_sim$X),labels=sort(fin_sim$X)) +
  scale_fill_continuous(low = "deepskyblue3",
                      high = "deeppink3",
                      guide = guide_colorbar(ticks=F),
                      breaks=c(.2, .7),
                      labels=c("low", "high")) +
  labs(title="Cosine Similarity of Word Embeddings", 
       fill="Similarity",
       subtitle="Generic BERT")
