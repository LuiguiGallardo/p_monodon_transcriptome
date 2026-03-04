#!/usr/bin/env python3
"""Figure05_B – eggNOG GO term types distribution (pie chart, reads xlsx)"""
import matplotlib
matplotlib.use("Agg")
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

OUT  = Path('../results/annotation_graphics')
OUT.mkdir(parents=True, exist_ok=True)
STEM = 'figure_05_b'
XLSX = '../results/comprehensive_protein_annotations.xlsx'

if __name__ == '__main__':
    df = pd.read_excel(XLSX, sheet_name='Protein Annotations')
    data = [df['EggNOG_GO_Biological'].notna().sum(),
            df['EggNOG_GO_Cellular'].notna().sum(),
            df['EggNOG_GO_Molecular'].notna().sum()]
    labels = ['Biological\nProcess', 'Cellular\nComponent', 'Molecular\nFunction']

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie(data, labels=labels, autopct='%1.1f%%',
           colors=['#2ecc71', '#f39c12', '#9b59b6'],
           textprops={'fontsize': 11, 'fontweight': 'bold'})
    ax.set_title('eggNOG GO Term Types Distribution', fontsize=13, fontweight='bold', pad=20)
    fig.tight_layout()
    fig.savefig(OUT / f'{STEM}.png', dpi=300, bbox_inches='tight')
    fig.savefig(OUT / f'{STEM}.svg', format='svg', bbox_inches='tight')
    print(f'✓ {STEM}.png / .svg')
    plt.close(fig)
