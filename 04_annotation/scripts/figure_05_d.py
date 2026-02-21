#!/usr/bin/env python3
"""Figure05_D – eggNOG GO terms by domain stats (horizontal bar, reads xlsx)"""
import matplotlib
matplotlib.use("Agg")
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

OUT  = Path('../results/annotation_graphics')
OUT.mkdir(parents=True, exist_ok=True)
STEM = 'figure_05_d'
XLSX = '../results/comprehensive_protein_annotations.xlsx'

if __name__ == '__main__':
    df = pd.read_excel(XLSX, sheet_name='Protein Annotations')
    domain_stats = {
        'Biological\nProcess': df['EggNOG_GO_Biological'].notna().sum(),
        'Cellular\nComponent': df['EggNOG_GO_Cellular'].notna().sum(),
        'Molecular\nFunction': df['EggNOG_GO_Molecular'].notna().sum(),
    }
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(list(domain_stats.keys()), list(domain_stats.values()),
            color=['#2ecc71', '#f39c12', '#9b59b6'], alpha=0.8, edgecolor='black', linewidth=1.5)
    ax.set_xlabel('Count', fontsize=11, fontweight='bold')
    ax.set_title('eggNOG GO Terms by Domain', fontsize=13, fontweight='bold')
    ax.grid(axis='x', alpha=0.3)
    for i, v in enumerate(domain_stats.values()):
        ax.text(v + 100, i, f'{int(v):,}', va='center', fontweight='bold')
    fig.tight_layout()
    fig.savefig(OUT / f'{STEM}.png', dpi=300, bbox_inches='tight')
    fig.savefig(OUT / f'{STEM}.svg', format='svg', bbox_inches='tight')
    print(f'✓ {STEM}.png / .svg')
    plt.close(fig)
