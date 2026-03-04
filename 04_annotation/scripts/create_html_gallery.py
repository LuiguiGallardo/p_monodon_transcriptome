#!/usr/bin/env python3
"""
Generate an HTML index page for all annotation graphics
This creates an interactive gallery to view all graphics at once
"""

import os
from pathlib import Path

def create_html_index(output_dir='../results/annotation_graphics'):
    """Create an HTML index file to view all graphics"""
    
    graphics_info = [
        {
            'file': '01_annotation_summary.png',
            'title': 'Annotation Summary Overview',
            'description': 'Comprehensive 4-panel overview showing annotation counts by database, overall coverage, KEGG coverage, and top InterProScan databases.'
        },
        {
            'file': '02_database_comparison.png',
            'title': 'Database Comparison',
            'description': 'Horizontal bar chart comparing annotation coverage across all major databases (BLAST, eggNOG, KEGG, GO, InterProScan).'
        },
        {
            'file': '03_kegg_analysis.png',
            'title': 'KEGG Pathway Analysis',
            'description': 'Analysis of KEGG annotations including KO, Pathway, and Module distribution plus top 10 most frequent pathways.'
        },
        {
            'file': '04_interpro_analysis.png',
            'title': 'InterProScan Database Distribution',
            'description': 'Coverage breakdown of all InterProScan databases with MobiDBLite and Coils being most abundant.'
        },
        {
            'file': '05_go_terms_analysis.png',
            'title': 'Gene Ontology (GO) Terms Analysis',
            'description': '4-panel analysis of GO terms from eggNOG and UniProt across biological process, cellular component, and molecular function domains.'
        },
        {
            'file': '06_eggnog_analysis.png',
            'title': 'eggNOG Annotation Features',
            'description': 'eggNOG coverage and feature combinations showing strong correlation with GO term annotation.'
        },
        {
            'file': '07_annotation_completeness.png',
            'title': 'Annotation Completeness Distribution',
            'description': 'Distribution showing how many annotation types each protein has, with mean and median statistics.'
        },
        {
            'file': '08_annotation_correlation_heatmap.png',
            'title': 'Annotation Co-occurrence Correlation Matrix',
            'description': 'Heatmap showing correlation between different annotation types, revealing complementary information sources.'
        },
        {
            'file': '09_cooccurrence_analysis.png',
            'title': 'Annotation Co-occurrence & Richness Analysis',
            'description': '4-panel analysis of how annotations co-occur, proteins by annotation count, and annotation richness levels.'
        },
        {
            'file': 'quick_coverage_pie.png',
            'title': 'Quick Reference: Overall Coverage',
            'description': 'Simple pie chart showing 56.2% of proteins have some annotation.'
        },
        {
            'file': 'quick_kegg_chart.png',
            'title': 'Quick Reference: KEGG Summary',
            'description': 'Quick bar chart summary of KEGG annotation coverage.'
        },
        {
            'file': 'quick_database_table.png',
            'title': 'Quick Reference: Database Statistics Table',
            'description': 'Summary table of annotation statistics by database.'
        },
    ]
    
    html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Transcriptome Annotation Graphics Gallery</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        
        header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 30px;
            text-align: center;
        }
        
        h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .subtitle {
            font-size: 1.1em;
            opacity: 0.9;
        }
        
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
            border-bottom: 1px solid #dee2e6;
        }
        
        .stat-box {
            text-align: center;
            padding: 20px;
            background: white;
            border-radius: 8px;
            border-left: 4px solid #667eea;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .stat-number {
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }
        
        .stat-label {
            color: #666;
            margin-top: 5px;
            font-size: 0.95em;
        }
        
        .gallery {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 30px;
            padding: 40px 30px;
        }
        
        .gallery-item {
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .gallery-item:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }
        
        .gallery-item img {
            width: 100%;
            height: 300px;
            object-fit: cover;
            background: #f0f0f0;
        }
        
        .gallery-item-content {
            padding: 20px;
        }
        
        .gallery-item h3 {
            color: #667eea;
            margin-bottom: 10px;
            font-size: 1.1em;
        }
        
        .gallery-item p {
            color: #666;
            font-size: 0.95em;
            line-height: 1.5;
        }
        
        .gallery-item-filename {
            margin-top: 10px;
            padding-top: 10px;
            border-top: 1px solid #eee;
            color: #999;
            font-size: 0.85em;
            font-family: monospace;
        }
        
        footer {
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #666;
            font-size: 0.9em;
            border-top: 1px solid #dee2e6;
        }
        
        .section-title {
            grid-column: 1 / -1;
            font-size: 1.5em;
            color: #333;
            margin-top: 20px;
            padding: 10px 0;
            border-bottom: 2px solid #667eea;
        }
        
        @media (max-width: 768px) {
            h1 {
                font-size: 1.8em;
            }
            
            .gallery {
                grid-template-columns: 1fr;
                gap: 20px;
                padding: 20px;
            }
            
            .stats {
                grid-template-columns: repeat(2, 1fr);
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🧬 Transcriptome Annotation Graphics</h1>
            <p class="subtitle">Comprehensive visualization of EnTAP and InterProScan results</p>
            <p class="subtitle" style="margin-top: 10px; font-size: 0.95em;">Penaeus monodon (Pacific white shrimp) - February 2026</p>
        </header>
        
        <div class="stats">
            <div class="stat-box">
                <div class="stat-number">28,423</div>
                <div class="stat-label">Total Proteins</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">15,966</div>
                <div class="stat-label">Annotated (56.2%)</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">13,361</div>
                <div class="stat-label">InterProScan (47.0%)</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">6,898</div>
                <div class="stat-label">KEGG KO (24.3%)</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">9,313</div>
                <div class="stat-label">eggNOG (32.8%)</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">7,372</div>
                <div class="stat-label">GO Terms (25.9%)</div>
            </div>
        </div>
        
        <div class="gallery">
'''
    
    # Main visualizations
    html_content += '            <div class="section-title">📊 Main Analysis Graphics</div>\n'
    for item in graphics_info[:9]:
        html_content += f'''            <div class="gallery-item">
                <img src="{item['file']}" alt="{item['title']}" loading="lazy">
                <div class="gallery-item-content">
                    <h3>{item['title']}</h3>
                    <p>{item['description']}</p>
                    <div class="gallery-item-filename">{item['file']}</div>
                </div>
            </div>
'''
    
    # Quick reference graphics
    html_content += '            <div class="section-title">⚡ Quick Reference Graphics</div>\n'
    for item in graphics_info[9:]:
        html_content += f'''            <div class="gallery-item">
                <img src="{item['file']}" alt="{item['title']}" loading="lazy">
                <div class="gallery-item-content">
                    <h3>{item['title']}</h3>
                    <p>{item['description']}</p>
                    <div class="gallery-item-filename">{item['file']}</div>
                </div>
            </div>
'''
    
    html_content += '''        </div>
        
        <footer>
            <p>Generated using Python 3 with matplotlib and seaborn</p>
            <p>For more information, see README.md in this directory</p>
        </footer>
    </div>
</body>
</html>
'''
    
    output_path = Path(output_dir) / 'index.html'
    with open(output_path, 'w') as f:
        f.write(html_content)
    
    print(f"✓ Created interactive gallery: {output_path}")
    return output_path


if __name__ == '__main__':
    create_html_index()
    print("\n✓ Open index.html in your web browser to view all graphics!\n")
