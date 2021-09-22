#!/bin/bash
# Title: script_trimmomatic.sh
# Purpose: Quality filters with trimmomatic
# Author: Luigui Gallardo-Becerra (bfllg77@gmail.com)
# Date: 03.09.2021

# Beginning of the script
trimmomatic-0.36.jar PE -phred33 1_S1_R1.fastq.gz 1_S1_R2.fastq.gz 1_S1_paired_R1_2.fastq.gz 1_S1_unpaired_R1_2.fastq.gz 1_S1_paired_R2_2.fastq.gz 1_S1_unpaired_R2_2.fastq.gz ILLUMINACLIP:/home/luigui/apps/Trimmomatic-0.36/adapters/TruSeq2-PE.fa:2:30:10 AVGQUAL:20 &
trimmomatic-0.36.jar PE -phred33 2_S2_R1.fastq.gz 2_S2_R2.fastq.gz 2_S2_paired_R1_2.fastq.gz 2_S2_unpaired_R1_2.fastq.gz 2_S2_paired_R2_2.fastq.gz 2_S2_unpaired_R2_2.fastq.gz ILLUMINACLIP:/home/luigui/apps/Trimmomatic-0.36/adapters/TruSeq2-PE.fa:2:30:10 AVGQUAL:20
trimmomatic-0.36.jar PE -phred33 3_S3_R1.fastq.gz 3_S3_R2.fastq.gz 3_S3_paired_R1_2.fastq.gz 3_S3_unpaired_R1_2.fastq.gz 3_S3_paired_R2_2.fastq.gz 3_S3_unpaired_R2_2.fastq.gz ILLUMINACLIP:/home/luigui/apps/Trimmomatic-0.36/adapters/TruSeq2-PE.fa:2:30:10 AVGQUAL:20 &
trimmomatic-0.36.jar PE -phred33 4_S4_R1.fastq.gz 4_S4_R2.fastq.gz 4_S4_paired_R1_2.fastq.gz 4_S4_unpaired_R1_2.fastq.gz 4_S4_paired_R2_2.fastq.gz 4_S4_unpaired_R2_2.fastq.gz ILLUMINACLIP:/home/luigui/apps/Trimmomatic-0.36/adapters/TruSeq2-PE.fa:2:30:10 AVGQUAL:20 &
trimmomatic-0.36.jar PE -phred33 5_S5_R1.fastq.gz 5_S5_R2.fastq.gz 5_S5_paired_R1_2.fastq.gz 5_S5_unpaired_R1_2.fastq.gz 5_S5_paired_R2_2.fastq.gz 5_S5_unpaired_R2_2.fastq.gz ILLUMINACLIP:/home/luigui/apps/Trimmomatic-0.36/adapters/TruSeq2-PE.fa:2:30:10 AVGQUAL:20 &
trimmomatic-0.36.jar PE -phred33 6_S6_R1.fastq.gz 6_S6_R2.fastq.gz 6_S6_paired_R1_2.fastq.gz 6_S6_unpaired_R1_2.fastq.gz 6_S6_paired_R2_2.fastq.gz 6_S6_unpaired_R2_2.fastq.gz ILLUMINACLIP:/home/luigui/apps/Trimmomatic-0.36/adapters/TruSeq2-PE.fa:2:30:10 AVGQUAL:20 &
trimmomatic-0.36.jar PE -phred33 7_S7_R1.fastq.gz 7_S7_R2.fastq.gz 7_S7_paired_R1_2.fastq.gz 7_S7_unpaired_R1_2.fastq.gz 7_S7_paired_R2_2.fastq.gz 7_S7_unpaired_R2_2.fastq.gz ILLUMINACLIP:/home/luigui/apps/Trimmomatic-0.36/adapters/TruSeq2-PE.fa:2:30:10 AVGQUAL:20 &
trimmomatic-0.36.jar PE -phred33 8_S8_R1.fastq.gz 8_S8_R2.fastq.gz 8_S8_paired_R1_2.fastq.gz 8_S8_unpaired_R1_2.fastq.gz 8_S8_paired_R2_2.fastq.gz 8_S8_unpaired_R2_2.fastq.gz ILLUMINACLIP:/home/luigui/apps/Trimmomatic-0.36/adapters/TruSeq2-PE.fa:2:30:10 AVGQUAL:20 &
trimmomatic-0.36.jar PE -phred33 9_S9_R1.fastq.gz 9_S9_R2.fastq.gz 9_S9_paired_R1_2.fastq.gz 9_S9_unpaired_R1_2.fastq.gz 9_S9_paired_R2_2.fastq.gz 9_S9_unpaired_R2_2.fastq.gz ILLUMINACLIP:/home/luigui/apps/Trimmomatic-0.36/adapters/TruSeq2-PE.fa:2:30:10 AVGQUAL:20 &
trimmomatic-0.36.jar PE -phred33 10_S10_R1.fastq.gz 10_S10_R2.fastq.gz 10_S10_paired_R1_2.fastq.gz 10_S10_unpaired_R1_2.fastq.gz 10_S10_paired_R2_2.fastq.gz 10_S10_unpaired_R2_2.fastq.gz ILLUMINACLIP:/home/luigui/apps/Trimmomatic-0.36/adapters/TruSeq2-PE.fa:2:30:10 AVGQUAL:20 &
trimmomatic-0.36.jar PE -phred33 11_S11_R1.fastq.gz 11_S11_R2.fastq.gz 11_S11_paired_R1_2.fastq.gz 11_S11_unpaired_R1_2.fastq.gz 11_S11_paired_R2_2.fastq.gz 11_S11_unpaired_R2_2.fastq.gz ILLUMINACLIP:/home/luigui/apps/Trimmomatic-0.36/adapters/TruSeq2-PE.fa:2:30:10 AVGQUAL:20 &
trimmomatic-0.36.jar PE -phred33 12_S12_R1.fastq.gz 12_S12_R2.fastq.gz 12_S12_paired_R1_2.fastq.gz 12_S12_unpaired_R1_2.fastq.gz 12_S12_paired_R2_2.fastq.gz 12_S12_unpaired_R2_2.fastq.gz ILLUMINACLIP:/home/luigui/apps/Trimmomatic-0.36/adapters/TruSeq2-PE.fa:2:30:10 AVGQUAL:20 &
wait

# The end!

