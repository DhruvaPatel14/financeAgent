from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
import chromadb
import pandas as pd
import os

# Supported file types
SUPPORTED_EXTENSIONS = (".pdf", ".xls", ".xlsx")

# Create embeddings model (explicitly set model name to avoid deprecation warning)
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

# Initialize ChromaDB client and collection
client = chromadb.Client()
collection = client.create_collection("financial_docs")

# Track whether documents have been loaded
docs_loaded = False


def _load_pdf(path: str) -> list[Document]:
    """Load and return pages from a PDF file."""
    loader = PyPDFLoader(path)
    return loader.load()


def _load_excel(path: str) -> list[Document]:
    """
    Load an XLS or XLSX file and convert each sheet into a Document.
    Each sheet becomes one document whose content is a readable text table.
    """
    docs = []
    engine = "xlrd" if path.lower().endswith(".xls") else "openpyxl"
    xl = pd.ExcelFile(path, engine=engine)

    for sheet_name in xl.sheet_names:
        df = xl.parse(sheet_name)
        # Drop completely empty rows/columns to keep content clean
        df.dropna(how="all", inplace=True)
        df.dropna(axis=1, how="all", inplace=True)

        if df.empty:
            print(f"  Skipping empty sheet: '{sheet_name}'")
            continue

        # Convert the sheet to a plain-text table for embedding
        content = f"Sheet: {sheet_name}\n\n{df.to_string(index=False)}"
        docs.append(Document(
            page_content=content,
            metadata={"source": path, "sheet": sheet_name}
        ))

    return docs


def load_documents(path: str) -> list[Document]:
    """Load documents from a PDF, XLS, or XLSX file."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"No file found at path: {path}")

    ext = os.path.splitext(path)[1].lower()
    if ext not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file type '{ext}'. Supported types: {', '.join(SUPPORTED_EXTENSIONS)}"
        )

    if ext == ".pdf":
        return _load_pdf(path)
    else:
        return _load_excel(path)


def store_docs(docs: list[Document]):
    """Embed and store documents in ChromaDB."""
    global docs_loaded
    for i, doc in enumerate(docs):
        collection.add(
            documents=[doc.page_content],
            ids=[str(i)]
        )
    docs_loaded = True
    print(f"Successfully stored {len(docs)} chunk(s) in the knowledge base.")


def load_and_store(path: str) -> int:
    """
    Convenience function: load a PDF/XLS/XLSX from path and store in ChromaDB.
    Returns the number of chunks stored.
    """
    ext = os.path.splitext(path)[1].lower()
    print(f"Loading {'PDF' if ext == '.pdf' else 'Excel'} file: {path}")
    docs = load_documents(path)
    store_docs(docs)
    return len(docs)


def retrieve_docs(query: str, n_results: int = 3) -> list:
    """Retrieve the most relevant document chunks for a given query."""
    if not docs_loaded:
        return []
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    return results["documents"]


def is_docs_loaded() -> bool:
    """Check whether documents have been loaded into the collection."""
    return docs_loaded