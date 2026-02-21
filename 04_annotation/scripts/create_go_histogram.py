#!/usr/bin/env python3
"""
Gene Ontology Histogram - Refined Publication Quality
Continuous layout (no blank spaces between categories)
"""

import matplotlib.pyplot as plt
from pathlib import Path

output_dir = Path('../results/annotation_graphics')
output_dir.mkdir(exist_ok=True)

def _save_figure(filename):
    plt.savefig(output_dir / f'{filename}.png', dpi=300, bbox_inches='tight')
    plt.savefig(output_dir / f'{filename}.svg', format='svg', bbox_inches='tight')
    print(f"✓ Saved: {filename}.png and .svg")

def create_go_histogram():

    cat_data = {
        'Cellular component': [
            ('Organelle', 9480, 26.83),
            ('Intracellular organelle', 9350, 26.43),
            ('Cytoplasm', 8400, 23.86),
            ('Membrane', 4400, 12.46),
            ('Cell periphery', 2750, 7.79),
            ('Membrane-enclosed lumen', 2680, 7.59),
            ('Endomembrane system', 2470, 7.00),
            ('Cytosol', 2060, 5.84),
            ('Intrinsic component of membrane', 1800, 5.09),
            ('Extracellular region', 1520, 4.32)
        ],
        'Molecular function': [
            ('Protein binding', 5440, 15.40),
            ('Ion binding', 3650, 10.33),
            ('Hydrolase activity', 3200, 9.08),
            ('Organic cyclic compound binding', 3190, 9.03),
            ('Heterocyclic compound binding', 3160, 8.94),
            ('Transferase activity', 2610, 7.39),
            ('Catalytic activity, acting on a protein', 2370, 6.71),
            ('Transmembrane transporter activity', 1285, 3.64),
            ('Oxidoreductase activity', 1088, 3.08),
            ('Small molecule binding', 745, 2.11)
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
            ('Cellular developmental process', 4640, 13.13)
        ]
    }

    colors = {
        'Cellular component': '#F4B183',
        'Molecular function': '#A9D18E',
        'Biological process': '#5B9BD5'
    }

    fig, ax = plt.subplots(figsize=(14, 11))

    y_pos = 0
    y_ticks = []
    y_labels = []
    category_bounds = []

    for cat_name in ['Cellular component', 'Molecular function', 'Biological process']:

        terms = cat_data[cat_name]
        start_y = y_pos

        for term, count, pct in reversed(terms):

            ax.barh(
                y_pos,
                count,
                color=colors[cat_name],
                edgecolor='black',
                linewidth=0.5,
                height=0.7
            )

            ax.text(count + 100, y_pos, f'{pct:.2f}%', va='center', fontsize=10)

            y_ticks.append(y_pos)
            y_labels.append(term)

            y_pos += 1

        end_y = y_pos - 1
        category_bounds.append((cat_name, start_y, end_y))

        # ✅ NO EXTRA SPACING

    # ---- Formatting ----

    ax.set_yticks(y_ticks)
    ax.set_yticklabels(y_labels, fontsize=10)

    ax.set_xlabel('Number of transcripts', fontsize=12, labelpad=10)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.xaxis.grid(True, linestyle='-', color='#E0E0E0', alpha=0.7)
    ax.set_axisbelow(True)

    ax.axvline(x=0, color='black', linewidth=1.2)

    for name, start, end in category_bounds:

        mid = (start + end) / 2

        ax.text(
            -0.35,
            mid,
            name,
            transform=ax.get_yaxis_transform(),
            rotation=90,
            va='center',
            ha='center',
            fontweight='bold',
            fontsize=12
        )
    
    # Remove white space at top and bottom
    ax.set_ylim(-0.5, y_pos - 0.5)
        
    plt.tight_layout()
    _save_figure('GO_Classification_Continuous')
    plt.show()

if __name__ == '__main__':
    create_go_histogram()
