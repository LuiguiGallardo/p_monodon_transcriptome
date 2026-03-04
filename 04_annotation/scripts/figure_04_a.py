#!/usr/bin/env python3
"""Figure04_A – InterProScan database coverage (bar chart, static data)"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

OUT  = Path('../results/annotation_graphics')
OUT.mkdir(parents=True, exist_ok=True)
STEM = 'figure_04_a'

INTERPRO = {'MobiDBLite':12351,'Coils':4917,'SMART':79,'CDD':66,
            'SUPERFAMILY':49,'Pfam':47,'PANTHER':30,'Gene3D':5,'TIGRFAM':1}

if __name__ == '__main__':
    sorted_data = dict(sorted(INTERPRO.items(), key=lambda x: x[1], reverse=True))
    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(range(len(sorted_data)), list(sorted_data.values()),
                  color=sns.color_palette('rocket', len(sorted_data)), alpha=0.8, edgecolor='black', linewidth=1.5)
    ax.set_xticks(range(len(sorted_data)))
    ax.set_xticklabels(list(sorted_data.keys()), rotation=40, ha='right', fontsize=10)
    ax.set_ylabel('Count', fontsize=11, fontweight='bold')
    ax.set_title('InterProScan Database Coverage', fontsize=13, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h,
                f'{int(h):,}', ha='center', va='bottom', fontweight='bold', fontsize=9)
    fig.tight_layout()
    fig.savefig(OUT / f'{STEM}.png', dpi=300, bbox_inches='tight')
    fig.savefig(OUT / f'{STEM}.svg', format='svg', bbox_inches='tight')
    print(f'✓ {STEM}.png / .svg')
    plt.close(fig)
