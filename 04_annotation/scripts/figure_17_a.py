#!/usr/bin/env python3
"""figure_17_a – Immune & defense pathway comparison PmSTAT vs WSSV, reads CSV"""
import matplotlib; matplotlib.use("Agg")
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
from pathlib import Path

OUT  = Path('../results/only_differential_expression_proteins')
STEM = 'figure_17_a'
IMMUNE = {
    'Immune Recognition': ['ko05152','ko05162','ko05226','ko05169'],
    'Signal Transduction': ['ko04010','ko04140','ko04145','ko04217'],
    'Protein Quality':     ['ko04142','ko03050','ko04120'],
    'Apoptosis':           ['ko04210','ko04214'],
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
    cats    = list(IMMUNE.keys())
    pm_vals = [sum(pm_p.get(c, 0) for c in IMMUNE[cat]) for cat in cats]
    ws_vals = [sum(ws_p.get(c, 0) for c in IMMUNE[cat]) for cat in cats]

    x, w = np.arange(len(cats)), 0.35
    fig, ax = plt.subplots(figsize=(12, 7))
    b1 = ax.bar(x - w/2, pm_vals, w, label='PmSTAT dsRNA+WSSV', color='#FF6B6B', edgecolor='black', linewidth=1.2)
    b2 = ax.bar(x + w/2, ws_vals, w, label='WSSV',              color='#4ECDC4', edgecolor='black', linewidth=1.2)
    for bars in [b1, b2]:
        for bar in bars:
            h = bar.get_height()
            if h > 0:
                ax.text(bar.get_x() + bar.get_width()/2., h, f'{int(h)}',
                        ha='center', va='bottom', fontsize=9, fontweight='bold')
    ax.set_ylabel('Number of Proteins', fontsize=11, fontweight='bold')
    ax.set_title('Immune & Defense Pathways', fontsize=13, fontweight='bold')
    ax.set_xticks(x); ax.set_xticklabels(cats, fontsize=10)
    ax.legend(fontsize=10, loc='upper right'); ax.grid(axis='y', alpha=0.3, linestyle='--')
    fig.tight_layout()
    fig.savefig(OUT / f'{STEM}.png', dpi=300, bbox_inches='tight')
    fig.savefig(OUT / f'{STEM}.svg', format='svg', bbox_inches='tight')
    print(f'✓ {STEM}.png / .svg'); plt.close(fig)
