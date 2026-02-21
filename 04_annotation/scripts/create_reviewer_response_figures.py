#!/usr/bin/env python3
"""
Generate comprehensive annotation figures for differential gene expression groups
Two groups: PmSTAT dsRNA+WSSV and WSSV
Individual module output: Each panel saved separately in PNG (300 DPI) and SVG (vector) formats
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from collections import Counter

# Load annotation data from Excel
excel_file = 'reviewer_response/Differential_Gene_Expression_Annotations.xlsx'
pmstat_annot = pd.read_excel(excel_file, sheet_name='genes_UP_PmSTAT dsRNA+WSSV')
wssv_annot = pd.read_excel(excel_file, sheet_name='genes_UP_WSSV')
output_dir = Path('reviewer_response')

# Print data verification
print(f"Loaded data: PmSTAT={len(pmstat_annot)}, WSSV={len(wssv_annot)}")

def _save_figure(filename):
    """Save figure in both PNG (300 DPI) and SVG (vector) formats"""
    png_path = output_dir / f'{filename}.png'
    plt.savefig(png_path, dpi=300, bbox_inches='tight')
    print(f"  ✓ Saved: {filename}.png")
    
    svg_path = output_dir / f'{filename}.svg'
    plt.savefig(svg_path, format='svg', bbox_inches='tight')
    print(f"  ✓ Saved: {filename}.svg")

# Helper function to count annotations
def count_annotations(row):
    count = 0
    if pd.notna(row['BLAST_Hit']):
        count += 1
    if pd.notna(row['EggNOG_Description']):
        count += 1
    if pd.notna(row['KEGG_KO']):
        count += 1
    if pd.notna(row['InterProScan']):
        count += 1
    return count

pmstat_annot['annot_count'] = pmstat_annot.apply(count_annotations, axis=1)
wssv_annot['annot_count'] = wssv_annot.apply(count_annotations, axis=1)

# Helper function to extract top pathways
def extract_top_pathways(df, n=8):
    all_pathways = []
    for pathways in df['KEGG_Pathway'].dropna():
        if isinstance(pathways, str):
            all_pathways.extend([p.strip() for p in str(pathways).split(';')])
    return Counter(all_pathways).most_common(n)

def create_individual_panels():
    """Create comprehensive comparison figures with individual panel modules"""
    
    print("\n" + "=" * 60)
    print("CREATING INDIVIDUAL FIGURE MODULES")
    print("=" * 60 + "\n")
    
    width = 0.35
    
    # ==================== FIGURE 1: Database Coverage Comparison ====================
    print("Figure 1: Database Coverage Comparison (4 panels)")
    
    # Figure 1A: Database coverage (absolute counts)
    print("  → Panel 1a: Coverage by Database")
    fig, ax = plt.subplots(figsize=(12, 7))
    
    databases = ['BLAST', 'eggNOG', 'KEGG', 'InterProScan']
    pmstat_counts = [
        pmstat_annot['BLAST_Hit'].notna().sum(),
        pmstat_annot['EggNOG_Description'].notna().sum(),
        pmstat_annot['KEGG_KO'].notna().sum(),
        pmstat_annot['InterProScan'].notna().sum()
    ]
    wssv_counts = [
        wssv_annot['BLAST_Hit'].notna().sum(),
        wssv_annot['EggNOG_Description'].notna().sum(),
        wssv_annot['KEGG_KO'].notna().sum(),
        wssv_annot['InterProScan'].notna().sum()
    ]
    
    x = np.arange(len(databases))
    bars1 = ax.bar(x - width/2, pmstat_counts, width, label='PmSTAT dsRNA+WSSV', color='#FF6B6B', edgecolor='black', linewidth=1.2)
    bars2 = ax.bar(x + width/2, wssv_counts, width, label='WSSV', color='#4ECDC4', edgecolor='black', linewidth=1.2)
    
    ax.set_ylabel('Number of Proteins', fontsize=12, fontweight='bold')
    ax.set_title('Database Coverage Comparison', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(databases)
    ax.legend(fontsize=11)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}', ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    plt.tight_layout()
    _save_figure('Figure_1a_Coverage_Counts')
    plt.close()
    
    # Figure 1B: Percentage coverage
    print("  → Panel 1b: Coverage Percentages")
    fig, ax = plt.subplots(figsize=(12, 7))
    
    pmstat_pct = [count/len(pmstat_annot)*100 for count in pmstat_counts]
    wssv_pct = [count/len(wssv_annot)*100 for count in wssv_counts]
    
    x = np.arange(len(databases))
    bars1 = ax.bar(x - width/2, pmstat_pct, width, label='PmSTAT dsRNA+WSSV', color='#FF6B6B', edgecolor='black', linewidth=1.2)
    bars2 = ax.bar(x + width/2, wssv_pct, width, label='WSSV', color='#4ECDC4', edgecolor='black', linewidth=1.2)
    
    ax.set_ylabel('Coverage (%)', fontsize=12, fontweight='bold')
    ax.set_title('Database Coverage Percentages', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(databases)
    ax.set_ylim([0, 105])
    ax.legend(fontsize=11)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.0f}%', ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    plt.tight_layout()
    _save_figure('Figure_1b_Coverage_Percentages')
    plt.close()
    
    # Figure 1C: Statistics table
    print("  → Panel 1c: Annotation Statistics")
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.axis('off')
    
    stats_data = [
        ['Database', 'PmSTAT dsRNA+WSSV', 'WSSV'],
        ['BLAST', f'{pmstat_counts[0]} ({pmstat_pct[0]:.1f}%)', f'{wssv_counts[0]} ({wssv_pct[0]:.1f}%)'],
        ['eggNOG', f'{pmstat_counts[1]} ({pmstat_pct[1]:.1f}%)', f'{wssv_counts[1]} ({wssv_pct[1]:.1f}%)'],
        ['KEGG', f'{pmstat_counts[2]} ({pmstat_pct[2]:.1f}%)', f'{wssv_counts[2]} ({wssv_pct[2]:.1f}%)'],
        ['InterProScan', f'{pmstat_counts[3]} ({pmstat_pct[3]:.1f}%)', f'{wssv_counts[3]} ({wssv_pct[3]:.1f}%)'],
    ]
    
    table = ax.table(cellText=stats_data, cellLoc='center', loc='center', colWidths=[0.3, 0.35, 0.35])
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1, 2.5)
    
    for i in range(len(stats_data)):
        for j in range(3):
            cell = table[(i, j)]
            if i == 0:
                cell.set_facecolor('#44546A')
                cell.set_text_props(weight='bold', color='white')
            else:
                if i % 2 == 0:
                    cell.set_facecolor('#E7E6E6')
    
    ax.set_title('Annotation Statistics', fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    _save_figure('Figure_1c_Statistics_Table')
    plt.close()
    
    # Figure 1D: Multi-annotation distribution
    print("  → Panel 1d: Multi-Source Distribution")
    fig, ax = plt.subplots(figsize=(12, 7))
    
    annot_cats = ['0', '1', '2', '3', '4']
    pmstat_dist = [len(pmstat_annot[pmstat_annot['annot_count']==i]) for i in range(5)]
    wssv_dist = [len(wssv_annot[wssv_annot['annot_count']==i]) for i in range(5)]
    
    x = np.arange(len(annot_cats))
    bars1 = ax.bar(x - width/2, pmstat_dist, width, label='PmSTAT dsRNA+WSSV', color='#FF6B6B', edgecolor='black', linewidth=1.2)
    bars2 = ax.bar(x + width/2, wssv_dist, width, label='WSSV', color='#4ECDC4', edgecolor='black', linewidth=1.2)
    
    ax.set_ylabel('Number of Proteins', fontsize=12, fontweight='bold')
    ax.set_xlabel('Number of Annotation Sources', fontsize=12, fontweight='bold')
    ax.set_title('Multi-Source Annotation Distribution', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(annot_cats)
    ax.legend(fontsize=11)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    _save_figure('Figure_1d_MultiSource_Distribution')
    plt.close()
    
    # ==================== FIGURE 2: Functional Annotations ====================
    print("\nFigure 2: Functional Annotations (4 panels)")
    
    # Figure 2A: KEGG Pathways - PmSTAT
    print("  → Panel 2a: Top KEGG Pathways - PmSTAT")
    fig, ax = plt.subplots(figsize=(12, 8))
    
    pmstat_pathways = extract_top_pathways(pmstat_annot)
    pmstat_pathway_names = [p[0][:40] for p in pmstat_pathways]
    pmstat_pathway_counts = [p[1] for p in pmstat_pathways]
    
    y_pos = np.arange(len(pmstat_pathway_names))
    ax.barh(y_pos, pmstat_pathway_counts, color='#FF6B6B', edgecolor='black', linewidth=1.2)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(pmstat_pathway_names, fontsize=10)
    ax.set_xlabel('Count', fontsize=12, fontweight='bold')
    ax.set_title('Top KEGG Pathways - PmSTAT dsRNA+WSSV', fontsize=14, fontweight='bold')
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    
    for i, v in enumerate(pmstat_pathway_counts):
        ax.text(v + 0.1, i, f'{int(v)}', va='center', fontweight='bold')
    
    plt.tight_layout()
    _save_figure('Figure_2a_KEGG_Pathways_PmSTAT')
    plt.close()
    
    # Figure 2B: KEGG Pathways - WSSV
    print("  → Panel 2b: Top KEGG Pathways - WSSV")
    fig, ax = plt.subplots(figsize=(12, 8))
    
    wssv_pathways = extract_top_pathways(wssv_annot)
    wssv_pathway_names = [p[0][:40] for p in wssv_pathways]
    wssv_pathway_counts = [p[1] for p in wssv_pathways]
    
    y_pos = np.arange(len(wssv_pathway_names))
    ax.barh(y_pos, wssv_pathway_counts, color='#4ECDC4', edgecolor='black', linewidth=1.2)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(wssv_pathway_names, fontsize=10)
    ax.set_xlabel('Count', fontsize=12, fontweight='bold')
    ax.set_title('Top KEGG Pathways - WSSV', fontsize=14, fontweight='bold')
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    
    for i, v in enumerate(wssv_pathway_counts):
        ax.text(v + 0.1, i, f'{int(v)}', va='center', fontweight='bold')
    
    plt.tight_layout()
    _save_figure('Figure_2b_KEGG_Pathways_WSSV')
    plt.close()
    
    # Figure 2C: GO term distribution
    print("  → Panel 2c: Gene Ontology Distribution")
    fig, ax = plt.subplots(figsize=(12, 7))
    
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
    bars1 = ax.bar(x - width/2, pmstat_go, width, label='PmSTAT dsRNA+WSSV', color='#FF6B6B', edgecolor='black', linewidth=1.2)
    bars2 = ax.bar(x + width/2, wssv_go, width, label='WSSV', color='#4ECDC4', edgecolor='black', linewidth=1.2)
    
    ax.set_ylabel('Number of Proteins', fontsize=12, fontweight='bold')
    ax.set_title('Gene Ontology Distribution', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(go_types, fontsize=11)
    ax.legend(fontsize=11)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}', ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    plt.tight_layout()
    _save_figure('Figure_2c_GO_Distribution')
    plt.close()
    
    # Figure 2D: eggNOG Functions
    print("  → Panel 2d: Top eggNOG Functions")
    fig, ax = plt.subplots(figsize=(12, 7))
    
    pmstat_func_counts = {}
    wssv_func_counts = {}
    
    for func in pmstat_annot['EggNOG_Function'].dropna():
        if pd.notna(func):
            func_str = str(func)
            for f in func_str.split(','):
                f = f.strip()
                pmstat_func_counts[f] = pmstat_func_counts.get(f, 0) + 1
    
    for func in wssv_annot['EggNOG_Function'].dropna():
        if pd.notna(func):
            func_str = str(func)
            for f in func_str.split(','):
                f = f.strip()
                wssv_func_counts[f] = wssv_func_counts.get(f, 0) + 1
    
    pmstat_top_func = Counter(pmstat_func_counts).most_common(6)
    
    if len(pmstat_top_func) > 0:
        func_names = [f[0][:35] for f in pmstat_top_func]
        pmstat_func_vals = [f[1] for f in pmstat_top_func]
        wssv_func_vals = [wssv_func_counts.get(f[0], 0) for f in pmstat_top_func]
        
        x = np.arange(len(func_names))
        bars1 = ax.bar(x - width/2, pmstat_func_vals, width, label='PmSTAT dsRNA+WSSV', color='#FF6B6B', edgecolor='black', linewidth=1.2)
        bars2 = ax.bar(x + width/2, wssv_func_vals, width, label='WSSV', color='#4ECDC4', edgecolor='black', linewidth=1.2)
        
        ax.set_ylabel('Number of Proteins', fontsize=12, fontweight='bold')
        ax.set_title('Top eggNOG Functions', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(func_names, rotation=45, ha='right', fontsize=9)
        ax.legend(fontsize=11)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    _save_figure('Figure_2d_eggNOG_Functions')
    plt.close()
    
    # ==================== FIGURE 3: Structural Features ====================
    print("\nFigure 3: Structural Features (4 panels)")
    
    # Figure 3A: InterProScan domain distribution
    print("  → Panel 3a: InterProScan Domains")
    fig, ax = plt.subplots(figsize=(12, 7))
    
    pmstat_with_domains = pmstat_annot['InterProScan'].notna().sum()
    pmstat_without = len(pmstat_annot) - pmstat_with_domains
    wssv_with_domains = wssv_annot['InterProScan'].notna().sum()
    wssv_without = len(wssv_annot) - wssv_with_domains
    
    categories = ['With Domains', 'Without Domains']
    pmstat_dom = [pmstat_with_domains, pmstat_without]
    wssv_dom = [wssv_with_domains, wssv_without]
    
    x = np.arange(len(categories))
    bars1 = ax.bar(x - width/2, pmstat_dom, width, label='PmSTAT dsRNA+WSSV', color='#FF6B6B', edgecolor='black', linewidth=1.2)
    bars2 = ax.bar(x + width/2, wssv_dom, width, label='WSSV', color='#4ECDC4', edgecolor='black', linewidth=1.2)
    
    ax.set_ylabel('Number of Proteins', fontsize=12, fontweight='bold')
    ax.set_title('InterProScan Domain Distribution', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.legend(fontsize=11)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}', ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    plt.tight_layout()
    _save_figure('Figure_3a_InterProScan_Domains')
    plt.close()
    
    # Figure 3B: Top InterProScan databases
    print("  → Panel 3b: Top InterPro Databases")
    fig, ax = plt.subplots(figsize=(12, 8))
    
    pmstat_dbs = {}
    for domains in pmstat_annot['InterProScan'].dropna():
        if pd.notna(domains):
            for db in str(domains).split(';'):
                db = db.strip()
                if db and '|' in db:
                    db_name = db.split('|')[0]
                    pmstat_dbs[db_name] = pmstat_dbs.get(db_name, 0) + 1
    
    pmstat_top_dbs = Counter(pmstat_dbs).most_common(8)
    
    if len(pmstat_top_dbs) > 0:
        db_names = [d[0][:25] for d in pmstat_top_dbs]
        db_counts = [d[1] for d in pmstat_top_dbs]
        
        y_pos = np.arange(len(db_names))
        ax.barh(y_pos, db_counts, color='#FF6B6B', edgecolor='black', linewidth=1.2)
        ax.set_yticks(y_pos)
        ax.set_yticklabels(db_names, fontsize=10)
        ax.set_xlabel('Count', fontsize=12, fontweight='bold')
        ax.set_title('Top InterPro Databases - PmSTAT', fontsize=14, fontweight='bold')
        ax.grid(axis='x', alpha=0.3, linestyle='--')
        
        for i, v in enumerate(db_counts):
            ax.text(v + 10, i, f'{int(v)}', va='center', fontweight='bold')
    
    plt.tight_layout()
    _save_figure('Figure_3b_InterPro_Databases')
    plt.close()
    
    # Figure 3C: Annotation completeness
    print("  → Panel 3c: Annotation Completeness")
    fig, ax = plt.subplots(figsize=(12, 7))
    
    completeness_levels = ['Unannotated', 'Partial\n(1-2 DBs)', 'Good\n(3 DBs)', 'Complete\n(4 DBs)']
    pmstat_complete = [
        len(pmstat_annot[pmstat_annot['annot_count']==0]),
        len(pmstat_annot[pmstat_annot['annot_count'].isin([1,2])]),
        len(pmstat_annot[pmstat_annot['annot_count']==3]),
        len(pmstat_annot[pmstat_annot['annot_count']==4])
    ]
    wssv_complete = [
        len(wssv_annot[wssv_annot['annot_count']==0]),
        len(wssv_annot[wssv_annot['annot_count'].isin([1,2])]),
        len(wssv_annot[wssv_annot['annot_count']==3]),
        len(wssv_annot[wssv_annot['annot_count']==4])
    ]
    
    x = np.arange(len(completeness_levels))
    bars1 = ax.bar(x - width/2, pmstat_complete, width, label='PmSTAT dsRNA+WSSV', color='#FF6B6B', edgecolor='black', linewidth=1.2)
    bars2 = ax.bar(x + width/2, wssv_complete, width, label='WSSV', color='#4ECDC4', edgecolor='black', linewidth=1.2)
    
    ax.set_ylabel('Number of Proteins', fontsize=12, fontweight='bold')
    ax.set_title('Annotation Completeness Level', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(completeness_levels, fontsize=11)
    ax.legend(fontsize=11)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{int(height)}', ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    plt.tight_layout()
    _save_figure('Figure_3c_Annotation_Completeness')
    plt.close()
    
    # Figure 3D: Summary statistics
    print("  → Panel 3d: Summary Statistics")
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.axis('off')
    
    summary_data = [
        ['Feature', 'PmSTAT dsRNA+WSSV', 'WSSV'],
        ['Total Proteins', f'{len(pmstat_annot)}', f'{len(wssv_annot)}'],
        ['Avg Annotations/Protein', f'{pmstat_annot["annot_count"].mean():.2f}', f'{wssv_annot["annot_count"].mean():.2f}'],
        ['With InterProScan', f'{pmstat_with_domains} ({pmstat_with_domains/len(pmstat_annot)*100:.1f}%)', f'{wssv_with_domains} ({wssv_with_domains/len(wssv_annot)*100:.1f}%)'],
        ['Fully Annotated', f'{pmstat_complete[3]} ({pmstat_complete[3]/len(pmstat_annot)*100:.1f}%)', f'{wssv_complete[3]} ({wssv_complete[3]/len(wssv_annot)*100:.1f}%)'],
    ]
    
    table = ax.table(cellText=summary_data, cellLoc='left', loc='center', colWidths=[0.4, 0.3, 0.3])
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1, 2.5)
    
    for i in range(len(summary_data)):
        for j in range(3):
            cell = table[(i, j)]
            if i == 0:
                cell.set_facecolor('#44546A')
                cell.set_text_props(weight='bold', color='white')
            else:
                if i % 2 == 0:
                    cell.set_facecolor('#E7E6E6')
    
    ax.set_title('Summary Statistics', fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    _save_figure('Figure_3d_Summary_Statistics')
    plt.close()
    
    print("\n" + "=" * 60)
    print("✓ ALL INDIVIDUAL FIGURE MODULES GENERATED")
    print("=" * 60)
    print(f"Saved to: reviewer_response/")
    print(f"\nFigure 1 (Database Coverage): 1a, 1b, 1c, 1d")
    print(f"Figure 2 (Functional Annotations): 2a, 2b, 2c, 2d")
    print(f"Figure 3 (Structural Features): 3a, 3b, 3c, 3d")
    print(f"\nEach panel available in both PNG (300 DPI) and SVG (vector) format\n")


if __name__ == '__main__':
    create_individual_panels()
