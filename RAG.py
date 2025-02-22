from pdfminer.high_level import extract_text
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np


PDF_PATH = "documents/gfcc-part-2.pdf"


# Extract text from the PDF
def extract_text_from_pdf(pdf_path):
    return extract_text(pdf_path)


# Chunk the text into manageable pieces
def chunk_text(text, chunk_size=500):
    words = text.split()
    return [
        " ".join(words[i : i + chunk_size]) for i in range(0, len(words), chunk_size)
    ]


# Initialize embeddings and FAISS index (run once at startup)
text = extract_text_from_pdf(PDF_PATH)
chunks = chunk_text(text)
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(chunks)
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))


def retrieve_relevant_chunks(query, k=3):
    """
    Retrieve the top k most relevant chunks from the coaching course based on the query.
    """
    query_embedding = model.encode([query])
    distances, indices = index.search(np.array(query_embedding), k)
    relevant_chunks = [chunks[i] for i in indices[0]]
    return " ".join(relevant_chunks)


if __name__ == "__main__":
    test_query = "How to improve passing in grassroots football?"
    context = retrieve_relevant_chunks(test_query)
    print("Retrieved Context:", context[:500])  # Print first 500 chars for testing
