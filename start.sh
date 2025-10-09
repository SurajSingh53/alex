#!/bin/bash
set -e

echo "🚀 Starting Alex RAG Librarian..."

# Start Ollama in background
ollama serve &
OLLAMA_PID=$!

# Wait for Ollama
echo "⏳ Waiting for Ollama..."
for i in {1..30}; do
    if curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
        echo "✅ Ollama ready!"
        break
    fi
    sleep 2
done

# Pull model
MODEL=${OLLAMA_MODEL:-llama3.1:8b}
if ! ollama list | grep -q "$MODEL"; then
    ollama pull "$MODEL"
fi

# Start Streamlit (this must be the final command)
exec streamlit run app.py \
    --server.port=${PORT:-8501} \
    --server.address=0.0.0.0 \
    --server.headless=true
