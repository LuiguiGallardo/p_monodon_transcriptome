#!/usr/bin/env python3
"""Figure07_A – Protein annotation completeness distribution (reads xlsx)"""
import matplotlib
matplotlib.use("Agg")
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

OUT  = Path('../results/annotation_graphics')
OUT.mkdir(parents=True, exist_ok=True)
STEM = 'figure_07_a'
XLSX = '../results/comprehensive_protein_annotations.xlsx'

FIELDS = ['BLAST_Description','EggNOG_Description','KEGG_KO',
          'EggNOG_GO_Biological','EggNOG_GO_Molecular','EggNOG_Domains','InterPro_Domains']

if __name__ == '__main__':
    df = pd.read_excel(XLSX, sheet_name='Protein Annotations')
    df['annotation_score'] = df[FIELDS].notna().sum(axis=1)
    score_counts = df['annotation_score'].value_counts().sort_index()
    mean_s   = df['annotation_score'].mean()
    median_s = df['annotation_score'].median()

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(score_counts.index, score_counts.values,
           color=sns.color_palette('viridis', len(score_counts)), alpha=0.8, edgecolor='black')
    ax.axvline(mean_s,   color='red',   linestyle='--', linewidth=2, label=f'Mean: {mean_s:.2f}')
    ax.axvline(median_s, color='green', linestyle='--', linewidth=2, label=f'Median: {median_s:.2f}')
    ax.set_xlabel('Number of Annotation Types', fontsize=12, fontweight='bold')
    ax.set_ylabel('Number of Proteins',         fontsize=12, fontweight='bold')
    ax.set_title('Annotation Completeness Distribution', fontsize=13, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(axis='y', alpha=0.3)
    for i, v in enumerate(score_counts.values):
        ax.text(score_counts.index[i], v + 200, f'{int(v):,}',
                ha='center', fontweight='bold', fontsize=9)
    fig.tight_layout()
    fig.savefig(OUT / f'{STEM}.png', dpi=300, bbox_inches='tight')
    fig.savefig(OUT / f'{STEM}.svg', format='svg', bbox_inches='tight')
    print(f'✓ {STEM}.png / .svg')
    plt.close(fig)
