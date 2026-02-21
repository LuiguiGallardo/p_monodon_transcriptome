#!/usr/bin/env python3
"""figure_13_a – Top KEGG pathways for PmSTAT dsRNA+WSSV (reads xlsx)"""
import matplotlib; matplotlib.use("Agg")
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from pathlib import Path

OUT  = Path('../results/only_differential_expression_proteins')
XLSX = '../results/only_differential_expression_proteins/Differential_Gene_Expression_Annotations.xlsx'
STEM = 'figure_13_a'

def top_pathways(df, n=8):
    paths = []
    for p in df['KEGG_Pathway'].dropna():
        if isinstance(p, str):
            paths.extend([x.strip() for x in str(p).split(';')])
    return Counter(paths).most_common(n)

if __name__ == '__main__':
    pm  = pd.read_excel(XLSX, sheet_name='genes_UP_PmSTAT dsRNA+WSSV')
    top = top_pathways(pm)
    names  = [p[0][:40] for p in top]
    counts = [p[1] for p in top]

    fig, ax = plt.subplots(figsize=(12, 8))
    y = np.arange(len(names))
    ax.barh(y, counts, color='#FF6B6B', edgecolor='black', linewidth=1.2)
    ax.set_yticks(y); ax.set_yticklabels(names, fontsize=10)
    ax.set_xlabel('Count', fontsize=12, fontweight='bold')
    ax.set_title('Top KEGG Pathways – PmSTAT dsRNA+WSSV', fontsize=14, fontweight='bold')
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    for i, v in enumerate(counts):
        ax.text(v + 0.1, i, f'{int(v)}', va='center', fontweight='bold')
    fig.tight_layout()
    fig.savefig(OUT / f'{STEM}.png', dpi=300, bbox_inches='tight')
    fig.savefig(OUT / f'{STEM}.svg', format='svg', bbox_inches='tight')
    print(f'✓ {STEM}.png / .svg'); plt.close(fig)
