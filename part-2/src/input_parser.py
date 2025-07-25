# src/input_parser.py
import json

def load_input_config(input_file):
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    challenge_info = data["challenge_info"]
    documents = data["documents"]
    persona = data["persona"]["role"]
    job = data["job_to_be_done"]["task"]

    return {
        "challenge_info": challenge_info,
        "documents": documents,
        "persona": {"role": persona},
        "job_to_be_done": {"task": job}
    }
