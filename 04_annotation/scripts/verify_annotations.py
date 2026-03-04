#!/usr/bin/env python3
"""
Fast verification of comprehensive_protein_annotations.xlsx
Uses openpyxl read_only (streaming) mode — works on large files quickly.

Run:
  python3 verify_annotations.py
"""

import openpyxl

EXCEL = (
    "/Users/luigui/Documents/p_monodon_transcriptome"
    "/04_annotation/results/comprehensive_protein_annotations.xlsx"
)

print("Opening (read-only streaming)…")
wb = openpyxl.load_workbook(EXCEL, read_only=True, data_only=True)
ws = wb["Protein Annotations"]

headers      = None
col_counts   = {}   # col_name -> int (filled count)
raw_stitle   = 0    # BLAST_Description cells that still have raw sp|...|... stitle
n_rows       = 0
blast_samples = []  # up to 3 fully-annotated rows to print

NA_VALS = {"N/A", "-", "", "None", "nan", None}

for row in ws.iter_rows(values_only=True):
    if headers is None:
        headers = list(row)
        col_counts = {h: 0 for h in headers}
        print(f"  Columns: {len(headers)}")
        for i, h in enumerate(headers):
            print(f"    {i+1:2d}: {h}")
        print()
        continue

    n_rows += 1
    d = dict(zip(headers, row))

    # Count filled cells per column
    for h, v in d.items():
        if str(v).strip() not in NA_VALS and v is not None:
            col_counts[h] += 1

    # Detect leftover raw stitle in BLAST_Description
    desc = str(d.get("BLAST_Description") or "")
    if desc.startswith("sp|") or desc.startswith("tr|"):
        raw_stitle += 1

    # Collect a few complete sample rows
    if (len(blast_samples) < 3
            and desc not in NA_VALS
            and not desc.startswith("sp|")
            and d.get("BLAST_Hit_ID") not in NA_VALS):
        blast_samples.append(d)

wb.close()

# ── Report ─────────────────────────────────────────────────────────────────
print(f"Total data rows: {n_rows}")
print(f"Raw stitle values remaining in BLAST_Description: {raw_stitle}  (should be 0)\n")

print("Fill rate per column:")
for h in headers:
    pct = 100 * col_counts[h] / n_rows if n_rows else 0
    bar = "█" * int(pct / 5)
    print(f"  {h:<35s} {col_counts[h]:6d}/{n_rows}  ({pct:5.1f}%)  {bar}")

print("\n── Sample annotated rows ──────────────────────────────────────────────")
for s in blast_samples:
    print(f"\nProtein         : {s.get('Protein_ID')}")
    print(f"BLAST_Description: {s.get('BLAST_Description')}")
    print(f"BLAST_Species   : {s.get('BLAST_Species')}")
    print(f"BLAST_Hit_ID    : {s.get('BLAST_Hit_ID')}")
    print(f"BLAST_Gene_Name : {s.get('BLAST_Gene_Name')}")
    print(f"BLAST_pident    : {s.get('BLAST_pident')}")
    print(f"BLAST_evalue    : {s.get('BLAST_evalue')}")
    print(f"EggNOG_Desc     : {s.get('EggNOG_Description')}")
    print(f"EggNOG_Preferred: {s.get('EggNOG_Preferred_name')}")
    print(f"KEGG_KO         : {s.get('KEGG_KO')}")
    print(f"EggNOG_EC       : {s.get('EggNOG_EC')}")
    print(f"EggNOG_OGs      : {str(s.get('EggNOG_OGs',''))[:80]}")
