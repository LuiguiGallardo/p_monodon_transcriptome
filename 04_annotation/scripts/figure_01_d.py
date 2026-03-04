#!/usr/bin/env python3
"""Figure01_D – Top 5 InterProScan databases (horizontal bar)"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

OUT = Path('../results/annotation_graphics')
OUT.mkdir(parents=True, exist_ok=True)
STEM = 'figure_01_d'

INTERPRO = {'MobiDBLite': 12351, 'Coils': 4917, 'SMART': 79, 'CDD': 66, 'SUPERFAMILY': 49}

if __name__ == '__main__':
    fig, ax = plt.subplots(figsize=(10, 6))
    dbs, counts = zip(*INTERPRO.items())
    ax.barh(list(dbs), list(counts),
            color=sns.color_palette('viridis', len(INTERPRO)), edgecolor='black', linewidth=1.5)
    ax.set_xlabel('Count', fontsize=11, fontweight='bold')
    ax.set_title('Top 5 InterProScan Databases', fontsize=13, fontweight='bold')
    ax.grid(axis='x', alpha=0.3)
    for i, v in enumerate(counts):
        ax.text(v + 100, i, f'{int(v):,}', va='center', fontweight='bold')
    fig.tight_layout()
    fig.savefig(OUT / f'{STEM}.png', dpi=300, bbox_inches='tight')
    fig.savefig(OUT / f'{STEM}.svg', format='svg', bbox_inches='tight')
    print(f'✓ {STEM}.png / .svg')
    plt.close(fig)
