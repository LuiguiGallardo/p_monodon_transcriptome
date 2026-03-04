#!/usr/bin/env python3
"""Figure09_A – Annotation co-occurrence counts (bar chart, reads xlsx)"""
import matplotlib
matplotlib.use("Agg")
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

OUT  = Path('../results/annotation_graphics')
OUT.mkdir(parents=True, exist_ok=True)
STEM = 'figure_09_a'
XLSX = '../results/comprehensive_protein_annotations.xlsx'

if __name__ == '__main__':
    df = pd.read_excel(XLSX, sheet_name='Protein Annotations')
    combos = {
        'BLAST +\neggNOG':   (df['BLAST_Description'].notna() & df['EggNOG_Description'].notna()).sum(),
        'BLAST +\nKEGG':     (df['BLAST_Description'].notna() & df['KEGG_KO'].notna()).sum(),
        'eggNOG +\nKEGG':   (df['EggNOG_Description'].notna() & df['KEGG_KO'].notna()).sum(),
        'eggNOG +\nGO':     (df['EggNOG_Description'].notna() &
                              (df['EggNOG_GO_Biological'].notna() |
                               df['EggNOG_GO_Cellular'].notna()  |
                               df['EggNOG_GO_Molecular'].notna())).sum(),
        'InterPro +\neggNOG': (df['InterPro_Domains'].notna() & df['EggNOG_Description'].notna()).sum(),
        'InterPro +\nKEGG':  (df['InterPro_Domains'].notna() & df['KEGG_KO'].notna()).sum(),
    }
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(range(len(combos)), list(combos.values()),
           color=sns.color_palette('husl', len(combos)), alpha=0.8, edgecolor='black')
    ax.set_xticks(range(len(combos)))
    ax.set_xticklabels(list(combos.keys()), fontsize=9)
    ax.set_ylabel('Number of Proteins', fontweight='bold')
    ax.set_title('Annotation Co-occurrence Counts', fontsize=13, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    for i, v in enumerate(combos.values()):
        ax.text(i, v + 50, f'{int(v):,}', ha='center', fontweight='bold', fontsize=9)
    fig.tight_layout()
    fig.savefig(OUT / f'{STEM}.png', dpi=300, bbox_inches='tight')
    fig.savefig(OUT / f'{STEM}.svg', format='svg', bbox_inches='tight')
    print(f'✓ {STEM}.png / .svg')
    plt.close(fig)
