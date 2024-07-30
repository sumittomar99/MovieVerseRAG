from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.vector_stores import MetadataFilter, MetadataFilters, FilterOperator
import chromadb
from datetime import datetime
from scripts.generate_story import generate_mixed_story
import openai

# Initialize ChromaDB client and collection with persistent storage
chroma_client = chromadb.PersistentClient(path="chromadb_storage")
chroma_collection = chroma_client.get_collection("movies_collection")

# Initialize embedding model
embed_model = OpenAIEmbedding()

# Create vector store and storage context
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# Initialize the VectorStoreIndex with the documents in the vector store
index = VectorStoreIndex.from_vector_store(vector_store, storage_context=storage_context, embed_model=embed_model)

def format_date(timestamp, date_format):
    return datetime.fromtimestamp(timestamp).strftime(date_format)

def query_data(query, filters=[], similarity_top_k=5, user_story ="", openai_api_key=""):
    metadata_filters = MetadataFilters(filters=[
        MetadataFilter(key=filter["key"], operator=FilterOperator(filter["operator"]), value=filter["value"])
        for filter in filters
    ])
    query_engine = index.as_retriever(similarity_top_k=similarity_top_k, filters=metadata_filters)
    response = query_engine.retrieve(query)

    results = []
    movie_descriptions = []
    mixed_story = ""
    error_message = ""
    
    for res in response:
        metadata = res.node.metadata
        release_date = format_date(metadata["release_date"], metadata["release_date_format"])
        result = {
            "title": metadata.get("title", "Unknown Title"),
            "release_date": release_date,
            "genre": metadata.get("genre", "N/A"),
            "score": metadata.get("score", "N/A"),
            "crew": metadata.get("crew", "N/A"),
            "overview": metadata.get("overview", "N/A"),
            "country": metadata.get("country", "N/A"),
            "original_title": metadata.get("original_title", "N/A"),
            "status": metadata.get("status", "N/A"),
            "original_language": metadata.get("original_language", "N/A"),
            "budget": metadata.get("budget", "N/A"),
            "revenue": metadata.get("revenue", "N/A"),
            "score": res.score
        }
        results.append(result)
        movie_descriptions.append(metadata.get("overview", "N/A"))

    if user_story:
        mixed_story, error_message = generate_mixed_story(user_story, movie_descriptions, openai_api_key)
    
    return results, mixed_story, error_message