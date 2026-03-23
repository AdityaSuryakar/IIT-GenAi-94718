from langchain.embeddings import init_embeddings
from langchain_community.vectorstores import Chroma


class VectorStoreManager:
    def __init__(self, chroma_dir):
        self.embed_model = init_embeddings(
            model="nomic-embed-text-v1.5",
            provider="openai",
            base_url="http://127.0.0.1:1234/v1",
            api_key="not-needed",
            check_embedding_ctx_length=False
        )

        self.vectorstore = Chroma(
            persist_directory=chroma_dir,
            embedding_function=self.embed_model
        )

    def add_embeddings(self, chunks, metadatas, ids):
        self.vectorstore._collection.add(
            documents=chunks,
            metadatas=metadatas,
            ids=ids,
            embeddings=self.embed_model.embed_documents(chunks)
        )
        self.vectorstore.persist()

    def delete_resume_embeddings(self, resume_name):
        self.vectorstore._collection.delete(where={"resume": resume_name})
        self.vectorstore.persist()

    def similarity_search(self, query, k):
        return self.vectorstore.similarity_search(query, k=k)
