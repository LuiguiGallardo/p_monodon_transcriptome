#!/usr/bin/env python3
"""Figure06_A – eggNOG annotation coverage (pie chart, static data)"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

OUT  = Path('../results/annotation_graphics')
OUT.mkdir(parents=True, exist_ok=True)
STEM = 'figure_06_a'

if __name__ == '__main__':
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie([9313, 28423 - 9313],
           labels=['With eggNOG\n(32.8%)', 'Without eggNOG\n(67.2%)'],
           autopct='%1.1f%%', colors=['#3498db', '#bdc3c7'], startangle=90,
           textprops={'fontsize': 11, 'fontweight': 'bold'})
    ax.set_title('eggNOG Annotation Coverage', fontsize=13, fontweight='bold', pad=20)
    fig.tight_layout()
    fig.savefig(OUT / f'{STEM}.png', dpi=300, bbox_inches='tight')
    fig.savefig(OUT / f'{STEM}.svg', format='svg', bbox_inches='tight')
    print(f'✓ {STEM}.png / .svg')
    plt.close(fig)
