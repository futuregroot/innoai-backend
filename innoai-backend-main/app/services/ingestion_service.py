import logging
import os
import fitz  # PyMuPDF for PDF handling
from datetime import datetime
from sentence_transformers import SentenceTransformer
from app.repositories.chroma_repository import ChromaRepository
import re
import nltk  # Ensure nltk is installed beforehand
from nltk.tokenize import word_tokenize

nltk.download('punkt')

class IngestionService:
    def __init__(self):
        self.logger = logging.getLogger("IngestionService")
        self.embed_model = SentenceTransformer('all-mpnet-base-v2')
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.chroma_storage_base = os.path.join(self.base_dir, '..', 'chroma_storage')
        self.tensorboard_logs = os.path.join(self.base_dir, '..', 'tensorboard_logs')

    def get_chroma_repo(self, collection_name):
        return ChromaRepository(collection_name=collection_name, embedding_dim=768)

    def delete_collection(self, collection_name):
        chroma_repo = self.get_chroma_repo(collection_name)
        self.logger.info(f"Deleting collection: {collection_name}")
        chroma_repo.delete_collection(collection_name)
        return {"message": f"Collection '{collection_name}' deleted successfully"}

    def delete_all_collections(self):
        self.logger.info("Deleting all collections")
        chroma_repo = ChromaRepository()
        chroma_repo.delete_all_collections()
        return {"message": "All collections deleted successfully"}

    def process_text(self, text, collection_name):
        chroma_repo = self.get_chroma_repo(collection_name)
        self.logger.info("Processing text input")
        try:
            text = self.clean_text(text)
            docs = [text]
            embeddings = self.create_embeddings(docs)
            now = datetime.now().isoformat()
            self.logger.debug(f"Documents: {docs}")
            self.logger.debug(f"Embeddings: {embeddings}")
            metadata = [{"update_time": now} for _ in docs]
            ids = [f"text_input_vec0"]
            chroma_repo.upsert_data(docs, embeddings, ids, metadata)
            self.logger.info("Ingestion complete")
            items = [{"id": ids[0], "content": docs[0], "metadata": metadata[0]}]
            return {"message": "Ingestion complete", "items": items}
        except Exception as e:
            self.logger.error(f"Error processing text: {str(e)}")
            raise ValueError("Failed to process text input")

    def process_pdf(self, file_path, collection_name):
        chroma_repo = self.get_chroma_repo(collection_name)
        self.logger.info(f"Processing file: {file_path}")
        try:
            raw_docs = self.load_pdf(file_path)
            docs = self.split_text(raw_docs)
            cleaned_docs = [self.clean_text(doc) for doc in docs]
            meaningful_docs = [doc for doc in cleaned_docs if len(doc.split()) > 5]
            embeddings = self.create_embeddings(meaningful_docs)
            base_filename = os.path.splitext(os.path.basename(file_path))[0]
            now = datetime.now().isoformat()
            self.logger.debug(f"Documents: {meaningful_docs}")
            self.logger.debug(f"Embeddings: {embeddings}")
            metadata = [{"update_time": now} for _ in meaningful_docs]
            ids = [f"{base_filename}_vec{idx}" for idx, _ in enumerate(meaningful_docs)]
            chroma_repo.upsert_data(meaningful_docs, embeddings, ids, metadata)
            self.logger.info("Ingestion complete")
            items = [{"id": id_, "content": doc, "metadata": meta} for id_, doc, meta in zip(ids, meaningful_docs, metadata)]
            return {"message": "Ingestion complete", "items": items}
        except Exception as e:
            self.logger.error(f"Error processing PDF: {str(e)}")
            raise ValueError("Failed to process PDF")

    def process_semantic_chunks(self, text, collection_name):
        chroma_repo = self.get_chroma_repo(collection_name)
        self.logger.info("Processing text using Semantic Chunker")
        try:
            # Assuming nlp() is a pre-configured NLP pipeline e.g., from SpaCy
            doc = nlp(text)
            docs = [self.clean_text(sent.text) for sent in doc.sents]
            meaningful_docs = [doc for doc in docs if len(doc.split()) > 5]
            embeddings = self.create_embeddings(meaningful_docs)
            now = datetime.now().isoformat()
            self.logger.debug(f"Documents: {meaningful_docs}")
            self.logger.debug(f"Embeddings: {embeddings}")
            metadata = [{"update_time": now} for _ in meaningful_docs]
            ids = [f"semantic_chunk_vec{idx}" for idx, _ in enumerate(meaningful_docs)]
            chroma_repo.upsert_data(meaningful_docs, embeddings, ids, metadata)
            self.logger.info("Ingestion complete")
            items = [{"id": id_, "content": doc, "metadata": meta} for id_, doc, meta in zip(ids, meaningful_docs, metadata)]
            return {"message": "Ingestion complete", "items": items}
        except Exception as e:
            self.logger.error(f"Error processing text: {str(e)}")
            raise ValueError("Failed to process text input")

    def process_token_text_splitter(self, text, collection_name):
        chroma_repo = self.get_chroma_repo(collection_name)
        self.logger.info("Processing text using Token Text Splitter")
        try:
            words = word_tokenize(self.clean_text(text))
            chunk_size = 50
            docs = [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
            meaningful_docs = [doc for doc in docs if len(doc.split()) > 5]
            embeddings = self.create_embeddings(meaningful_docs)
            now = datetime.now().isoformat()
            self.logger.debug(f"Documents: {meaningful_docs}")
            self.logger.debug(f"Embeddings: {embeddings}")
            metadata = [{"update_time": now} for _ in meaningful_docs]
            ids = [f"token_text_split_vec{idx}" for idx, _ in enumerate(meaningful_docs)]
            chroma_repo.upsert_data(meaningful_docs, embeddings, ids, metadata)
            self.logger.info("Ingestion complete")
            items = [{"id": id_, "content": doc, "metadata": meta} for id_, doc, meta in zip(ids, meaningful_docs, metadata)]
            return {"message": "Ingestion complete", "items": items}
        except Exception as e:
            self.logger.error(f"Error processing text: {str(e)}")
            raise ValueError("Failed to process text input")

    def process_all_pdfs_in_directory(self, directory_path, collection_name):
        chroma_repo = self.get_chroma_repo(collection_name)
        self.logger.info(f"Processing all PDFs in directory: {directory_path}")
        results = []
        for filename in os.listdir(directory_path):
            if filename.endswith('.pdf'):
                file_path = os.path.join(directory_path, filename)
                try:
                    result = self.process_pdf(file_path, collection_name)
                    results.append(result)
                except Exception as e:
                    self.logger.error(f"Failed to process file {file_path}: {str(e)}")
        self.logger.info("All PDFs processed")
        return {"message": "All PDFs processed", "results": results}

    def load_pdf(self, file_path):
        self.logger.info(f"Loading PDF file: {file_path}")
        doc = fitz.open(file_path)
        texts = [page.get_text() for page in doc]
        return texts

    def split_text(self, texts):
        self.logger.info(f"Splitting texts into chunks")
        CHUNK_SIZE = 1000
        chunks = []
        for text in texts:
            for i in range(0, len(text), CHUNK_SIZE):
                chunk = text[i:i + CHUNK_SIZE]
                chunks.append(chunk)
        self.logger.debug(f"Text split into {len(chunks)} chunks")
        return chunks

    def clean_text(self, text):
        # Remove 특수기호, 심볼, whitespace 삭제
        clean_text = re.sub(r'[\W_]+', ' ', text)  # text만 추출
        # page number, footer 삭제
        clean_text = re.sub(r'(\b\d{1,2}\b)(?:\s[.\W_]+)*', '', clean_text)
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()
        return clean_text

    def create_embeddings(self, texts):
        self.logger.info(f"Creating embeddings")
        embeddings = self.embed_model.encode(texts)
        self.logger.debug(f"Created embeddings: {embeddings[:5]}")
        return embeddings

    def search(self, query, collection_name):
        chroma_repo = self.get_chroma_repo(collection_name)
        try:
            self.logger.info(f"Searching for query: {query}")

            # Create query embedding
            query_embedding = self.embed_model.encode([query])[0].tolist()
            self.logger.debug(f"Query embedding created: {query_embedding}")

            search_results = chroma_repo.query_data(query_embedding, n_results=10)
            self.logger.debug(f"Search results from Chroma DB: {search_results}")

            if not search_results or not search_results.get("ids"):
                raise ValueError("Search results are empty")

            # Extract results
            ids = search_results["ids"][0]
            distances = search_results["distances"][0]
            documents = search_results["documents"][0]
            metadatas = search_results["metadatas"][0]

            # Find the result with the closest distance
            closest_distance = float('inf')
            closest_result = None
            for result_id, distance, document, metadata in zip(ids, distances, documents, metadatas):
                self.logger.debug(f"Result - ID: {result_id}, Distance: {distance}, Document: {document}, Metadata: {metadata}")
                if distance < closest_distance:
                    closest_distance = distance
                    closest_result = {
                        "id": result_id,
                        "distance": distance,
                        "document": document,
                        "metadata": metadata
                    }

            if closest_result is None:
                raise ValueError("No suitable result found")

            self.logger.info(f"Search complete, closest result: {closest_result}")
            return {"message": "Search complete", "results": closest_result}

        except Exception as e:
            self.logger.error(f"Error searching Chroma DB: {str(e)}")
            return {"error": str(e)}

    def get_all_data(self, collection_name):
        chroma_repo = self.get_chroma_repo(collection_name)
        try:
            all_data = chroma_repo.get_all_data()
            self.logger.debug(f"All data in the collection: {all_data}")
            return all_data
        except Exception as e:
            self.logger.error(f"An error occurred while retrieving all data: {e}")
            return {"results": []}

    def visualize_embeddings_with_tensorboard(self, collection_name, log_dir=None):
        chroma_repo = self.get_chroma_repo(collection_name)
        self.logger.info("Visualizing embeddings with TensorBoard")
        data = chroma_repo.get_all_data()
        if data is None or "results" not in data or not data["results"]:
            self.logger.warning("No data found or data format is incorrect in Chroma repository.")
            return
        if log_dir is None:
            log_dir = self.tensorboard_logs
        self.logger.debug(f"Data retrieved: {data['results']}")
        embeddings = []
        metadata = []
        for record in data["results"]:
            self.logger.debug(f"Processing record: {record}")
            if isinstance(record, dict) and "embedding" in record and "document" in record:
                embedding = record["embedding"]
                document = record["document"]
                if embedding and document:
                    embeddings.append(embedding)
                    metadata.append(document)
                else:
                    self.logger.error(f"Record missing 'embedding' or 'document': {record}")
            else:
                self.logger.error(f"Record is not in expected dictionary format: {record}")
        if embeddings and metadata:
            self.logger.info(f"Saving embeddings and metadata to {log_dir}")
            save_embeddings(embeddings, metadata, log_dir)
            setup_tensorboard(log_dir)
        else:
            self.logger.error("No valid embeddings or metadata to save.")