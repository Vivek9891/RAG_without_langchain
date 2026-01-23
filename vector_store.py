import chromadb
from chromadb.utils import embedding_functions


# --------------- Setting Up ChromaDB ---------------------
# Initialize ChromaDB clien 
client = chromadb.PersistentClient(path = "../AI/RAG_OpenAI")

# use sentence-transformer embeddings for embedding out data
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name= "all-MiniLM-L6-v2"
)

collection = client.get_or_create_collection(
    name="documents_collection",
    embedding_function=sentence_transformer_ef
)