import pdfplumber
import os

def extract_chunks_from_pdf(pdf_path, max_chunk_length=1000):
    """
    Extracts text chunks from a single PDF.
    Chunks are paragraph-separated or fixed-length (if very long).
    Returns a list of (document_name, chunk_text, page_number).
    """
    chunks = []
    document_name = os.path.basename(pdf_path)

    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if not text:
                continue

            paragraphs = text.split('\n\n')
            for para in paragraphs:
                clean_para = para.strip().replace('\n', ' ')
                if not clean_para:
                    continue

                # Split if paragraph too long
                if len(clean_para) > max_chunk_length:
                    for i in range(0, len(clean_para), max_chunk_length):
                        chunk = clean_para[i:i+max_chunk_length]
                        chunks.append((document_name, chunk.strip(), page_number))
                else:
                    chunks.append((document_name, clean_para, page_number))

    return chunks


def extract_all_chunks_from_folder(folder_path):
    """
    Extracts chunks from all PDFs in a folder.
    Returns a combined list of tuples: (document_name, chunk_text, page_number)
    """
    all_chunks = []
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.pdf'):
            full_path = os.path.join(folder_path, filename)
            chunks = extract_chunks_from_pdf(full_path)
            all_chunks.extend(chunks)
    
    return all_chunks
