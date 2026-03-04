#!/usr/bin/env python3
"""figure_14_d – Summary statistics table PmSTAT vs WSSV (reads xlsx)"""
import matplotlib; matplotlib.use("Agg")
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

OUT  = Path('../results/only_differential_expression_proteins')
XLSX = '../results/only_differential_expression_proteins/Differential_Gene_Expression_Annotations.xlsx'
STEM = 'figure_14_d'

def annot_count(row):
    return sum(pd.notna(row[c]) for c in ['BLAST_Hit','EggNOG_Description','KEGG_KO','InterProScan'])

if __name__ == '__main__':
    pm = pd.read_excel(XLSX, sheet_name='genes_UP_PmSTAT dsRNA+WSSV')
    ws = pd.read_excel(XLSX, sheet_name='genes_UP_WSSV')
    pm['ac'] = pm.apply(annot_count, axis=1)
    ws['ac'] = ws.apply(annot_count, axis=1)
    pm_dom = pm['InterProScan'].notna().sum()
    ws_dom = ws['InterProScan'].notna().sum()
    pm_full = len(pm[pm['ac']==4]); ws_full = len(ws[ws['ac']==4])

    rows = [
        ['Feature', 'PmSTAT dsRNA+WSSV', 'WSSV'],
        ['Total Proteins', str(len(pm)), str(len(ws))],
        ['Avg Annots/Protein', f'{pm["ac"].mean():.2f}', f'{ws["ac"].mean():.2f}'],
        ['With InterProScan', f'{pm_dom} ({pm_dom/len(pm)*100:.1f}%)', f'{ws_dom} ({ws_dom/len(ws)*100:.1f}%)'],
        ['Fully Annotated', f'{pm_full} ({pm_full/len(pm)*100:.1f}%)', f'{ws_full} ({ws_full/len(ws)*100:.1f}%)'],
    ]
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.axis('off')
    tbl = ax.table(cellText=rows, cellLoc='left', loc='center', colWidths=[0.4, 0.3, 0.3])
    tbl.auto_set_font_size(False); tbl.set_fontsize(11); tbl.scale(1, 2.5)
    for i in range(len(rows)):
        for j in range(3):
            cell = tbl[(i, j)]
            if i == 0:
                cell.set_facecolor('#44546A'); cell.set_text_props(weight='bold', color='white')
            elif i % 2 == 0:
                cell.set_facecolor('#E7E6E6')
    ax.set_title('Summary Statistics', fontsize=14, fontweight='bold', pad=20)
    fig.tight_layout()
    fig.savefig(OUT / f'{STEM}.png', dpi=300, bbox_inches='tight')
    fig.savefig(OUT / f'{STEM}.svg', format='svg', bbox_inches='tight')
    print(f'✓ {STEM}.png / .svg'); plt.close(fig)
