MAX_DOC_CHARS = 800     # per document
MAX_CONTEXT_CHARS = 2500  # total context

def retrieve_context(collection, embed_model, query, k=3):
    query_embedding = embed_model.embed_query(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )

    documents = results.get("documents", [[]])[0]

    cleaned_docs = []
    total_chars = 0

    for doc in documents:
        doc = doc.strip()

        # limit each document
        doc = doc[:MAX_DOC_CHARS]

        # stop if total context exceeds limit
        if total_chars + len(doc) > MAX_CONTEXT_CHARS:
            break

        cleaned_docs.append(doc)
        total_chars += len(doc)

    return "\n\n".join(cleaned_docs)
