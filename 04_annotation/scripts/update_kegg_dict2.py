import re
import sys

def main():
    try:
        with open('kegg_names.py', 'r') as f:
            text = f.read()

        match = re.search(r'KEGG_NAMES = \{(.*?)\}', text, re.DOTALL)
        if not match:
            print("Cannot find KEGG_NAMES dict")
            return

        dict_text = match.group(1)
        kegg_names = {}
        for line in dict_text.split('\n'):
            line = line.strip()
            if line.startswith("'"):
                parts = line.split(":", 1)
                if len(parts) == 2:
                    key = parts[0].strip().strip("'")
                    val = parts[1].strip().rstrip(",").strip("'")
                    # unescape backslash quotes
                    val = val.replace("\\'", "'")
                    kegg_names[key] = val

        added = 0
        with open('kegg_ko_list.txt', 'r') as f:
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) == 2:
                    code = parts[0].replace('path:', '')
                    name = parts[1]
                    if code not in kegg_names:
                        kegg_names[code] = name
                        added += 1
                    map_code = code.replace('ko', 'map')
                    if map_code not in kegg_names:
                        kegg_names[map_code] = name + " (ref. map)"
                        added += 1

        print(f"Added {added} items. Total is now {len(kegg_names)}")

        lines = []
        lines.append('"""')
        lines.append('kegg_names.py – Complete KEGG pathway name lookup (generated from KEGG REST API)')
        lines.append('Includes both map reference pathways and ko orthology pathways.')
        lines.append('"""')
        lines.append("KEGG_NAMES = {")
        for k, v in sorted(kegg_names.items()):
            val = v.replace("'", "\\'")
            lines.append(f"    '{k}': '{val}',")
        lines.append("}")
        lines.append("")
        lines.append("def pathway_label(code: str) -> str:")
        lines.append('    """Return human-readable name for a KEGG pathway code."""')
        lines.append("    return KEGG_NAMES.get(code.strip(), code.strip())")
        lines.append("")

        with open('kegg_names.py', 'w') as f:
            f.write("\n".join(lines))
        print("Done rewriting kegg_names.py")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
