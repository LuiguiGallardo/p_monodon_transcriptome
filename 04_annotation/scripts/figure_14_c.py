#!/usr/bin/env python3
"""figure_14_c – Annotation completeness levels PmSTAT vs WSSV (reads xlsx)"""
import matplotlib; matplotlib.use("Agg")
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

OUT  = Path('../results/only_differential_expression_proteins')
XLSX = '../results/only_differential_expression_proteins/Differential_Gene_Expression_Annotations.xlsx'
STEM = 'figure_14_c'

def annot_count(row):
    return sum(pd.notna(row[c]) for c in ['BLAST_Hit','EggNOG_Description','KEGG_KO','InterProScan'])

if __name__ == '__main__':
    pm = pd.read_excel(XLSX, sheet_name='genes_UP_PmSTAT dsRNA+WSSV')
    ws = pd.read_excel(XLSX, sheet_name='genes_UP_WSSV')
    pm['ac'] = pm.apply(annot_count, axis=1)
    ws['ac'] = ws.apply(annot_count, axis=1)
    lvls = ['Unannotated', 'Partial\n(1-2 DBs)', 'Good\n(3 DBs)', 'Complete\n(4 DBs)']
    pm_c = [len(pm[pm['ac']==0]), len(pm[pm['ac'].isin([1,2])]), len(pm[pm['ac']==3]), len(pm[pm['ac']==4])]
    ws_c = [len(ws[ws['ac']==0]), len(ws[ws['ac'].isin([1,2])]), len(ws[ws['ac']==3]), len(ws[ws['ac']==4])]

    x, w = np.arange(len(lvls)), 0.35
    fig, ax = plt.subplots(figsize=(12, 7))
    b1 = ax.bar(x - w/2, pm_c, w, label='PmSTAT dsRNA+WSSV', color='#FF6B6B', edgecolor='black', linewidth=1.2)
    b2 = ax.bar(x + w/2, ws_c, w, label='WSSV',              color='#4ECDC4', edgecolor='black', linewidth=1.2)
    for bars in [b1, b2]:
        for bar in bars:
            h = bar.get_height()
            if h > 0:
                ax.text(bar.get_x() + bar.get_width()/2., h, f'{int(h)}',
                        ha='center', va='bottom', fontsize=9, fontweight='bold')
    ax.set_ylabel('Number of Proteins', fontsize=12, fontweight='bold')
    ax.set_title('Annotation Completeness Level', fontsize=14, fontweight='bold')
    ax.set_xticks(x); ax.set_xticklabels(lvls, fontsize=11)
    ax.legend(fontsize=11); ax.grid(axis='y', alpha=0.3, linestyle='--')
    fig.tight_layout()
    fig.savefig(OUT / f'{STEM}.png', dpi=300, bbox_inches='tight')
    fig.savefig(OUT / f'{STEM}.svg', format='svg', bbox_inches='tight')
    print(f'✓ {STEM}.png / .svg'); plt.close(fig)
