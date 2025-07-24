# PDF Outline Extractor 📖

A blazing-fast PDF processing solution developed for **Adobe India Hackathon 2025 - Challenge 1a**. It extracts structured data including the **document title** and **table of contents (outline)** from PDFs and outputs JSON files. Fully containerized, offline-compatible, and optimized under strict performance constraints.

---

## 🔍 Approach

This solution processes all PDFs in the `/input` directory and generates corresponding structured `.json` files in the `/output` directory. It extracts:
- The **document title**
- A hierarchical **outline** (table of contents/bookmarks), including:
  - `text`: heading text
  - `level`: outline depth (hierarchy)
  - `page`: page number where the section starts

It uses PyMuPDF to access internal PDF metadata and outline structure, then formats the extracted data to match a predefined schema.

**Key Features:**
- Processes multiple PDFs in one go
- Skips files without outlines
- Fully offline and Dockerized
- Meets all resource constraints:
  - ≤200MB model size (no ML models used)
  - ≤10 seconds for a 50-page PDF
  - CPU-only execution
  - ≤16GB RAM

---

## 📚 Models and Libraries Used

This solution **does not use any heavy ML model**. It is built using the following Python library:

- [`PyMuPDF`](https://pymupdf.readthedocs.io/en/latest/) (`fitz`) – For parsing PDF metadata and outlines

Install dependencies using:

```bash
pip install -r requirements.txt
```

**Dependencies (from `requirements.txt`):**

```
PyMuPDF==1.22.3
```

---

## ⚙️ How to Build and Run the Solution

> This section is for documentation only. The evaluation process uses the “Expected Execution” procedure.

### 📁 Folder Structure

```
Challenge_1a/
├── Dockerfile
├── README.md
├── requirements.txt
├── process_pdfs.py         # Entry point script
├── parser.py               # Core PDF parsing logic
├── json_generator.py       # (Optional) Test PDF generator
├── output_schema.json      # JSON schema definition
├── input/                  # Input folder (place PDFs here)
└── output/                 # Output folder (results saved here)
```

### 🐳 Build Docker Image

```bash
docker build -t pdf-processor .
```

### 🐳 Run the Container

```bash
docker run --rm \
  -v $(pwd)/input:/app/input:ro \
  -v $(pwd)/output:/app/output \
  --network none \
  pdf-processor
```

- `input/`: place your input PDF files here.
- `output/`: will contain extracted JSON outputs.
- `--network none`: ensures full offline compliance.

---

## 🧪 Output Format

Each output `.json` file conforms to this schema:

```json
{
  "title": "Document Title",
  "outline": [
    {
      "level": "1",
      "text": "Chapter 1",
      "page": 1
    },
    {
      "level": "2",
      "text": "Section 1.1",
      "page": 2
    }
  ]
}
```

You can validate this structure using the provided `output_schema.json`.

---

## ✅ Optional: Testing With Sample PDF

To test the system with a sample input:

```bash
python json_generator.py
```

This generates a sample PDF (e.g., `outlined_50_pages.pdf`) with a mock table of contents inside the `input/` folder.

---

## 🙏 Acknowledgements

- Adobe India Hackathon Team
- [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/)

---

## 👨‍💻 Author

**Raman Kumar**  
GitHub: [@Raman0101](https://github.com/Raman0101)
