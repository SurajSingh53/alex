# 🤖📚 Alex RAG Librarian Simple

**A bulletproof PDF AI assistant designed for Render deployment—intelligent document Q&A with source citations using Ollama models and Pinecone vector search.**

---

## 🚀 Deploy on Render (One-Click)

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

**Or deploy manually:**

1. **Fork this repository** to your GitHub account
2. **Create a new Web Service** on Render
3. **Connect your GitHub repository**
4. **Set environment variables** in Render dashboard:
   - `PINECONE_API_KEY`: Get from [Pinecone Console](https://app.pinecone.io/)
   - `PINECONE_INDEX`: alex-librarian (or your preferred name)
   - `OLLAMA_MODEL`: llama3.1:8b (or mistral:7b)
5. **Deploy!** 🚀

---

## ✨ What It Does

- **PDF Upload & Processing**: Drag-and-drop PDF files for instant indexing
- **Semantic Search**: Uses sentence transformers for intelligent document search
- **AI-Powered Q&A**: Ask natural language questions, get answers with page citations
- **Source Attribution**: Every answer includes the original document and page numbers
- **Ollama Integration**: Runs Llama 3.1 or Mistral locally for privacy and speed

---

## 🛠 Technical Requirements

### For Render Deployment:
- **Pinecone API key** (free tier works)
- **4GB+ RAM** (Render's free tier is sufficient for small docs)
- **Persistent disk space** for model downloads (~4GB)

### For Local Development:
- **Docker** (if running locally)
- **Python 3.11+**
- **Ollama** (for local model serving)

---

## ⚙️ Configuration

Set these environment variables in your Render dashboard:

| Variable | Default | Description |
|----------|---------|-------------|
| `PINECONE_API_KEY` | *required* | Your Pinecone API key |
| `PINECONE_INDEX` | alex-librarian | Pinecone index name |
| `OLLAMA_MODEL` | llama3.1:8b | Model to use (llama3.1:8b or mistral:7b) |
| `CHUNK_SIZE` | 800 | Text chunk size for processing |
| `MAX_DOCS` | 5 | Maximum sources per answer |
| `SIMILARITY_THRESHOLD` | 0.4 | Relevance threshold for search |

---

## 💡 Usage Examples

### Research Assistant
```
Upload: research-paper.pdf
Ask: "What are the main findings of this study?"
Get: Detailed summary with page citations
```

### Document Analysis
```
Upload: company-manual.pdf
Ask: "What is the refund policy?"
Get: Specific policy details with source pages
```

### Study Helper
```
Upload: textbook-chapter.pdf
Ask: "Explain quantum entanglement in simple terms"
Get: Clear explanation with textbook references
```

---

## 🔧 Troubleshooting

### Common Issues:

**App won't start:**
- Check Render logs for specific errors
- Verify `PINECONE_API_KEY` is set correctly
- Ensure sufficient memory allocation

**PDF processing fails:**
- Try with a smaller, simpler PDF first
- Check file isn't corrupted or password-protected
- Monitor memory usage during processing

**No answers returned:**
- Lower `SIMILARITY_THRESHOLD` to 0.2-0.3
- Increase `MAX_DOCS` to 8-10
- Verify your question relates to uploaded content

**Slow responses:**
- Switch to `OLLAMA_MODEL=mistral:7b` for speed
- Reduce `CHUNK_SIZE` to 600
- Consider upgrading Render plan for more resources

---

## 🚀 Performance Tips

- **Use Mistral** for faster responses (lower accuracy)
- **Use Llama 3.1** for better accuracy (slower responses)
- **Reduce chunk size** for faster processing
- **Increase similarity threshold** for more relevant results

---

## 📊 Project Structure

```
alex-rag-librarian/
├── app.py                 # Main Streamlit application
├── Dockerfile            # Render deployment config
├── requirements.txt      # Python dependencies
├── render.yaml          # Render service configuration
├── .env.template        # Environment variables template
├── healthcheck.sh       # Health monitoring script
├── start.sh            # Startup orchestration script
└── README.md           # This file
```

---

## 🔒 Security & Privacy

- **API keys** are stored securely in Render environment variables
- **Document processing** happens on your Render instance
- **No external API calls** for text processing (uses local Ollama)
- **Pinecone** stores only vector embeddings, not original text

---

## 🎯 Production Considerations

- **Upgrade Render plan** for high-volume usage
- **Monitor memory usage** with large PDF files
- **Set up alerts** for service health monitoring
- **Regular backups** of important Pinecone indexes

---

## 🆘 Support & Contributing

- **Issues**: [GitHub Issues](https://github.com/SurajSingh53/alex/issues)
- **Discussions**: [GitHub Discussions](https://github.com/SurajSingh53/alex/discussions)
- **PRs Welcome**: Fork, improve, submit!

---

## 📝 License

MIT License - Use, modify, and distribute freely!

---

**Built for researchers, students, and knowledge workers who need reliable document AI without the complexity.**

🚀 **Deploy to Render and start chatting with your PDFs in minutes!**