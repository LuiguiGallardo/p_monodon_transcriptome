#!/usr/bin/env python3
"""figure_13_c – GO term distribution PmSTAT vs WSSV (reads xlsx)"""
import matplotlib; matplotlib.use("Agg")
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

OUT  = Path('../results/only_differential_expression_proteins')
XLSX = '../results/only_differential_expression_proteins/Differential_Gene_Expression_Annotations.xlsx'
STEM = 'figure_13_c'

if __name__ == '__main__':
    pm = pd.read_excel(XLSX, sheet_name='genes_UP_PmSTAT dsRNA+WSSV')
    ws = pd.read_excel(XLSX, sheet_name='genes_UP_WSSV')
    go_types = ['Biological\nProcess', 'Molecular\nFunction', 'Cellular\nComponent']
    pm_go = [pm['GO_BP'].notna().sum(), pm['GO_MF'].notna().sum(), pm['GO_CC'].notna().sum()]
    ws_go = [ws['GO_BP'].notna().sum(), ws['GO_MF'].notna().sum(), ws['GO_CC'].notna().sum()]

    x, w = np.arange(len(go_types)), 0.35
    fig, ax = plt.subplots(figsize=(12, 7))
    b1 = ax.bar(x - w/2, pm_go, w, label='PmSTAT dsRNA+WSSV', color='blue', edgecolor='black', linewidth=1.2)
    b2 = ax.bar(x + w/2, ws_go, w, label='WSSV',              color='red', edgecolor='black', linewidth=1.2)
    for bars in [b1, b2]:
        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., h, f'{int(h)}',
                    ha='center', va='bottom', fontsize=9, fontweight='bold')
    ax.set_ylabel('Number of Proteins', fontsize=12, fontweight='bold')
    ax.set_title('Gene Ontology Distribution', fontsize=14, fontweight='bold')
    ax.set_xticks(x); ax.set_xticklabels(go_types, fontsize=11)
    ax.legend(fontsize=11); ax.grid(axis='y', alpha=0.3, linestyle='--')
    fig.tight_layout()
    fig.savefig(OUT / f'{STEM}.png', dpi=300, bbox_inches='tight')
    fig.savefig(OUT / f'{STEM}.svg', format='svg', bbox_inches='tight')
    print(f'✓ {STEM}.png / .svg'); plt.close(fig)
