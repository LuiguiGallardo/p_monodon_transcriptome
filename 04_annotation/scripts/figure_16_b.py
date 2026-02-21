#!/usr/bin/env python3
"""figure_16_b – Functional categories WSSV (EggNOG_Function), reads CSV"""
import matplotlib; matplotlib.use("Agg")
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

OUT  = Path('../results/only_differential_expression_proteins')
STEM = 'figure_16_b'

if __name__ == '__main__':
    ws = pd.read_csv('../docs/wssv_annot.csv')
    funcs = {}
    for func in ws['EggNOG_Function'].dropna():
        for f in str(func).split(','):
            f = f.strip()
            funcs[f] = funcs.get(f, 0) + 1
    top = sorted(funcs.items(), key=lambda x: x[1], reverse=True)[:10]
    names  = [f[0][:40] for f in top]
    counts = [f[1] for f in top]

    fig, ax = plt.subplots(figsize=(12, 7))
    y = np.arange(len(names))
    bars = ax.barh(y, counts, color='#4ECDC4', edgecolor='black', linewidth=1.2)
    ax.set_yticks(y); ax.set_yticklabels(names, fontsize=9)
    ax.set_xlabel('Number of Proteins', fontsize=11, fontweight='bold')
    ax.set_title('Functional Categories – WSSV', fontsize=13, fontweight='bold')
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    for bar in bars:
        w = bar.get_width()
        ax.text(w, bar.get_y() + bar.get_height()/2., f'{int(w)}', ha='left', va='center', fontsize=8, fontweight='bold')
    fig.tight_layout()
    fig.savefig(OUT / f'{STEM}.png', dpi=300, bbox_inches='tight')
    fig.savefig(OUT / f'{STEM}.svg', format='svg', bbox_inches='tight')
    print(f'✓ {STEM}.png / .svg'); plt.close(fig)
