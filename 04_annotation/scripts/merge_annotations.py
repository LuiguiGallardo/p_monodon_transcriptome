#!/usr/bin/env python3
"""
Merge Protein Annotations from Multiple Sources

This script combines protein annotations from:
1. EnTAP results (DIAMOND, eggNOG, KEGG, GO terms)
2. InterProScan (protein domains, families, GO terms)

Output: Comprehensive Excel file with multiple sheets
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys
from collections import defaultdict

# File paths
SCRIPT_DIR = Path(__file__).parent
BASE_DIR = SCRIPT_DIR.parent
ENTAP_RESULTS = BASE_DIR / "results/entap_output/final_results/entap_results.tsv"
INTERPROSCAN_RESULTS = BASE_DIR / "results/interproscan_output/Trinity_longest_isoform_final_clean.fasta.tsv"
OUTPUT_FILE = BASE_DIR / "results/comprehensive_protein_annotations.xlsx"

# InterProScan TSV column names (no header in file)
INTERPROSCAN_COLUMNS = [
    'Protein_ID', 'MD5', 'Length', 'Analysis', 'Signature_Accession',
    'Signature_Description', 'Start', 'End', 'Score', 'Status',
    'Date', 'InterPro_Accession', 'InterPro_Description', 'GO_Terms',
    'Pathways'
]

def load_entap_results():
    """Load EnTAP results as the base dataframe"""
    print("Loading EnTAP results...")
    df = pd.read_csv(ENTAP_RESULTS, sep='\t', low_memory=False)
    print(f"  Loaded {len(df)} proteins from EnTAP")
    return df

def load_interproscan_results():
    """Load and aggregate InterProScan results per protein"""
    print("Loading InterProScan results...")
    df = pd.read_csv(INTERPROSCAN_RESULTS, sep='\t', header=None, 
                     names=INTERPROSCAN_COLUMNS, low_memory=False)
    print(f"  Loaded {len(df)} InterProScan annotations")
    
    # Aggregate by protein
    print("  Aggregating InterProScan data per protein...")
    aggregated = defaultdict(lambda: {
        'domains': set(),
        'databases': set(),
        'interpro_ids': set(),
        'interpro_descriptions': set(),
        'go_terms': set(),
        'pathways': set()
    })
    
    for _, row in df.iterrows():
        protein_id = row['Protein_ID']
        
        # Collect domain/signature information
        if pd.notna(row['Signature_Description']):
            aggregated[protein_id]['domains'].add(
                f"{row['Analysis']}:{row['Signature_Accession']} ({row['Signature_Description']})"
            )
        
        # Collect database sources
        if pd.notna(row['Analysis']):
            aggregated[protein_id]['databases'].add(row['Analysis'])
        
        # Collect InterPro IDs and descriptions
        if pd.notna(row['InterPro_Accession']):
            aggregated[protein_id]['interpro_ids'].add(row['InterPro_Accession'])
        if pd.notna(row['InterPro_Description']):
            aggregated[protein_id]['interpro_descriptions'].add(row['InterPro_Description'])
        
        # Collect GO terms
        if pd.notna(row['GO_Terms']) and row['GO_Terms']:
            go_terms = str(row['GO_Terms']).split('|')
            aggregated[protein_id]['go_terms'].update(go_terms)
        
        # Collect pathways
        if pd.notna(row['Pathways']) and row['Pathways']:
            pathways = str(row['Pathways']).split('|')
            aggregated[protein_id]['pathways'].update(pathways)
    
    # Convert to dataframe
    interproscan_data = []
    for protein_id, data in aggregated.items():
        interproscan_data.append({
            'Protein_ID': protein_id,
            'InterProScan_Domains': ' | '.join(sorted(data['domains'])) if data['domains'] else '',
            'InterProScan_Databases': ', '.join(sorted(data['databases'])) if data['databases'] else '',
            'InterProScan_InterPro_IDs': ', '.join(sorted(data['interpro_ids'])) if data['interpro_ids'] else '',
            'InterProScan_InterPro_Descriptions': ' | '.join(sorted(data['interpro_descriptions'])) if data['interpro_descriptions'] else '',
            'InterProScan_GO_Terms': ', '.join(sorted(data['go_terms'])) if data['go_terms'] else '',
            'InterProScan_Pathways': ', '.join(sorted(data['pathways'])) if data['pathways'] else '',
            'InterProScan_Domain_Count': len(data['domains']),
            'InterProScan_Database_Count': len(data['databases'])
        })
    
    interproscan_df = pd.DataFrame(interproscan_data)
    print(f"  Aggregated to {len(interproscan_df)} unique proteins")
    
    return df, interproscan_df

def merge_annotations(entap_df, interproscan_agg_df):
    """Merge EnTAP and InterProScan annotations"""
    print("Merging annotations...")
    
    # Merge on protein ID
    merged_df = entap_df.merge(
        interproscan_agg_df,
        left_on='Query_Sequence',
        right_on='Protein_ID',
        how='left'
    )
    
    # Drop duplicate Protein_ID column
    if 'Protein_ID' in merged_df.columns:
        merged_df = merged_df.drop(columns=['Protein_ID'])
    
    # Fill NaN values in InterProScan columns
    interproscan_cols = [col for col in merged_df.columns if col.startswith('InterProScan_')]
    for col in interproscan_cols:
        if col.endswith('_Count'):
            merged_df[col] = merged_df[col].fillna(0).astype(int)
        else:
            merged_df[col] = merged_df[col].fillna('N/A')
    
    # Select only annotation-relevant columns (remove numerical/statistical data)
    columns_to_keep = [
        'Query_Sequence',  # Protein ID
        
        # BLAST/Similarity Search - Functional annotations only
        'SeqSearch_Description',  # Protein description
        'SeqSearch_Species',  # Species
        
        # UniProt annotations
        'Database_UniProt_KEGG_Terms',  # KEGG terms
        'Database_UniProt_Protein_Domains',  # Protein domains
        'Database_UniProt_GO_Biological',  # GO Biological Process
        'Database_UniProt_GO_Cellular',  # GO Cellular Component
        'Database_UniProt_GO_Molecular',  # GO Molecular Function
        
        # EggNOG annotations
        'Database_EggNOG_Description',  # EggNOG description
        'Database_EggNOG_COG_Description',  # COG functional description
        'Database_EggNOG_KEGG_KO',  # KEGG KO
        'Database_EggNOG_KEGG_Pathway',  # KEGG Pathway
        'Database_EggNOG_KEGG_Module',  # KEGG Module
        'Database_EggNOG_GO_Biological',  # GO Biological Process
        'Database_EggNOG_GO_Cellular',  # GO Cellular Component
        'Database_EggNOG_GO_Molecular',  # GO Molecular Function
        'Database_EggNOG_Protein_Domains',  # Protein domains
        
        # InterProScan annotations
        'InterProScan_InterPro_Descriptions',  # InterPro descriptions
        'InterProScan_Domains',  # All domain matches
        'InterProScan_Databases',  # Databases matched
        'InterProScan_GO_Terms',  # GO terms
        'InterProScan_Pathways',  # Pathways
    ]
    
    # Keep only columns that exist in the dataframe
    columns_to_keep = [col for col in columns_to_keep if col in merged_df.columns]
    merged_df_clean = merged_df[columns_to_keep].copy()
    
    # Replace all NaN, empty strings, and 'nan' with 'N/A'
    merged_df_clean = merged_df_clean.fillna('N/A')
    merged_df_clean = merged_df_clean.replace('', 'N/A')
    merged_df_clean = merged_df_clean.replace('nan', 'N/A')
    merged_df_clean = merged_df_clean.replace('NaN', 'N/A')
    
    # Rename columns for better readability
    column_rename = {
        'Query_Sequence': 'Protein_ID',
        'SeqSearch_Description': 'BLAST_Description',
        'SeqSearch_Species': 'BLAST_Species',
        'Database_UniProt_KEGG_Terms': 'UniProt_KEGG',
        'Database_UniProt_Protein_Domains': 'UniProt_Domains',
        'Database_UniProt_GO_Biological': 'UniProt_GO_Biological',
        'Database_UniProt_GO_Cellular': 'UniProt_GO_Cellular',
        'Database_UniProt_GO_Molecular': 'UniProt_GO_Molecular',
        'Database_EggNOG_Description': 'EggNOG_Description',
        'Database_EggNOG_COG_Description': 'EggNOG_Function',
        'Database_EggNOG_KEGG_KO': 'KEGG_KO',
        'Database_EggNOG_KEGG_Pathway': 'KEGG_Pathway',
        'Database_EggNOG_KEGG_Module': 'KEGG_Module',
        'Database_EggNOG_GO_Biological': 'EggNOG_GO_Biological',
        'Database_EggNOG_GO_Cellular': 'EggNOG_GO_Cellular',
        'Database_EggNOG_GO_Molecular': 'EggNOG_GO_Molecular',
        'Database_EggNOG_Protein_Domains': 'EggNOG_Domains',
        'InterProScan_InterPro_Descriptions': 'InterPro_Descriptions',
        'InterProScan_Domains': 'InterPro_Domains',
        'InterProScan_Databases': 'InterPro_Databases',
        'InterProScan_GO_Terms': 'InterPro_GO_Terms',
        'InterProScan_Pathways': 'InterPro_Pathways',
    }
    
    merged_df_clean = merged_df_clean.rename(columns=column_rename)
    
    print(f"  Merged dataframe has {len(merged_df_clean)} rows and {len(merged_df_clean.columns)} columns")
    
    return merged_df_clean

def create_summary_statistics(merged_df, interproscan_full_df):
    """Create summary statistics sheet"""
    print("Creating summary statistics...")
    
    stats = {
        'Metric': [],
        'Count': [],
        'Percentage': []
    }
    
    total_proteins = len(merged_df)
    
    # Basic statistics
    stats['Metric'].append('Total Proteins')
    stats['Count'].append(total_proteins)
    stats['Percentage'].append('100.0%')
    
    # Proteins with BLAST hits
    blast_hits = (merged_df['BLAST_Description'] != 'N/A').sum()
    stats['Metric'].append('Proteins with BLAST Hits')
    stats['Count'].append(blast_hits)
    stats['Percentage'].append(f'{blast_hits/total_proteins*100:.1f}%')
    
    # Proteins with eggNOG annotations
    eggnog_hits = (merged_df['EggNOG_Description'] != 'N/A').sum()
    stats['Metric'].append('Proteins with eggNOG Annotations')
    stats['Count'].append(eggnog_hits)
    stats['Percentage'].append(f'{eggnog_hits/total_proteins*100:.1f}%')
    
    # Proteins with KEGG KO
    kegg_ko = (merged_df['KEGG_KO'] != 'N/A').sum()
    stats['Metric'].append('Proteins with KEGG KO')
    stats['Count'].append(kegg_ko)
    stats['Percentage'].append(f'{kegg_ko/total_proteins*100:.1f}%')
    
    # Proteins with GO terms (from eggNOG)
    go_bio = (merged_df['EggNOG_GO_Biological'] != 'N/A').sum()
    stats['Metric'].append('Proteins with GO Terms (eggNOG)')
    stats['Count'].append(go_bio)
    stats['Percentage'].append(f'{go_bio/total_proteins*100:.1f}%')
    
    # InterProScan statistics
    interproscan_hits = (merged_df['InterPro_Descriptions'] != 'N/A').sum()
    stats['Metric'].append('Proteins with InterProScan Matches')
    stats['Count'].append(interproscan_hits)
    stats['Percentage'].append(f'{interproscan_hits/total_proteins*100:.1f}%')
    
    # Total annotations
    total_interproscan_annotations = len(interproscan_full_df)
    stats['Metric'].append('Total InterProScan Annotations')
    stats['Count'].append(total_interproscan_annotations)
    stats['Percentage'].append('-')
    
    # Proteins with any annotation
    any_annotation = (
        (merged_df['BLAST_Description'] != 'N/A') |
        (merged_df['InterPro_Descriptions'] != 'N/A')
    ).sum()
    stats['Metric'].append('Proteins with Any Annotation')
    stats['Count'].append(any_annotation)
    stats['Percentage'].append(f'{any_annotation/total_proteins*100:.1f}%')
    
    # Database coverage
    stats['Metric'].append('')
    stats['Count'].append('')
    stats['Percentage'].append('')
    
    stats['Metric'].append('InterProScan Database Coverage:')
    stats['Count'].append('')
    stats['Percentage'].append('')
    
    # Count proteins per database
    for db in ['Pfam', 'SMART', 'PANTHER', 'Gene3D', 'CDD', 'SUPERFAMILY', 'TIGRFAM', 'Coils', 'MobiDBLite']:
        db_count = merged_df['InterPro_Databases'].str.contains(db, na=False).sum()
        if db_count > 0:
            stats['Metric'].append(f'  {db}')
            stats['Count'].append(db_count)
            stats['Percentage'].append(f'{db_count/total_proteins*100:.1f}%')
    
    return pd.DataFrame(stats)

def save_to_excel(merged_df, interproscan_full_df, summary_df):
    """Save all data to Excel with multiple sheets"""
    print(f"Saving to Excel: {OUTPUT_FILE}")
    
    with pd.ExcelWriter(OUTPUT_FILE, engine='openpyxl') as writer:
        # Sheet 1: Complete merged annotations (cleaned)
        merged_df.to_excel(writer, sheet_name='Protein Annotations', index=False)
        
        # Sheet 2: Summary statistics
        summary_df.to_excel(writer, sheet_name='Summary Statistics', index=False)
        
        # Auto-adjust column widths for readability
        for sheet_name in writer.sheets:
            worksheet = writer.sheets[sheet_name]
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 80)  # Cap at 80 for readability
                worksheet.column_dimensions[column_letter].width = adjusted_width
    
    print(f"  ✓ Excel file saved successfully!")
    print(f"  Location: {OUTPUT_FILE}")

def main():
    """Main execution function"""
    print("Combining Protein Annotations...")
    print()
    
    try:
        # Load data
        entap_df = load_entap_results()
        interproscan_full_df, interproscan_agg_df = load_interproscan_results()
        
        # Merge
        merged_df = merge_annotations(entap_df, interproscan_agg_df)
        
        # Create summary
        summary_df = create_summary_statistics(merged_df, interproscan_full_df)
        
        # Save to Excel
        save_to_excel(merged_df, interproscan_full_df, summary_df)
        
        print("\nSUCCESS! Merged annotations created.")
        print(f"Output saved to: {OUTPUT_FILE}\n")
        print("Sheets in the Excel file:")
        print("  1. Protein Annotations")
        print("  2. Summary Statistics\n")
        
        # Print quick summary
        print("Quick Summary:")
        print(f"  Total proteins: {len(merged_df)}")
        print(f"  Columns in output: {len(merged_df.columns)}")
        print(f"  Proteins with BLAST hits: {(merged_df['BLAST_Description'] != 'N/A').sum()}")
        print(f"  Proteins with InterProScan matches: {(merged_df['InterPro_Descriptions'] != 'N/A').sum()}")
        print()
        
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
