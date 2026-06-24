# 📚 ReadMeAI

I built this RAG (Retrieval-Augmented Generation) application to help you interact with PDF documents using AI. Upload any PDF and ask questions to get instant, intelligent answers!

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red.svg)
![LangChain](https://img.shields.io/badge/LangChain-Latest-green.svg)





### Prerequisites

- Python 3.10 or higher
- Mistral API key (get it from [Mistral AI](https://mistral.ai/))

### Installation

1. **Clone this repository:**
```bash
git clone https://github.com/markensomya/ReadMeAI.git
cd ReadMeAI
```

2. **Create virtual environment (recommended):**
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**
Create a `.env` file in the root directory:
```env
MISTRAL_API_KEY=your_mistral_api_key_here
```

### Running the Application

#### Web Interface (Recommended)
```bash
streamlit run app.py
```
Then open http://localhost:8501 in your browser.

#### Command Line Interface
```bash
python main.py
```

## Project Structure

```
ReadMeAI/
├── app.py                  # Streamlit web application with beautiful UI
├── main.py                 # Command-line interface version
├── create_database.py      # Standalone database creation script
├── requirements.txt        # All Python dependencies
├── .env                    # Your API keys (not tracked in git)
├── .gitignore             # Files to ignore in git
├── document_loaders/      # Folder for your PDF documents
│   └── GRU.pdf           # Sample document included
└── chroma_db/            # Vector database (auto-generated)
```

##  How It Works

I implemented a complete RAG pipeline:

1. **Document Loading**: PyPDFLoader extracts text from PDF files
2. **Text Splitting**: Documents are chunked into 1000-character segments with 200-character overlap
3. **Embeddings**: Mistral's embedding model converts text chunks into vectors
4. **Vector Storage**: ChromaDB stores and indexes embeddings for fast retrieval
5. **Smart Retrieval**: MMR algorithm retrieves relevant and diverse context
6. **Answer Generation**: Mistral-small generates accurate answers based on retrieved context

## Technologies I Used

- **LangChain** - Framework for building LLM applications
- **ChromaDB** - Vector database for semantic search
- **Mistral AI** - Advanced language and embedding models
- **Streamlit** - Beautiful, interactive web interface
- **PyPDF** - PDF document processing

## How to Use

### Web Interface (app.py)
1. Launch the app with `streamlit run app.py`
2. Upload your PDF document using the file uploader
3. Click "Create Vector Database" to process the document
4. Type your question in the input field
5. Get instant AI-generated answers!

### CLI Version (main.py)
1. Place your PDF in the `document_loaders/` folder
2. Run `python create_database.py` to build the vector database
3. Run `python main.py` to start the interactive CLI
4. Type your questions and press Enter
5. Type `0` to exit

## UI Highlights

I designed the interface with:
- Beautiful purple gradient background
- Clean, modern layout
- Smooth animations and transitions
- Responsive design
- Semi-transparent glass-effect answer boxes

## Contributing

I welcome contributions! Feel free to:
- Open issues for bugs or feature requests
- Submit pull requests
- Suggest improvements

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Mistral AI for their powerful language models
- LangChain community for the excellent framework
- Streamlit team for making web apps so easy to build

---

**Made with ❤️ by Somya**

If you find this project useful, please give it a ⭐ on GitHub!
