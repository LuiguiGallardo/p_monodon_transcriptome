#!/usr/bin/env python3
"""Figure11_B – Annotation statistics summary table (reads xlsx)"""
import matplotlib
matplotlib.use("Agg")
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

OUT  = Path('../results/annotation_graphics')
OUT.mkdir(parents=True, exist_ok=True)
STEM = 'figure_11_b'
XLSX = '../results/comprehensive_protein_annotations.xlsx'

if __name__ == '__main__':
    df = pd.read_excel(XLSX, sheet_name='Summary Statistics')
    relevant = df.iloc[:7, :2]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis('tight')
    ax.axis('off')
    table_data = [[str(row['Metric']), f"{row['Count']:.0f}"] for _, row in relevant.iterrows()]
    table = ax.table(cellText=table_data,
                     colLabels=['Annotation Type', 'Count'],
                     cellLoc='center', loc='center', colWidths=[0.6, 0.4])
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2)
    for i in range(2):
        table[(0, i)].set_facecolor('#3498db')
        table[(0, i)].set_text_props(weight='bold', color='white')
    for i in range(1, len(table_data) + 1):
        clr = '#ecf0f1' if i % 2 == 0 else 'white'
        for j in range(2):
            table[(i, j)].set_facecolor(clr)
    ax.set_title('Annotation Statistics Summary', fontsize=12, fontweight='bold', pad=20)
    fig.tight_layout()
    fig.savefig(OUT / f'{STEM}.png', dpi=300, bbox_inches='tight')
    fig.savefig(OUT / f'{STEM}.svg', format='svg', bbox_inches='tight')
    print(f'✓ {STEM}.png / .svg')
    plt.close(fig)
