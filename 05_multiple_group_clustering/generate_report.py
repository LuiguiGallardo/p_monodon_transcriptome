#!/usr/bin/env python3
"""
Script to generate a complete markdown report for all 40 iterations
following the pattern from iteration 1.
"""

def generate_iteration_section(iter_num):
    """Generate markdown section for a single iteration."""
    section = f"""### Iteration {iter_num}
#### Clustering
![results_iterations/iter_{iter_num}/deseq2_genes/diffExpr.P1e-3_C2.matrix.log2.centered.sample_cor_matrix.png](results_iterations/iter_{iter_num}/deseq2_genes/diffExpr.P1e-3_C2.matrix.log2.centered.sample_cor_matrix.png)

#### Differential expression analysis

![results_iterations/iter_{iter_num}/deseq2_genes/diffExpr.P1e-3_C2.matrix.log2.centered.genes_vs_samples_heatmap.png](results_iterations/iter_{iter_num}/deseq2_genes/diffExpr.P1e-3_C2.matrix.log2.centered.genes_vs_samples_heatmap.png)
"""
    return section

def main():
    """Generate the complete report."""
    # Start with the title
    report = "## 40 iterations of clustering\n\n"
    
    # Generate sections for all 40 iterations
    for i in range(1, 41):
        report += generate_iteration_section(i)
        if i < 40:  # Add blank line between iterations except after the last one
            report += "\n"
    
    # Write to file
    output_file = "report_40_iterations.md"
    with open(output_file, 'w') as f:
        f.write(report)
    
    print(f"Generated {output_file} with all 40 iterations")
    print(f"Total length: {len(report)} characters")

if __name__ == "__main__":
    main()
