#!/usr/bin/env python3
"""Figure01_C – KEGG annotation coverage (pie chart)"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

OUT = Path('../results/annotation_graphics')
OUT.mkdir(parents=True, exist_ok=True)
STEM = 'figure_01_c'

if __name__ == '__main__':
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie([6898, 28423 - 6898],
           labels=['With KEGG\n(24.3%)', 'Without KEGG\n(75.7%)'],
           autopct='%1.1f%%', colors=['#3498db', '#bdc3c7'], startangle=90,
           textprops={'fontsize': 11, 'fontweight': 'bold'})
    ax.set_title('KEGG Annotation Coverage', fontsize=13, fontweight='bold', pad=20)
    fig.tight_layout()
    fig.savefig(OUT / f'{STEM}.png', dpi=300, bbox_inches='tight')
    fig.savefig(OUT / f'{STEM}.svg', format='svg', bbox_inches='tight')
    print(f'✓ {STEM}.png / .svg')
    plt.close(fig)
