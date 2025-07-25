import json
from datetime import datetime

def generate_output_json(input_config, top_sections, output_path):
    """
    input_config: Parsed challenge1b_input.json dict
    top_sections: List of dicts from rank_chunks()
    output_path: Path to write output JSON
    """

    metadata = {
        "input_documents": [doc["filename"] for doc in input_config["documents"]],
        "persona": input_config["persona"]["role"],
        "job_to_be_done": input_config["job_to_be_done"]["task"],
        "processing_timestamp": datetime.now().isoformat()
    }

    extracted_sections = []
    subsection_analysis = []

    for section in top_sections:
        extracted_sections.append({
            "document": section["document"],
            "section_title": section["section_title"],
            "importance_rank": section["importance_rank"],
            "page_number": section["page_number"]
        })

        subsection_analysis.append({
            "document": section["document"],
            "refined_text": section["refined_text"],
            "page_number": section["page_number"]
        })

    output_data = {
        "metadata": metadata,
        "extracted_sections": extracted_sections,
        "subsection_analysis": subsection_analysis
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(f"[✔] Output written to {output_path}")
