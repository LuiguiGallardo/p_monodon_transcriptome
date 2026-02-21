#!/usr/bin/env python3
"""figure_03_b – Top 10 KEGG pathways with readable names (reads xlsx)

ko codes (KO-based pathways) and map codes (KEGG reference maps) are kept
separate since they represent different KEGG concepts, each labelled with
a meaningful name via kegg_names.pathway_label().
"""
import matplotlib
matplotlib.use("Agg")
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from pathlib import Path
from kegg_names import pathway_label  # shared lookup

OUT  = Path('../results/annotation_graphics')
OUT.mkdir(parents=True, exist_ok=True)
STEM = 'figure_03_b'
XLSX = '../results/comprehensive_protein_annotations.xlsx'

if __name__ == '__main__':
    df = pd.read_excel(XLSX, sheet_name='Protein Annotations')

    # Collect all pathway codes as-is (ko and map kept separate)
    all_codes = []
    for p in df['KEGG_Pathway'].dropna():
        if isinstance(p, str):
            for code in p.split(','):
                all_codes.append(code.strip())

    top = Counter(all_codes).most_common(10)

    fig, ax = plt.subplots(figsize=(12, 7))
    if top:
        names  = [pathway_label(code) for code, _ in top]
        values = [count for _, count in top]

        ax.barh(range(len(top)), values,
                color=sns.color_palette('viridis', len(top)),
                edgecolor='black', linewidth=1.5)
        ax.set_yticks(range(len(top)))
        ax.set_yticklabels(names, fontsize=10)
        ax.set_xlabel('Count', fontsize=11, fontweight='bold')
        ax.grid(axis='x', alpha=0.3)
        for i, v in enumerate(values):
            ax.text(v + 5, i, f'{int(v)}', va='center', fontweight='bold')

    ax.set_title('Top 10 KEGG Pathways', fontsize=13, fontweight='bold')
    fig.tight_layout()
    fig.savefig(OUT / f'{STEM}.png', dpi=300, bbox_inches='tight')
    fig.savefig(OUT / f'{STEM}.svg', format='svg', bbox_inches='tight')
    print(f'✓ {STEM}.png / .svg')
    plt.close(fig)
