import os
import json
from parser import extract_pdf_data

INPUT_DIR = "/app/input"
OUTPUT_DIR = "/app/output"

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

def process_all_pdfs():
    documents = []
    for filename in os.listdir(INPUT_DIR):
        if filename.endswith(".pdf"):
            input_path = os.path.join(INPUT_DIR, filename)
            parsed_data = extract_pdf_data(input_path)
            documents.append({
                "filename": filename,
                "title": parsed_data.get("title", "")
            })
    return documents

def generate_combined_json(metadata, documents):
    combined = {
        "challenge_info": metadata["challenge_info"],
        "documents": documents,
        "persona": metadata["persona"],
        "job_to_be_done": metadata["job_to_be_done"]
    }
    combined_path = os.path.join(OUTPUT_DIR, "combined_output.json")
    with open(combined_path, "w") as f:
        json.dump(combined, f, indent=4)
    print(f"[INFO] Combined output written to combined_output.json")

if __name__ == "__main__":
    metadata = get_user_metadata()
    documents = process_all_pdfs()
    generate_combined_json(metadata, documents)