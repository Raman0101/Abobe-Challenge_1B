# PDF Collection Analyzer 📖

A blazing-fast PDF processing solution developed for **Adobe India Hackathon 2025 - Challenge 1a**. This system acts as an intelligent document analyst, extracting the **title** from each PDF in a collection and generating a single, structured `combined_output.json` file. The solution is fully containerized, offline-compatible, and optimized for strict performance constraints.

---

## 🔍 Approach

This solution processes all PDFs in the `/input` directory and generates **one combined JSON file** in the `/output` directory. It extracts:
- The **document title** from each PDF
- The **filename** of each PDF

It then combines these with user-provided metadata:
- **Challenge Info** (challenge ID, test case name, description)
- **Persona** (role)
- **Job-to-be-done** (task)

All metadata is collected via command-line prompts at runtime, making the solution fully generic and adaptable to any domain, persona, or task.

---

## 📚 Libraries Used

This solution **does not use any heavy ML model**. It is built using the following Python library:

- [`pdfplumber`](https://github.com/jsvine/pdfplumber) – For parsing PDF content and extracting titles

Install dependencies using:

```bash
pip install -r requirements.txt
```

**Dependencies (from `requirements.txt`):**

```
pdfplumber==0.10.2
```

---

## ⚙️ How to Build and Run the Solution

### 📁 Folder Structure

```
Abobe-Challenge_1a/
├── Dockerfile
├── README.md
├── requirements.txt
├── process_pdfs.py         # Entry point script
├── parser.py               # Core PDF parsing logic
├── output_schema.json      # JSON schema definition (optional)
├── input/                  # Input folder (place PDFs here)
└── output/                 # Output folder (combined_output.json saved here)
```

### 🐳 Build Docker Image

```bash
docker build -t pdf-collection-analyzer .
```

### 🐳 Run the Container

```bash
docker run --rm -it \
  -v $(pwd)/input:/app/input:ro \
  -v $(pwd)/output:/app/output \
  --network none \
  pdf-collection-analyzer
```

- `input/`: place your input PDF files here.
- `output/`: will contain the single `combined_output.json` result.
- `--network none`: ensures full offline compliance.

---

## 🧑‍💻 How to Use (Locally)

1. Place your PDFs in the `input/` directory.
2. Run:
    ```bash
    python3 process_pdfs.py
    ```
3. When prompted, enter:
    - Challenge ID
    - Test Case Name
    - Description
    - Persona Role
    - Job-to-be-done Task
4. The combined output will be saved as `output/combined_output.json`.

---

## 🧪 Output Format

The output `combined_output.json` file will look like:

```json
{
  "challenge_info": {
    "challenge_id": "round_1b_002",
    "test_case_name": "travel_planner",
    "description": "France Travel"
  },
  "documents": [
    {
      "filename": "South of France - Cities.pdf",
      "title": "Comprehensive Guide to Major Cities in the South of France"
    },
    {
      "filename": "South of France - Cuisine.pdf",
      "title": "A Culinary Journey Through the South of France"
    }
    // ...more documents
  ],
  "persona": {
    "role": "Travel Planner"
  },
  "job_to_be_done": {
    "task": "Plan a trip of 4 days for a group of 10 college friends."
  }
}
```

---

## ✅ Notes

- Only a single `combined_output.json` is generated per run.
- No individual JSON files are created for each PDF.
- The solution is fully generic: all metadata is provided by the user at runtime.

---

## 🙏 Acknowledgements

- Adobe India Hackathon Team
- [pdfplumber](https://github.com/jsvine/pdfplumber)

---

## 👨‍💻 Author

**Raman Kumar**  
GitHub: [@Raman0101](https://github.com/Raman0101)