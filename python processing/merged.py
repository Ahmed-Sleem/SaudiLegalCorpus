import os

def merge_md_files(output_file):
    """
    Merge all .md files in the current directory into one text file.
    """
    # Get all .md files in the current directory
    md_files = [f for f in os.listdir('.') if f.endswith('.md')]
    
    if not md_files:
        print("No .md files found in the current directory.")
        return
    
    # Sort files alphabetically
    md_files.sort()
    
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for md_file in md_files:
            # Write filename as a header
            outfile.write(f"=== {md_file} ===\n\n")
            
            # Write file content
            with open(md_file, 'r', encoding='utf-8') as infile:
                outfile.write(infile.read())
            
            # Add 3 newlines between files
            outfile.write("\n\n\n")
    
    print(f"Merged {len(md_files)} .md files into '{output_file}'")

if __name__ == "__main__":
    OUTPUT_FILE = "legal_dataset.txt"  # Change this if needed
    merge_md_files(OUTPUT_FILE)