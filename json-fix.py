import json
import os

def update_json_format(input_file, output_file=None):
    """
    Updates the format of a JSON file from a simple key-value structure
    to a nested structure: "idx": {"url": "original_url"}

    Args:
        input_file (str): Path to the input JSON file.
        output_file (str, optional): Path to the output JSON file.
                                      If None, overwrite the input file.
    """
    if output_file is None:
        output_file = input_file  # Overwrite if no output file is specified

    try:
        with open(input_file, 'r') as f_in:
            data = json.load(f_in)
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: Input file '{input_file}' is not a valid JSON.")
        return

    # Transform the data
    transformed_data = {}
    for key, value in data.items():
        transformed_data[key] = {"url": value}

    # Write the transformed data back to the file
    try:
        with open(output_file, 'w') as f_out:
            json.dump(transformed_data, f_out, indent=2)
        print(f"Successfully transformed JSON data and saved to '{output_file}'.")
    except Exception as e:
        print(f"Error writing to file '{output_file}': {e}")

# Example usage
input_file = "scam-active.json"  # Replace with your file name
update_json_format(input_file)
