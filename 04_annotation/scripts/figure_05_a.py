#!/usr/bin/env python3
"""Figure05_A – GO term comparison: eggNOG vs UniProt (reads xlsx)"""
import matplotlib
matplotlib.use("Agg")
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

OUT  = Path('../results/annotation_graphics')
OUT.mkdir(parents=True, exist_ok=True)
STEM = 'figure_05_a'
XLSX = '../results/comprehensive_protein_annotations.xlsx'

if __name__ == '__main__':
    df = pd.read_excel(XLSX, sheet_name='Protein Annotations')
    eggnog = [df['EggNOG_GO_Biological'].notna().sum(),
              df['EggNOG_GO_Cellular'].notna().sum(),
              df['EggNOG_GO_Molecular'].notna().sum()]
    uniprot = [df['UniProt_GO_Biological'].notna().sum(),
               df['UniProt_GO_Cellular'].notna().sum(),
               df['UniProt_GO_Molecular'].notna().sum()]
    types = ['Biological Process', 'Cellular Component', 'Molecular Function']
    x, w = np.arange(len(types)), 0.35

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(x - w/2, eggnog,  w, label='eggNOG',  color='#3498db', alpha=0.8, edgecolor='black', linewidth=1.5)
    ax.bar(x + w/2, uniprot, w, label='UniProt', color='#e74c3c', alpha=0.8, edgecolor='black', linewidth=1.5)
    ax.set_ylabel('Count', fontsize=11, fontweight='bold')
    ax.set_title('GO Term Distribution: eggNOG vs UniProt', fontsize=13, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(types, rotation=15, ha='right')
    ax.legend(fontsize=11)
    ax.grid(axis='y', alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT / f'{STEM}.png', dpi=300, bbox_inches='tight')
    fig.savefig(OUT / f'{STEM}.svg', format='svg', bbox_inches='tight')
    print(f'✓ {STEM}.png / .svg')
    plt.close(fig)
