import re

missing = {
    'ko00072': 'Synthesis and degradation of ketone bodies',
    'map00072': 'Synthesis and degradation of ketone bodies (ref. map)',
    'ko00281': 'Geraniol degradation',
    'map00281': 'Geraniol degradation (ref. map)',
    'ko00471': 'D-Glutamine and D-glutamate metabolism',
    'map00471': 'D-Glutamine and D-glutamate metabolism (ref. map)',
    'ko00472': 'D-Arginine and D-ornithine metabolism',
    'map00472': 'D-Arginine and D-ornithine metabolism (ref. map)',
    'ko00473': 'D-Alanine metabolism',
    'map00473': 'D-Alanine metabolism (ref. map)',
    'ko01130': 'Biosynthesis of antibiotics',
    'map01130': 'Biosynthesis of antibiotics (ref. map)',
}

with open('kegg_names.py', 'r') as f:
    text = f.read()

match = re.search(r'KEGG_NAMES = \{(.*?)\}', text, re.DOTALL)
dict_text = match.group(1)
kegg_names = {}
for line in dict_text.split('\n'):
    line = line.strip()
    if line.startswith("'"):
        parts = line.split(":", 1)
        if len(parts) == 2:
            key = parts[0].strip().strip("'")
            val = parts[1].strip().rstrip(",").strip("'").replace("\\'", "'")
            kegg_names[key] = val

for k, v in missing.items():
    kegg_names[k] = v

lines = []
lines.append('"""')
lines.append('kegg_names.py – Complete KEGG pathway name lookup (generated from KEGG REST API and manual additions)')
lines.append('"""')
lines.append("KEGG_NAMES = {")
for k, v in sorted(kegg_names.items()):
    val = v.replace("'", "\\'")
    lines.append(f"    '{k}': '{val}',")
lines.append("}")
lines.append("")
lines.append("def pathway_label(code: str) -> str:")
lines.append("    return KEGG_NAMES.get(code.strip(), code.strip())")
lines.append("")

with open('kegg_names.py', 'w') as f:
    f.write("\n".join(lines))
print("Done adding final codes.")
