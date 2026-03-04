#!/usr/bin/env python3
"""figure_12_d – Multi-source annotation distribution (reads xlsx)"""
import matplotlib; matplotlib.use("Agg")
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

OUT  = Path('../results/only_differential_expression_proteins')
XLSX = '../results/only_differential_expression_proteins/Differential_Gene_Expression_Annotations.xlsx'
STEM = 'figure_12_d'

def annot_count(row):
    return sum(pd.notna(row[c]) for c in ['BLAST_Hit','EggNOG_Description','KEGG_KO','InterProScan'])

if __name__ == '__main__':
    pm = pd.read_excel(XLSX, sheet_name='genes_UP_PmSTAT dsRNA+WSSV')
    ws = pd.read_excel(XLSX, sheet_name='genes_UP_WSSV')
    pm['ac'] = pm.apply(annot_count, axis=1)
    ws['ac'] = ws.apply(annot_count, axis=1)
    cats = ['0', '1', '2', '3', '4']
    pm_dist = [len(pm[pm['ac'] == i]) for i in range(5)]
    ws_dist = [len(ws[ws['ac'] == i]) for i in range(5)]

    x, w = np.arange(len(cats)), 0.35
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.bar(x - w/2, pm_dist, w, label='PmSTAT dsRNA+WSSV', color='blue', edgecolor='black', linewidth=1.2)
    ax.bar(x + w/2, ws_dist, w, label='WSSV',              color='red', edgecolor='black', linewidth=1.2)
    ax.set_ylabel('Number of Proteins', fontsize=12, fontweight='bold')
    ax.set_xlabel('Number of Annotation Sources', fontsize=12, fontweight='bold')
    ax.set_title('Multi-Source Annotation Distribution', fontsize=14, fontweight='bold')
    ax.set_xticks(x); ax.set_xticklabels(cats)
    ax.legend(fontsize=11); ax.grid(axis='y', alpha=0.3, linestyle='--')
    fig.tight_layout()
    fig.savefig(OUT / f'{STEM}.png', dpi=300, bbox_inches='tight')
    fig.savefig(OUT / f'{STEM}.svg', format='svg', bbox_inches='tight')
    print(f'✓ {STEM}.png / .svg'); plt.close(fig)
