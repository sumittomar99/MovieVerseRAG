import csv
from llama_index.core import VectorStoreIndex, Document
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from llama_index.embeddings.openai import OpenAIEmbedding
import chromadb
import os
import openai
from datetime import datetime

# Ensure the OpenAI API key is set in the environment
if "OPENAI_API_KEY" not in os.environ:
    raise EnvironmentError("OPENAI_API_KEY environment variable not set")

openai.api_key = os.environ["OPENAI_API_KEY"]

# Initialize ChromaDB client with persistent storage
chroma_client = chromadb.PersistentClient(path="chromadb_storage")

# Check if collection exists and delete it
collection_name = "movies_collection"
all_collections = chroma_client.list_collections()
if collection_name in [col.name for col in all_collections]:
    chroma_client.delete_collection(collection_name)

# Create new collection
chroma_collection = chroma_client.create_collection(collection_name)

# Initialize embedding model
embed_model = OpenAIEmbedding()

# Function to parse date with multiple formats
def parse_date(date_str):
    formats = ["%m/%d/%Y", "%Y-%m-%d"]  # Add more formats if needed
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).timestamp(), fmt
        except ValueError:
            continue
    raise ValueError(f"Date {date_str} is not in recognized format")

# Custom function to read documents and add metadata
def load_documents_with_metadata(file_path):
    documents = []
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for idx, row in enumerate(reader):
            if len(row) >= 12:  # Ensure there are enough fields
                title = row[0].strip()
                release_date = row[1].strip()
                try:
                    # Convert release_date to a timestamp and get the format
                    release_date_timestamp, date_format = parse_date(release_date)
                except ValueError as e:
                    print(f"Skipping row {idx} due to invalid date: {e}")
                    continue
                score = float(row[2].strip())
                genre = row[3].strip()
                overview = row[4].strip()
                crew = row[5].strip()
                original_title = row[6].strip()
                status = row[7].strip()
                original_language = row[8].strip()
                budget = float(row[9].strip())
                revenue = float(row[10].strip())
                country = row[11].strip()
                
                text = f"Title: {title}\nRelease Date: {release_date}\nScore: {score}\nGenre: {genre}\nOverview: {overview}\nCrew: {crew}\nOriginal Title: {original_title}\nStatus: {status}\nOriginal Language: {original_language}\nBudget: {budget}\nRevenue: {revenue}\nCountry: {country}"
                
                metadata = {
                    "title": title,
                    "release_date": release_date_timestamp,  # Store as timestamp
                    "release_date_format": date_format,      # Store the format
                    "score": score,
                    "genre": genre,
                    "overview": overview,
                    "crew": crew,
                    "original_title": original_title,
                    "status": status,
                    "original_language": original_language,
                    "budget": budget,
                    "revenue": revenue,
                    "country": country
                }
                
                doc = Document(text=text, metadata=metadata)
                doc.id_ = f"doc_{idx}"
                documents.append(doc)
    return documents

# Load documents with metadata
documents = load_documents_with_metadata("./data/movies_dataset_full.csv")

# Create vector store and storage context
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# Build vector store index from filtered documents
index = VectorStoreIndex.from_documents(documents, storage_context=storage_context, embed_model=embed_model)

print("Data insertion completed.")