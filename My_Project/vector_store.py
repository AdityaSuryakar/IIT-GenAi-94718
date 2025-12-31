import chromadb
import os
from config import VECTOR_DB_PATH

def get_collection(name="embeddings"):
    client = chromadb.PersistentClient(path=VECTOR_DB_PATH)
    return client.get_or_create_collection(name)

def store_documents(collection, docs, embed_model):
    ids, texts, metadatas = [], [], []

    for doc in docs:
        file_name = os.path.splitext(
            os.path.basename(doc.metadata["source"])
        )[0]

        ids.append(file_name)
        texts.append(doc.page_content)
        metadatas.append({"doc_id": file_name})

    if collection.count() == 0:
        embeddings = embed_model.embed_documents(texts)
        collection.add(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas
        )
