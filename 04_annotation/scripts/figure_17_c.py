#!/usr/bin/env python3
"""figure_17_c – Signaling pathway representation PmSTAT vs WSSV, reads CSV"""
import matplotlib; matplotlib.use("Agg")
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
from pathlib import Path

OUT  = Path('../results/only_differential_expression_proteins')
STEM = 'figure_17_c'
SIGNALING = {
    'TGF-beta': ['ko04350'],
    'Wnt':      ['ko04310','ko05016'],
    'MAPK':     ['ko04010','ko04015'],
    'JAK-STAT': ['ko04630'],
    'PI3K-Akt': ['ko04151'],
    'Hippo':    ['ko04390','ko04391','ko04392'],
}

def pathway_dict(df):
    d = {}
    for s in df['KEGG_Pathway'].dropna():
        if isinstance(s, str):
            for c in set(re.findall(r'ko\d+', s)): d[c] = d.get(c, 0) + 1
    return d

if __name__ == '__main__':
    pm_p = pathway_dict(pd.read_csv('../docs/pmstat_annot.csv'))
    ws_p = pathway_dict(pd.read_csv('../docs/wssv_annot.csv'))
    names, pm_v, ws_v = [], [], []
    for path, codes in SIGNALING.items():
        pc = sum(pm_p.get(c, 0) for c in codes)
        wc = sum(ws_p.get(c, 0) for c in codes)
        if pc > 0 or wc > 0:
            names.append(path); pm_v.append(pc); ws_v.append(wc)

    fig, ax = plt.subplots(figsize=(12, 7))
    if names:
        x, w = np.arange(len(names)), 0.35
        ax.bar(x - w/2, pm_v, w, label='PmSTAT dsRNA+WSSV', color='blue', edgecolor='black', linewidth=1.2)
        ax.bar(x + w/2, ws_v, w, label='WSSV',              color='red', edgecolor='black', linewidth=1.2)
        ax.set_xticks(x); ax.set_xticklabels(names, fontsize=10)
        ax.legend(fontsize=10, loc='upper right'); ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_ylabel('Number of Proteins', fontsize=11, fontweight='bold')
    ax.set_title('Signaling Pathway Representation', fontsize=13, fontweight='bold')
    fig.tight_layout()
    fig.savefig(OUT / f'{STEM}.png', dpi=300, bbox_inches='tight')
    fig.savefig(OUT / f'{STEM}.svg', format='svg', bbox_inches='tight')
    print(f'✓ {STEM}.png / .svg'); plt.close(fig)
