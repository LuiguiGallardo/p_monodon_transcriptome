#!/usr/bin/env python3
"""Figure06_B – eggNOG feature combinations (bar chart, reads xlsx)"""
import matplotlib
matplotlib.use("Agg")
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

OUT  = Path('../results/annotation_graphics')
OUT.mkdir(parents=True, exist_ok=True)
STEM = 'figure_06_b'
XLSX = '../results/comprehensive_protein_annotations.xlsx'

if __name__ == '__main__':
    df = pd.read_excel(XLSX, sheet_name='Protein Annotations')
    with_go = len(df[df['EggNOG_GO_Biological'].notna() |
                     df['EggNOG_GO_Cellular'].notna()  |
                     df['EggNOG_GO_Molecular'].notna()])
    categories = [
        ('eggNOG Only',     9313 - with_go),
        ('eggNOG + GO',     with_go),
        ('eggNOG + Domains', df['EggNOG_Domains'].notna().sum()),
        ('All Features',    0),
    ]
    labels, counts = zip(*categories)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(range(len(labels)), counts,
           color=sns.color_palette('Set2', len(categories)), alpha=0.8, edgecolor='black', linewidth=1.5)
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=30, ha='right')
    ax.set_ylabel('Count', fontsize=11, fontweight='bold')
    ax.set_title('eggNOG Feature Combinations', fontsize=13, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    for i, cnt in enumerate(counts):
        ax.text(i, cnt + 100, f'{int(cnt):,}', ha='center', fontweight='bold')
    fig.tight_layout()
    fig.savefig(OUT / f'{STEM}.png', dpi=300, bbox_inches='tight')
    fig.savefig(OUT / f'{STEM}.svg', format='svg', bbox_inches='tight')
    print(f'✓ {STEM}.png / .svg')
    plt.close(fig)
