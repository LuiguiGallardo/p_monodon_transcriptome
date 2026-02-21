#!/usr/bin/env python3
"""Figure08_A – Annotation type co-occurrence correlation heatmap (reads xlsx)"""
import matplotlib
matplotlib.use("Agg")
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

OUT  = Path('../results/annotation_graphics')
OUT.mkdir(parents=True, exist_ok=True)
STEM = 'figure_08_a'
XLSX = '../results/comprehensive_protein_annotations.xlsx'

ANNOTATION_COLS = {
    'BLAST':           'BLAST_Description',
    'eggNOG':          'EggNOG_Description',
    'KEGG KO':         'KEGG_KO',
    'KEGG Pathway':    'KEGG_Pathway',
    'UniProt GO-BP':   'UniProt_GO_Biological',
    'UniProt GO-CC':   'UniProt_GO_Cellular',
    'UniProt GO-MF':   'UniProt_GO_Molecular',
    'eggNOG GO-BP':    'EggNOG_GO_Biological',
    'eggNOG GO-CC':    'EggNOG_GO_Cellular',
    'eggNOG GO-MF':    'EggNOG_GO_Molecular',
    'eggNOG Domains':  'EggNOG_Domains',
    'InterPro':        'InterPro_Domains',
}

if __name__ == '__main__':
    df = pd.read_excel(XLSX, sheet_name='Protein Annotations')
    matrix = pd.DataFrame({
        label: df[col].notna().astype(int)
        for label, col in ANNOTATION_COLS.items()
        if col in df.columns
    })
    corr = matrix.corr()

    fig, ax = plt.subplots(figsize=(12, 10))
    sns.heatmap(corr, annot=True, fmt='.2f', cmap='RdYlGn',
                cbar_kws={'label': 'Correlation Coefficient'},
                vmin=0, vmax=1, square=True, linewidths=0.5, ax=ax)
    ax.set_title('Annotation Type Co-occurrence Correlation Matrix',
                 fontsize=14, fontweight='bold', pad=20)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    fig.tight_layout()
    fig.savefig(OUT / f'{STEM}.png', dpi=300, bbox_inches='tight')
    fig.savefig(OUT / f'{STEM}.svg', format='svg', bbox_inches='tight')
    print(f'✓ {STEM}.png / .svg')
    plt.close(fig)
