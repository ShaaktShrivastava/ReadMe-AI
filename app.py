import streamlit as st
from dotenv import load_dotenv
import tempfile
import os

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_mistralai import MistralAIEmbeddings
from langchain_chroma import Chroma
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate


load_dotenv()

# Check for API key
mistral_api_key = os.getenv("MISTRAL_API_KEY")
if not mistral_api_key:
    # Try Streamlit secrets for cloud deployment
    try:
        mistral_api_key = st.secrets["MISTRAL_API_KEY"]
        os.environ["MISTRAL_API_KEY"] = mistral_api_key
    except:
        pass

st.set_page_config(
    page_title="ReadMeAI",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enhanced Custom CSS with dynamic styles and animations
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Animated gradient background */
    .stApp {
        background: linear-gradient(-45deg, #667eea, #764ba2, #f093fb, #4facfe);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Floating particles effect */
    .stApp::before {
        content: '';
        position: fixed;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(circle at 20% 50%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 40% 20%, rgba(255, 255, 255, 0.1) 0%, transparent 50%);
        animation: floatParticles 20s ease-in-out infinite;
        pointer-events: none;
        z-index: 0;
    }
    
    @keyframes floatParticles {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
    }
    
    /* Main container with glass effect */
    .main {
        position: relative;
        z-index: 1;
    }
    
    /* Header with animation */
    .header-container {
        text-align: center;
        margin-bottom: 3rem;
        animation: fadeInDown 1s ease-out;
    }
    
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    h1 {
        color: white;
        text-align: center;
        font-size: 4rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 0 4px 6px rgba(0,0,0,0.3);
        letter-spacing: 2px;
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { text-shadow: 0 0 20px rgba(255,255,255,0.5), 0 4px 6px rgba(0,0,0,0.3); }
        to { text-shadow: 0 0 30px rgba(255,255,255,0.8), 0 4px 6px rgba(0,0,0,0.3); }
    }
    
    .subtitle {
        color: rgba(255, 255, 255, 0.95);
        text-align: center;
        font-size: 1.3rem;
        font-weight: 300;
        margin-bottom: 2rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    /* Card-style containers */
    .upload-container, .question-container {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        animation: fadeInUp 1s ease-out;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    h3 {
        color: white !important;
        font-weight: 600;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
        margin-bottom: 1rem;
    }
    
    /* Enhanced buttons */
    .stButton>button {
        background: linear-gradient(135deg, rgba(255,255,255,0.2), rgba(255,255,255,0.1));
        backdrop-filter: blur(10px);
        color: white;
        border: 2px solid rgba(255,255,255,0.3);
        padding: 0.75rem 2.5rem;
        border-radius: 50px;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 6px 25px rgba(0,0,0,0.3);
        background: linear-gradient(135deg, rgba(255,255,255,0.3), rgba(255,255,255,0.2));
        border-color: rgba(255,255,255,0.5);
    }
    
    .stButton>button:active {
        transform: translateY(-1px);
    }
    
    /* File uploader styling */
    .stFileUploader {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 1.5rem;
        border: 2px dashed rgba(255, 255, 255, 0.3);
        transition: all 0.3s ease;
    }
    
    .stFileUploader:hover {
        border-color: rgba(255, 255, 255, 0.6);
        background: rgba(255, 255, 255, 0.15);
    }
    
    /* Text input styling */
    .stTextInput>div>div>input {
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-radius: 50px;
        color: white;
        padding: 1rem 1.5rem;
        font-size: 1.1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: rgba(255, 255, 255, 0.6);
        box-shadow: 0 0 20px rgba(255, 255, 255, 0.3);
        background: rgba(255, 255, 255, 0.25);
    }
    
    .stTextInput>div>div>input::placeholder {
        color: rgba(255, 255, 255, 0.6);
    }
    
    /* Answer box with enhanced styling */
    .answer-box {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0.1));
        backdrop-filter: blur(20px);
        padding: 2rem;
        border-radius: 20px;
        border: 2px solid rgba(255, 255, 255, 0.3);
        color: white;
        font-size: 1.15rem;
        line-height: 1.8;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        animation: slideIn 0.5s ease-out;
        margin-top: 2rem;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Success/Info messages */
    .stSuccess, .stInfo {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        border-left: 4px solid rgba(255, 255, 255, 0.8);
        color: white;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-color: rgba(255, 255, 255, 0.3);
        border-top-color: white;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Responsive design */
    @media (max-width: 768px) {
        h1 { font-size: 2.5rem; }
        .subtitle { font-size: 1rem; }
        .upload-container, .question-container { padding: 1.5rem; }
    }
    </style>
""", unsafe_allow_html=True)

# Animated header
st.markdown("""
    <div class='header-container'>
        <h1>📚 ReadMeAI</h1>
        <p class='subtitle'>✨ Your AI-Powered Reading Companion • Upload PDFs and Get Instant Answers ✨</p>
    </div>
""", unsafe_allow_html=True)


# Upload Section with container
st.markdown("<div class='upload-container'>", unsafe_allow_html=True)
st.markdown("### 📤 Upload Your Document")
uploaded_file = st.file_uploader("Choose a PDF file to analyze", type="pdf", label_visibility="collapsed")
st.markdown("</div>", unsafe_allow_html=True)

if uploaded_file:

    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.read())
        file_path = tmp_file.name

    st.success("✅ PDF uploaded successfully!")

    if st.button("🚀 Create Vector Database"):
        
        # Check API key
        if not os.getenv("MISTRAL_API_KEY"):
            st.error("⚠️ MISTRAL_API_KEY not found! Please add it to Streamlit Cloud Secrets or your .env file.")
            st.stop()

        try:
            with st.spinner("🔄 Processing document..."):

                loader = PyPDFLoader(file_path)
                docs = loader.load()

                splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1000,
                    chunk_overlap=200
                )

                chunks = splitter.split_documents(docs)

                embeddings = MistralAIEmbeddings(model="mistral-embed")

                vectorstore = Chroma.from_documents(
                    documents=chunks,
                    embedding=embeddings,
                    persist_directory="chroma_db"
                )

            st.success(f"✨ Vector database created! Processed {len(docs)} pages into {len(chunks)} chunks.")
        
        except Exception as e:
            st.error(f"❌ Error creating vector database: {str(e)}")
            st.info("💡 Please check that your MISTRAL_API_KEY is valid and has sufficient credits.")

# Question Section
if os.path.exists("chroma_db"):
    
    embeddings = MistralAIEmbeddings(model="mistral-embed")

    vectorstore = Chroma(
        persist_directory="chroma_db",
        embedding_function=embeddings
    )

    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k":4,
            "fetch_k":10,
            "lambda_mult":0.5
        }
    )

    llm = ChatMistralAI(model="mistral-small-2506")

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are a helpful AI assistant.

Use ONLY the provided context to answer the question.

If the answer is not present in the context,
say: "I could not find the answer in the document."
"""
            ),
            (
                "human",
                """Context:
{context}

Question:
{question}
"""
            )
        ]
    )

    st.markdown("### 💬 Ask Questions About Your Document")
    
    st.markdown("<div class='question-container'>", unsafe_allow_html=True)
    query = st.text_input(
        "Enter your question:", 
        placeholder="✨ What would you like to know about this document?", 
        label_visibility="collapsed"
    )
    st.markdown("</div>", unsafe_allow_html=True)

    if query:

        try:
            with st.spinner("🤔 Thinking..."):
                docs = retriever.invoke(query)

                context = "\n\n".join(
                    [doc.page_content for doc in docs]
                )

                final_prompt = prompt.invoke({
                    "context": context,
                    "question": query
                })

                response = llm.invoke(final_prompt)

            st.markdown("---")
            st.markdown("### 🤖 AI Response")
            st.markdown(f"<div class='answer-box'>{response.content}</div>", unsafe_allow_html=True)
            
            # Add a fun fact or tip
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""
                <div style='text-align: center; color: rgba(255,255,255,0.7); font-size: 0.9rem; margin-top: 1rem;'>
                    💡 Tip: Try asking follow-up questions for deeper insights!
                </div>
            """, unsafe_allow_html=True)
        
        except Exception as e:
            st.error(f"❌ Error generating response: {str(e)}")
            st.info("💡 Please check your API key and try again.")
else:
    st.markdown("<div class='upload-container'>", unsafe_allow_html=True)
    st.info("📌 Please upload a PDF and create the vector database first to start asking questions.")
    st.markdown("</div>", unsafe_allow_html=True)

# Add elegant footer
st.markdown("""
    <div style='text-align: center; margin-top: 4rem; padding: 2rem; color: rgba(255,255,255,0.8);'>
        <hr style='border: none; height: 1px; background: rgba(255,255,255,0.2); margin-bottom: 1rem;'>
        <p style='font-size: 0.95rem; font-weight: 300;'>
            Made with ❤️ by <strong>Somya</strong> | Powered by <strong>Mistral AI</strong> & <strong>LangChain</strong>
        </p>
        <p style='font-size: 0.85rem; opacity: 0.7; margin-top: 0.5rem;'>
            🚀 Transform your PDFs into interactive knowledge bases
        </p>
    </div>
""", unsafe_allow_html=True)