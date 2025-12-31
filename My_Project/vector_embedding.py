from langchain.embeddings import init_embeddings
from config import EMBEDDING_MODEL, BASE_URL, DUMMY_API_KEY

def get_embedding_model():
    return init_embeddings(
        model=EMBEDDING_MODEL,
        provider="openai",
        base_url=BASE_URL,
        api_key=DUMMY_API_KEY,
        check_embedding_ctx_length=False
    )
