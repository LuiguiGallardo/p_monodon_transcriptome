import pandas as pd
df = pd.read_excel('../results/comprehensive_protein_annotations.xlsx', sheet_name='Protein Annotations')
codes = set()
for p in df['KEGG_Pathway'].dropna():
    for c in str(p).split(','):
        c = c.strip()
        if c.startswith('ko') or c.startswith('map'):
            codes.add(c)

from kegg_names import KEGG_NAMES
missing = sorted([c for c in codes if c not in KEGG_NAMES])
print("Missing pathways:")
for m in missing:
    print(m)
