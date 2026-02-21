#!/usr/bin/env python3
"""figure_16_c – Shared functional categories PmSTAT vs WSSV, reads CSV"""
import matplotlib; matplotlib.use("Agg")
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

OUT  = Path('../results/only_differential_expression_proteins')
STEM = 'figure_16_c'

def count_funcs(df):
    d = {}
    for func in df['EggNOG_Function'].dropna():
        for f in str(func).split(','):
            f = f.strip()
            d[f] = d.get(f, 0) + 1
    return d

if __name__ == '__main__':
    pm = pd.read_csv('../docs/pmstat_annot.csv')
    ws = pd.read_csv('../docs/wssv_annot.csv')
    pm_f = count_funcs(pm); ws_f = count_funcs(ws)
    common = list((set(pm_f.keys()) & set(ws_f.keys())))[:10]

    fig, ax = plt.subplots(figsize=(12, 7))
    if common:
        pm_c = [pm_f.get(f, 0) for f in common]
        ws_c = [ws_f.get(f, 0) for f in common]
        x, w = np.arange(len(common)), 0.35
        ax.bar(x - w/2, pm_c, w, label='PmSTAT', color='#FF6B6B', edgecolor='black', linewidth=1.2)
        ax.bar(x + w/2, ws_c, w, label='WSSV',   color='#4ECDC4', edgecolor='black', linewidth=1.2)
        ax.set_xticks(x); ax.set_xticklabels([f[:20] for f in common], rotation=45, ha='right', fontsize=8)
        ax.legend(fontsize=10); ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_ylabel('Number of Proteins', fontsize=11, fontweight='bold')
    ax.set_title('Shared Functional Categories', fontsize=13, fontweight='bold')
    fig.tight_layout()
    fig.savefig(OUT / f'{STEM}.png', dpi=300, bbox_inches='tight')
    fig.savefig(OUT / f'{STEM}.svg', format='svg', bbox_inches='tight')
    print(f'✓ {STEM}.png / .svg'); plt.close(fig)
