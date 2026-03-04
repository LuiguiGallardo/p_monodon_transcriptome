#!/usr/bin/env python3
"""figure_12_c – Annotation statistics table (reads xlsx)"""
import matplotlib; matplotlib.use("Agg")
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

OUT  = Path('../results/only_differential_expression_proteins')
XLSX = '../results/only_differential_expression_proteins/Differential_Gene_Expression_Annotations.xlsx'
STEM = 'figure_12_c'

if __name__ == '__main__':
    pm = pd.read_excel(XLSX, sheet_name='genes_UP_PmSTAT dsRNA+WSSV')
    ws = pd.read_excel(XLSX, sheet_name='genes_UP_WSSV')
    cols = ['BLAST_Hit', 'EggNOG_Description', 'KEGG_KO', 'InterProScan']
    dbs  = ['BLAST', 'eggNOG', 'KEGG', 'InterProScan']
    pm_c = [pm[c].notna().sum() for c in cols]
    ws_c = [ws[c].notna().sum() for c in cols]
    pm_p = [v / len(pm) * 100 for v in pm_c]
    ws_p = [v / len(ws) * 100 for v in ws_c]

    rows = [['Database', 'PmSTAT dsRNA+WSSV', 'WSSV']] + [
        [d, f'{pc} ({pp:.1f}%)', f'{wc} ({wp:.1f}%)']
        for d, pc, pp, wc, wp in zip(dbs, pm_c, pm_p, ws_c, ws_p)
    ]
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.axis('off')
    tbl = ax.table(cellText=rows, cellLoc='center', loc='center', colWidths=[0.3, 0.35, 0.35])
    tbl.auto_set_font_size(False); tbl.set_fontsize(11); tbl.scale(1, 2.5)
    for i in range(len(rows)):
        for j in range(3):
            cell = tbl[(i, j)]
            if i == 0:
                cell.set_facecolor('#44546A'); cell.set_text_props(weight='bold', color='white')
            elif i % 2 == 0:
                cell.set_facecolor('#E7E6E6')
    ax.set_title('Annotation Statistics', fontsize=14, fontweight='bold', pad=20)
    fig.tight_layout()
    fig.savefig(OUT / f'{STEM}.png', dpi=300, bbox_inches='tight')
    fig.savefig(OUT / f'{STEM}.svg', format='svg', bbox_inches='tight')
    print(f'✓ {STEM}.png / .svg'); plt.close(fig)
