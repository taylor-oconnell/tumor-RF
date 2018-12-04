#!/usr/bin/env bash
#
# Usage: GDC_mRNA_analysis_pipeline.sh [reads] [index] [reference]
#	[reads]: fastq or fasta file of reads (single-end)
#	[index]: STAR index for human genome (download at https://api.gdc.cancer.gov/data/50e11f67-ceb4-41f9-a73c-2a5aa9ed0af0)
#	[reference]: Reference sequence for human genome (download at https://api.gdc.cancer.gov/data/254f697d-310d-4d7d-a27b-27fbf767a834)
#


READS=$1
INDEX=$2
REF=$3


#Alignment 1st pass
STAR \
--genomeDir $INDEX \
--readFilesIn $READS \
--runThreadN 20 \
--outFilterMultimapScoreRange 1 \
--outFilterMultimapNmax 20 \
--outFilterMismatchNmax 10 \
--alignIntronMax 500000 \
--alignMatesGapMax 1000000 \
--sjdbScore 2 \
--alignSJDBoverhangMin 1 \
--genomeLoad NoSharedMemory \
--outFilterMatchNminOverLread 0.33 \
--outFilterScoreMinOverLread 0.33 \
--sjdbOverhang 100 \
--outSAMstrandField intronMotif \
--outSAMtype None \
--outSAMmode None \

#Intermediate index generation
STAR \
--runMode genomeGenerate \
--genomeDir intermediate_GRCh38_index \
--genomeFastaFiles $REF \
--sjdbOverhang 100 \
--runThreadN 20 \
--sjdbFileChrStartEnd SJ.out.tab

#Alignment 2nd pass
STAR \
--genomeDir intermediate_GRCh38_index \
--readFilesIn $READS
--runThreadN 20
--outFilterMultimapScoreRange 1
--outFilterMultimapNmax 20
--outFilterMismatchNmax 10
--alignIntronMax 500000
--alignMatesGapMax 1000000
--sjdbScore 2
--alignSJDBoverhangMin 1
--genomeLoad NoSharedMemory
--limitBAMsortRAM 0
--outFilterMatchNminOverLread 0.33
--outFilterScoreMinOverLread 0.33
--sjdbOverhang 100
--outSAMstrandField intronMotif
--outSAMattributes NH HI NM MD AS XS
--outSAMunmapped Within
--outSAMtype BAM SortedByCoordinate
--outSAMheaderHD @HD VN:1.4

#Enumerate reads mapped to genes using HTSeq
samtools view -F 4 Aligned.sortedByCoord.out.bam |
htseq-count \
-m intersection-nonempty \
-i gene_id \
-r pos \
-s no \
- gencode.v22.annotation.gtf > htseq-count_gene_counts.txt

