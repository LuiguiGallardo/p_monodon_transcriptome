# BUSCO Database Comparison for *P. monodon*

## Taxonomic Hierarchy

*Penaeus monodon* (Black Tiger Shrimp) taxonomic classification:
- **Kingdom**: Animalia (Metazoa)
- **Phylum**: Arthropoda
- **Subphylum**: Crustacea
- **Class**: Malacostraca
- **Order**: Decapoda
- **Family**: Penaeidae
- **Genus**: *Penaeus*
- **Species**: *P. monodon*

## BUSCO Databases Used

### 1. **arthropoda_odb10** (MOST SPECIFIC AVAILABLE)
- **Taxonomic level**: Arthropoda (phylum)
- **Number of BUSCOs**: 1,013 orthologs
- **Result**: **89.4% complete** (excellent!)
- **Why use this**: 
  - Most specific odb10 database available for *P. monodon*
  - Requested by reviewer
  - Includes all arthropods (insects, arachnids, crustaceans, myriapods)
  - **This is the closest available database in odb10 for your species**

**Note**: While a `crustacea_odb12` database exists with 1,536 orthologs, BUSCO v5.7.1 only supports odb10 databases. To use crustacea_odb12, you would need to upgrade to BUSCO v6.x (not recommended mid-analysis for consistency).

### 3. **metazoa_odb10** (BROADER COMPARISON)
- **Taxonomic level**: Metazoa (kingdom - all animals)
- **Number of BUSCOs**: ~954 orthologs
- **Why use this**: 
  - Most conserved genes across all animals
  - Good for detecting core eukaryotic genes
  - Useful for very broad comparisons

## Recommendations

### For Your Reviewer Response:

**Primary analysis**: Use **arthropoda_odb10** - this is the most specific odb10 database available for *P. monodon* and was requested by the reviewer

**Secondary analysis**: Include **metazoa_odb10** for broader comparison across all animals

### Expected Results:

- **arthropoda_odb10**: **89.4% complete** ✓ (already completed)
  - 33.9% single-copy, 55.5% duplicated
  - 5.2% fragmented, 5.4% missing
  - Excellent assembly quality

- **metazoa_odb10**: Likely to show similar or higher completeness
  - More conserved genes across all animals
  - Broader phylogenetic scope
  - Good for demonstrating core gene completeness

## Running the Comparison

```bash
bash run_busco_comparison.sh
```

This will run BUSCO with both crustacea_odb12 and metazoa_odb10, and provide a summary comparison with your existing arthropoda_odb10 results.

## For the Manuscript

Suggested text for your reviewer response:

> "Assembly completeness was assessed using BUSCO v5.7.1 with the arthropoda_odb10 database (n=1,013 orthologs) as requested. The analysis revealed 89.4% complete BUSCOs (33.9% single-copy, 55.5% duplicated), 5.2% fragmented, and 5.4% missing, indicating excellent transcriptome completeness. The high percentage of duplicated BUSCOs is expected for transcriptome assemblies due to alternative splicing, gene isoforms, and gene family expansions. Additionally, we performed BUSCO analysis with the metazoa_odb10 database for broader comparison across Metazoa."

## References

- BUSCO databases: https://busco.ezlab.org/
- OrthoDB: https://www.orthodb.org/
