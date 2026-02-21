#!/usr/bin/env python3
"""Figure04_B – Top 5 InterProScan databases (pie chart, static data)"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

OUT  = Path('../results/annotation_graphics')
OUT.mkdir(parents=True, exist_ok=True)
STEM = 'figure_04_b'

INTERPRO = {'MobiDBLite':12351,'Coils':4917,'SMART':79,'CDD':66,'SUPERFAMILY':49}
OTHER = 79   # Pfam + PANTHER + Gene3D + TIGRFAM

if __name__ == '__main__':
    labels = list(INTERPRO.keys()) + ['Others']
    values = list(INTERPRO.values()) + [OTHER]
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90,
           textprops={'fontsize': 11, 'fontweight': 'bold'})
    ax.set_title('Top 5 InterProScan Databases Distribution', fontsize=13, fontweight='bold', pad=20)
    fig.tight_layout()
    fig.savefig(OUT / f'{STEM}.png', dpi=300, bbox_inches='tight')
    fig.savefig(OUT / f'{STEM}.svg', format='svg', bbox_inches='tight')
    print(f'✓ {STEM}.png / .svg')
    plt.close(fig)
