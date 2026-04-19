from langchain_community.vectorstores import FAISS
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from pypdf import PdfReader

def process_pdf(pdf):
    reader = PdfReader(pdf)
    text = ""

    for p in reader.pages:
        if p.extract_text():
            text += p.extract_text()

    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_text(text)

    emb = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    db = FAISS.from_texts(chunks, emb)

    return db