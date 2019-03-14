#==================================================#
#========= pre-registered analysis script =========#
#==== for music/language congruency experiment ====#
#==================================================#
# By Courtney Hilton, June/July, 2018

#==================================================#
#============== data and packages =================#
#==================================================#
if(!require(dplyr)){install.packages('dplyr')}
if(!require(ggplot2)){install.packages('ggplot2')}
if(!require(stringr)){install.packages('stringr')}
if(!require(ez)){install.packages('ez')}
library(dplyr)
library(ggplot2)
library(stringr)
library(ez)
library(tidyverse)
library(lme4)
setwd("/Users/courtneyhilton/Research/PhD/Exp2/Data/")


# create tibble for analysis
data_list <- list()

for (i in 1:40) {
  # creating filename string
  index    <- toString(i)
  index    <- str_pad(index, 3, pad = "0") # creates 001 out of 1
  filename <- paste(index, "trial_log.txt", sep = "") # joins 001 to trial_log
  # load trial data into variable
  trial_data          <- read_delim(filename, delim = "\t")
  trial_data$Sentence <- as.character(trial_data$Sentence)
  trial_data$Probe    <- as.character(trial_data$Probe)
  trial_data$Accuracy <- as.numeric(trial_data$Accuracy)
  trial_data$subnum   <- i
  #trial_data$subnum   <- as.factor(trial_data$subnum)
  
  # create subset variables
  data_for_analysis <- trial_data %>%
    filter(Sentence_extraction != "assorted") %>% # filtering out 'other'/distractor trials 
    mutate(RT = if_else(RT > 5.0, true = 5.0, false = RT)) # dealing with outliers
  data_list[[i]] <- data_for_analysis 
}

selected_data <- bind_rows(data_list) # big structure of all trials for all participants

# filter out outlier RTs and convert to log-scale

participant_avg <- selected_data %>%
  group_by(subnum, Congruency, Sentence_extraction, Probe_clause) %>%
  summarise(sub_acc = mean(Accuracy), avg_RT = mean(RT), max_rt = max(RT), min_rt = min(RT) )
  
group_avg <- participant_avg %>%
  group_by(Congruency, Sentence_extraction, Probe_clause) %>%
  summarise(group_acc = mean(sub_acc), group_sd = sd(sub_acc), group_RT = mean(avg_RT), group_max_rt = max(max_rt), group_min_rt = min(min_rt), group_rt_sd = sd(avg_RT), Acc_se = group_sd/sqrt(40), RT_se = group_rt_sd/sqrt(40) )

test <- selected_data %>%
  group_by(Congruency, Sentence_extraction, Probe_clause) %>%
  summarise(Acc = mean(Accuracy), avg_RT = mean(RT), max_rt = max(RT), min_rt = min(RT), Acc_sd = sd(Accuracy), Acc_se = Acc_sd/sqrt(40))

test2 <- selected_data %>%
  group_by(subnum, Congruency, Sentence_extraction) %>%
  summarise(Acc = mean(Accuracy), avg_RT = mean(RT), max_rt = max(RT), min_rt = min(RT), AccSd = sd(Accuracy), RT_sd = sd(RT))


  




# for RTs, reject outliers

# rescale RTs on log-scale
#==================================================#
#============ Calculating stats etc ===============#
#==================================================#

lmeTest <- glmer(Accuracy ~ Congruency * Sentence_extraction + Probe_clause +
                   (1|subnum) + (1|Sentence), family = 'binomial', data = selected_data) #need to account for probe clause  + (1 + Congruency * Sentence_extraction|subnum)

# (1 + Congruency * Sentence_extraction|Probe_clause)

ggplot(group_avg, aes(x= Sentence_extraction, y = group_acc, fill = Congruency)) + 
  geom_boxplot() +
  facet_grid(. ~Sentence_extraction)

ggplot(participant_avg, aes(x = Sentence_extraction, y = sub_acc)) +
  geom_jitter(size = 2, shape = 21) + 
  facet_grid(. ~ Congruency)



ggplot(group_avg, aes(x = Sentence_extraction, y = group_acc, fill = Congruency, ymin = group_acc - Acc_se, ymax = group_acc + Acc_se)) +
  geom_bar(stat = "identity", position = "dodge") +
  coord_cartesian(ylim=c(.5,1)) +
  geom_errorbar(position = position_dodge(width = .9), width = .2) + 
  xlab("Relative-clause extraction") + 
  ylab("Percentage correct") +
  facet_grid(. ~ Probe_clause)
  
ggplot(group_avg, aes(x = Sentence_extraction, y = group_RT, fill = Congruency, ymin = group_RT - RT_se, ymax = group_RT + RT_se)) +
  geom_bar(stat = "identity", position = "dodge") +
  coord_cartesian(ylim=c(1.5,3)) +
  geom_errorbar(position = position_dodge(width = .9), width = .2) + 
  xlab("Relative-clause extraction") + 
  ylab("Reaction time")  +
  facet_grid(. ~ Probe_clause)

ggplot(test2, aes(x = Sentence_extraction, y = Acc, fill = Congruency)) +
  geom_bar(position = "dodge", stat = "identity") + 
  geom_errorbar(aes(ymin = Acc - Acc_sd, ymax = Acc + Acc_sd))

test_anova <- aov(trial_data$Accuracy ~ trial_data$Congruency)