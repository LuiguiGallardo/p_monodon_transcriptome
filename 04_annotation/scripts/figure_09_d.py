#!/usr/bin/env python3
"""Figure09_D – Annotation completeness score distribution (bar chart, reads xlsx)"""
import matplotlib
matplotlib.use("Agg")
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

OUT  = Path('../results/annotation_graphics')
OUT.mkdir(parents=True, exist_ok=True)
STEM = 'figure_09_d'
XLSX = '../results/comprehensive_protein_annotations.xlsx'

ANNOTATION_COLS = ['BLAST_Description','EggNOG_Description','KEGG_KO','KEGG_Pathway',
                   'UniProt_GO_Biological','UniProt_GO_Cellular','UniProt_GO_Molecular',
                   'EggNOG_GO_Biological','EggNOG_GO_Cellular','EggNOG_GO_Molecular',
                   'EggNOG_Domains','InterPro_Domains']

if __name__ == '__main__':
    df = pd.read_excel(XLSX, sheet_name='Protein Annotations')
    cols = [c for c in ANNOTATION_COLS if c in df.columns]
    df['completeness_score'] = df[cols].notna().sum(axis=1)
    dist = df['completeness_score'].value_counts().sort_index()

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(dist.index, dist.values,
           color=sns.color_palette('rocket', len(dist)), alpha=0.8, edgecolor='black')
    ax.set_xlabel('Number of Annotation Types', fontweight='bold')
    ax.set_ylabel('Number of Proteins',         fontweight='bold')
    ax.set_title('Annotation Completeness Score Distribution', fontsize=13, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT / f'{STEM}.png', dpi=300, bbox_inches='tight')
    fig.savefig(OUT / f'{STEM}.svg', format='svg', bbox_inches='tight')
    print(f'✓ {STEM}.png / .svg')
    plt.close(fig)
