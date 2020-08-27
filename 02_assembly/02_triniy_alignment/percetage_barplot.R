#!/usr/bin/env Rscript
## Purpose of script: percetage aligned barplot
## Date created: 26.08.2020
## Author: luigui gallardo-becerra (bfllg77@gmail.com)
# Package installation
library(ggplot2)
library(ggpubr)
library(reshape)
# Input table
table <- read.table(file = "./percentage_aligned.txt",
    header = TRUE,
    sep = "\t")
table <- melt(table, id = c("sample"))
# Plot
barplot_percentage_aligned <- ggplot(data = table) +
geom_col(aes(x = sample,
    y = value),
    position = 'dodge') +
labs(x = "",
    y = "Percetage aligned",
    fill = "") +
scale_x_discrete(expand = c(0, 0)) +
scale_y_continuous(expand = c(0, 0),
    limits  = c(0, 101)) +
theme_test() +
theme(text = element_text(size = 12),
    axis.text.x = element_text(size = 7,
        angle = 0)) +
theme(legend.position = "none")
# Create .pdf
pdf(file = "barplot_percentage_aligned.pdf", width = 7.5, height = 7.5)
print(barplot_percentage_aligned)
dev.off()
# Create png
png(file = "barplot_percentage_aligned.png", width = 500, height = 500)
print(barplot_percentage_aligned)
dev.off()
