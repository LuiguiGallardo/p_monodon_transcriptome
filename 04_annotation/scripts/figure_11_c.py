#!/usr/bin/env python3
"""Figure11_C – KEGG annotation summary bar chart (static data)"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

OUT  = Path('../results/annotation_graphics')
OUT.mkdir(parents=True, exist_ok=True)
STEM = 'figure_11_c'

KEGG_STATS = {
    'Proteins with KEGG KO':      6898,
    'Proteins with KEGG Pathway': 4200,
    'Proteins with KEGG Module':  1500,
}

if __name__ == '__main__':
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(KEGG_STATS.keys(), KEGG_STATS.values(),
                  color=['#3498db', '#e74c3c', '#2ecc71'], edgecolor='black', linewidth=1.5)
    ax.set_ylabel('Count', fontweight='bold')
    ax.set_title('KEGG Annotation Summary', fontsize=12, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    for i, v in enumerate(KEGG_STATS.values()):
        ax.text(i, v + 100, f'{v:,}', ha='center', fontweight='bold')
    fig.tight_layout()
    fig.savefig(OUT / f'{STEM}.png', dpi=300, bbox_inches='tight')
    fig.savefig(OUT / f'{STEM}.svg', format='svg', bbox_inches='tight')
    print(f'✓ {STEM}.png / .svg')
    plt.close(fig)
