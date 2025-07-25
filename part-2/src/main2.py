import argparse
import os

from input_parser import load_input_config
from pdf_reader import extract_all_chunks_from_folder
from chunk_embedder import embed_chunks, embed_query
from ranker import rank_chunks
from output_writer import generate_output_json

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_json", required=True, help="Input JSON from part-1")
    parser.add_argument("--output_json", required=True, help="Output JSON for part-2")
    args = parser.parse_args()

    # 1. Load input config
    input_config = load_input_config(args.input_json)
    pdf_folder = None
    # Find the folder containing the PDFs
    for doc in input_config["documents"]:
        # Assume all PDFs are in the same folder as the first one
        pdf_folder = os.path.dirname(os.path.abspath(args.input_json)).replace("output", "input")  # crude but works if structure is consistent
        break

    # 2. Extract all chunks from PDFs
    # You may want to pass the actual folder path, e.g., input/collection_xx/pdfs
    # For that, you may need to pass the folder as an argument or infer from input_json name
    collection_name = os.path.basename(args.input_json).replace("_input.json", "")
    pdfs_folder = os.path.join("input", collection_name, "pdfs")
    all_chunks = extract_all_chunks_from_folder(pdfs_folder)

    # 3. Embed chunks
    embedded_chunks = embed_chunks(all_chunks)

    # 4. Embed query (persona + job)
    persona = input_config["persona"]["role"]
    job = input_config["job_to_be_done"]["task"]
    query = f"{persona}: {job}"
    query_embedding = embed_query(query)

    # 5. Rank chunks
    top_sections = rank_chunks(embedded_chunks, query_embedding, top_k=5)

    # 6. Write output
    generate_output_json(input_config, top_sections, args.output_json)

if __name__ == "__main__":
    main()