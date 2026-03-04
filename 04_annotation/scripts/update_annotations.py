#!/usr/bin/env python3
"""
Update comprehensive_protein_annotations.xlsx with all available data
from entap_output (DIAMOND similarity search + EggNOG gene family).

Sources:
  1. DIAMOND/blastp - similarity search results (uniprot_sprot)
  2. EggNOG/emapper.annotations - gene family / GO / KEGG / enzyme / pathway annotations

The script reads the existing Excel, augments each row with new data
where currently 'N/A', saves back to the same file (backup first).

New/Updated columns added or enriched:
  BLAST columns: BLAST_Description, BLAST_Species, BLAST_Hit_ID,
                 BLAST_pident, BLAST_evalue, BLAST_bitscore, BLAST_Gene_Name
  UniProt columns: UniProt_KEGG (from KEGG_ko via UniProt subject accession)
  EggNOG columns: EggNOG_Description, EggNOG_Function (COG), KEGG_KO,
                  KEGG_Pathway, KEGG_Module, KEGG_Reaction, EggNOG_EC,
                  EggNOG_BRITE, EggNOG_TC, EggNOG_CAZy, EggNOG_OGs,
                  EggNOG_seed_ortholog, EggNOG_GO_Biological,
                  EggNOG_GO_Cellular, EggNOG_GO_Molecular, EggNOG_Domains
"""

import re
import sys
import shutil
import pandas as pd
from pathlib import Path
from collections import defaultdict

# ─── Paths ────────────────────────────────────────────────────────────────────
BASE = Path("/Users/luigui/Documents/p_monodon_transcriptome/04_annotation/results")
EXCEL_IN  = BASE / "comprehensive_protein_annotations_backup.xlsx"  # always start from original
EXCEL_OUT = BASE / "comprehensive_protein_annotations.xlsx"
BACKUP    = BASE / "comprehensive_protein_annotations_backup.xlsx"

DIAMOND_FILE = (BASE / "entap_output/similarity_search/DIAMOND/"
                "blastp_Trinity_longest_isoform_final_uniprot_sprot.out")
EGGNOG_FILE  = (BASE / "entap_output/gene_family/EggNOG/"
                "blastp_Trinity_longest_isoform.emapper.annotations")

# ─── GO namespace classifier ──────────────────────────────────────────────────
# Simple prefix-based split; EggNOG GOs include all three categories mixed.
# We'll look them up from the annotation file by category prefix in go name.
# Since EggNOG doesn't separate GO by namespace in the raw file,
# we'll use a curated map approach for common GO terms.
# For simplicity we'll keep all in "EggNOG_GO_All" and also try prefix split
# using a GO namespace map if available; otherwise keep as-is.

def na(v):
    """Return 'N/A' for empty or missing values."""
    if v is None:
        return "N/A"
    v = str(v).strip()
    if v in ("", "-", "N/A", "nan", "None"):
        return "N/A"
    return v

def parse_go_by_prefix(go_str, namespace_map):
    """Split GO IDs by namespace using a provided map {go_id: namespace}."""
    bio, cell, mol = [], [], []
    for go_id in go_str.split(","):
        go_id = go_id.strip()
        ns = namespace_map.get(go_id)
        if ns == "biological_process":
            bio.append(go_id)
        elif ns == "cellular_component":
            cell.append(go_id)
        elif ns == "molecular_function":
            mol.append(go_id)
    return (
        ", ".join(bio) if bio else "N/A",
        ", ".join(cell) if cell else "N/A",
        ", ".join(mol) if mol else "N/A",
    )

# ─── 1. Load DIAMOND blast results ────────────────────────────────────────────
print("Loading DIAMOND similarity search results...")
DIAMOND_COLS = [
    "query", "subject", "pident", "length", "mismatch", "gapopen",
    "qstart", "qend", "sstart", "send", "evalue", "bitscore", "ppos", "stitle"
]
diamond_df = pd.read_csv(DIAMOND_FILE, sep="\t", header=None, names=DIAMOND_COLS)
print(f"  Total DIAMOND hits: {len(diamond_df)}")

# Keep only best hit per query (lowest evalue, then highest bitscore)
diamond_best = (
    diamond_df
    .sort_values(["evalue", "bitscore"], ascending=[True, False])
    .drop_duplicates(subset="query", keep="first")
    .set_index("query")
)
print(f"  Unique queries with DIAMOND hit: {len(diamond_best)}")

def parse_diamond_stitle(stitle):
    """
    Parse the subject title from DIAMOND output.
    Format: 'sp|ACCESSION|GENE_NAME Description OS=Species OX=TaxID GN=GeneName PE=X SV=X'
    Returns dict with keys: accession, gene_symbol, description, species, gene_name
    """
    result = {"accession": "N/A", "gene_symbol": "N/A",
              "description": "N/A", "species": "N/A", "gene_name": "N/A"}
    if not stitle or stitle == "N/A":
        return result
    # Extract species OS=...
    os_m = re.search(r" OS=(.+?)(?= OX=| PE=| SV=|$)", stitle)
    if os_m:
        result["species"] = os_m.group(1).strip()
    # Extract gene name GN=...
    gn_m = re.search(r" GN=(.+?)(?= PE=| SV=|$)", stitle)
    if gn_m:
        result["gene_name"] = gn_m.group(1).strip()
    # Extract description (between pipe and OS=)
    desc_m = re.search(r"\|[A-Z0-9_]+\s+(.+?)\s+OS=", stitle)
    if desc_m:
        result["description"] = desc_m.group(1).strip()
    # Extract accession/gene symbol from subject ID: sp|ACC|GENESYM
    subj_m = re.match(r"(?:sp|tr)\|([A-Z0-9]+)\|(\S+)", stitle)
    if subj_m:
        result["accession"] = subj_m.group(1)
        result["gene_symbol"] = subj_m.group(2)
    return result

# ─── 2. Load EggNOG annotations ───────────────────────────────────────────────
print("Loading EggNOG annotations...")
eggnog_rows = []
with open(EGGNOG_FILE) as fh:
    for line in fh:
        if line.startswith("##"):
            continue
        if line.startswith("#"):
            # This is the header line
            header = line.strip().lstrip("#").split("\t")
            continue
        eggnog_rows.append(line.strip().split("\t"))

eggnog_df = pd.DataFrame(eggnog_rows, columns=header)
eggnog_df = eggnog_df.set_index("query")
print(f"  EggNOG annotated sequences: {len(eggnog_df)}")

# ─── 3. Build GO namespace map from EggNOG data ───────────────────────────────
# We can use the obo file or approximate split by checking the counts.
# Since GO namespace lookup requires the obo file, we'll check the existing
# Excel's separation (Biological/Cellular/Molecular) using the GO IDs present
# in each category in the EggNOG data from the existing Excel columns
# (which were separated in the original data build).
# The most reliable approach: use the existing Excel as reference for which
# GOs belong to which namespace.

print("Building GO namespace map from existing Excel data...")
go_namespace = {}  # go_id -> namespace

# ─── 4. Load existing Excel ───────────────────────────────────────────────────
print("Loading existing Excel file...")
xl = pd.ExcelFile(EXCEL_IN)
df = xl.parse("Protein Annotations")
print(f"  Rows: {len(df)}, Columns: {list(df.columns)}")

# Build GO namespace map from existing data
for _, row in df.iterrows():
    for go_id_str in str(row.get("EggNOG_GO_Biological", "") or "").split(","):
        go_id = go_id_str.strip()
        if go_id.startswith("GO:"):
            go_namespace[go_id] = "biological_process"
    for go_id_str in str(row.get("EggNOG_GO_Cellular", "") or "").split(","):
        go_id = go_id_str.strip()
        if go_id.startswith("GO:"):
            go_namespace[go_id] = "cellular_component"
    for go_id_str in str(row.get("EggNOG_GO_Molecular", "") or "").split(","):
        go_id = go_id_str.strip()
        if go_id.startswith("GO:"):
            go_namespace[go_id] = "molecular_function"

print(f"  GO namespace map size: {len(go_namespace)} terms")

# ─── 5. Define new columns to add ─────────────────────────────────────────────
NEW_COLS = [
    "BLAST_Hit_ID",        # UniProt accession ID
    "BLAST_Gene_Symbol",   # Gene symbol from UniProt
    "BLAST_Gene_Name",     # Full gene name (GN field)
    "BLAST_pident",        # Percent identity
    "BLAST_evalue",        # E-value
    "BLAST_bitscore",      # Bitscore
    "EggNOG_seed_ortholog",# seed ortholog from EggNOG
    "EggNOG_evalue",       # EggNOG evalue
    "EggNOG_score",        # EggNOG score
    "EggNOG_OGs",          # EggNOG Orthologous Groups
    "EggNOG_max_annot_lvl",# Max annotation level
    "EggNOG_EC",           # Enzyme Commission numbers
    "KEGG_Reaction",       # KEGG Reactions
    "EggNOG_BRITE",        # BRITE hierarchy
    "EggNOG_TC",           # Transporter Classification
    "EggNOG_CAZy",         # CAZy family
    "EggNOG_Preferred_name", # Preferred gene name from EggNOG
]

# Add new columns if they don't exist
for col in NEW_COLS:
    if col not in df.columns:
        df[col] = "N/A"

# ─── 6. Update rows with DIAMOND and EggNOG data ─────────────────────────────
print("Updating annotation rows...")
updated_diamond = 0
updated_eggnog = 0

for idx, row in df.iterrows():
    protein_id = str(row["Protein_ID"]).strip()

    # ── DIAMOND update ──────────────────────────────────────────────────────
    if protein_id in diamond_best.index:
        d = diamond_best.loc[protein_id]
        stitle = str(d["stitle"])
        parsed = parse_diamond_stitle(stitle)

        # Always overwrite BLAST_Description and BLAST_Species from DIAMOND
        # (previous Excel may have had raw stitle strings instead of parsed values)
        df.at[idx, "BLAST_Description"] = parsed["description"]
        df.at[idx, "BLAST_Species"]     = parsed["species"]

        # Always update/fill these new/empty columns
        df.at[idx, "BLAST_Hit_ID"]      = parsed["accession"]
        df.at[idx, "BLAST_Gene_Symbol"] = parsed["gene_symbol"]
        df.at[idx, "BLAST_Gene_Name"]   = parsed["gene_name"]
        df.at[idx, "BLAST_pident"]      = f"{d['pident']}"
        df.at[idx, "BLAST_evalue"]      = f"{d['evalue']}"
        df.at[idx, "BLAST_bitscore"]    = f"{d['bitscore']}"
        updated_diamond += 1

    # ── EggNOG update ───────────────────────────────────────────────────────
    if protein_id in eggnog_df.index:
        e = eggnog_df.loc[protein_id]
        # Handle case where multiple rows exist (take first)
        if isinstance(e, pd.DataFrame):
            e = e.iloc[0]

        def eg(col):
            v = str(e.get(col, "-")).strip()
            return "N/A" if v in ("", "-", "nan", "None") else v

        # EggNOG description / function
        if na(row["EggNOG_Description"]) == "N/A":
            df.at[idx, "EggNOG_Description"] = eg("Description")

        if na(row["EggNOG_Function"]) == "N/A":
            # COG_category -> map to function name
            cog_cat = eg("COG_category")
            df.at[idx, "EggNOG_Function"] = cog_cat

        # KEGG_KO
        if na(row["KEGG_KO"]) == "N/A":
            df.at[idx, "KEGG_KO"] = eg("KEGG_ko")

        # KEGG_Pathway
        if na(row["KEGG_Pathway"]) == "N/A":
            df.at[idx, "KEGG_Pathway"] = eg("KEGG_Pathway")

        # KEGG_Module
        if na(row["KEGG_Module"]) == "N/A":
            df.at[idx, "KEGG_Module"] = eg("KEGG_Module")

        # EggNOG_Domains (PFAMs)
        if na(row["EggNOG_Domains"]) == "N/A":
            df.at[idx, "EggNOG_Domains"] = eg("PFAMs")

        # GO terms - split by namespace using our map
        go_str = eg("GOs")
        if go_str != "N/A":
            bio_ids, cell_ids, mol_ids = parse_go_by_prefix(go_str, go_namespace)

            # Update EggNOG GO columns if empty
            if na(row["EggNOG_GO_Biological"]) == "N/A" and bio_ids != "N/A":
                df.at[idx, "EggNOG_GO_Biological"] = bio_ids
            if na(row["EggNOG_GO_Cellular"]) == "N/A" and cell_ids != "N/A":
                df.at[idx, "EggNOG_GO_Cellular"] = cell_ids
            if na(row["EggNOG_GO_Molecular"]) == "N/A" and mol_ids != "N/A":
                df.at[idx, "EggNOG_GO_Molecular"] = mol_ids

        # New EggNOG columns
        df.at[idx, "EggNOG_seed_ortholog"]   = eg("seed_ortholog")
        df.at[idx, "EggNOG_evalue"]          = eg("evalue")
        df.at[idx, "EggNOG_score"]           = eg("score")
        df.at[idx, "EggNOG_OGs"]             = eg("eggNOG_OGs")
        df.at[idx, "EggNOG_max_annot_lvl"]   = eg("max_annot_lvl")
        df.at[idx, "EggNOG_EC"]              = eg("EC")
        df.at[idx, "KEGG_Reaction"]          = eg("KEGG_Reaction")
        df.at[idx, "EggNOG_BRITE"]           = eg("BRITE")
        df.at[idx, "EggNOG_TC"]              = eg("KEGG_TC")
        df.at[idx, "EggNOG_CAZy"]            = eg("CAZy")
        df.at[idx, "EggNOG_Preferred_name"]  = eg("Preferred_name")

        updated_eggnog += 1

print(f"  Updated {updated_diamond} rows with DIAMOND data")
print(f"  Updated {updated_eggnog} rows with EggNOG data")

# ─── 7. Write updated Excel ─────────────────────────────────────────────────
# Backup already exists (it's what we read from); just write the output.
print(f"Writing updated Excel to {EXCEL_OUT}...")
with pd.ExcelWriter(EXCEL_OUT, engine="xlsxwriter") as writer:
    df.to_excel(writer, sheet_name="Protein Annotations", index=False)

    workbook  = writer.book
    worksheet = writer.sheets["Protein Annotations"]

    # ── Formatting ──────────────────────────────────────────────────────────
    header_fmt = workbook.add_format({
        "bold":       True,
        "bg_color":   "#1F4E79",
        "font_color": "#FFFFFF",
        "border":     1,
        "align":      "center",
        "valign":     "vcenter",
        "text_wrap":  True,
    })
    cell_fmt = workbook.add_format({
        "border":  1,
        "valign":  "top",
        "text_wrap": True,
    })
    na_fmt = workbook.add_format({
        "border":     1,
        "valign":     "top",
        "font_color": "#AAAAAA",
        "italic":     True,
    })

    # Write header row with formatting
    for col_num, col_name in enumerate(df.columns):
        worksheet.write(0, col_num, col_name, header_fmt)

    # Set column widths
    col_widths = {
        "Gene_ID": 30, "Protein_ID": 35,
        "BLAST_Description": 40, "BLAST_Species": 25,
        "BLAST_Hit_ID": 15, "BLAST_Gene_Symbol": 18, "BLAST_Gene_Name": 20,
        "BLAST_pident": 10, "BLAST_evalue": 12, "BLAST_bitscore": 12,
        "UniProt_KEGG": 20, "UniProt_Domains": 30,
        "UniProt_GO_Biological": 50, "UniProt_GO_Cellular": 50, "UniProt_GO_Molecular": 50,
        "EggNOG_Description": 40, "EggNOG_Function": 15,
        "KEGG_KO": 20, "KEGG_Pathway": 30, "KEGG_Module": 30,
        "KEGG_Reaction": 20,
        "EggNOG_GO_Biological": 50, "EggNOG_GO_Cellular": 50, "EggNOG_GO_Molecular": 50,
        "EggNOG_Domains": 40,
        "EggNOG_seed_ortholog": 25, "EggNOG_evalue": 12, "EggNOG_score": 10,
        "EggNOG_OGs": 60, "EggNOG_max_annot_lvl": 18,
        "EggNOG_EC": 20, "EggNOG_BRITE": 40, "EggNOG_TC": 15,
        "EggNOG_CAZy": 15, "EggNOG_Preferred_name": 20,
        "InterPro_Descriptions": 50, "InterPro_Domains": 40,
        "InterPro_Databases": 25, "InterPro_GO_Terms": 50, "InterPro_Pathways": 30,
    }
    for col_num, col_name in enumerate(df.columns):
        width = col_widths.get(col_name, 20)
        worksheet.set_column(col_num, col_num, width)

    # Freeze top row
    worksheet.freeze_panes(1, 2)

    # Auto-filter
    worksheet.autofilter(0, 0, len(df), len(df.columns) - 1)

print("Done! Summary of updated annotation:")
# Final stats
for col in df.columns:
    filled = df[col].apply(lambda v: str(v).strip() not in ("N/A", "-", "", "nan", "None")).sum()
    total  = len(df)
    print(f"  {col}: {filled}/{total} filled ({100*filled/total:.1f}%)")
