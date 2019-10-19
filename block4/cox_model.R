#install.packages(c("survival", "survminer"))
#install.packages(c("ggfortify","ranger"))
#install.packages("GGally")
library(survminer)
library(ggpubr)
library(magrittr)
library(survival)
library(ranger)
library(ggplot2)
library(dplyr)
library(ggfortify)
library(GGally)
require(survival)

coxdata <- read.csv("norm-stat-analysis-data.csv", header = TRUE, sep = ',')

head(coxdata)
attach(coxdata)
time <- uptime
event <- event
coxdata$event <- as.numeric(coxdata$event)



res.cox <- coxph(Surv(time, event) ~ listings_norm, data = coxdata)
res.cox
summary(res.cox)


ggsurvplot(survfit(res.cox), palette = "#2E9FDF", ggtheme = theme_minimal(), data = coxdata)



