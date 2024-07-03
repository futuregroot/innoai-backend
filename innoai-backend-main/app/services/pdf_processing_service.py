import fitz  # PyMuPDF
from transformers import AutoTokenizer, AutoModel
import chromadb
from chromadb.config import Settings

def extract_text_from_pdf(pdf_path):
    document = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text += page.get_text()
    return text

def get_embedding(text):
    tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
    model = AutoModel.from_pretrained("bert-base-uncased")
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).squeeze()

def save_to_chroma_db(text, pdf_path):
    client = chromadb.Client(Settings())
    collection = client.create_collection("pdf_embeddings")
    embedding = get_embedding(text)
    collection.add(
        documents=[text],
        metadatas=[{"source": pdf_path}],
        embeddings=[embedding.tolist()]
    )
    print("Data added to Chroma DB")

def process_pdf(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    save_to_chroma_db(text, pdf_path)

# Example usage
if __name__ == "__main__":
    pdf_path = "C:/Users/heung/Downloads/Chabot_innocean data ex - news.pdf"
    process_pdf(pdf_path)
