#!/usr/bin/env python3
"""
Script to convert all PDF files from differential expression analysis to PNG format.
This script searches for all PDF files in the results_iterations directory and converts
them to PNG images with high resolution.
"""

import os
import sys
from pathlib import Path
from pdf2image import convert_from_path
from tqdm import tqdm

def find_pdf_files(base_dir):
    """
    Recursively find all PDF files in the given directory.
    
    Args:
        base_dir (str): Base directory to search for PDF files
        
    Returns:
        list: List of Path objects for all PDF files found
    """
    base_path = Path(base_dir)
    pdf_files = list(base_path.rglob("*.pdf"))
    return pdf_files

def convert_pdf_to_png(pdf_path, output_dir=None, dpi=300):
    """
    Convert a PDF file to PNG format.
    
    Args:
        pdf_path (Path): Path to the PDF file
        output_dir (str, optional): Directory to save PNG files. If None, saves in same directory as PDF
        dpi (int): Resolution for the output PNG (default: 300)
        
    Returns:
        list: List of paths to the generated PNG files
    """
    try:
        # Convert PDF to images
        images = convert_from_path(str(pdf_path), dpi=dpi)
        
        # Determine output directory
        if output_dir is None:
            output_dir = pdf_path.parent
        else:
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save each page as PNG
        png_files = []
        base_name = pdf_path.stem
        
        for i, image in enumerate(images):
            if len(images) > 1:
                # Multiple pages: add page number
                png_filename = f"{base_name}_page_{i+1}.png"
            else:
                # Single page: no page number needed
                png_filename = f"{base_name}.png"
            
            png_path = output_dir / png_filename
            image.save(str(png_path), 'PNG')
            png_files.append(png_path)
        
        return png_files
    
    except Exception as e:
        print(f"Error converting {pdf_path}: {str(e)}", file=sys.stderr)
        return []

def main():
    # Get the script directory
    script_dir = Path(__file__).parent
    
    # Define the results directory
    results_dir = script_dir.parent / "results" / "results_iterations"
    
    if not results_dir.exists():
        print(f"Error: Results directory not found: {results_dir}", file=sys.stderr)
        sys.exit(1)
    
    # Find all PDF files
    print(f"Searching for PDF files in {results_dir}...")
    pdf_files = find_pdf_files(results_dir)
    
    if not pdf_files:
        print("No PDF files found.")
        sys.exit(0)
    
    print(f"Found {len(pdf_files)} PDF files.")
    
    # Convert each PDF to PNG
    total_converted = 0
    total_png_files = 0
    
    print("\nConverting PDFs to PNG...")
    for pdf_file in tqdm(pdf_files, desc="Converting", unit="file"):
        png_files = convert_pdf_to_png(pdf_file)
        if png_files:
            total_converted += 1
            total_png_files += len(png_files)
    
    print(f"\nConversion complete!")
    print(f"Successfully converted {total_converted}/{len(pdf_files)} PDF files")
    print(f"Generated {total_png_files} PNG images")
    print(f"PNG files saved in the same directories as the original PDFs")

if __name__ == "__main__":
    main()
