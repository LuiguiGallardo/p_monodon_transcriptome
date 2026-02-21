#!/usr/bin/env python3
"""Figure03_A – KEGG annotation types distribution (reads xlsx)"""
import matplotlib
matplotlib.use("Agg")
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

OUT  = Path('../results/annotation_graphics')
OUT.mkdir(parents=True, exist_ok=True)
STEM = 'figure_03_a'
XLSX = '../results/comprehensive_protein_annotations.xlsx'

if __name__ == '__main__':
    df = pd.read_excel(XLSX, sheet_name='Protein Annotations')
    categories = ['KEGG KO', 'KEGG Pathway', 'KEGG Module']
    counts = [df['KEGG_KO'].notna().sum(),
              df['KEGG_Pathway'].notna().sum(),
              df['KEGG_Module'].notna().sum()]
    total = len(df)

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(categories, counts, color=['#3498db','#e74c3c','#2ecc71'],
                  alpha=0.8, edgecolor='black', linewidth=1.5)
    for bar, cnt in zip(bars, counts):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                f'{int(cnt):,}\n({cnt/total*100:.1f}%)',
                ha='center', va='bottom', fontweight='bold')
    ax.set_ylabel('Count', fontsize=11, fontweight='bold')
    ax.set_title('KEGG Annotation Types Distribution', fontsize=13, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT / f'{STEM}.png', dpi=300, bbox_inches='tight')
    fig.savefig(OUT / f'{STEM}.svg', format='svg', bbox_inches='tight')
    print(f'✓ {STEM}.png / .svg')
    plt.close(fig)
