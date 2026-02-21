#!/usr/bin/env python3
"""Figure03_B – Top 10 KEGG pathways (reads xlsx)"""
import matplotlib
matplotlib.use("Agg")
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from pathlib import Path

OUT  = Path('../results/annotation_graphics')
OUT.mkdir(parents=True, exist_ok=True)
STEM = 'figure_03_b'
XLSX = '../results/comprehensive_protein_annotations.xlsx'

if __name__ == '__main__':
    df = pd.read_excel(XLSX, sheet_name='Protein Annotations')
    pathways_list = []
    for p in df['KEGG_Pathway'].dropna():
        if isinstance(p, str):
            pathways_list.extend([x.strip() for x in p.split(',')])
    top = Counter(pathways_list).most_common(10)

    fig, ax = plt.subplots(figsize=(10, 7))
    if top:
        names  = [p[0][:15] for p in top]
        values = [p[1] for p in top]
        ax.barh(range(len(top)), values,
                color=sns.color_palette('viridis', len(top)), edgecolor='black', linewidth=1.5)
        ax.set_yticks(range(len(top)))
        ax.set_yticklabels(names, fontsize=10)
        ax.set_xlabel('Count', fontsize=11, fontweight='bold')
        ax.grid(axis='x', alpha=0.3)
        for i, v in enumerate(values):
            ax.text(v + 5, i, f'{int(v)}', va='center', fontweight='bold')
    ax.set_title('Top 10 KEGG Pathways', fontsize=13, fontweight='bold')
    fig.tight_layout()
    fig.savefig(OUT / f'{STEM}.png', dpi=300, bbox_inches='tight')
    fig.savefig(OUT / f'{STEM}.svg', format='svg', bbox_inches='tight')
    print(f'✓ {STEM}.png / .svg')
    plt.close(fig)
