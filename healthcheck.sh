#!/bin/bash

# Health check script for Alex RAG Librarian
# This script checks if all services are running properly

echo "🔧 Alex RAG Librarian Health Check"

# Check if Streamlit is running
if curl -f http://localhost:8501/_stcore/health >/dev/null 2>&1; then
    echo "✅ Streamlit: Running"
    STREAMLIT_OK=1
else
    echo "❌ Streamlit: Failed"
    STREAMLIT_OK=0
fi

# Check if Ollama is running
if curl -f http://localhost:11434/api/tags >/dev/null 2>&1; then
    echo "✅ Ollama: Running"
    OLLAMA_OK=1
else
    echo "❌ Ollama: Failed"
    OLLAMA_OK=0
fi

# Check environment variables
if [ -z "$PINECONE_API_KEY" ]; then
    echo "❌ PINECONE_API_KEY not set"
    ENV_OK=0
else
    echo "✅ Environment: Configured"
    ENV_OK=1
fi

# Overall health status
if [ $STREAMLIT_OK -eq 1 ] && [ $OLLAMA_OK -eq 1 ] && [ $ENV_OK -eq 1 ]; then
    echo "🎉 System Status: Healthy"
    exit 0
else
    echo "💥 System Status: Unhealthy"
    exit 1
fi