#!/usr/bin/env python3
"""figure_14_b – Top InterPro databases from PmSTAT (reads xlsx)"""
import matplotlib; matplotlib.use("Agg")
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from pathlib import Path

OUT  = Path('../results/only_differential_expression_proteins')
XLSX = '../results/only_differential_expression_proteins/Differential_Gene_Expression_Annotations.xlsx'
STEM = 'figure_14_b'

if __name__ == '__main__':
    pm = pd.read_excel(XLSX, sheet_name='genes_UP_PmSTAT dsRNA+WSSV')
    db_counts = {}
    for domains in pm['InterProScan'].dropna():
        for db in str(domains).split(';'):
            db = db.strip()
            if db and '|' in db:
                name = db.split('|')[0]
                db_counts[name] = db_counts.get(name, 0) + 1
    top = Counter(db_counts).most_common(8)

    fig, ax = plt.subplots(figsize=(12, 8))
    if top:
        names  = [d[0][:25] for d in top]
        counts = [d[1] for d in top]
        y = np.arange(len(names))
        ax.barh(y, counts, color='#FF6B6B', edgecolor='black', linewidth=1.2)
        ax.set_yticks(y); ax.set_yticklabels(names, fontsize=10)
        ax.set_xlabel('Count', fontsize=12, fontweight='bold')
        ax.grid(axis='x', alpha=0.3, linestyle='--')
        for i, v in enumerate(counts):
            ax.text(v + 10, i, f'{int(v)}', va='center', fontweight='bold')
    ax.set_title('Top InterPro Databases – PmSTAT', fontsize=14, fontweight='bold')
    fig.tight_layout()
    fig.savefig(OUT / f'{STEM}.png', dpi=300, bbox_inches='tight')
    fig.savefig(OUT / f'{STEM}.svg', format='svg', bbox_inches='tight')
    print(f'✓ {STEM}.png / .svg'); plt.close(fig)
