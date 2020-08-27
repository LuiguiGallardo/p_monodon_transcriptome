#!/bin/bash
# Quality filtering with Trimmomatic 1
# remove of adapters
# sliding window of 6, Q > 20
echo "#!/bin/bash" > script_trimmomatic_exec_1.sh
for s in $(cat sampleslist.txt)  ;
    do echo trimmomatic-0.36.jar PE -phred33 $s\_R1.fastq.gz $s\_R2.fastq.gz $s\_paired_R1_1.fastq.gz $s\_unpaired_R1_1.fastq.gz $s\_paired_R2_1.fastq.gz $s\_unpaired_R2_1.fastq.gz ILLUMINACLIP:/home/luigui/apps/Trimmomatic-0.36/adapters/TruSeq2-PE.fa:2:30:10 SLIDINGWINDOW:6:20 \& ;
done >> script_trimmomatic_exec_1.sh
echo "wait" >> script_trimmomatic_exec_1.sh
# Execute
nohup sh script_trimmomatic_exec_1.sh > nohup_script_trimmomatic_exec_1.sh
mkdir 01_exec_1 ; mv *paired*fastq.gz 01_exec_1
# Quality filtering with Trimmomatic 2
# remove of adapters
# average quality Q > 20
echo "#!/bin/bash" > script_trimmomatic_exec_2.sh
for s in $(cat sampleslist.txt)  ;
    do echo trimmomatic-0.36.jar PE -phred33 $s\_R1.fastq.gz $s\_R2.fastq.gz $s\_paired_R1_2.fastq.gz $s\_unpaired_R1_2.fastq.gz $s\_paired_R2_2.fastq.gz $s\_unpaired_R2_2.fastq.gz ILLUMINACLIP:/home/luigui/apps/Trimmomatic-0.36/adapters/TruSeq2-PE.fa:2:30:10 AVGQUAL:20 \& ;
done >> script_trimmomatic_exec_2.sh
echo "wait" >> script_trimmomatic_exec_2.sh
# Execute
nohup sh script_trimmomatic_exec_2.sh > nohup_script_trimmomatic_exec_2.sh
mkdir 02_exec_2 ; mv *paired*fastq.gz 02_exec_2
