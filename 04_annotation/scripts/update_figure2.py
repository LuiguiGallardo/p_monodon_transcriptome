#!/usr/bin/env python3
"""
Update Figure 2 with named KEGG pathways in panels A and B
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec
import re

# Load annotation data
pmstat_annot = pd.read_csv('../docs/pmstat_annot.csv')
wssv_annot = pd.read_csv('../docs/wssv_annot.csv')

KEGG_PATHWAYS = {
    'ko03010': 'Ribosome',
    'ko03040': 'Spliceosome',
    'ko03020': 'RNA polymerase',
    'ko03410': 'Base excision repair',
    'ko03050': 'Proteasome',
    'ko04010': 'MAPK signaling pathway',
    'ko04140': 'Regulation of autophagy',
    'ko04217': 'Necroptosis',
    'ko00310': 'Lysine metabolism',
    'ko00350': 'Tyrosine metabolism',
    'ko00950': 'Isoquinoline alkaloid biosynthesis',
    'ko00965': 'Betalain biosynthesis',
    'ko01100': 'Metabolic pathways',
    'ko01110': 'Biosynthesis of secondary metabolites',
    'ko04916': 'Melanogenesis',
    'ko00780': 'Biotin metabolism',
    'ko04142': 'Lysosome',
    'ko04612': 'Antigen processing and presentation',
    'ko04145': 'Phagosome',
    'ko05152': 'Tuberculosis',
    'ko05162': 'Measles',
    'ko05226': 'Hepatitis C',
    'ko05169': 'Epstein-Barr virus infection',
    'ko04210': 'Apoptosis',
    'ko04212': 'Transcriptional misregulation in cancer',
    'ko04214': 'Apoptosis',
    'ko04111': 'Cell cycle',
    'ko04610': 'Complement and coagulation cascades',
    'ko00970': 'Aminoacyl-tRNA synthetase',
    'ko04390': 'Hippo signaling pathway',
    'ko04391': 'Hippo signaling pathway-multiple species',
    'ko04392': 'Hippo signaling pathway-fly',
    'ko04015': 'Rap1 signaling pathway',
    'ko04151': 'PI3K-Akt signaling pathway',
    'ko04510': 'Focal adhesion',
    'ko04512': 'ECM-receptor interaction',
    'ko04514': 'Cell adhesion molecules',
    'ko04611': 'Platelet activation',
    'ko04640': 'Hematopoietic cell lineage',
    'ko04810': 'Regulation of actin cytoskeleton',
    'ko04919': 'Thyroid hormone signaling pathway',
    'ko05165': 'Human papillomavirus infection',
    'ko05200': 'Pathways in cancer',
    'ko05205': 'Proteoglycans in cancer',
    'ko05222': 'Small cell lung cancer',
    'ko05410': 'Hypertrophic cardiomyopathy',
    'ko05412': 'Arrhythmogenic right ventricular cardiomyopathy',
    'ko05414': 'Dilated cardiomyopathy',
    'ko05418': 'Hemolytic uremic syndrome',
    'ko05146': 'Amoebiasis',
    'ko05142': 'Chagas disease',
    'ko05166': 'HTLV-I infection',
    'ko04072': 'Phospholipase D signaling pathway',
    'ko05110': 'Vibrio cholerae infection',
    'ko05134': 'Legionellosis',
    'ko03060': 'Protein export',
    'ko03013': 'RNA transport',
    'ko03320': 'PPAR signaling pathway',
    'ko04068': 'FoxO signaling pathway',
    'ko04922': 'Oxytocin signaling pathway',
    'ko04530': 'Tight junction',
    'ko04110': 'Cell cycle',
    'ko04114': 'Oocyte meiosis',
    'ko04120': 'Ubiquitin mediated proteolysis',
    'ko04141': 'Protein processing in endoplasmic reticulum',
    'ko04310': 'Wnt signaling pathway',
    'ko04341': 'Hedgehog signaling pathway',
    'ko04350': 'TGF-beta signaling pathway',
    'ko04710': 'Circadian rhythm',
    'ko05168': 'Herpes simplex virus 1 infection',
    'ko04144': 'Endocytosis',
    'ko04721': 'Synaptic vesicle cycle',
    'ko04961': 'Endocrine and other factor-regulated calcium reabsorption',
    'ko05016': 'Wnt signaling pathway',
    'ko04520': 'Adherens junction',
    'ko04630': 'Jak-STAT signaling pathway',
    'ko04910': 'Insulin signaling pathway',
    'ko04931': 'Insulin resistance',
    'ko00190': 'Oxidative phosphorylation',
    'ko04714': 'Thermogenesis',
    'ko04723': 'Retrograde endocannabinoid signaling',
    'ko04932': 'Non-alcoholic fatty liver disease',
    'ko05010': 'Alzheimer disease',
    'ko05012': 'Parkinson disease',
    'ko04623': 'Cytosolic DNA-sensing pathway',
    'ko00230': 'Purine metabolism',
    'ko00240': 'Pyrimidine metabolism',
    'ko04974': 'Protein digestion and absorption',
}

def get_pathway_name(ko_code):
    """Get human-readable pathway name from KO code"""
    code = ko_code.strip()
    return KEGG_PATHWAYS.get(code, code)

def extract_pathways(pathways_str):
    """Extract individual pathway codes from string"""
    if not isinstance(pathways_str, str):
        return []
    ko_codes = re.findall(r'ko\d+', pathways_str)
    return list(set(ko_codes))

def create_updated_figure2():
    """Create updated Figure 2 with named KEGG pathways"""
    
    print("Cooking up updated Figure 2 with named KEGG pathways...\n")
    
    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)
    
    # Extract pathways for both groups
    pmstat_pathways = {}
    for pathways_str in pmstat_annot['KEGG_Pathway'].dropna():
        for code in extract_pathways(pathways_str):
            pmstat_pathways[code] = pmstat_pathways.get(code, 0) + 1
    
    wssv_pathways = {}
    for pathways_str in wssv_annot['KEGG_Pathway'].dropna():
        for code in extract_pathways(pathways_str):
            wssv_pathways[code] = wssv_pathways.get(code, 0) + 1
    
    # Panel A: KEGG Pathways for PmSTAT (NAMED)
    ax_a = fig.add_subplot(gs[0, 0])
    top_pmstat = sorted(pmstat_pathways.items(), key=lambda x: x[1], reverse=True)[:8]
    pmstat_names = [get_pathway_name(p[0]) for p in top_pmstat]
    pmstat_counts = [p[1] for p in top_pmstat]
    
    y_pos = np.arange(len(pmstat_names))
    bars = ax_a.barh(y_pos, pmstat_counts, color='blue', edgecolor='black', linewidth=1.2)
    ax_a.set_yticks(y_pos)
    ax_a.set_yticklabels(pmstat_names, fontsize=9)
    ax_a.set_xlabel('Count', fontsize=11, fontweight='bold')
    ax_a.set_title('A) Top KEGG Pathways - PmSTAT dsRNA+WSSV', fontsize=12, fontweight='bold', loc='left')
    ax_a.grid(axis='x', alpha=0.3, linestyle='--')
    
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax_a.text(width, bar.get_y() + bar.get_height()/2., f'{int(width)}',
                 ha='left', va='center', fontsize=9, fontweight='bold')
    
    # Panel B: KEGG Pathways for WSSV (NAMED)
    ax_b = fig.add_subplot(gs[0, 1])
    top_wssv = sorted(wssv_pathways.items(), key=lambda x: x[1], reverse=True)[:8]
    wssv_names = [get_pathway_name(p[0]) for p in top_wssv]
    wssv_counts = [p[1] for p in top_wssv]
    
    y_pos = np.arange(len(wssv_names))
    bars = ax_b.barh(y_pos, wssv_counts, color='red', edgecolor='black', linewidth=1.2)
    ax_b.set_yticks(y_pos)
    ax_b.set_yticklabels(wssv_names, fontsize=9)
    ax_b.set_xlabel('Count', fontsize=11, fontweight='bold')
    ax_b.set_title('B) Top KEGG Pathways - WSSV', fontsize=12, fontweight='bold', loc='left')
    ax_b.grid(axis='x', alpha=0.3, linestyle='--')
    
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax_b.text(width, bar.get_y() + bar.get_height()/2., f'{int(width)}',
                 ha='left', va='center', fontsize=9, fontweight='bold')
    
    # Panel C: Gene Ontology distribution
    ax_c = fig.add_subplot(gs[1, 0])
    
    pmstat_go_bio = pmstat_annot['GO_BP'].notna().sum()
    pmstat_go_mol = pmstat_annot['GO_MF'].notna().sum()
    pmstat_go_cell = pmstat_annot['GO_CC'].notna().sum()
    
    wssv_go_bio = wssv_annot['GO_BP'].notna().sum()
    wssv_go_mol = wssv_annot['GO_MF'].notna().sum()
    wssv_go_cell = wssv_annot['GO_CC'].notna().sum()
    
    go_types = ['Biological\nProcess', 'Molecular\nFunction', 'Cellular\nComponent']
    pmstat_go = [pmstat_go_bio, pmstat_go_mol, pmstat_go_cell]
    wssv_go = [wssv_go_bio, wssv_go_mol, wssv_go_cell]
    
    x = np.arange(len(go_types))
    width = 0.35
    bars1 = ax_c.bar(x - width/2, pmstat_go, width, label='PmSTAT dsRNA+WSSV', color='blue', edgecolor='black', linewidth=1.2)
    bars2 = ax_c.bar(x + width/2, wssv_go, width, label='WSSV', color='red', edgecolor='black', linewidth=1.2)
    
    ax_c.set_ylabel('Number of Proteins', fontsize=11, fontweight='bold')
    ax_c.set_title('C) Gene Ontology Distribution', fontsize=12, fontweight='bold', loc='left')
    ax_c.set_xticks(x)
    ax_c.set_xticklabels(go_types, fontsize=10)
    ax_c.legend(fontsize=10)
    ax_c.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Panel D: Top eggNOG functions
    ax_d = fig.add_subplot(gs[1, 1])
    
    pmstat_func_counts = {}
    for func in pmstat_annot['EggNOG_Function'].dropna():
        if pd.notna(func):
            func_str = str(func)
            for f in func_str.split(','):
                f = f.strip()
                pmstat_func_counts[f] = pmstat_func_counts.get(f, 0) + 1
    
    from collections import Counter
    pmstat_top_func = Counter(pmstat_func_counts).most_common(6)
    
    func_names = [f[0][:25] for f in pmstat_top_func]
    pmstat_func_vals = [f[1] for f in pmstat_top_func]
    
    wssv_func_counts = {}
    for func in wssv_annot['EggNOG_Function'].dropna():
        if pd.notna(func):
            func_str = str(func)
            for f in func_str.split(','):
                f = f.strip()
                wssv_func_counts[f] = wssv_func_counts.get(f, 0) + 1
    
    wssv_func_vals = [wssv_func_counts.get(f[0], 0) for f in pmstat_top_func]
    
    x = np.arange(len(func_names))
    bars1 = ax_d.bar(x - width/2, pmstat_func_vals, width, label='PmSTAT dsRNA+WSSV', color='blue', edgecolor='black', linewidth=1.2)
    bars2 = ax_d.bar(x + width/2, wssv_func_vals, width, label='WSSV', color='red', edgecolor='black', linewidth=1.2)
    
    ax_d.set_ylabel('Number of Proteins', fontsize=11, fontweight='bold')
    ax_d.set_title('D) Top eggNOG Functions', fontsize=12, fontweight='bold', loc='left')
    ax_d.set_xticks(x)
    ax_d.set_xticklabels(func_names, rotation=45, ha='right', fontsize=9)
    ax_d.legend(fontsize=10)
    ax_d.grid(axis='y', alpha=0.3, linestyle='--')
    
    plt.suptitle('Figure 2: Functional Annotation Distribution - Updated with Named KEGG Pathways', 
                 fontsize=16, fontweight='bold', y=0.98)
    
    plt.savefig('../results/only_differential_expression_proteins/Figure_2_Functional_Annotations.pdf', dpi=300, bbox_inches='tight', format='pdf')
    print("    ✓ Saved Figure 2 (updated)")
    plt.close()

if __name__ == '__main__':
    create_updated_figure2()
