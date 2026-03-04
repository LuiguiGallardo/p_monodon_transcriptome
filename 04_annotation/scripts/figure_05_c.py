#!/usr/bin/env python3
"""Figure05_C – Overall GO term coverage (pie chart, reads xlsx)"""
import matplotlib
matplotlib.use("Agg")
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

OUT  = Path('../results/annotation_graphics')
OUT.mkdir(parents=True, exist_ok=True)
STEM = 'figure_05_c'
XLSX = '../results/comprehensive_protein_annotations.xlsx'

if __name__ == '__main__':
    df = pd.read_excel(XLSX, sheet_name='Protein Annotations')
    with_go = len(df[df['EggNOG_GO_Biological'].notna() |
                     df['EggNOG_GO_Cellular'].notna()  |
                     df['EggNOG_GO_Molecular'].notna()])
    total = len(df)
    pct_with = with_go / total * 100

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie([with_go, total - with_go],
           labels=[f'With GO Terms\n({pct_with:.1f}%)',
                   f'Without GO Terms\n({100-pct_with:.1f}%)'],
           autopct='%1.1f%%', colors=['#1abc9c', '#bdc3c7'],
           textprops={'fontsize': 11, 'fontweight': 'bold'})
    ax.set_title('Overall GO Term Coverage', fontsize=13, fontweight='bold', pad=20)
    fig.tight_layout()
    fig.savefig(OUT / f'{STEM}.png', dpi=300, bbox_inches='tight')
    fig.savefig(OUT / f'{STEM}.svg', format='svg', bbox_inches='tight')
    print(f'✓ {STEM}.png / .svg')
    plt.close(fig)
