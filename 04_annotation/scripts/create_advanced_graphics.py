#!/usr/bin/env python3
"""
Advanced Annotation Heatmap - Shows correlations between annotation types
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def create_annotation_heatmap(xlsx_file, output_dir='../results/annotation_graphics'):
    """Create heatmap showing presence/absence correlations of annotations"""
    
    # Load data
    df_annot = pd.read_excel(xlsx_file, sheet_name='Protein Annotations')
    
    # Create binary matrix for annotation presence
    annotation_cols = {
        'BLAST': 'BLAST_Description',
        'eggNOG': 'EggNOG_Description',
        'KEGG KO': 'KEGG_KO',
        'KEGG Pathway': 'KEGG_Pathway',
        'UniProt GO-BP': 'UniProt_GO_Biological',
        'UniProt GO-CC': 'UniProt_GO_Cellular',
        'UniProt GO-MF': 'UniProt_GO_Molecular',
        'eggNOG GO-BP': 'EggNOG_GO_Biological',
        'eggNOG GO-CC': 'EggNOG_GO_Cellular',
        'eggNOG GO-MF': 'EggNOG_GO_Molecular',
        'eggNOG Domains': 'EggNOG_Domains',
        'InterPro': 'InterPro_Domains',
    }
    
    # Create binary matrix
    annotation_matrix = pd.DataFrame()
    for label, col in annotation_cols.items():
        if col in df_annot.columns:
            annotation_matrix[label] = df_annot[col].notna().astype(int)
    
    # Calculate co-occurrence matrix (correlation)
    correlation_matrix = annotation_matrix.corr()
    
    # Create heatmap
    fig, ax = plt.subplots(figsize=(12, 10))
    
    sns.heatmap(correlation_matrix, 
                annot=True, 
                fmt='.2f', 
                cmap='RdYlGn',
                cbar_kws={'label': 'Correlation Coefficient'},
                vmin=0, vmax=1,
                square=True,
                linewidths=0.5,
                ax=ax)
    
    ax.set_title('Annotation Type Co-occurrence Correlation Matrix', 
                fontsize=14, fontweight='bold', pad=20)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/08_annotation_correlation_heatmap.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: 08_annotation_correlation_heatmap.png")
    plt.savefig(f'{output_dir}/08_annotation_correlation_heatmap.svg', format='svg', bbox_inches='tight')
    print("✓ Saved: 08_annotation_correlation_heatmap.svg")
    plt.close()
    
    # Create co-occurrence statistics
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Annotation Co-occurrence Analysis', fontsize=14, fontweight='bold')
    
    # Count proteins with specific annotation combinations
    blast_eggnong = ((df_annot['BLAST_Description'].notna()) & 
                     (df_annot['EggNOG_Description'].notna())).sum()
    blast_kegg = ((df_annot['BLAST_Description'].notna()) & 
                  (df_annot['KEGG_KO'].notna())).sum()
    eggnong_kegg = ((df_annot['EggNOG_Description'].notna()) & 
                    (df_annot['KEGG_KO'].notna())).sum()
    eggnong_go = ((df_annot['EggNOG_Description'].notna()) & 
                  ((df_annot['EggNOG_GO_Biological'].notna()) |
                   (df_annot['EggNOG_GO_Cellular'].notna()) |
                   (df_annot['EggNOG_GO_Molecular'].notna()))).sum()
    interpro_eggnong = ((df_annot['InterPro_Domains'].notna()) & 
                        (df_annot['EggNOG_Description'].notna())).sum()
    interpro_kegg = ((df_annot['InterPro_Domains'].notna()) & 
                     (df_annot['KEGG_KO'].notna())).sum()
    
    # Plot 1: Co-occurrence counts
    combinations = [
        'BLAST +\neggNOG',
        'BLAST +\nKEGG',
        'eggNOG +\nKEGG',
        'eggNOG +\nGO',
        'InterPro +\neggNOG',
        'InterPro +\nKEGG'
    ]
    counts = [blast_eggnong, blast_kegg, eggnong_kegg, eggnong_go, interpro_eggnong, interpro_kegg]
    colors = sns.color_palette("husl", len(combinations))
    
    axes[0, 0].bar(range(len(combinations)), counts, color=colors, alpha=0.8, edgecolor='black')
    axes[0, 0].set_xticks(range(len(combinations)))
    axes[0, 0].set_xticklabels(combinations, fontsize=9)
    axes[0, 0].set_ylabel('Number of Proteins', fontweight='bold')
    axes[0, 0].set_title('Annotation Co-occurrence Counts', fontweight='bold')
    axes[0, 0].grid(axis='y', alpha=0.3)
    
    for i, v in enumerate(counts):
        axes[0, 0].text(i, v + 50, f'{int(v):,}', ha='center', fontweight='bold', fontsize=9)
    
    # Plot 2: Percentage with multiple annotations
    only_one = (annotation_matrix.sum(axis=1) == 1).sum()
    two_to_three = ((annotation_matrix.sum(axis=1) >= 2) & (annotation_matrix.sum(axis=1) <= 3)).sum()
    four_plus = (annotation_matrix.sum(axis=1) >= 4).sum()
    none = (annotation_matrix.sum(axis=1) == 0).sum()
    
    multi_annot = [none, only_one, two_to_three, four_plus]
    multi_labels = ['No annotations', '1 type', '2-3 types', '4+ types']
    colors_multi = ['#e74c3c', '#f39c12', '#3498db', '#2ecc71']
    
    axes[0, 1].pie(multi_annot, labels=multi_labels, autopct='%1.1f%%', colors=colors_multi)
    axes[0, 1].set_title('Proteins by Annotation Count', fontweight='bold')
    
    # Plot 3: Top annotation combinations (from fully annotated proteins)
    fully_annotated = df_annot[
        (df_annot['EggNOG_Description'].notna()) &
        (df_annot['KEGG_KO'].notna()) &
        ((df_annot['EggNOG_GO_Biological'].notna()) |
         (df_annot['EggNOG_GO_Cellular'].notna()) |
         (df_annot['EggNOG_GO_Molecular'].notna())) &
        (df_annot['InterPro_Domains'].notna())
    ]
    
    annotation_levels = {
        'Only BLAST': 0,
        'BLAST + 1 DB': (annotation_matrix[annotation_matrix.sum(axis=1) == 2].shape[0]),
        'BLAST + 2-3 DB': (annotation_matrix[annotation_matrix.sum(axis=1).isin([3, 4])].shape[0]),
        'BLAST + 4+ DB': (annotation_matrix[annotation_matrix.sum(axis=1) >= 5].shape[0]),
        'Fully Annotated': len(fully_annotated)
    }
    
    axes[1, 0].barh(list(annotation_levels.keys()), list(annotation_levels.values()),
                    color=sns.color_palette("viridis", len(annotation_levels)), alpha=0.8, edgecolor='black')
    axes[1, 0].set_xlabel('Number of Proteins', fontweight='bold')
    axes[1, 0].set_title('Annotation Richness Levels', fontweight='bold')
    axes[1, 0].grid(axis='x', alpha=0.3)
    
    # Plot 4: Annotation completeness score distribution
    df_annot['completeness_score'] = annotation_matrix.sum(axis=1)
    score_dist = df_annot['completeness_score'].value_counts().sort_index()
    
    axes[1, 1].bar(score_dist.index, score_dist.values, 
                   color=sns.color_palette("rocket", len(score_dist)), alpha=0.8, edgecolor='black')
    axes[1, 1].set_xlabel('Number of Annotation Types', fontweight='bold')
    axes[1, 1].set_ylabel('Number of Proteins', fontweight='bold')
    axes[1, 1].set_title('Annotation Completeness Score Distribution', fontweight='bold')
    axes[1, 1].grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/09_cooccurrence_analysis.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: 09_cooccurrence_analysis.png")
    plt.savefig(f'{output_dir}/09_cooccurrence_analysis.svg', format='svg', bbox_inches='tight')
    print("✓ Saved: 09_cooccurrence_analysis.svg")
    plt.close()


if __name__ == '__main__':
    import sys
    
    xlsx_file = '../results/comprehensive_protein_annotations.xlsx'
    output_dir = '../results/annotation_graphics'
    
    if len(sys.argv) > 1:
        xlsx_file = sys.argv[1]
    if len(sys.argv) > 2:
        output_dir = sys.argv[2]
    
    print("\nCreating advanced heatmap visualizations...")
    create_annotation_heatmap(xlsx_file, output_dir)
    print("\n✓ Advanced visualizations completed!\n")
