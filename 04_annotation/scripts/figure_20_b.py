#!/usr/bin/env python3
"""figure_20_b – Top eggNOG functions WSSV (reads xlsx)"""
import matplotlib; matplotlib.use("Agg")
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from pathlib import Path

OUT  = Path('../results/only_differential_expression_proteins')
XLSX = '../results/only_differential_expression_proteins/Differential_Gene_Expression_Annotations.xlsx'
STEM = 'figure_20_b'

def count_funcs(df):
    counts = {}
    for func in df['EggNOG_Function'].dropna():
        for f in str(func).split(','):
            f = f.strip()
            counts[f] = counts.get(f, 0) + 1
    return counts

if __name__ == '__main__':
    ws = pd.read_excel(XLSX, sheet_name='genes_UP_WSSV')
    ws_f = count_funcs(ws)
    top = sorted(ws_f.items(), key=lambda x: x[1], reverse=True)[:10]
    
    names  = [f[0][:40] for f in top]
    counts = [f[1] for f in top]

    fig, ax = plt.subplots(figsize=(5, 7))
    y = np.arange(len(names))
    bars = ax.barh(y, counts, color='red', edgecolor='black', linewidth=1.2)
    ax.set_yticks(y)
    ax.set_yticklabels(names, fontsize=9)
    ax.invert_yaxis()
    ax.set_xlabel('Number of Proteins', fontsize=11, fontweight='bold')
    ax.set_title('Top eggNOG Functions – WSSV', fontsize=13, fontweight='bold')
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    
    fig.tight_layout()
    fig.savefig(OUT / f'{STEM}.png', dpi=300, bbox_inches='tight')
    fig.savefig(OUT / f'{STEM}.svg', format='svg', bbox_inches='tight')
    print(f'✓ {STEM}.png / .svg')
    plt.close(fig)
