#!/usr/bin/env python3
"""Figure01_A – Annotation counts by database (bar chart)"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

OUT = Path('../results/annotation_graphics')
OUT.mkdir(parents=True, exist_ok=True)
STEM = 'figure_01_a'

STATS = [('Total Proteins',28423),('With BLAST',5138),
         ('With eggNOG',9313),('With KEGG',6898),('Any Annotation',15966)]

if __name__ == '__main__':
    labels, counts = zip(*STATS)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(range(len(labels)), counts,
           color=sns.color_palette('husl', len(STATS)), edgecolor='black', linewidth=1.5)
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=35, ha='right')
    ax.set_ylabel('Count', fontsize=11, fontweight='bold')
    ax.set_title('Annotation Counts by Database', fontsize=13, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    for i, v in enumerate(counts):
        ax.text(i, v + 200, f'{int(v):,}', ha='center', fontweight='bold', fontsize=9)
    fig.tight_layout()
    fig.savefig(OUT / f'{STEM}.png', dpi=300, bbox_inches='tight')
    fig.savefig(OUT / f'{STEM}.svg', format='svg', bbox_inches='tight')
    print(f'✓ {STEM}.png / .svg')
    plt.close(fig)
