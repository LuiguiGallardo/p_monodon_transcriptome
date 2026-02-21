# BUSCO Analysis

Transcriptome assembly completeness evaluation for *Penaeus monodon* using BUSCO v5.7.1.

## Quick Start

```bash
# 1. Setup environment
cd scripts
bash 01_setup_environment.sh

# 2. Run analysis
bash 02_run_arthropoda_analysis.sh  # Primary analysis (arthropoda_odb10)
bash 03_run_metazoa_analysis.sh     # Broader comparison (metazoa_odb10)
```

## Results

- **Arthropoda (odb10)**: 89.4% complete BUSCOs ✓
- **Metazoa (odb10)**: 91.3% complete BUSCOs ✓

Both analyses demonstrate **excellent transcriptome completeness**.

## Directory Structure

```
06_busco_analysis/
├── scripts/           # Analysis scripts (numbered 01-03)
├── results/           # BUSCO results by database
├── docs/              # Detailed documentation
├── downloads/         # BUSCO database files
└── logs/              # Run logs
```

## Documentation

- **[docs/README.md](docs/README.md)** - Complete setup and usage guide
- **[docs/database_information.md](docs/database_information.md)** - Database comparison details
- **[results/comparison_summary.md](results/comparison_summary.md)** - Results summary for reviewer

## For Reviewer Response

See `results/comparison_summary.md` for the recommended text to include in your manuscript.
