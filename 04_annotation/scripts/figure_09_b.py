#!/usr/bin/env python3
"""Figure09_B – Proteins by annotation count (pie chart, reads xlsx)"""
import matplotlib
matplotlib.use("Agg")
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

OUT  = Path('../results/annotation_graphics')
OUT.mkdir(parents=True, exist_ok=True)
STEM = 'figure_09_b'
XLSX = '../results/comprehensive_protein_annotations.xlsx'

ANNOTATION_COLS = ['BLAST_Description','EggNOG_Description','KEGG_KO','KEGG_Pathway',
                   'UniProt_GO_Biological','UniProt_GO_Cellular','UniProt_GO_Molecular',
                   'EggNOG_GO_Biological','EggNOG_GO_Cellular','EggNOG_GO_Molecular',
                   'EggNOG_Domains','InterPro_Domains']

if __name__ == '__main__':
    df = pd.read_excel(XLSX, sheet_name='Protein Annotations')
    cols = [c for c in ANNOTATION_COLS if c in df.columns]
    scores = df[cols].notna().sum(axis=1)

    none      = (scores == 0).sum()
    one       = (scores == 1).sum()
    two_three = ((scores >= 2) & (scores <= 3)).sum()
    four_plus = (scores >= 4).sum()

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie([none, one, two_three, four_plus],
           labels=['No annotations', '1 type', '2-3 types', '4+ types'],
           autopct='%1.1f%%',
           colors=['#e74c3c', '#f39c12', '#3498db', '#2ecc71'])
    ax.set_title('Proteins by Annotation Count', fontsize=13, fontweight='bold', pad=20)
    fig.tight_layout()
    fig.savefig(OUT / f'{STEM}.png', dpi=300, bbox_inches='tight')
    fig.savefig(OUT / f'{STEM}.svg', format='svg', bbox_inches='tight')
    print(f'✓ {STEM}.png / .svg')
    plt.close(fig)
