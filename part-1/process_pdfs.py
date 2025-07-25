import os
import json
import argparse
from parser import extract_pdf_data

def process_all_pdfs(input_dir):
    documents = []
    for filename in os.listdir(input_dir):
        if filename.endswith(".pdf"):
            input_path = os.path.join(input_dir, filename)
            parsed_data = extract_pdf_data(input_path)
            documents.append({
                "filename": filename,
                "title": parsed_data.get("title", "")
            })
    return documents

def get_user_metadata():
    print("Enter challenge info:")
    challenge_id = input("Challenge ID: ")
    test_case_name = input("Test Case Name: ")
    description = input("Description: ")

    print("\nEnter persona info:")
    persona_role = input("Persona Role: ")

    print("\nEnter job to be done:")
    job_task = input("Task: ")

    return {
        "challenge_info": {
            "challenge_id": challenge_id,
            "test_case_name": test_case_name,
            "description": description
        },
        "persona": {
            "role": persona_role
        },
        "job_to_be_done": {
            "task": job_task
        }
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", required=True, help="Directory containing PDFs")
    parser.add_argument("--output_json", required=True, help="Path to output combined JSON")
    args = parser.parse_args()

    metadata = get_user_metadata()
    documents = process_all_pdfs(args.input_dir)
    combined = {
        "challenge_info": metadata["challenge_info"],
        "documents": documents,
        "persona": metadata["persona"],
        "job_to_be_done": metadata["job_to_be_done"]
    }
    with open(args.output_json, "w") as f:
        json.dump(combined, f, indent=4)
    print(f"[INFO] Combined input JSON written to {args.output_json}")

if __name__ == "__main__":
    main()