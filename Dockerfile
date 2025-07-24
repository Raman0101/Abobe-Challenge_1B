# syntax=docker/dockerfile:1

FROM --platform=linux/amd64 python:3.10-slim

WORKDIR /app

# Copy dependency files
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Run the processing script automatically
CMD ["python", "process_pdfs.py"]
