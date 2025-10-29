import json

# Define input files
input_files = [
    r"C:\Users\shasa\OneDrive\Desktop\BTP\CodemixedQAC\CodemixedQAC\dump\master-normalized\amazonshop\langdetect\amazontask2_detect_train.jsonl",
    r"C:\Users\shasa\OneDrive\Desktop\BTP\CodemixedQAC\CodemixedQAC\dump\master-normalized\msmarco\langdetect\msmarco_detect_dev.jsonl",
    r"C:\Users\shasa\OneDrive\Desktop\BTP\CodemixedQAC\CodemixedQAC\dump\master-normalized\msmarco\langdetect\msmarco_detect_test.jsonl",
]

# Define output files
french_italian_output_file = r"C:\Users\shasa\OneDrive\Desktop\BTP\french_italian_queries.jsonl"
polish_english_output_file = r"C:\Users\shasa\OneDrive\Desktop\BTP\polish_english_queries.jsonl"
danish_english_output_file = r"C:\Users\shasa\OneDrive\Desktop\BTP\danish_english_queries.jsonl"
french_spanish_output_file = r"C:\Users\shasa\OneDrive\Desktop\BTP\french_spanish_queries.jsonl"

# Function to process a single file and append to outputs
def process_file(input_file_path):
    try:
        with open(input_file_path, 'r', encoding='utf-8') as infile:
            for line in infile:
                try:
                    data = json.loads(line.strip())

                    # Check for French/Italian
                    if len(data.get('lang', [])) == 2 and 'french' in data.get('lang', []) and 'italian' in data.get('lang', []):
                        with open(french_italian_output_file, 'a', encoding='utf-8') as outfile:
                            outfile.write(json.dumps(data, ensure_ascii=False) + '\n')

                    # Check for Polish/English
                    if len(data.get('lang', [])) == 2 and 'polish' in data.get('lang', []) and 'english' in data.get('lang', []):
                        with open(polish_english_output_file, 'a', encoding='utf-8') as outfile:
                            outfile.write(json.dumps(data, ensure_ascii=False) + '\n')

                    # Check for Danish/English
                    if len(data.get('lang', [])) == 2 and 'danish' in data.get('lang', []) and 'english' in data.get('lang', []):
                        with open(danish_english_output_file, 'a', encoding='utf-8') as outfile:
                            outfile.write(json.dumps(data, ensure_ascii=False) + '\n')

                    # Check for French/Spanish
                    if len(data.get('lang', [])) == 2 and 'french' in data.get('lang', []) and 'spanish' in data.get('lang', []):
                        with open(french_spanish_output_file, 'a', encoding='utf-8') as outfile:
                            outfile.write(json.dumps(data, ensure_ascii=False) + '\n')

                except json.JSONDecodeError:
                    print(f"Skipping malformed JSON line in {input_file_path}: {line.strip()}")
    except FileNotFoundError:
        print(f"Error: Input file not found at {input_file_path}")
    except Exception as e:
        print(f"An error occurred while processing {input_file_path}: {e}")

# Main execution
if __name__ == "__main__":
    # Clear existing content in output files before appending new data
    # This ensures we don't duplicate entries from previous runs if the script is run multiple times
    open(french_italian_output_file, 'w', encoding='utf-8').close()
    open(polish_english_output_file, 'w', encoding='utf-8').close()
    open(danish_english_output_file, 'w', encoding='utf-8').close()
    open(french_spanish_output_file, 'w', encoding='utf-8').close()

    for file_path in input_files:
        print(f"Processing {file_path}...")
        process_file(file_path)
    print("Processing complete.")
