# Optimized Dockerfile for Alex RAG Librarian - Render Ready
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y     curl     git     build-essential     && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Copy requirements first for better Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Make scripts executable
RUN chmod +x start.sh healthcheck.sh

# Create necessary directories
RUN mkdir -p /app/data /app/uploads /tmp/ollama

# Set environment variables for Ollama
ENV OLLAMA_HOST=0.0.0.0
ENV OLLAMA_ORIGINS=*

# Expose port for Streamlit (Render will set PORT env var)
EXPOSE 8501
# Use startup script
CMD ["./start.sh"]
# Health check for Render
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1


