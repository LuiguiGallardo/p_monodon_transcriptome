#!/usr/bin/env python3
"""
Transcriptome Annotation Graphics Generator
Creates comprehensive visualizations of annotation statistics from EnTAP and InterProScan
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
import re
from collections import Counter

# Set style
sns.set_style("whitegrid")
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 8)

class AnnotationVisualizer:
    def __init__(self, xlsx_file, output_dir='../results/annotation_graphics'):
        """Initialize the visualizer with Excel file path"""
        self.xlsx_file = xlsx_file
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Load data
        self.df_stats = pd.read_excel(xlsx_file, sheet_name='Summary Statistics')
        self.df_annot = pd.read_excel(xlsx_file, sheet_name='Protein Annotations')
    
    def _save_figure(self, filename):
        """Save figure in both PNG (300 DPI raster) and SVG (vector) formats"""
        # Save PNG (raster, high resolution)
        png_path = self.output_dir / f'{filename}.png'
        plt.savefig(png_path, dpi=300, bbox_inches='tight')
        print(f"✓ Saved: {filename}.png")
        
        # Save SVG (vector, scalable)
        svg_path = self.output_dir / f'{filename}.svg'
        plt.savefig(svg_path, format='svg', bbox_inches='tight')
        print(f"✓ Saved: {filename}.svg")
        
    def plot_annotation_counts(self):
        """Panel 1: Annotation counts by database"""
        fig, ax = plt.subplots(figsize=(12, 7))
        
        stats = [
            ('Total Proteins', 28423),
            ('With BLAST Hits', 5138),
            ('With eggNOG', 9313),
            ('With KEGG', 6898),
            ('With Any Annotation', 15966),
        ]
        labels, counts = zip(*stats)
        colors = sns.color_palette("husl", len(stats))
        
        ax.bar(range(len(labels)), counts, color=colors, edgecolor='black', linewidth=1.5)
        ax.set_xticks(range(len(labels)))
        ax.set_xticklabels(labels, rotation=45, ha='right')
        ax.set_ylabel('Count', fontsize=11, fontweight='bold')
        ax.set_title('Annotation Counts by Database', fontsize=13, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        
        for i, v in enumerate(counts):
            ax.text(i, v + 200, f'{int(v):,}', ha='center', fontweight='bold')
        
        plt.tight_layout()
        self._save_figure('01a_annotation_counts')
        plt.close()
    
    def plot_annotation_coverage(self):
        """Panel 2: Overall annotation coverage pie"""
        fig, ax = plt.subplots(figsize=(10, 8))
        
        annotation_data = [15966, 28423 - 15966]
        ax.pie(annotation_data, labels=['Annotated\n(56.2%)', 'Unannotated\n(43.8%)'],
               autopct='%1.1f%%', colors=['#2ecc71', '#e74c3c'], startangle=90,
               textprops={'fontsize': 11, 'fontweight': 'bold'})
        ax.set_title('Overall Annotation Coverage', fontsize=13, fontweight='bold', pad=20)
        
        plt.tight_layout()
        self._save_figure('01b_annotation_coverage')
        plt.close()
    
    def plot_kegg_coverage(self):
        """Panel 3: KEGG coverage pie"""
        fig, ax = plt.subplots(figsize=(10, 8))
        
        kegg_stats = [6898, 28423 - 6898]
        ax.pie(kegg_stats, labels=['With KEGG\n(24.3%)', 'Without KEGG\n(75.7%)'],
               autopct='%1.1f%%', colors=['#3498db', '#bdc3c7'], startangle=90,
               textprops={'fontsize': 11, 'fontweight': 'bold'})
        ax.set_title('KEGG Annotation Coverage', fontsize=13, fontweight='bold', pad=20)
        
        plt.tight_layout()
        self._save_figure('01c_kegg_coverage')
        plt.close()
    
    def plot_top_interpro_databases(self):
        """Panel 4: Top 5 InterProScan databases"""
        fig, ax = plt.subplots(figsize=(12, 7))
        
        interpro_stats = {
            'MobiDBLite': 12351,
            'Coils': 4917,
            'SMART': 79,
            'CDD': 66,
            'SUPERFAMILY': 49,
            'PANTHER': 30,
            'Gene3D': 5,
            'TIGRFAM': 1,
            'Pfam': 47
        }
        top_interpro = dict(sorted(interpro_stats.items(), key=lambda x: x[1], reverse=True)[:5])
        
        ax.barh(list(top_interpro.keys()), list(top_interpro.values()),
                color=sns.color_palette("viridis", len(top_interpro)), edgecolor='black', linewidth=1.5)
        ax.set_xlabel('Count', fontsize=11, fontweight='bold')
        ax.set_title('Top 5 InterProScan Databases', fontsize=13, fontweight='bold')
        ax.grid(axis='x', alpha=0.3)
        
        for i, v in enumerate(top_interpro.values()):
            ax.text(v + 100, i, f'{int(v):,}', va='center', fontweight='bold')
        
        plt.tight_layout()
        self._save_figure('01d_interpro_top5')
        plt.close()
    
    def plot_annotation_summary(self):
        """Create individual overview panels - DEPRECATED, use individual methods"""
        # Now calls individual panel methods instead
        self.plot_annotation_counts()
        self.plot_annotation_coverage()
        self.plot_kegg_coverage()
        self.plot_top_interpro_databases()
        
    def plot_database_comparison(self):
        """Compare annotation coverage across different databases"""
        fig, ax = plt.subplots(figsize=(12, 7))
        
        databases = [
            'Total Proteins',
            'BLAST Hits',
            'eggNOG Annot.',
            'KEGG KO',
            'GO Terms',
            'InterProScan',
            'Any Annotation'
        ]
        counts = [28423, 5138, 9313, 6898, 7372, 13361, 15966]
        percentages = [100.0, 18.1, 32.8, 24.3, 25.9, 47.0, 56.2]
        
        colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c', '#34495e']
        bars = ax.barh(databases, counts, color=colors)
        
        # Add percentage labels
        for i, (bar, pct) in enumerate(zip(bars, percentages)):
            width = bar.get_width()
            ax.text(width + 300, bar.get_y() + bar.get_height()/2,
                   f'({pct}%)',
                   ha='left', va='center', fontweight='bold', fontsize=10)
        
        ax.set_xlabel('Number of Proteins', fontsize=12)
        # ax.set_title('Annotation Coverage by Database', fontsize=14, fontweight='bold')
        ax.grid(axis='x', alpha=0.3)
        
        plt.tight_layout()
        self._save_figure('02_database_comparison')
        plt.close()
        
    def plot_kegg_types(self):
        """Panel 1: KEGG annotation types distribution"""
        fig, ax = plt.subplots(figsize=(12, 7))
        
        ko_data = self.df_annot['KEGG_KO'].dropna()
        pathway_data = self.df_annot['KEGG_Pathway'].dropna()
        module_data = self.df_annot['KEGG_Module'].dropna()
        
        kegg_categories = ['KEGG KO', 'KEGG Pathway', 'KEGG Module']
        kegg_counts = [len(ko_data), len(pathway_data), len(module_data)]
        
        colors_kegg = ['#3498db', '#e74c3c', '#2ecc71']
        bars = ax.bar(kegg_categories, kegg_counts, color=colors_kegg, alpha=0.8, edgecolor='black', linewidth=1.5)
        
        ax.set_ylabel('Count', fontsize=11, fontweight='bold')
        ax.set_title('KEGG Annotation Types Distribution', fontsize=13, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, height,
                   f'{int(height):,}\n({height/len(self.df_annot)*100:.1f}%)',
                   ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        self._save_figure('03a_kegg_types')
        plt.close()
    
    def plot_kegg_pathways(self):
        """Panel 2: Top KEGG pathways"""
        fig, ax = plt.subplots(figsize=(12, 7))
        
        pathway_data = self.df_annot['KEGG_Pathway'].dropna()
        pathways_list = []
        for paths in pathway_data:
            if isinstance(paths, str):
                pathways_list.extend([p.strip() for p in str(paths).split(',')])
        
        pathway_counter = Counter(pathways_list)
        top_pathways = dict(pathway_counter.most_common(10))
        
        if top_pathways:
            top_path_names = [p.replace('ko', 'KEGG') if len(p) < 10 else p[:10] for p in top_pathways.keys()]
            ax.barh(range(len(top_pathways)), list(top_pathways.values()),
                   color=sns.color_palette("viridis", len(top_pathways)), edgecolor='black', linewidth=1.5)
            ax.set_yticks(range(len(top_pathways)))
            ax.set_yticklabels(top_path_names, fontsize=10)
            ax.set_xlabel('Count', fontsize=11, fontweight='bold')
            ax.set_title('Top 10 KEGG Pathways', fontsize=13, fontweight='bold')
            ax.grid(axis='x', alpha=0.3)
            
            for i, v in enumerate(top_pathways.values()):
                ax.text(v + 5, i, f'{int(v)}', va='center', fontweight='bold')
        
        plt.tight_layout()
        self._save_figure('03b_kegg_pathways')
        plt.close()
    
    def plot_kegg_analysis(self):
        """Analyze KEGG pathway and KO distribution - calls individual panel methods"""
        self.plot_kegg_types()
        self.plot_kegg_pathways()
        
    def plot_interpro_databases(self):
        """Panel 1: InterProScan database coverage bar chart"""
        fig, ax = plt.subplots(figsize=(12, 7))
        
        interpro_data = {
            'MobiDBLite': 12351,
            'Coils': 4917,
            'Pfam': 47,
            'SMART': 79,
            'CDD': 66,
            'SUPERFAMILY': 49,
            'PANTHER': 30,
            'Gene3D': 5,
            'TIGRFAM': 1
        }
        
        sorted_data = dict(sorted(interpro_data.items(), key=lambda x: x[1], reverse=True))
        
        bars = ax.bar(range(len(sorted_data)), list(sorted_data.values()),
                     color=sns.color_palette("rocket", len(sorted_data)), alpha=0.8, edgecolor='black', linewidth=1.5)
        ax.set_xticks(range(len(sorted_data)))
        ax.set_xticklabels(list(sorted_data.keys()), rotation=45, ha='right', fontsize=10)
        ax.set_ylabel('Count', fontsize=11, fontweight='bold')
        ax.set_title('InterProScan Database Coverage', fontsize=13, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, height,
                   f'{int(height):,}', ha='center', va='bottom', fontweight='bold', fontsize=9)
        
        plt.tight_layout()
        self._save_figure('04a_interpro_databases')
        plt.close()
    
    def plot_interpro_distribution(self):
        """Panel 2: Top 5 InterProScan databases pie chart"""
        fig, ax = plt.subplots(figsize=(10, 8))
        
        interpro_data = {
            'MobiDBLite': 12351,
            'Coils': 4917,
            'Pfam': 47,
            'SMART': 79,
            'CDD': 66,
            'SUPERFAMILY': 49,
            'PANTHER': 30,
            'Gene3D': 5,
            'TIGRFAM': 1
        }
        
        top_5 = dict(sorted(interpro_data.items(), key=lambda x: x[1], reverse=True)[:5])
        other = sum([v for k, v in interpro_data.items() if k not in top_5])
        pie_data = list(top_5.values()) + [other]
        pie_labels = list(top_5.keys()) + ['Others']
        
        ax.pie(pie_data, labels=pie_labels, autopct='%1.1f%%', startangle=90,
               textprops={'fontsize': 11, 'fontweight': 'bold'})
        ax.set_title('Top 5 InterProScan Databases Distribution', fontsize=13, fontweight='bold', pad=20)
        
        plt.tight_layout()
        self._save_figure('04b_interpro_distribution')
        plt.close()
    
    def plot_interpro_analysis(self):
        """Analyze InterProScan database distribution - calls individual panel methods"""
        self.plot_interpro_databases()
        self.plot_interpro_distribution()
        
    def plot_go_comparison(self):
        """Panel 1: GO term distribution comparison between eggNOG and UniProt"""
        fig, ax = plt.subplots(figsize=(12, 7))
        
        bio_proc = self.df_annot['EggNOG_GO_Biological'].notna().sum()
        cell_comp = self.df_annot['EggNOG_GO_Cellular'].notna().sum()
        mol_func = self.df_annot['EggNOG_GO_Molecular'].notna().sum()
        
        uniprot_bio = self.df_annot['UniProt_GO_Biological'].notna().sum()
        uniprot_cell = self.df_annot['UniProt_GO_Cellular'].notna().sum()
        uniprot_mol = self.df_annot['UniProt_GO_Molecular'].notna().sum()
        
        go_types = ['Biological Process', 'Cellular Component', 'Molecular Function']
        eggnong_counts = [bio_proc, cell_comp, mol_func]
        uniprot_counts = [uniprot_bio, uniprot_cell, uniprot_mol]
        
        x = np.arange(len(go_types))
        width = 0.35
        
        bars1 = ax.bar(x - width/2, eggnong_counts, width, label='eggNOG', color='#3498db', alpha=0.8, edgecolor='black', linewidth=1.5)
        bars2 = ax.bar(x + width/2, uniprot_counts, width, label='UniProt', color='#e74c3c', alpha=0.8, edgecolor='black', linewidth=1.5)
        
        ax.set_ylabel('Count', fontsize=11, fontweight='bold')
        ax.set_title('GO Term Distribution: eggNOG vs UniProt', fontsize=13, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(go_types, rotation=15, ha='right')
        ax.legend(fontsize=11)
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        self._save_figure('05a_go_comparison')
        plt.close()
    
    def plot_go_eggnog_types(self):
        """Panel 2: eggNOG GO term types distribution pie chart"""
        fig, ax = plt.subplots(figsize=(10, 8))
        
        bio_proc = self.df_annot['EggNOG_GO_Biological'].notna().sum()
        cell_comp = self.df_annot['EggNOG_GO_Cellular'].notna().sum()
        mol_func = self.df_annot['EggNOG_GO_Molecular'].notna().sum()
        
        go_data = [bio_proc, cell_comp, mol_func]
        ax.pie(go_data, labels=['Biological\nProcess', 'Cellular\nComponent', 'Molecular\nFunction'],
              autopct='%1.1f%%', colors=['#2ecc71', '#f39c12', '#9b59b6'],
              textprops={'fontsize': 11, 'fontweight': 'bold'})
        ax.set_title('eggNOG GO Term Types Distribution', fontsize=13, fontweight='bold', pad=20)
        
        plt.tight_layout()
        self._save_figure('05b_go_eggnog_types')
        plt.close()
    
    def plot_go_coverage(self):
        """Panel 3: Overall GO term coverage pie chart"""
        fig, ax = plt.subplots(figsize=(10, 8))
        
        total_with_go = len(self.df_annot[
            (self.df_annot['EggNOG_GO_Biological'].notna()) |
            (self.df_annot['EggNOG_GO_Cellular'].notna()) |
            (self.df_annot['EggNOG_GO_Molecular'].notna())
        ])
        
        go_coverage = [total_with_go, len(self.df_annot) - total_with_go]
        pct_with = (total_with_go / len(self.df_annot)) * 100
        pct_without = 100 - pct_with
        
        ax.pie(go_coverage, labels=[f'With GO Terms\n({pct_with:.1f}%)', f'Without GO Terms\n({pct_without:.1f}%)'],
              autopct='%1.1f%%', colors=['#1abc9c', '#bdc3c7'],
              textprops={'fontsize': 11, 'fontweight': 'bold'})
        ax.set_title('Overall GO Term Coverage', fontsize=13, fontweight='bold', pad=20)
        
        plt.tight_layout()
        self._save_figure('05c_go_coverage')
        plt.close()
    
    def plot_go_domain_stats(self):
        """Panel 4: GO terms by domain statistics"""
        fig, ax = plt.subplots(figsize=(12, 7))
        
        bio_proc = self.df_annot['EggNOG_GO_Biological'].notna().sum()
        cell_comp = self.df_annot['EggNOG_GO_Cellular'].notna().sum()
        mol_func = self.df_annot['EggNOG_GO_Molecular'].notna().sum()
        
        domain_stats = {
            'Biological\nProcess': bio_proc,
            'Cellular\nComponent': cell_comp,
            'Molecular\nFunction': mol_func
        }
        bars = ax.barh(list(domain_stats.keys()), list(domain_stats.values()),
                      color=['#2ecc71', '#f39c12', '#9b59b6'], alpha=0.8, edgecolor='black', linewidth=1.5)
        ax.set_xlabel('Count', fontsize=11, fontweight='bold')
        ax.set_title('eggNOG GO Terms by Domain', fontsize=13, fontweight='bold')
        ax.grid(axis='x', alpha=0.3)
        
        for i, v in enumerate(domain_stats.values()):
            ax.text(v + 100, i, f'{int(v):,}', va='center', fontweight='bold')
        
        plt.tight_layout()
        self._save_figure('05d_go_domain_stats')
        plt.close()
    
    def plot_go_terms_analysis(self):
        """Analyze Gene Ontology terms distribution - calls individual panel methods"""
        self.plot_go_comparison()
        self.plot_go_eggnog_types()
        self.plot_go_coverage()
        self.plot_go_domain_stats()
        
    def plot_eggnog_coverage(self):
        """Panel 1: eggNOG coverage pie chart"""
        fig, ax = plt.subplots(figsize=(10, 8))
        
        with_eggnog = 9313
        without_eggnog = 28423 - 9313
        
        ax.pie([with_eggnog, without_eggnog],
              labels=[f'With eggNOG\n(32.8%)', f'Without eggNOG\n(67.2%)'],
              autopct='%1.1f%%', colors=['#3498db', '#bdc3c7'],
              textprops={'fontsize': 11, 'fontweight': 'bold'})
        ax.set_title('eggNOG Annotation Coverage', fontsize=13, fontweight='bold', pad=20)
        
        plt.tight_layout()
        self._save_figure('06a_eggnog_coverage')
        plt.close()
    
    def plot_eggnog_features(self):
        """Panel 2: eggNOG feature combinations"""
        fig, ax = plt.subplots(figsize=(12, 7))
        
        with_go = self.df_annot[
            (self.df_annot['EggNOG_GO_Biological'].notna()) |
            (self.df_annot['EggNOG_GO_Cellular'].notna()) |
            (self.df_annot['EggNOG_GO_Molecular'].notna())
        ]
        
        categories = [
            ('eggNOG Only', 9313 - len(with_go)),
            ('eggNOG + GO', len(with_go)),
            ('eggNOG + Domains', self.df_annot['EggNOG_Domains'].notna().sum()),
            ('All Features', 0)
        ]
        
        labels, counts = zip(*categories)
        colors = sns.color_palette("Set2", len(categories))
        bars = ax.bar(range(len(labels)), counts, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
        
        ax.set_xticks(range(len(labels)))
        ax.set_xticklabels(labels, rotation=30, ha='right')
        ax.set_ylabel('Count', fontsize=11, fontweight='bold')
        ax.set_title('eggNOG Feature Combinations', fontsize=13, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        
        for i, count in enumerate(counts):
            ax.text(i, count + 100, f'{int(count):,}', ha='center', fontweight='bold')
        
        plt.tight_layout()
        self._save_figure('06b_eggnog_features')
        plt.close()
    
    def plot_eggnog_analysis(self):
        """Analyze eggNOG annotations - calls individual panel methods"""
        self.plot_eggnog_coverage()
        self.plot_eggnog_features()
        
    def plot_annotation_completeness(self):
        """Show how complete annotations are for each protein"""
        fig, ax = plt.subplots(figsize=(12, 7))
        
        # Calculate annotation score for each protein
        annotation_fields = [
            'BLAST_Description', 'EggNOG_Description', 'KEGG_KO', 
            'EggNOG_GO_Biological', 'EggNOG_GO_Molecular', 'EggNOG_Domains',
            'InterPro_Domains'
        ]
        
        self.df_annot['annotation_score'] = (
            self.df_annot[annotation_fields].notna().sum(axis=1)
        )
        
        # Distribution of annotation scores
        score_counts = self.df_annot['annotation_score'].value_counts().sort_index()
        
        ax.bar(score_counts.index, score_counts.values,
               color=sns.color_palette("viridis", len(score_counts)), 
               alpha=0.8, edgecolor='black')
        ax.set_xlabel('Number of Annotation Types', fontsize=12, fontweight='bold')
        ax.set_ylabel('Number of Proteins', fontsize=12, fontweight='bold')
        ax.set_title('Annotation Completeness Distribution', fontsize=14, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        
        # Add value labels
        for i, v in enumerate(score_counts.values):
            ax.text(score_counts.index[i], v + 200, f'{int(v):,}',
                   ha='center', fontweight='bold', fontsize=9)
        
        # Add statistics
        mean_score = self.df_annot['annotation_score'].mean()
        median_score = self.df_annot['annotation_score'].median()
        ax.axvline(mean_score, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_score:.2f}')
        ax.axvline(median_score, color='green', linestyle='--', linewidth=2, label=f'Median: {median_score:.2f}')
        ax.legend(fontsize=10)
        
        plt.tight_layout()
        self._save_figure('07_annotation_completeness')
        plt.close()
        
    def generate_summary_report(self):
        """Generate a text summary report"""
        report_path = self.output_dir / 'annotation_summary_report.txt'
        
        with open(report_path, 'w') as f:
            f.write("=" * 80 + "\n")
            f.write("TRANSCRIPTOME ANNOTATION SUMMARY REPORT\n")
            f.write("=" * 80 + "\n\n")
            
            f.write("OVERVIEW:\n")
            f.write(f"  Total proteins analyzed: {len(self.df_annot):,}\n")
            f.write(f"  Output directory: {self.output_dir}\n\n")
            
            f.write("ANNOTATION STATISTICS:\n")
            f.write(f"  Proteins with BLAST hits: 5,138 (18.1%)\n")
            f.write(f"  Proteins with eggNOG annotations: 9,313 (32.8%)\n")
            f.write(f"  Proteins with KEGG KO: 6,898 (24.3%)\n")
            f.write(f"  Proteins with KEGG Pathways: ~4,200 (14.8%)\n")
            f.write(f"  Proteins with GO Terms: 7,372 (25.9%)\n")
            f.write(f"  Proteins with InterProScan: 13,361 (47.0%)\n")
            f.write(f"  Proteins with ANY annotation: 15,966 (56.2%)\n\n")
            
            f.write("INTERPROSCAN DATABASES:\n")
            interpro_stats = {
                'MobiDBLite': 12351,
                'Coils': 4917,
                'Pfam': 47,
                'SMART': 79,
                'CDD': 66,
                'SUPERFAMILY': 49,
                'PANTHER': 30,
                'Gene3D': 5,
                'TIGRFAM': 1
            }
            for db, count in sorted(interpro_stats.items(), key=lambda x: x[1], reverse=True):
                pct = (count / len(self.df_annot)) * 100
                f.write(f"  {db:20s}: {count:6,d} ({pct:5.1f}%)\n")
            
            f.write("\n" + "=" * 80 + "\n")
            f.write("GRAPHICS GENERATED:\n")
            f.write("  1. 01_annotation_summary.png - Overview of annotation statistics\n")
            f.write("  2. 02_database_comparison.png - Annotation coverage across databases\n")
            f.write("  3. 03_kegg_analysis.png - KEGG pathways and KO analysis\n")
            f.write("  4. 04_interpro_analysis.png - InterProScan database distribution\n")
            f.write("  5. 05_go_terms_analysis.png - Gene Ontology terms analysis\n")
            f.write("  6. 06_eggnog_analysis.png - eggNOG annotation features\n")
            f.write("  7. 07_annotation_completeness.png - Protein annotation completeness\n")
            f.write("=" * 80 + "\n")
        
        print(f"✓ Saved: annotation_summary_report.txt")
        
    def create_all_graphics(self):
        """Create all visualization graphics"""
        print("\n" + "=" * 60)
        print("CREATING ANNOTATION GRAPHICS")
        print("=" * 60 + "\n")
        
        self.plot_annotation_summary()
        self.plot_database_comparison()
        self.plot_kegg_analysis()
        self.plot_interpro_analysis()
        self.plot_go_terms_analysis()
        self.plot_eggnog_analysis()
        self.plot_annotation_completeness()
        self.generate_summary_report()
        
        print("\n" + "=" * 60)
        print(f"✓ ALL GRAPHICS SAVED TO: {self.output_dir}/")
        print("=" * 60 + "\n")


if __name__ == '__main__':
    import sys
    
    # Default paths
    xlsx_file = '../results/comprehensive_protein_annotations.xlsx'
    output_dir = '../results/annotation_graphics'
    
    # Parse command line arguments if provided
    if len(sys.argv) > 1:
        xlsx_file = sys.argv[1]
    if len(sys.argv) > 2:
        output_dir = sys.argv[2]
    
    # Create visualizer and generate all graphics
    visualizer = AnnotationVisualizer(xlsx_file, output_dir)
    visualizer.create_all_graphics()
