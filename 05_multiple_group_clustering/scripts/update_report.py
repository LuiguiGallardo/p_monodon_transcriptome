#!/usr/bin/env python3
"""
Script to update the report with metadata tables and formatted images
"""

import os
import re

# Read all metadata files
base_dir = os.path.dirname(os.path.abspath(__file__))
metadata_dir = os.path.join(base_dir, "..", "metadata", "metadata_iterations")
report_file = os.path.join(base_dir, "..", "results", "report_40_iterations.md")

def read_metadata(iteration_num):
    """Read metadata file for a given iteration and extract groups and sample IDs"""
    metadata_file = os.path.join(metadata_dir, f"metadata_trinity_iter_{iteration_num}.txt")
    
    groups = {}
    with open(metadata_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('\t')
            if len(parts) >= 2:
                group = parts[0]
                sample_id = parts[1]
                if group not in groups:
                    groups[group] = []
                groups[group].append(sample_id)
    
    return groups

def create_metadata_table(groups):
    """Create a markdown table from groups and sample IDs"""
    table = "| Group | Sample IDs |\n"
    table += "|-------|------------|\n"
    
    for group, samples in groups.items():
        samples_str = ", ".join(samples)
        table += f"| {group} | {samples_str} |\n"
    
    return table

# Generate the updated report
output_lines = ["## Iterations of clustering\n\n"]

for i in range(1, 41):
    # Read metadata for this iteration
    groups = read_metadata(i)
    
    # Add iteration header
    output_lines.append(f"### Iteration {i}\n\n")
    
    # Add metadata table
    output_lines.append("#### Metadata\n\n")
    output_lines.append(create_metadata_table(groups))
    output_lines.append("\n")
    
    # Add clustering section with resized image
    output_lines.append("#### Clustering\n\n")
    img_path = f"results_iterations/iter_{i}/deseq2_genes/diffExpr.P1e-3_C2.matrix.log2.centered.sample_cor_matrix.png"
    output_lines.append(f'<img src="{img_path}" width="50%">\n\n')
    
    # Add differential expression section with resized image
    output_lines.append("#### Differential expression analysis\n\n")
    img_path = f"results_iterations/iter_{i}/deseq2_genes/diffExpr.P1e-3_C2.matrix.log2.centered.genes_vs_samples_heatmap.png"
    output_lines.append(f'<img src="{img_path}" width="50%">\n\n')
    
    # Add page break after each iteration (except the last one)
    if i < 40:
        output_lines.append('<div style="page-break-after: always;"></div>\n\n')

# Write the updated report
with open(report_file, 'w') as f:
    f.writelines(output_lines)

print(f"Report updated successfully! Check {report_file}")
