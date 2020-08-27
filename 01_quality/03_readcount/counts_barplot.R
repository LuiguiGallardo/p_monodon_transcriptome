#!/usr/bin/env Rscript
## Purpose of script: read counts barplot
## Date created: 13.07.2020
## Author: luigui gallardo-becerra (bfllg77@gmail.com)
# Package installation #
library(ggplot2)
library(ggpubr)
library(reshape)
# Input table #
table <- read.table(file = "readcount_quality.txt",
    header = TRUE,
    sep = "\t")
table <- melt(table, id = c("sample"))
# Plot #
table$variable <- factor(table$variable,
    levels = c("raw_data", "quality_1", "quality_2"))
barplot_qual_readcount <- ggplot(data = table) +
geom_col(aes(x = sample,
    y = value,
    fill = variable),
    position = 'dodge') +
labs(x = "",
    y = "Number of reads",
    fill = "") +
scale_x_discrete(expand = c(0, 0)) +
scale_y_continuous(expand = c(0, 0),
    limits  = c(0, 45000000)) +
theme_test() +
theme(text = element_text(size = 12),
    axis.text.x = element_text(size = 7,
        angle = 0))
#theme(legend.position = "none")
# Create .pdf #
pdf(file = "barplot_qual_readcount.pdf", width = 7.5, height = 7.5)
print(barplot_qual_readcount)
dev.off()
# Create png #
png(file = "barplot_qual_readcount.png", width = 500, height = 500)
print(barplot_qual_readcount)
dev.off()
