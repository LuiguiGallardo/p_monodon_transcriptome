#!/usr/bin/env python3
"""
BUSCO Results Visualization Script
Creates publication-quality bar plots for BUSCO analysis results with detailed labels
and generates a CSV summary table.
"""

import re
import csv
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

# BUSCO color scheme (official colors)
COLORS = {
    'complete_single': '#56B4E9',  # Light blue
    'complete_duplicated': '#3373ba',  # Dark blue
    'fragmented': '#F0E442',  # Yellow
    'missing': '#E74C3C'  # Red
}

def parse_busco_summary(summary_file):
    """Parse BUSCO short_summary.txt file to extract raw counts"""
    with open(summary_file, 'r') as f:
        content = f.read()
    
    # Extract lineage
    lineage_match = re.search(r'lineage dataset is: (\S+)', content)
    lineage = lineage_match.group(1) if lineage_match else "Unknown"

    # Extract counts using regex looking for lines like "905     Complete BUSCOs (C)"
    # We use regex to be robust against whitespace
    def get_count(pattern):
        match = re.search(pattern, content)
        return int(match.group(1)) if match else 0

    total = get_count(r'(\d+)\s+Total BUSCO groups searched')
    complete = get_count(r'(\d+)\s+Complete BUSCOs \(C\)')
    single = get_count(r'(\d+)\s+Complete and single-copy BUSCOs \(S\)')
    duplicated = get_count(r'(\d+)\s+Complete and duplicated BUSCOs \(D\)')
    fragmented = get_count(r'(\d+)\s+Fragmented BUSCOs \(F\)')
    missing = get_count(r'(\d+)\s+Missing BUSCOs \(M\)')

    # Calculate percentages for plotting
    return {
        'lineage': lineage,
        'total': total,
        'complete': complete,
        'single': single,
        'duplicated': duplicated,
        'fragmented': fragmented,
        'missing': missing,
        # Percentages
        'pct_single': (single / total) * 100,
        'pct_duplicated': (duplicated / total) * 100,
        'pct_fragmented': (fragmented / total) * 100,
        'pct_missing': (missing / total) * 100,
    }

def create_busco_plot(data_list, labels, output_file, title="BUSCO Assessment"):
    """
    Create a horizontal stacked bar plot for BUSCO results with detailed labels inside bars.
    """
    fig, ax = plt.subplots(figsize=(10, 2 + len(data_list) * 0.8))
    
    y_pos = range(len(labels))
    
    # Plot stacked bars
    for i, (data, label) in enumerate(zip(data_list, labels)):
        left = 0
        
        # Complete single-copy (light blue)
        ax.barh(i, data['pct_single'], left=left, height=0.6,
                color=COLORS['complete_single'], edgecolor='white', linewidth=0)
        left += data['pct_single']
        
        # Complete duplicated (dark blue)
        ax.barh(i, data['pct_duplicated'], left=left, height=0.6,
                color=COLORS['complete_duplicated'], edgecolor='white', linewidth=0)
        left += data['pct_duplicated']
        
        # Fragmented (yellow)
        ax.barh(i, data['pct_fragmented'], left=left, height=0.6,
                color=COLORS['fragmented'], edgecolor='white', linewidth=0)
        left += data['pct_fragmented']
        
        # Missing (red)
        ax.barh(i, data['pct_missing'], left=left, height=0.6,
                color=COLORS['missing'], edgecolor='white', linewidth=0)

        # Create the label string: C:750 [S:715, D:35], F:9, M:241, n:1000
        label_text = f"C:{data['complete']} [S:{data['single']}, D:{data['duplicated']}], F:{data['fragmented']}, M:{data['missing']}, n:{data['total']}"
        
        # Add text label centered in the bar area
        # We place it at x=50% (middle of plot)
        ax.text(50, i, label_text, ha='center', va='center', fontsize=10, fontweight='bold', color='black')

    # Customize plot
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=11)
    ax.set_xlabel('%BUSCOs', fontsize=12, fontweight='bold')
    ax.set_xlim(0, 100)
    
    # Remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(1.5)
    ax.spines['bottom'].set_linewidth(1.5)
    
    # Remove title
    # ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    
    # Create legend with official text
    legend_elements = [
        mpatches.Patch(facecolor=COLORS['complete_single'], label='Complete (C) and single-copy (S)'),
        mpatches.Patch(facecolor=COLORS['complete_duplicated'], label='Complete (C) and duplicated (D)'),
        mpatches.Patch(facecolor=COLORS['fragmented'], label='Fragmented (F)'),
        mpatches.Patch(facecolor=COLORS['missing'], label='Missing (M)')
    ]
    
    # Legend placement similar to official plots (top center/right)
    ax.legend(handles=legend_elements, loc='lower center', bbox_to_anchor=(0.5, 1.05),
             frameon=False, fontsize=9, ncol=2)
    
    plt.tight_layout()
    plt.subplots_adjust(top=0.85) # Make room for legend and title
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Plot saved to: {output_file}")
    plt.close()

def save_csv_table(data_list, labels, output_file):
    """Save BUSCO results to a CSV file"""
    headers = ['Sample', 'Lineage', 'Total_BUSCOs', 'Complete_BUSCOs', 'Complete_Single', 'Complete_Duplicated', 'Fragmented', 'Missing']
    
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        
        for data, label in zip(data_list, labels):
            # Clean label to match sample name if needed (remove " (n=...)")
            sample_name = label.split(' (')[0]
            writer.writerow([
                sample_name,
                data['lineage'],
                data['total'],
                data['complete'],
                data['single'],
                data['duplicated'],
                data['fragmented'],
                data['missing']
            ])
    print(f"✓ Table saved to: {output_file}")

def main():
    # Define paths
    results_dir = Path("../results")
    figures_dir = results_dir / "figures"
    figures_dir.mkdir(exist_ok=True)
    
    # Parse both BUSCO results
    print("Parsing BUSCO results...")
    
    # Original Transcriptome
    arthropoda_file = results_dir / "arthropoda_odb10" / "short_summary.specific.arthropoda_odb10.busco_p_monodon.txt"
    metazoa_file = results_dir / "metazoa_odb10" / "short_summary.specific.metazoa_odb10.busco_p_monodon_metazoa_odb10.txt"
    
    # Longest Isoforms
    arthropoda_iso_file = results_dir / "arthropoda_longest_isoform" / "short_summary.specific.arthropoda_odb10.arthropoda_longest_isoform.txt"
    metazoa_iso_file = results_dir / "metazoa_longest_isoform" / "short_summary.specific.metazoa_odb10.metazoa_longest_isoform.txt"

    # Load Data
    arthropoda_data = parse_busco_summary(arthropoda_file)
    metazoa_data = parse_busco_summary(metazoa_file)
    
    # We use try-except for the new files in case they haven't run yet
    has_isoforms = False
    try:
        arthropoda_iso_data = parse_busco_summary(arthropoda_iso_file)
        metazoa_iso_data = parse_busco_summary(metazoa_iso_file)
        has_isoforms = True
    except FileNotFoundError:
        print("Warning: Longest isoform results not found. Skipping them.")
    
    print(f"✓ Arthropoda (Full): {arthropoda_data['complete']} complete (n={arthropoda_data['total']})")
    print(f"✓ Metazoa (Full): {metazoa_data['complete']} complete (n={metazoa_data['total']})")
    if has_isoforms:
        print(f"✓ Arthropoda (1-Isoform): {arthropoda_iso_data['complete']} complete (n={arthropoda_iso_data['total']})")
        print(f"✓ Metazoa (1-Isoform): {metazoa_iso_data['complete']} complete (n={metazoa_iso_data['total']})")

    # Create comparison plot
    print("\nGenerating comprehensive comparison plot...")
    
    # Prepare data for comparison
    all_data = [arthropoda_data, metazoa_data]
    all_labels = ["Arthropoda (Full)", "Metazoa (Full)"]
    
    if has_isoforms:
        all_data.extend([arthropoda_iso_data, metazoa_iso_data])
        all_labels.extend(["Arthropoda (1-Isoform)", "Metazoa (1-Isoform)"])

    create_busco_plot(
        all_data,
        all_labels,
        figures_dir / "busco_comparison.png",
        "BUSCO Assessment Results"
    )

    # Save CSV table
    print("\nGenerating table...")
    save_csv_table(
        all_data,
        all_labels,
        figures_dir / "busco_results.csv"
    )
    
    print("\n" + "="*50)
    print("All outputs generated successfully!")
    print("="*50)
    print(f"\nOutputs saved in: {figures_dir}/")
    print("  - busco_arthropoda.png")
    print("  - busco_metazoa.png")
    print("  - busco_comparison.png")
    print("  - busco_results.csv")

if __name__ == "__main__":
    main()
