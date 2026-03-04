#!/usr/bin/env python3
"""Figure11_A – Overall annotation coverage quick reference (pie chart)"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

OUT  = Path('../results/annotation_graphics')
OUT.mkdir(parents=True, exist_ok=True)
STEM = 'figure_11_a'

if __name__ == '__main__':
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.pie([15966, 12457],
           labels=['With Annotation\n(56.2%)', 'No Annotation\n(43.8%)'],
           autopct='%1.1f%%', colors=['#2ecc71', '#e74c3c'], startangle=90,
           textprops={'fontsize': 11, 'fontweight': 'bold'})
    ax.set_title('Overall Annotation Coverage', fontsize=12, fontweight='bold')
    fig.tight_layout()
    fig.savefig(OUT / f'{STEM}.png', dpi=300, bbox_inches='tight')
    fig.savefig(OUT / f'{STEM}.svg', format='svg', bbox_inches='tight')
    print(f'✓ {STEM}.png / .svg')
    plt.close(fig)
