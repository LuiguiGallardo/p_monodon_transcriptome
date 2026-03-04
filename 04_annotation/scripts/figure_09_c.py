#!/usr/bin/env python3
"""Figure09_C – Annotation richness levels (horizontal bar, reads xlsx)"""
import matplotlib
matplotlib.use("Agg")
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

OUT  = Path('../results/annotation_graphics')
OUT.mkdir(parents=True, exist_ok=True)
STEM = 'figure_09_c'
XLSX = '../results/comprehensive_protein_annotations.xlsx'

ANNOTATION_COLS = ['BLAST_Description','EggNOG_Description','KEGG_KO','KEGG_Pathway',
                   'UniProt_GO_Biological','UniProt_GO_Cellular','UniProt_GO_Molecular',
                   'EggNOG_GO_Biological','EggNOG_GO_Cellular','EggNOG_GO_Molecular',
                   'EggNOG_Domains','InterPro_Domains']

if __name__ == '__main__':
    df = pd.read_excel(XLSX, sheet_name='Protein Annotations')
    cols = [c for c in ANNOTATION_COLS if c in df.columns]
    scores = df[cols].notna().sum(axis=1)
    fully = df[df['EggNOG_Description'].notna() &
               df['KEGG_KO'].notna() &
               (df['EggNOG_GO_Biological'].notna() | df['EggNOG_GO_Cellular'].notna() | df['EggNOG_GO_Molecular'].notna()) &
               df['InterPro_Domains'].notna()]
    levels = {
        'Fully Annotated':       len(fully),
        'BLAST + 4+ DB':         (scores >= 5).sum(),
        'BLAST + 2-3 DB':        scores.isin([3, 4]).sum(),
        'BLAST + 1 DB':          (scores == 2).sum(),
        'Only BLAST':            0,
    }
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(list(levels.keys()), list(levels.values()),
            color=sns.color_palette('viridis', len(levels)), alpha=0.8, edgecolor='black')
    ax.set_xlabel('Number of Proteins', fontweight='bold')
    ax.set_title('Annotation Richness Levels', fontsize=13, fontweight='bold')
    ax.grid(axis='x', alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT / f'{STEM}.png', dpi=300, bbox_inches='tight')
    fig.savefig(OUT / f'{STEM}.svg', format='svg', bbox_inches='tight')
    print(f'✓ {STEM}.png / .svg')
    plt.close(fig)
