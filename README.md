# PDF Collection Analyzer – Team - TechnoidX

## 🚀 Overview

This project is an intelligent document analysis pipeline designed for the Adobe India Hackathon Challenge. It processes collections of PDFs, extracts structured information, and ranks the most relevant sections based on a user-defined persona and job-to-be-done. The solution is modular, fully containerized, and supports batch processing of multiple collections.

---

## 🗂️ Project Structure

```
Abobe-Challenge_1b/
├── main.py
├── Dockerfile
├── requirements.txt
├── README.md
├── approach_explanation.md
├── input/
│   ├── Collection_1/
│   │   └── pdfs/
│   │       └── ...pdfs...
│   ├── Collection_2/
│   │   └── pdfs/
│   │       └── ...pdfs...
│   └── ...
├── output/
│   ├── Collection_1_input.json
│   ├── Collection_1_output.json
│   ├── Collection_2_input.json
│   ├── Collection_2_output.json
│   └── ...
├── part-1/
│   ├── process_pdfs.py
│   └── parser.py
├── part-2/
│   └── src/
│       ├── main2.py
│       ├── input_parser.py
│       ├── pdf_reader.py
│       ├── chunk_embedder.py
│       ├── ranker.py
│       └── output_writer.py
```

---

## ⚙️ How to Build and Run

### 1. **Build the Docker Image**

```bash
docker build -t pdf-collection-analyzer .
```

### 2. **Prepare Your Data**

- Place each collection of PDFs in its own folder under `input/Collection_xx/pdfs/`.

### 3. **Run the Pipeline**

```bash
docker run --rm -it \
  -v $(pwd)/input:/app/input:ro \
  -v $(pwd)/output:/app/output \
  --network none \
  pdf-collection-analyzer
```

- The pipeline will process each collection in `input/`, generating:
  - `Collection_xx_input.json` (combined metadata and document info)
  - `Collection_xx_output.json` (final ranked sections and analysis)

---

## 🧑‍💻 Workflow Details

1. **main.py**  
   - Iterates over all collections in `input/`.
   - For each collection:
     - Runs `part-1/process_pdfs.py` to generate `Collection_xx_input.json`.
     - Runs `part-2/src/main2.py` to generate `Collection_xx_output.json`.

2. **part-1/process_pdfs.py**  
   - Prompts the user for persona and job-to-be-done.
   - Extracts titles and metadata from all PDFs in the collection.
   - Outputs a single combined input JSON.

3. **part-2/src/main2.py**  
   - Loads the combined input JSON.
   - Extracts, embeds, and ranks document sections using modular logic.
   - Outputs the final JSON in the required format.

---

## 📤 Output Format

Each `Collection_xx_output.json` will contain:
- `metadata`: input documents, persona, job-to-be-done, processing timestamp
- `extracted_sections`: top-ranked sections with importance and page numbers
- `subsection_analysis`: refined text for each top section

---

## 📝 Notes

- All dependencies are listed in `requirements.txt`.
- The solution is fully containerized and runs completely offline.
- The input and output are consolidated at the collection level (not per PDF).

---

## 🙏 Acknowledgements

- Adobe India Hackathon Team
- [pdfplumber](https://github.com/jsvine/pdfplumber) and other open-source libraries

---

## 👨‍💻 Author

**Raman Kumar**
**Ram Samujh Singh**
**Rishabh Dubey**
