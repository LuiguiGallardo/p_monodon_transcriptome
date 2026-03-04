#!/usr/bin/env python3
"""figure_18_a – Top KEGG pathways PmSTAT vs WSSV (reads CSVs)"""
import matplotlib; matplotlib.use("Agg")
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
from collections import Counter
from pathlib import Path
from kegg_names import pathway_label

OUT   = Path('../results/only_differential_expression_proteins')
STEM  = 'figure_18_a'

def extract(pathways_str):
    if not isinstance(pathways_str, str): return []
    return list(set(re.findall(r'ko\d+', pathways_str)))

def count_kegg(df):
    paths = {}
    for p_str in df['KEGG_Pathway'].dropna():
        for code in extract(p_str):
            paths[code] = paths.get(code, 0) + 1
    return paths

if __name__ == '__main__':
    pm = pd.read_csv('../docs/pmstat_annot.csv')
    ws = pd.read_csv('../docs/wssv_annot.csv')
    
    pm_f = count_kegg(pm)
    ws_f = count_kegg(ws)
    
    top_pm = [k for k, v in Counter(pm_f).most_common(10)]
    top_ws = [k for k, v in Counter(ws_f).most_common(10)]
    all_keys = set(top_pm) | set(top_ws)
    all_keys = sorted(list(all_keys), key=lambda k: (pm_f.get(k, 0), ws_f.get(k, 0)), reverse=True)

    fig, ax = plt.subplots(figsize=(14, 8))
    if all_keys:
        names     = [pathway_label(k)[:40] for k in all_keys]
        pm_vals   = [pm_f.get(k, 0) for k in all_keys]
        ws_vals   = [ws_f.get(k, 0) for k in all_keys]
        
        x, w = np.arange(len(names)), 0.35
        ax.bar(x - w/2, pm_vals, w, label='PmSTAT dsRNA+WSSV', color='blue', edgecolor='black', linewidth=1.2)
        ax.bar(x + w/2, ws_vals, w, label='WSSV',              color='red', edgecolor='black', linewidth=1.2)
        
        ax.set_xticks(x)
        ax.set_xticklabels(names, rotation=45, ha='right', fontsize=9)
        ax.legend(fontsize=11)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        
    ax.set_ylabel('Number of Proteins', fontsize=12, fontweight='bold')
    ax.set_title('Top KEGG Pathways', fontsize=14, fontweight='bold')
    fig.tight_layout()
    fig.savefig(OUT / f'{STEM}.png', dpi=300, bbox_inches='tight')
    fig.savefig(OUT / f'{STEM}.svg', format='svg', bbox_inches='tight')
    print(f'✓ {STEM}.png / .svg')
    plt.close(fig)
