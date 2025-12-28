# 6. Sentence-Based Chunking (NLP-Style)
from langchain_text_splitters import SentenceTransformersTokenTextSplitter
raw_text = """
Large Language Models have strict token limits.
Token-based chunking ensures we do not exceed those limits.
This is especially useful for GPT-style models.
"""
text_splitter= SentenceTransformersTokenTextSplitter(chunk_size=256, chunk_overlap=20)
docs = text_splitter.create_documents([raw_text])
# Best for: Q&A datasets, Short factual text, High precision retrieval