# Reporte de calidad transcriptoma *Penaeus monodon*

## Comparación de número de lecturas entre datos crudos y limpiezas

La prueba 1 con *Trimmomatic* incluyó los siguientes parámetros:

1. Remoción de adaptadores y N's
2. Calidad por ventanas de 6 bases de longitud y Q > 20

La prueba 2 con *Trimmomatic* incluyó los siguientes parámetros:

1. Remoción de adaptadores y N's
2. Calidad promedio de todo la lectura Q > 20

No se ve que existan diferencias entre los dos tratamientos con *Trimmomatic*.

<img src="03_readcount/barplot_qual_readcount.png" alt="barplot_qual_readcount" style="zoom:100%;" />

Como se puede ver más adelante, con los dos tratamientos de calidad se mejora la calidad por base a lo largo de todas las lecturas, sin embargo no se pudo mejorar la distribución de nucleótidos al inicio y al final de las lecturas (primeras 14 bases y últimas dos bases). 

<div style="page-break-after: always; break-after: page;"></div>

## *fastqc* de los datos crudos
Ejemplo con la muestra 1_S1:

#### Calidad por base, R1 (izquierda) y R2 (derecha):
<img src="00_rawdata/01_fastqc/1_S1_R1_fastqc/Images/per_base_quality.png" alt="1_r1_per_base_quality" style="zoom:30%;" /><img src="00_rawdata/01_fastqc/1_S1_R2_fastqc/Images/per_base_quality.png" alt="1_r2_per_base_quality" style="zoom:30%;" />

#### Distribución de nucleótidos, R1 (izquierda) y R2 (derecha):
<img src="00_rawdata/01_fastqc/1_S1_R1_fastqc/Images/per_base_sequence_content.png" alt="1_r1_per_base_sequence_content" style="zoom:30%;" /><img src="00_rawdata/01_fastqc/1_S1_R2_fastqc/Images/per_base_sequence_content.png" alt="1_r2_per_base_sequence_content" style="zoom:30%;" />

#### Longitud de lecturas, R1 (izquierda) y R2 (derecha):
<img src="00_rawdata/01_fastqc/1_S1_R1_fastqc/Images/sequence_length_distribution.png" alt="1_r1_sequence_length_distribution" style="zoom:30%;" /><img src="00_rawdata/01_fastqc/1_S1_R2_fastqc/Images/sequence_length_distribution.png" alt="1_r2_sequence_length_distribution" style="zoom:30%;" />

<div style="page-break-after: always; break-after: page;"></div>

## Prueba 1 de limpieza con *Trimmomatic*

La prueba incluía lo siguientes parámetros:
1. Remoción de adaptadores y N's
2. Calidad por ventanas de 6 bases de longitud y Q > 20

Ejemplo con la muestra 1_S1:

#### Calidad por base, R1 (izquierda) y R2 (derecha)
<img src="01_trimmomatic1/1_S1_paired_R1_1_fastqc/Images/per_base_quality.png" alt="1_r1_per_base_quality" style="zoom:30%;" /><img src="01_trimmomatic1/1_S1_paired_R2_1_fastqc/Images/per_base_quality.png" alt="1_r2_per_base_quality" style="zoom:30%;" />

#### Distribución de nucleótidos, R1 (izquierda) y R2 (derecha):
<img src="01_trimmomatic1/1_S1_paired_R1_1_fastqc/Images/per_base_sequence_content.png" alt="1_r1_per_base_sequence_content" style="zoom:30%;" /><img src="01_trimmomatic1/1_S1_paired_R2_1_fastqc/Images/per_base_sequence_content.png" alt="1_r2_per_base_sequence_content" style="zoom:30%;" />

#### Longitud de lecturas, R1 (izquierda) y R2 (derecha):
<img src="01_trimmomatic1/1_S1_paired_R1_1_fastqc/Images/sequence_length_distribution.png" alt="1_r1_sequence_length_distribution" style="zoom:30%;" /><img src="01_trimmomatic1/1_S1_paired_R2_1_fastqc/Images/sequence_length_distribution.png" alt="1_r2_sequence_length_distribution" style="zoom:30%;" />

<div style="page-break-after: always; break-after: page;"></div>

## Prueba 2 de limpieza con *Trimmomatic*

La prueba incluía lo siguientes parámetros:
1. Remoción de adaptadores y N's
2. Calidad promedio Q > 20

Ejemplo con la muestra 1_S1:

#### Calidad por base, R1 (izquierda) y R2 (derecha):
<img src="02_trimmomatic2/1_S1_paired_R1_2_fastqc/Images/per_base_quality.png" alt="1_r1_per_base_quality" style="zoom:30%;" /><img src="02_trimmomatic2/1_S1_paired_R2_2_fastqc/Images/per_base_quality.png" alt="1_r2_per_base_quality" style="zoom:30%;" />

#### Distribución de nucleótidos, R1 (izquierda) y R2 (derecha):
<img src="02_trimmomatic2/1_S1_paired_R1_2_fastqc/Images/per_base_sequence_content.png" alt="1_r1_per_base_sequence_content" style="zoom:30%;" /><img src="02_trimmomatic2/1_S1_paired_R2_2_fastqc/Images/per_base_sequence_content.png" alt="1_r2_per_base_sequence_content" style="zoom:30%;" />

#### Longitud de lecturas, R1 (izquierda) y R2 (derecha):
<img src="02_trimmomatic2/1_S1_paired_R1_2_fastqc/Images/sequence_length_distribution.png" alt="1_r1_sequence_length_distribution" style="zoom:30%;" /><img src="02_trimmomatic2/1_S1_paired_R2_2_fastqc/Images/sequence_length_distribution.png" alt="1_r2_sequence_length_distribution" style="zoom:30%;" />

<div style="page-break-after: always; break-after: page;"></div>
