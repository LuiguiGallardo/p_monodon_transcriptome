#!/usr/bin/env python3
"""figure_15_b – Top KEGG pathways WSSV (named), reads CSV"""
import matplotlib; matplotlib.use("Agg")
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
from pathlib import Path

OUT  = Path('../results/only_differential_expression_proteins')
STEM = 'figure_15_b'
KEGG = {
    'ko03010':'Ribosome','ko03040':'Spliceosome','ko03020':'RNA polymerase',
    'ko03410':'Base excision repair','ko03050':'Proteasome','ko04010':'MAPK signaling',
    'ko04140':'Regulation of autophagy','ko04217':'Necroptosis','ko01100':'Metabolic pathways',
    'ko04210':'Apoptosis','ko04142':'Lysosome','ko04612':'Antigen processing',
    'ko04145':'Phagosome','ko04630':'Jak-STAT signaling','ko04120':'Ubiquitin proteolysis',
    'ko04141':'Protein processing in ER','ko04310':'Wnt signaling','ko04350':'TGF-beta signaling',
    'ko04390':'Hippo signaling','ko04151':'PI3K-Akt signaling','ko04510':'Focal adhesion',
}

def extract(pathways_str):
    if not isinstance(pathways_str, str): return []
    return list(set(re.findall(r'ko\d+', pathways_str)))

if __name__ == '__main__':
    ws = pd.read_csv('../docs/wssv_annot.csv')
    paths = {}
    for p_str in ws['KEGG_Pathway'].dropna():
        for code in extract(p_str):
            paths[code] = paths.get(code, 0) + 1
    top = sorted(paths.items(), key=lambda x: x[1], reverse=True)[:10]
    names  = [KEGG.get(p[0], p[0]) for p in top]
    counts = [p[1] for p in top]

    fig, ax = plt.subplots(figsize=(12, 7))
    y = np.arange(len(names))
    bars = ax.barh(y, counts, color='#4ECDC4', edgecolor='black', linewidth=1.2)
    ax.set_yticks(y); ax.set_yticklabels(names, fontsize=9)
    ax.set_xlabel('Number of Proteins', fontsize=11, fontweight='bold')
    ax.set_title('Top KEGG Pathways – WSSV', fontsize=13, fontweight='bold')
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    for bar in bars:
        w = bar.get_width()
        ax.text(w, bar.get_y() + bar.get_height()/2., f'{int(w)}', ha='left', va='center', fontsize=9, fontweight='bold')
    fig.tight_layout()
    fig.savefig(OUT / f'{STEM}.png', dpi=300, bbox_inches='tight')
    fig.savefig(OUT / f'{STEM}.svg', format='svg', bbox_inches='tight')
    print(f'✓ {STEM}.png / .svg'); plt.close(fig)
