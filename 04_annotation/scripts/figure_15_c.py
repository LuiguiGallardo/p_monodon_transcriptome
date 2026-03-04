#!/usr/bin/env python3
"""figure_15_c – KEGG pathway categories comparison PmSTAT vs WSSV, reads CSV"""
import matplotlib; matplotlib.use("Agg")
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
from pathlib import Path

OUT  = Path('../results/only_differential_expression_proteins')
STEM = 'figure_15_c'
PATHWAY_CATEGORIES = {
    'Signal Transduction': ['ko04010','ko04015','ko04068','ko04110','ko04140','ko04141','ko04142',
                            'ko04144','ko04145','ko04151','ko04217','ko04310','ko04341','ko04350',
                            'ko04390','ko04510','ko04612','ko04630','ko04710','ko04919','ko04922','ko04974'],
    'Cell Processes':      ['ko04110','ko04114','ko04120','ko04141','ko04142','ko04144','ko04145',
                            'ko04217','ko04514','ko04520','ko04530','ko04810'],
    'Immune Response':     ['ko04612','ko05110','ko05134','ko05142','ko05146','ko05152','ko05162',
                            'ko05165','ko05166','ko05168','ko05169','ko05200','ko05205','ko05226'],
    'Metabolism':          ['ko00190','ko00230','ko00240','ko00310','ko00350','ko00780',
                            'ko00950','ko00965','ko01100','ko01110'],
    'Gene Expression':     ['ko03010','ko03013','ko03020','ko03040','ko03050','ko03060','ko03320','ko03410'],
}

def extract(s):
    return list(set(re.findall(r'ko\d+', str(s)))) if isinstance(s, str) else []

def pathway_dict(df):
    d = {}
    for s in df['KEGG_Pathway'].dropna():
        for c in extract(s): d[c] = d.get(c, 0) + 1
    return d

if __name__ == '__main__':
    pm = pd.read_csv('../docs/pmstat_annot.csv')
    ws = pd.read_csv('../docs/wssv_annot.csv')
    pm_p = pathway_dict(pm); ws_p = pathway_dict(ws)
    cats    = list(PATHWAY_CATEGORIES.keys())
    pm_vals = [sum(pm_p.get(c, 0) for c in PATHWAY_CATEGORIES[cat]) for cat in cats]
    ws_vals = [sum(ws_p.get(c, 0) for c in PATHWAY_CATEGORIES[cat]) for cat in cats]

    x, w = np.arange(len(cats)), 0.35
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.bar(x - w/2, pm_vals, w, label='PmSTAT dsRNA+WSSV', color='blue', edgecolor='black', linewidth=1.2)
    ax.bar(x + w/2, ws_vals, w, label='WSSV',              color='red', edgecolor='black', linewidth=1.2)
    ax.set_ylabel('Number of Proteins', fontsize=11, fontweight='bold')
    ax.set_title('KEGG Pathway Categories', fontsize=13, fontweight='bold')
    ax.set_xticks(x); ax.set_xticklabels(cats, rotation=25, ha='right', fontsize=9)
    ax.legend(fontsize=10, loc='upper right'); ax.grid(axis='y', alpha=0.3, linestyle='--')
    fig.tight_layout()
    fig.savefig(OUT / f'{STEM}.png', dpi=300, bbox_inches='tight')
    fig.savefig(OUT / f'{STEM}.svg', format='svg', bbox_inches='tight')
    print(f'✓ {STEM}.png / .svg'); plt.close(fig)
