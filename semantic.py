def semantic_search(collection,query:str, n_results: int = 2):
    """Perfrom sementic search on the collection"""
    return collection.query(
        query_texts = [query],
        n_results = n_results
    )

def print_search_result(results):
    """print formatted search results"""
    print("\nSearch Results:\n"+ "-" * 20)

    for i in range(len(results["documents"][0])):
        doc = results['documents'][0][i]
        meta = results['metadatas'][0][i]
        print(f"\nResult {i+1}: Source: {meta['source']}, Chunk {meta['chunk']}")
        print(f"content: {doc}\n")

def get_context_with_sources(results):
    """Extract context and source information from search results"""
    # Combine document chunks into a single context
    context = "\n\n".join(results['documents'][0])

    # Format sources with metadata
    sources = [
        f"{meta['source']} (chunk {meta['chunk']})" 
        for meta in results['metadatas'][0]
    ]

    return context, sources