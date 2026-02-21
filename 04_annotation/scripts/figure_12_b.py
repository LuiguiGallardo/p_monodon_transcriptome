#!/usr/bin/env python3
"""figure_12_b – DB coverage percentages (reads xlsx)"""
import matplotlib; matplotlib.use("Agg")
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

OUT  = Path('../results/only_differential_expression_proteins')
XLSX = '../results/only_differential_expression_proteins/Differential_Gene_Expression_Annotations.xlsx'
STEM = 'figure_12_b'

if __name__ == '__main__':
    pm = pd.read_excel(XLSX, sheet_name='genes_UP_PmSTAT dsRNA+WSSV')
    ws = pd.read_excel(XLSX, sheet_name='genes_UP_WSSV')
    dbs  = ['BLAST', 'eggNOG', 'KEGG', 'InterProScan']
    cols = ['BLAST_Hit', 'EggNOG_Description', 'KEGG_KO', 'InterProScan']
    pm_pct = [pm[c].notna().sum() / len(pm) * 100 for c in cols]
    ws_pct = [ws[c].notna().sum() / len(ws) * 100 for c in cols]

    x, w = np.arange(len(dbs)), 0.35
    fig, ax = plt.subplots(figsize=(12, 7))
    b1 = ax.bar(x - w/2, pm_pct, w, label='PmSTAT dsRNA+WSSV', color='#FF6B6B', edgecolor='black', linewidth=1.2)
    b2 = ax.bar(x + w/2, ws_pct, w, label='WSSV',              color='#4ECDC4', edgecolor='black', linewidth=1.2)
    for bars in [b1, b2]:
        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., h, f'{h:.0f}%',
                    ha='center', va='bottom', fontsize=9, fontweight='bold')
    ax.set_ylabel('Coverage (%)', fontsize=12, fontweight='bold')
    ax.set_title('Database Coverage Percentages', fontsize=14, fontweight='bold')
    ax.set_xticks(x); ax.set_xticklabels(dbs); ax.set_ylim([0, 105])
    ax.legend(fontsize=11); ax.grid(axis='y', alpha=0.3, linestyle='--')
    fig.tight_layout()
    fig.savefig(OUT / f'{STEM}.png', dpi=300, bbox_inches='tight')
    fig.savefig(OUT / f'{STEM}.svg', format='svg', bbox_inches='tight')
    print(f'✓ {STEM}.png / .svg'); plt.close(fig)
