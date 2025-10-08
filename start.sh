#!/bin/bash

# Startup script for Alex RAG Librarian on Render
set -e

echo "🚀 Starting Alex RAG Librarian..."

# Start Ollama in the background
echo "🤖 Starting Ollama service..."
ollama serve &
OLLAMA_PID=$!

# Wait for Ollama to be ready
echo "⏳ Waiting for Ollama to be ready..."
for i in {1..30}; do
    if curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
        echo "✅ Ollama is ready!"
        break
    fi
    echo "Waiting... ($i/30)"
    sleep 2
done

# Pull the specified model if it doesn't exist
MODEL=${OLLAMA_MODEL:-llama3.1:8b}
echo "📦 Checking for model: $MODEL"

if ! ollama list | grep -q "$MODEL"; then
    echo "⬇️ Downloading model: $MODEL"
    ollama pull "$MODEL"
    echo "✅ Model downloaded: $MODEL"
else
    echo "✅ Model already available: $MODEL"
fi

# Start Streamlit
echo "🎨 Starting Streamlit app..."
exec streamlit run app.py \
    --server.port=${PORT:-8501} \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --server.enableCORS=false \
    --server.enableXsrfProtection=false