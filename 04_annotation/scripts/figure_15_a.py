#!/usr/bin/env python3
"""figure_15_a – Top KEGG pathways PmSTAT (named), reads CSV"""
import matplotlib; matplotlib.use("Agg")
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
from pathlib import Path

OUT   = Path('../results/only_differential_expression_proteins')
STEM  = 'figure_15_a'
from kegg_names import pathway_label

OUT   = Path('../results/only_differential_expression_proteins')
STEM  = 'figure_15_a'

def extract(pathways_str):
    if not isinstance(pathways_str, str): return []
    return list(set(re.findall(r'ko\d+', pathways_str)))

if __name__ == '__main__':
    pm = pd.read_csv('../docs/pmstat_annot.csv')
    paths = {}
    for p_str in pm['KEGG_Pathway'].dropna():
        for code in extract(p_str):
            paths[code] = paths.get(code, 0) + 1
    top = sorted(paths.items(), key=lambda x: x[1], reverse=True)[:10]
    names  = [pathway_label(p[0]) for p in top]
    counts = [p[1] for p in top]

    fig, ax = plt.subplots(figsize=(5, 7))
    y = np.arange(len(names))
    bars = ax.barh(y, counts, color='blue', edgecolor='black', linewidth=1.2)
    ax.set_yticks(y); ax.set_yticklabels(names, fontsize=9)
    ax.invert_yaxis()
    ax.set_xlabel('Number of Proteins', fontsize=11, fontweight='bold')
    ax.set_title('Top KEGG Pathways – PmSTAT dsRNA+WSSV', fontsize=13, fontweight='bold')
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    fig.tight_layout()
    fig.savefig(OUT / f'{STEM}.png', dpi=300, bbox_inches='tight')
    fig.savefig(OUT / f'{STEM}.svg', format='svg', bbox_inches='tight')
    print(f'✓ {STEM}.png / .svg'); plt.close(fig)
