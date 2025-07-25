import os
import json

OUTPUT_DIR = "/app/output"
COMBINED_FILE = "/app/output/combined_output.json"

challenge_info = {
    "challenge_id": "round_1b_002",
    "test_case_name": "travel_planner",
    "description": "France Travel"
}
persona = {
    "role": "Travel Planner"
}
job_to_be_done = {
    "task": "Plan a trip of 4 days for a group of 10 college friends."
}

def main():
    documents = []
    for filename in os.listdir(OUTPUT_DIR):
        if filename.endswith(".json") and filename != "combined_output.json":
            file_path = os.path.join(OUTPUT_DIR, filename)
            with open(file_path, "r") as f:
                data = json.load(f)
                documents.append({
                    "filename": filename.replace(".json", ".pdf"),
                    "title": data.get("title", "")
                })

    combined = {
        "challenge_info": challenge_info,
        "documents": documents,
        "persona": persona,
        "job_to_be_done": job_to_be_done
    }

    with open(COMBINED_FILE, "w") as f:
        json.dump(combined, f, indent=4)

    print(f"[INFO] Combined output written to {COMBINED_FILE}")

if __name__ == "__main__":
    main()