# syntax=docker/dockerfile:1

FROM --platform=linux/amd64 python:3.10-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Copy dependency file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all source code and project files
COPY . .

# Ensure input, output, and model directories exist
RUN mkdir -p /app/input && mkdir -p /app/output && mkdir -p /app/models

# Set the default command to run your main orchestrator
CMD ["python", "main.py"]
