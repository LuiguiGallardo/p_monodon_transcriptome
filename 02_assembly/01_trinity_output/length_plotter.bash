#!/bin/bash
echo "Calculating length distribution"
printf "read_count\tlength\n" > $1\_length.txt 
awk '/^>/ {if (seqlen){print seqlen}; print ;seqlen=0;next; } { seqlen += length($0)}END{print seqlen}' $1 | grep -v \> | sort | uniq -c | sed 's/^ *//g' | sort -k 2 -h | tr " " "\t" >> $1\_length.txt
echo "Plotting length_$1.png"
echo "file <- read.delim(file = \"$1_length.txt\")" > tmpplot.R
echo "png(\"length_$1.png\", width = 600, height = 350)" >> tmpplot.R
echo "plot(x = file\$length, y = file\$read_count, type = \"l\", main = \"Lecture length distribution $1\", xlab = \"Length\", ylab = \"Number of reads\",col = \"blue\")" >> tmpplot.R
echo "dev.off()" >> tmpplot.R
chmod +x tmpplot.R
Rscript tmpplot.R > /dev/null 2> /dev/null
echo "Removing temporary files"
rm tmpplot.R
echo "Done"
