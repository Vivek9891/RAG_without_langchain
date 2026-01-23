from docs_reader import DocumentReader
from text_chunk import TextSplitter
import os



#--------------------- Inserting Data into ChromaDB ---------------

def process_document(file_path: str):
    """Process a single document and prepare it for ChromaDB"""
    try:
        # Read the document 
        reader = DocumentReader()
        content = reader.read_document(file_path)

        #Split into chunks 
        splitter = TextSplitter()
        chunks = splitter.sentence_aware_text_splitter(content)

        #prepare metadata
        file_name = os.path.basename(file_path)
        metadatas = [{"source": file_name, "chunk":i} for i in range(len(chunks))]
        ids = [f"{file_name}_chunks_{i}" for i in range(len(chunks))]

        return ids,chunks,metadatas

    except Exception as e:
        print(f"Error processing {file_path} : {str(e)}")
        return [],[],[]

def add_to_collection(collection,ids,chunks,metadatas):
    """Add documents to collection in batches"""
    if not chunks:
        return 
    
    batch_size = 100     # suppose we have 10000 chunks so, we want to add chunks batches of 100
    for i in range(0,len(chunks),batch_size):
        end_idx = min(i + batch_size, len(chunks))
        collection.add(
            documents= chunks[i:end_idx],
            metadatas=metadatas[i:end_idx],
            ids=ids[i:end_idx]   
        )

def process_and_add_documents(collection, file_paths: list[str]):
    """
    file_paths: List[str] → paths of newly uploaded files
    """
    # files = [os.path.join(folder_path,file) 
    #         for file in os.listdir(folder_path) 
    #         if os.path.isfile(os.path.join(folder_path,file))
    # ]

    for file_path in file_paths:
        print(f"Processing {os.path.basename(file_path)}...")
        ids,chunks,metadatas = process_document(file_path)
        add_to_collection(collection,ids,chunks,metadatas)
        print(f"Added {len(chunks)} chunks to collections")

