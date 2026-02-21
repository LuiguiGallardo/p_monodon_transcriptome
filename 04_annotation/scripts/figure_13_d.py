#!/usr/bin/env python3
"""figure_13_d – Top eggNOG functions PmSTAT vs WSSV (reads xlsx)"""
import matplotlib; matplotlib.use("Agg")
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from pathlib import Path

OUT  = Path('../results/only_differential_expression_proteins')
XLSX = '../results/only_differential_expression_proteins/Differential_Gene_Expression_Annotations.xlsx'
STEM = 'figure_13_d'

def count_funcs(df):
    counts = {}
    for func in df['EggNOG_Function'].dropna():
        for f in str(func).split(','):
            f = f.strip()
            counts[f] = counts.get(f, 0) + 1
    return counts

if __name__ == '__main__':
    pm = pd.read_excel(XLSX, sheet_name='genes_UP_PmSTAT dsRNA+WSSV')
    ws = pd.read_excel(XLSX, sheet_name='genes_UP_WSSV')
    pm_f = count_funcs(pm); ws_f = count_funcs(ws)
    top = Counter(pm_f).most_common(6)

    fig, ax = plt.subplots(figsize=(12, 7))
    if top:
        names     = [f[0][:35] for f in top]
        pm_vals   = [f[1] for f in top]
        ws_vals   = [ws_f.get(f[0], 0) for f in top]
        x, w = np.arange(len(names)), 0.35
        ax.bar(x - w/2, pm_vals, w, label='PmSTAT dsRNA+WSSV', color='#FF6B6B', edgecolor='black', linewidth=1.2)
        ax.bar(x + w/2, ws_vals, w, label='WSSV',              color='#4ECDC4', edgecolor='black', linewidth=1.2)
        ax.set_xticks(x); ax.set_xticklabels(names, rotation=45, ha='right', fontsize=9)
        ax.legend(fontsize=11); ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_ylabel('Number of Proteins', fontsize=12, fontweight='bold')
    ax.set_title('Top eggNOG Functions', fontsize=14, fontweight='bold')
    fig.tight_layout()
    fig.savefig(OUT / f'{STEM}.png', dpi=300, bbox_inches='tight')
    fig.savefig(OUT / f'{STEM}.svg', format='svg', bbox_inches='tight')
    print(f'✓ {STEM}.png / .svg'); plt.close(fig)
