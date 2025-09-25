# FASTA File Reassembly Instructions

This directory contains FASTA files that have been split into 5 parts each and compressed with gzip to comply with GitHub's file size limits.

## Split Files Information

### Trinity.fasta (Original: 778,680 sequences, 477MB)
- `file1_Trinity.fasta.gz` - 155,736 sequences (23MB compressed)
- `file2_Trinity.fasta.gz` - 155,736 sequences (27MB compressed)
- `file3_Trinity.fasta.gz` - 155,736 sequences (26MB compressed)
- `file4_Trinity.fasta.gz` - 155,736 sequences (26MB compressed)
- `file5_Trinity.fasta.gz` - 155,736 sequences (26MB compressed)

### Trinity_longest_isoform.fasta (Original: 586,928 sequences, 300MB)
- `file1_Trinity_longest_isoform.fasta.gz` - 117,386 sequences (39MB compressed)
- `file2_Trinity_longest_isoform.fasta.gz` - 117,386 sequences (19MB compressed)
- `file3_Trinity_longest_isoform.fasta.gz` - 117,386 sequences (15MB compressed)
- `file4_Trinity_longest_isoform.fasta.gz` - 117,386 sequences (12MB compressed)
- `file5_Trinity_longest_isoform.fasta.gz` - 117,384 sequences (10MB compressed)

## How to Decompress and Reassemble

### Step 1: Decompress all files
```bash
# Decompress all Trinity split files
gunzip file*_Trinity*.fasta.gz
```

### Step 2: Reassemble the original files

#### To reconstruct Trinity.fasta:
```bash
cat file1_Trinity.fasta file2_Trinity.fasta file3_Trinity.fasta file4_Trinity.fasta file5_Trinity.fasta > Trinity.fasta
```

#### To reconstruct Trinity_longest_isoform.fasta:
```bash
cat file1_Trinity_longest_isoform.fasta file2_Trinity_longest_isoform.fasta file3_Trinity_longest_isoform.fasta file4_Trinity_longest_isoform.fasta file5_Trinity_longest_isoform.fasta > Trinity_longest_isoform.fasta
```

### Alternative: One-step decompression and reassembly
```bash
# For Trinity.fasta
zcat file1_Trinity.fasta.gz file2_Trinity.fasta.gz file3_Trinity.fasta.gz file4_Trinity.fasta.gz file5_Trinity.fasta.gz > Trinity.fasta

# For Trinity_longest_isoform.fasta
zcat file1_Trinity_longest_isoform.fasta.gz file2_Trinity_longest_isoform.fasta.gz file3_Trinity_longest_isoform.fasta.gz file4_Trinity_longest_isoform.fasta.gz file5_Trinity_longest_isoform.fasta.gz > Trinity_longest_isoform.fasta
```

## Verification

After reassembly, verify the sequence counts:

```bash
# Check Trinity.fasta
grep -c "^>" Trinity.fasta
# Should return: 778680

# Check Trinity_longest_isoform.fasta  
grep -c "^>" Trinity_longest_isoform.fasta
# Should return: 586928
```

## File Checksums (for integrity verification)

You can verify file integrity using checksums if needed:

```bash
# Generate checksums for compressed split files
md5sum file*_Trinity*.fasta.gz > checksums_compressed.md5

# After decompression, generate checksums for split files
md5sum file*_Trinity*.fasta > checksums_decompressed.md5

# After reassembly, verify original files
md5sum Trinity.fasta Trinity_longest_isoform.fasta
```

## Notes

- The split was performed by sequence count to ensure similar numbers of sequences per file
- All files are compressed with gzip and well under GitHub's 100MB limit (largest is 39MB)
- Compression achieved ~66-75% size reduction
- The original large files can be safely removed once split files are confirmed working
- Files maintain FASTA format integrity - each sequence remains complete
- Use `zcat` for direct decompression-to-stdout, or `gunzip` to decompress to files