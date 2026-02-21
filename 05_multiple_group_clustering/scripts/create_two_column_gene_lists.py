#!/usr/bin/env python3
"""
Script to create two-column gene/isoform list files for each iteration.
Each file will have genes/isoforms from both conditions side by side.
Processes both deseq2_genes and deseq2_isoforms directories.
"""

import os
import sys
from pathlib import Path

def extract_ids(file_path):
    """Extract gene/isoform IDs from a DESeq2 results file."""
    if not os.path.exists(file_path):
        return []
    
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
        
        ids = []
        for line in lines[1:]:  # Skip header
            line = line.strip()
            if line:
                id_val = line.split('\t')[0]
                ids.append(id_val)
        
        return ids
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []

def create_two_column_file(file1, file2, output_file, header):
    """
    Create a two-column list file.
    
    Args:
        file1: Path to first condition file
        file2: Path to second condition file
        output_file: Path to output file
        header: Header line to write
    """
    ids1 = extract_ids(file1)
    ids2 = extract_ids(file2)
    
    # Determine the maximum length
    max_len = max(len(ids1), len(ids2))
    
    # Pad shorter list with empty strings
    ids1.extend([''] * (max_len - len(ids1)))
    ids2.extend([''] * (max_len - len(ids2)))
    
    # Write output file
    with open(output_file, 'w') as f_out:
        f_out.write(header + '\n')
        for id1, id2 in zip(ids1, ids2):
            f_out.write(f"{id1}\t{id2}\n")
    
    non_empty_ids1 = len([x for x in ids1 if x])
    non_empty_ids2 = len([x for x in ids2 if x])
    print(f"Created: {output_file} ({non_empty_ids1} in col1, {non_empty_ids2} in col2)")
    return non_empty_ids1 > 0 or non_empty_ids2 > 0

def process_deseq2_directory(deseq2_dir, data_type, iter_num):
    """
    Process a DESeq2 directory (genes or isoforms).
    
    Args:
        deseq2_dir: Path to deseq2_genes or deseq2_isoforms directory
        data_type: 'gene' or 'isoform'
        iter_num: Iteration number
    """
    if not deseq2_dir.exists():
        print(f"  {data_type.capitalize()} directory not found, skipping...")
        return
    
    print(f"  Processing {data_type}s...")
    
    # Comparison 1: knockdown_PmSTAT vs knockdown_P (knockdown_PmSTAT_WSSV_infection)
    for c_value in ['C2', 'C3', 'C4']:
        file1 = deseq2_dir / f"RSEM_matrix.{data_type}.counts.matrix.knockdown_PmSTAT_vs_knockdown_PmSTAT_WSSV_infection.DESeq2.DE_results.P1e-3_{c_value}.knockdown_PmSTAT-UP.subset"
        file2 = deseq2_dir / f"RSEM_matrix.{data_type}.counts.matrix.knockdown_PmSTAT_vs_knockdown_PmSTAT_WSSV_infection.DESeq2.DE_results.P1e-3_{c_value}.knockdown_PmSTAT_WSSV_infection-UP.subset"
        output_file = deseq2_dir / f"knockdown_PmSTAT_vs_knockdown_P.P1e-3_{c_value}.two_column_{data_type}s.txt"
        header = "knockdown_PmSTAT-UP\tknockdown_PmSTAT_WSSV_infection-UP"
        create_two_column_file(file1, file2, output_file, header)
    
    # Comparison 2: WSSV_infection vs knockdown_PmS (knockdown_PmSTAT)
    for c_value in ['C2', 'C3', 'C4']:
        file1 = deseq2_dir / f"RSEM_matrix.{data_type}.counts.matrix.WSSV_infection_vs_knockdown_PmSTAT.DESeq2.DE_results.P1e-3_{c_value}.knockdown_PmSTAT-UP.subset"
        file2 = deseq2_dir / f"RSEM_matrix.{data_type}.counts.matrix.WSSV_infection_vs_knockdown_PmSTAT.DESeq2.DE_results.P1e-3_{c_value}.WSSV_infection-UP.subset"
        output_file = deseq2_dir / f"WSSV_infection_vs_knockdown_PmS.P1e-3_{c_value}.two_column_{data_type}s.txt"
        header = "knockdown_PmSTAT-UP\tWSSV_infection-UP"
        create_two_column_file(file1, file2, output_file, header)
    
    # Comparison 3: WSSV_infection vs knockdown_P-1 (knockdown_PmSTAT_WSSV_infection)
    for c_value in ['C2', 'C3', 'C4']:
        file1 = deseq2_dir / f"RSEM_matrix.{data_type}.counts.matrix.WSSV_infection_vs_knockdown_PmSTAT_WSSV_infection.DESeq2.DE_results.P1e-3_{c_value}.knockdown_PmSTAT_WSSV_infection-UP.subset"
        file2 = deseq2_dir / f"RSEM_matrix.{data_type}.counts.matrix.WSSV_infection_vs_knockdown_PmSTAT_WSSV_infection.DESeq2.DE_results.P1e-3_{c_value}.WSSV_infection-UP.subset"
        output_file = deseq2_dir / f"WSSV_infection_vs_knockdown_P-1.P1e-3_{c_value}.two_column_{data_type}s.txt"
        header = "knockdown_PmSTAT_WSSV_infection-UP\tWSSV_infection-UP"
        create_two_column_file(file1, file2, output_file, header)

def process_iteration(iter_dir, iter_num):
    """Process a single iteration directory."""
    print(f"\nProcessing iteration {iter_num}...")
    
    # Process genes
    deseq2_genes_dir = iter_dir / "deseq2_genes"
    process_deseq2_directory(deseq2_genes_dir, "gene", iter_num)
    
    # Process isoforms
    deseq2_isoforms_dir = iter_dir / "deseq2_isoforms"
    process_deseq2_directory(deseq2_isoforms_dir, "isoform", iter_num)

def main():
    """Main function to process all iterations."""
    base_dir = Path(__file__).resolve().parent.parent / "results/results_iterations"
    
    if not base_dir.exists():
        print(f"Error: Base directory not found: {base_dir}")
        sys.exit(1)
    
    # Process all iterations
    for i in range(1, 41):
        iter_dir = base_dir / f"iter_{i}"
        if iter_dir.exists():
            process_iteration(iter_dir, i)
        else:
            print(f"Warning: Iteration directory not found: iter_{i}")
    
    print("\n✓ Processing complete!")

if __name__ == "__main__":
    main()
