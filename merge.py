import os

def merge_files(directory, output_filename):
    """
    Merges all text files in a directory into a single output file.

    Args:
        directory (str): The path to the directory containing the text files.
        output_filename (str): The name of the output file to create.
    """
    try:
        with open(output_filename, 'w') as outfile:
            for filename in os.listdir(directory):
                if filename.startswith("scam-") and filename.endswith(".txt"):
                    filepath = os.path.join(directory, filename)
                    try:
                        with open(filepath, 'r') as infile:
                            for line in infile:
                                outfile.write(line)
                    except Exception as e:
                        print(f"Error reading file {filename}: {e}")
        print(f"Successfully merged files into {output_filename}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
directory = "."  # Current directory
output_filename = "merged_scam_domains.txt"
merge_files(directory, output_filename)
