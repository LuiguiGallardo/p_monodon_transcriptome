#!/usr/bin/env python3
"""Figure10_A – GO term histogram classification (static data, continuous layout)"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

OUT  = Path('../results/annotation_graphics')
OUT.mkdir(parents=True, exist_ok=True)
STEM = 'figure_10_a'

CAT_DATA = {
    'Cellular component': [
        ('Organelle', 9480, 26.83), ('Intracellular organelle', 9350, 26.43),
        ('Cytoplasm', 8400, 23.86), ('Membrane', 4400, 12.46),
        ('Cell periphery', 2750, 7.79), ('Membrane-enclosed lumen', 2680, 7.59),
        ('Endomembrane system', 2470, 7.00), ('Cytosol', 2060, 5.84),
        ('Intrinsic component of membrane', 1800, 5.09), ('Extracellular region', 1520, 4.32),
    ],
    'Molecular function': [
        ('Protein binding', 5440, 15.40), ('Ion binding', 3650, 10.33),
        ('Hydrolase activity', 3200, 9.08), ('Organic cyclic compound binding', 3190, 9.03),
        ('Heterocyclic compound binding', 3160, 8.94), ('Transferase activity', 2610, 7.39),
        ('Catalytic activity, acting on a protein', 2370, 6.71),
        ('Transmembrane transporter activity', 1285, 3.64),
        ('Oxidoreductase activity', 1088, 3.08), ('Small molecule binding', 745, 2.11),
    ],
    'Biological process': [
        ('Organic substance metabolic process', 9720, 27.52),
        ('Cellular metabolic process', 9410, 26.63),
        ('Primary metabolic process', 9230, 26.13),
        ('Nitrogen compound metabolic process', 8860, 25.07),
        ('Regulation of cellular process', 7200, 20.38),
        ('Cellular component organization', 6420, 18.16),
        ('Anatomical structure development', 6390, 18.08),
        ('Multicellular organism development', 5560, 15.74),
        ('Biosynthetic process', 5020, 14.21),
        ('Cellular developmental process', 4640, 13.13),
    ],
}
COLORS = {
    'Cellular component': '#F4B183',
    'Molecular function': '#A9D18E',
    'Biological process': '#5B9BD5',
}

if __name__ == '__main__':
    fig, ax = plt.subplots(figsize=(14, 11))
    y_pos, y_ticks, y_labels, bounds = 0, [], [], []

    for cat in ['Cellular component', 'Molecular function', 'Biological process']:
        terms = CAT_DATA[cat]
        start = y_pos
        for term, count, pct in reversed(terms):
            ax.barh(y_pos, count, color=COLORS[cat], edgecolor='black', linewidth=0.1, height=0.7)
            ax.text(count + 100, y_pos, f'{pct:.2f}%', va='center', fontsize=14)
            y_ticks.append(y_pos)
            y_labels.append(term)
            y_pos += 1
        bounds.append((cat, start, y_pos - 1))

    ax.set_yticks(y_ticks)
    ax.set_yticklabels(y_labels, fontsize=14)
    ax.set_xlabel('Number of proteins', fontsize=16, fontweight='bold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.xaxis.grid(True, linestyle='-', color='#E0E0E0', alpha=0.7)
    ax.set_axisbelow(True)
    ax.axvline(x=0, color='black', linewidth=1.2)
    for name, start, end in bounds:
        mid = (start + end) / 2
        ax.text(-0.45, mid, name, transform=ax.get_yaxis_transform(),
                rotation=90, va='center', ha='center', fontweight='bold', fontsize=16)
    ax.set_ylim(-0.5, y_pos - 0.5)
    ax.set_title('GO Term Classification', fontsize=18, fontweight='bold', pad=15)
    fig.tight_layout()
    fig.subplots_adjust(left=0.32)  # extra left margin for group labels
    fig.savefig(OUT / f'{STEM}.png', dpi=300, bbox_inches='tight')
    fig.savefig(OUT / f'{STEM}.svg', format='svg', bbox_inches='tight')
    print(f'✓ {STEM}.png / .svg')
    plt.close(fig)
