import os
import subprocess

INPUT_ROOT = "input"
OUTPUT_ROOT = "output"

def run_part1(collection_path, collection_name):
    subprocess.run([
        "python", "part-1/process_pdfs.py",
        "--input_dir", os.path.join(collection_path, "pdfs"),
        "--output_json", os.path.join(OUTPUT_ROOT, f"{collection_name}_input.json")
    ], check=True)

def run_part2(collection_name):
    subprocess.run([
    "python", "part-2/src/main2.py",
    "--input_json", os.path.join(OUTPUT_ROOT, f"{collection_name}_input.json"),
    "--output_json", os.path.join(OUTPUT_ROOT, f"{collection_name}_output.json")
], check=True)

def main():
    for collection in os.listdir(INPUT_ROOT):
        collection_path = os.path.join(INPUT_ROOT, collection)
        if os.path.isdir(collection_path) and os.path.exists(os.path.join(collection_path, "pdfs")):
            print(f"Processing {collection}...")
            run_part1(collection_path, collection)
            run_part2(collection)
            print(f"Completed {collection}.\n")

if __name__ == "__main__":
    main()