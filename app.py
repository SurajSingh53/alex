import streamlit as st
import os
import requests
from dotenv import load_dotenv
import tempfile
import PyPDF2
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
import numpy as np
import time
from pinecone import Pinecone, ServerlessSpec

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="Alex RAG Librarian",
    page_icon="🤖📚",
    layout="wide"
)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'documents' not in st.session_state:
    st.session_state.documents = []

def init_pinecone():
    """Initialize Pinecone connection"""
    try:
        api_key = os.getenv('PINECONE_API_KEY')
        if not api_key:
            st.error("❌ Pinecone API key not found. Please set PINECONE_API_KEY environment variable.")
            return None
        
        pc = Pinecone(api_key=api_key)
        index_name = os.getenv('PINECONE_INDEX', 'alex-librarian')
        
        # Create index if it doesn't exist
        existing_indexes = [index.name for index in pc.list_indexes()]
        if index_name not in existing_indexes:
            pc.create_index(
                name=index_name,
                dimension=384,
                metric='cosine',
                spec=ServerlessSpec(
                    cloud='aws',
                    region='us-east-1'
                )
            )
            # Wait for index to be ready
            while not pc.describe_index(index_name).status['ready']:
                time.sleep(1)
        
        return pc.Index(index_name)
    except Exception as e:
        st.error(f"❌ Failed to connect to Pinecone: {str(e)}")
        return None


@st.cache_resource
def load_embedding_model():
    """Load sentence transformer model for embeddings"""
    try:
        return SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    except Exception as e:
        st.error(f"❌ Failed to load embedding model: {str(e)}")
        return None

def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF"""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(pdf_file.getvalue())
            tmp_file.flush()

            text = ""
            with open(tmp_file.name, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page_num, page in enumerate(pdf_reader.pages):
                    page_text = page.extract_text()
                    text += f"[Page {page_num + 1}] {page_text}\n\n"

            os.unlink(tmp_file.name)
            return text
    except Exception as e:
        st.error(f"❌ Failed to extract text from PDF: {str(e)}")
        return None

def chunk_text(text, chunk_size=800, overlap=100):
    """Split text into chunks for processing"""
    chunks = []
    words = text.split()

    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks

def query_ollama(question, context):
    """Query Ollama model with context"""
    try:
        model = os.getenv('OLLAMA_MODEL', 'llama3.1:8b')
        prompt = f"""Based on the following context from documents, answer the question. If the answer isn't in the context, say so.

Context:
{context}

Question: {question}

Answer:"""

        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                'model': model,
                'prompt': prompt,
                'stream': False
            },
            timeout=30
        )

        if response.status_code == 200:
            return response.json()['response']
        else:
            return f"❌ Ollama error: {response.status_code}"
    except Exception as e:
        return f"❌ Failed to query Ollama: {str(e)}"

def main():
    st.title("🤖📚 Alex RAG Librarian")
    st.markdown("**Your intelligent PDF assistant with source citations**")

    # Initialize services
    index = init_pinecone()
    embedding_model = load_embedding_model()

    if not index or not embedding_model:
        st.stop()

    # Sidebar for document management
    with st.sidebar:
        st.header("📁 Document Management")

        uploaded_file = st.file_uploader(
            "Upload PDF", 
            type=['pdf'],
            help="Upload a PDF document to add to your knowledge base"
        )

        if uploaded_file and st.button("Process PDF"):
            with st.spinner("Processing PDF..."):
                # Extract text
                text = extract_text_from_pdf(uploaded_file)
                if text:
                    # Chunk text
                    chunks = chunk_text(text)

                    # Generate embeddings and store in Pinecone
                    embeddings = embedding_model.encode(chunks)

                    vectors = []
                    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                        vectors.append({
                            'id': f"{uploaded_file.name}_{i}",
                            'values': embedding.tolist(),
                            'metadata': {
                                'text': chunk,
                                'source': uploaded_file.name,
                                'chunk_id': i
                            }
                        })

                    # Upsert to Pinecone
                    index.upsert(vectors)
                    st.success(f"✅ Processed {len(chunks)} chunks from {uploaded_file.name}")
                    st.session_state.documents.append(uploaded_file.name)

        # Show uploaded documents
        if st.session_state.documents:
            st.subheader("📚 Uploaded Documents")
            for doc in st.session_state.documents:
                st.text(f"• {doc}")

    # Main chat interface
    st.header("💬 Ask Questions")

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask a question about your documents..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # Search for relevant chunks
                query_embedding = embedding_model.encode([prompt])[0]

                search_results = index.query(
                    vector=query_embedding.tolist(),
                    top_k=int(os.getenv('MAX_DOCS', 5)),
                    include_metadata=True
                )

                # Prepare context
                context = ""
                sources = set()
                for match in search_results['matches']:
                    if match['score'] > float(os.getenv('SIMILARITY_THRESHOLD', 0.4)):
                        context += f"{match['metadata']['text']}\n\n"
                        sources.add(match['metadata']['source'])

                if context:
                    # Query Ollama
                    response = query_ollama(prompt, context)

                    # Add sources
                    if sources:
                        response += f"\n\n📖 **Sources:** {', '.join(sources)}"
                else:
                    response = "❌ No relevant information found in your documents."

                st.write(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

    # Health status
    with st.expander("🔧 System Status"):
        col1, col2, col3 = st.columns(3)

        with col1:
            # Check Pinecone
            if index:
                st.success("✅ Pinecone Connected")
            else:
                st.error("❌ Pinecone Failed")

        with col2:
            # Check Ollama
            try:
                response = requests.get('http://localhost:11434/api/tags', timeout=5)
                if response.status_code == 200:
                    st.success("✅ Ollama Ready")
                else:
                    st.error("❌ Ollama Failed")
            except:
                st.error("❌ Ollama Failed")

        with col3:
            # Check embedding model
            if embedding_model:
                st.success("✅ Embeddings Ready")
            else:
                st.error("❌ Embeddings Failed")

if __name__ == "__main__":
    main()
