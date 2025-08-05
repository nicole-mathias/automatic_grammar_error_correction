FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py .
COPY templates/ templates/
COPY models/ models/
COPY t5_jfleg/ t5_jfleg/

# Expose port for HF Spaces
EXPOSE 7860

# Run the application
CMD ["python", "app.py"] 