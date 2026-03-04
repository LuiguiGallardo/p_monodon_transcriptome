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
    
    cat_counts = [(cat, sum(pm_p.get(c, 0) for c in IMMUNE[cat])) for cat in IMMUNE.keys()]
    cat_counts.sort(key=lambda x: x[1], reverse=True)
    cat_counts = cat_counts[:10]
    
    cats = [x[0] for x in cat_counts]
    pm_vals = [x[1] for x in cat_counts]

    fig, ax = plt.subplots(figsize=(5, 7))
    y = np.arange(len(cats))
    bars = ax.barh(y, pm_vals, color='blue', edgecolor='black', linewidth=1.2)
    ax.set_yticks(y); ax.set_yticklabels(cats, fontsize=10)
    ax.invert_yaxis()
    ax.set_xlabel('Number of Proteins', fontsize=11, fontweight='bold')
    ax.set_title('Immune & Defense Pathways – PmSTAT dsRNA+WSSV', fontsize=10, fontweight='bold')
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    fig.tight_layout()
    fig.savefig(OUT / f'{STEM}.png', dpi=300, bbox_inches='tight')
    fig.savefig(OUT / f'{STEM}.svg', format='svg', bbox_inches='tight')
    print(f'✓ {STEM}.png / .svg'); plt.close(fig)
