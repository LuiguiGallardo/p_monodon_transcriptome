import os

# Source metadata file
import os
source_file = os.path.join(os.path.dirname(__file__), "..", "metadata", "metadata_trinity.txt")

# Iteration data (Sample IDs for each iteration)
iterations = {
    1: ["1_S1", "2_S2", "3_S3", "4_S4", "5_S5", "6_S6", "10_S10", "11_S11", "12_S12"],
    2: ["1_S1", "2_S2", "3_S3", "4_S4", "5_S5", "6_S6", "10_S10", "11_S11", "9_S9"],
    3: ["1_S1", "2_S2", "3_S3", "4_S4", "5_S5", "6_S6", "10_S10", "12_S12", "9_S9"],
    4: ["1_S1", "2_S2", "3_S3", "4_S4", "5_S5", "6_S6", "11_S11", "12_S12", "9_S9"],
    5: ["1_S1", "2_S2", "3_S3", "4_S4", "5_S5", "7_S7", "10_S10", "11_S11", "12_S12"],
    6: ["1_S1", "2_S2", "3_S3", "4_S4", "5_S5", "7_S7", "10_S10", "11_S11", "9_S9"],
    7: ["1_S1", "2_S2", "3_S3", "4_S4", "5_S5", "7_S7", "10_S10", "12_S12", "9_S9"],
    8: ["1_S1", "2_S2", "3_S3", "4_S4", "5_S5", "7_S7", "11_S11", "12_S12", "9_S9"],
    9: ["1_S1", "2_S2", "3_S3", "4_S4", "5_S5", "8_S8", "10_S10", "11_S11", "12_S12"],
    10: ["1_S1", "2_S2", "3_S3", "4_S4", "5_S5", "8_S8", "10_S10", "11_S11", "9_S9"],
    11: ["1_S1", "2_S2", "3_S3", "4_S4", "5_S5", "8_S8", "10_S10", "12_S12", "9_S9"],
    12: ["1_S1", "2_S2", "3_S3", "4_S4", "5_S5", "8_S8", "11_S11", "12_S12", "9_S9"],
    13: ["1_S1", "2_S2", "3_S3", "4_S4", "6_S6", "7_S7", "10_S10", "11_S11", "12_S12"],
    14: ["1_S1", "2_S2", "3_S3", "4_S4", "6_S6", "7_S7", "10_S10", "11_S11", "9_S9"],
    15: ["1_S1", "2_S2", "3_S3", "4_S4", "6_S6", "7_S7", "10_S10", "12_S12", "9_S9"],
    16: ["1_S1", "2_S2", "3_S3", "4_S4", "6_S6", "7_S7", "11_S11", "12_S12", "9_S9"],
    17: ["1_S1", "2_S2", "3_S3", "4_S4", "6_S6", "8_S8", "10_S10", "11_S11", "12_S12"],
    18: ["1_S1", "2_S2", "3_S3", "4_S4", "6_S6", "8_S8", "10_S10", "11_S11", "9_S9"],
    19: ["1_S1", "2_S2", "3_S3", "4_S4", "6_S6", "8_S8", "10_S10", "12_S12", "9_S9"],
    20: ["1_S1", "2_S2", "3_S3", "4_S4", "6_S6", "8_S8", "11_S11", "12_S12", "9_S9"],
    21: ["1_S1", "2_S2", "3_S3", "4_S4", "7_S7", "8_S8", "10_S10", "11_S11", "12_S12"],
    22: ["1_S1", "2_S2", "3_S3", "4_S4", "7_S7", "8_S8", "10_S10", "11_S11", "9_S9"],
    23: ["1_S1", "2_S2", "3_S3", "4_S4", "7_S7", "8_S8", "10_S10", "12_S12", "9_S9"],
    24: ["1_S1", "2_S2", "3_S3", "4_S4", "7_S7", "8_S8", "11_S11", "12_S12", "9_S9"],
    25: ["1_S1", "2_S2", "3_S3", "5_S5", "6_S6", "7_S7", "10_S10", "11_S11", "12_S12"],
    26: ["1_S1", "2_S2", "3_S3", "5_S5", "6_S6", "7_S7", "10_S10", "11_S11", "9_S9"],
    27: ["1_S1", "2_S2", "3_S3", "5_S5", "6_S6", "7_S7", "10_S10", "12_S12", "9_S9"],
    28: ["1_S1", "2_S2", "3_S3", "5_S5", "6_S6", "7_S7", "11_S11", "12_S12", "9_S9"],
    29: ["1_S1", "2_S2", "3_S3", "5_S5", "6_S6", "8_S8", "10_S10", "11_S11", "12_S12"],
    30: ["1_S1", "2_S2", "3_S3", "5_S5", "6_S6", "8_S8", "10_S10", "11_S11", "9_S9"],
    31: ["1_S1", "2_S2", "3_S3", "5_S5", "6_S6", "8_S8", "10_S10", "12_S12", "9_S9"],
    32: ["1_S1", "2_S2", "3_S3", "5_S5", "6_S6", "8_S8", "11_S11", "12_S12", "9_S9"],
    33: ["1_S1", "2_S2", "3_S3", "5_S5", "7_S7", "8_S8", "10_S10", "11_S11", "12_S12"],
    34: ["1_S1", "2_S2", "3_S3", "5_S5", "7_S7", "8_S8", "10_S10", "11_S11", "9_S9"],
    35: ["1_S1", "2_S2", "3_S3", "5_S5", "7_S7", "8_S8", "10_S10", "12_S12", "9_S9"],
    36: ["1_S1", "2_S2", "3_S3", "5_S5", "7_S7", "8_S8", "11_S11", "12_S12", "9_S9"],
    37: ["1_S1", "2_S2", "3_S3", "6_S6", "7_S7", "8_S8", "10_S10", "11_S11", "12_S12"],
    38: ["1_S1", "2_S2", "3_S3", "6_S6", "7_S7", "8_S8", "10_S10", "11_S11", "9_S9"],
    39: ["1_S1", "2_S2", "3_S3", "6_S6", "7_S7", "8_S8", "10_S10", "12_S12", "9_S9"],
    40: ["1_S1", "2_S2", "3_S3", "6_S6", "7_S7", "8_S8", "11_S11", "12_S12", "9_S9"],
}

def load_metadata(filepath):
    """
    Loads metadata into a dictionary keyed by SampleID.
    Assumes SampleID is the second column.
    """
    metadata = {}
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) >= 2:
                sample_id = parts[1]
                metadata[sample_id] = line
    return metadata

def write_iterations(metadata, iterations):
    """
    Writes iteration files to ./metadata_iterations/.
    """
    output_dir = os.path.join(os.path.dirname(__file__), "..", "metadata", "metadata_iterations")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")

    for i in range(1, 41):
        if i not in iterations:
            print(f"Warning: Iteration {i} not defined.")
            continue
        
        output_filename = os.path.join(output_dir, f"metadata_trinity_iter_{i}.txt")
        sample_ids = iterations[i]
        
        with open(output_filename, 'w') as f:
            for sample_id in sample_ids:
                if sample_id in metadata:
                    line = metadata[sample_id]
                    parts = line.split()
                    if len(parts) >= 4:
                        # Prepend relative path to fastq files
                        parts[2] = f"tmp_quality_data/{parts[2]}"
                        parts[3] = f"tmp_quality_data/{parts[3]}"
                        new_line = "\t".join(parts)
                        f.write(new_line + '\n')
                    else:
                        f.write(line + '\n') # Fallback if structure is unexpected
                else:
                    print(f"Warning: Sample ID {sample_id} not found in source metadata for iteration {i}.")
        
        print(f"Created {output_filename}")

if __name__ == "__main__":
    if not os.path.exists(source_file):
        print(f"Error: {source_file} not found.")
    else:
        metadata_dict = load_metadata(source_file)
        write_iterations(metadata_dict, iterations)
