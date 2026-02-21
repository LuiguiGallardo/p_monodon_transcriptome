import sys
import ast

def main():
    try:
        from kegg_names import KEGG_NAMES
    except Exception as e:
        print(f"Error importing KEGG_NAMES: {e}")
        return

    added = 0
    with open('kegg_ko_list.txt', 'r') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) == 2:
                code = parts[0].replace('path:', '')
                name = parts[1]
                if code not in KEGG_NAMES:
                    KEGG_NAMES[code] = name
                    added += 1
                map_code = code.replace('ko', 'map')
                if map_code not in KEGG_NAMES:
                    KEGG_NAMES[map_code] = name
                    added += 1

    print(f'Added {added} properties to dict. Total: {len(KEGG_NAMES)}')

    header = '''"""
kegg_names.py – Complete KEGG pathway name lookup (generated from KEGG REST API)
Includes both map reference pathways and ko orthology pathways.
"""
'''
    with open('kegg_names.py', 'w') as f:
        f.write(header)
        f.write('KEGG_NAMES = {\n')
        for k, v in sorted(KEGG_NAMES.items()):
            v_escaped = v.replace("'", "\\'")
            f.write(f"    '{k}': '{v_escaped}',\n")
        f.write('}\n\n')
        f.write('def pathway_label(code: str) -> str:\n')
        f.write('    """Return human-readable name for a KEGG pathway code."""\n')
        f.write('    return KEGG_NAMES.get(code.strip(), code.strip())\n')

    print("Success.")

if __name__ == "__main__":
    main()
