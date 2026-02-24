#!/usr/bin/env python3
"""
Add EggNOG_EC column to comprehensive_protein_annotations.xlsx.

Reads the existing Excel, adds (or updates) the EggNOG_EC column from the
EggNOG emapper annotations file, and saves back to the same file.

Formatting: only bold column headers. No colours, borders, or width limits.
"""

import pandas as pd
from pathlib import Path

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE      = Path("/Users/luigui/Documents/p_monodon_transcriptome/04_annotation/results")
EXCEL_IN  = BASE / "comprehensive_protein_annotations.xlsx"
EXCEL_OUT = BASE / "comprehensive_protein_annotations.xlsx"   # overwrite in place

EGGNOG_FILE = (
    BASE / "entap_output/gene_family/EggNOG/"
           "blastp_Trinity_longest_isoform.emapper.annotations"
)

# ── 1. Load EggNOG annotations ────────────────────────────────────────────────
print("Loading EggNOG annotations...")
eggnog_rows, header = [], None
with open(EGGNOG_FILE) as fh:
    for line in fh:
        if line.startswith("##"):
            continue
        if line.startswith("#"):
            header = line.strip().lstrip("#").split("\t")
            continue
        eggnog_rows.append(line.strip().split("\t"))

eggnog_df = pd.DataFrame(eggnog_rows, columns=header).set_index("query")
print(f"  EggNOG annotated sequences: {len(eggnog_df)}")

def eg(series, col):
    """Return clean value or 'N/A'."""
    v = str(series.get(col, "-")).strip()
    return "N/A" if v in ("", "-", "nan", "None") else v

# ── 2. Load existing Excel ────────────────────────────────────────────────────
print("Loading existing Excel file...")
df = pd.read_excel(EXCEL_IN, sheet_name="Protein Annotations")
print(f"  Rows: {len(df)}, Columns: {len(df.columns)}")

# ── 3. Add / update EggNOG_EC column ─────────────────────────────────────────
print("Adding EggNOG_EC column...")
if "EggNOG_EC" not in df.columns:
    df["EggNOG_EC"] = "N/A"

updated = 0
for idx, row in df.iterrows():
    protein_id = str(row["Protein_ID"]).strip()
    if protein_id in eggnog_df.index:
        e = eggnog_df.loc[protein_id]
        if isinstance(e, pd.DataFrame):
            e = e.iloc[0]
        ec_val = eg(e, "EC")
        df.at[idx, "EggNOG_EC"] = ec_val
        if ec_val != "N/A":
            updated += 1

filled = (df["EggNOG_EC"].apply(lambda v: str(v).strip() not in ("N/A", "-", "", "nan", "None"))).sum()
print(f"  EggNOG_EC: {filled}/{len(df)} filled ({100*filled/len(df):.1f}%)")

# ── 4. Drop numeric / statistical columns ─────────────────────────────────────
NUMERIC_COLS = [
    "BLAST_pident", "BLAST_evalue", "BLAST_bitscore",
    "EggNOG_evalue", "EggNOG_score", "EggNOG_max_annot_lvl",
]
drop_cols = [c for c in NUMERIC_COLS if c in df.columns]
if drop_cols:
    df = df.drop(columns=drop_cols)
    print(f"  Dropped columns: {drop_cols}")

# ── 5. Fill empty cells with N/A ──────────────────────────────────────────────
df = df.fillna("N/A")
# Also replace blank strings
df = df.replace(r'^\s*$', "N/A", regex=True)

# ── 5. Write Excel with bold-only headers ─────────────────────────────────────
from openpyxl import load_workbook
from openpyxl.styles import Font

print(f"Writing updated Excel to {EXCEL_OUT}...")
with pd.ExcelWriter(EXCEL_OUT, engine="openpyxl") as writer:
    df.to_excel(writer, sheet_name="Protein Annotations", index=False)

    ws = writer.sheets["Protein Annotations"]
    bold = Font(bold=True)
    for cell in ws[1]:          # row 1 = header
        cell.font = bold

print("Done!")
