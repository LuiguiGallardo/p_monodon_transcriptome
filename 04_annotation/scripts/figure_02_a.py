#!/usr/bin/env python3
"""Figure02_A – Annotation coverage by database (horizontal bar)"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

OUT = Path('../results/annotation_graphics')
OUT.mkdir(parents=True, exist_ok=True)
STEM = 'figure_02_a'

DATABASES   = ['Total Proteins','BLAST Hits','eggNOG Annot.','KEGG KO',
               'GO Terms','InterProScan','Any Annotation']
COUNTS      = [28423, 5138, 9313, 6898, 7372, 13361, 15966]
PERCENTAGES = [100.0, 18.1, 32.8, 24.3, 25.9,  47.0,  56.2]
COLORS      = ['#3498db','#e74c3c','#2ecc71','#f39c12','#9b59b6','#1abc9c','#34495e']

if __name__ == '__main__':
    fig, ax = plt.subplots(figsize=(12, 7))
    bars = ax.barh(DATABASES, COUNTS, color=COLORS)
    for bar, pct in zip(bars, PERCENTAGES):
        w = bar.get_width()
        ax.text(w + 300, bar.get_y() + bar.get_height() / 2,
                f'{pct}%', ha='left', va='center', fontsize=16)
    ax.tick_params(axis='y', labelsize=16)
    ax.set_xlabel('Number of proteins', fontsize=16, fontweight='bold')
    ax.set_title('Annotation Coverage by Database', fontsize=18, fontweight='bold')
    ax.set_xlim(0, max(COUNTS) + 3500)
    ax.grid(axis='x', alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT / f'{STEM}.png', dpi=300, bbox_inches='tight')
    fig.savefig(OUT / f'{STEM}.svg', format='svg', bbox_inches='tight')
    print(f'✓ {STEM}.png / .svg')
    plt.close(fig)
