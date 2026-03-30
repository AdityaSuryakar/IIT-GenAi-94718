from langchain_text_splitters import TokenTextSplitter

raw_text = """
Large Language Models have strict token limits.
Token-based chunking ensures we do not exceed those limits.
This is especially useful for GPT-style models.
"""

text_splitter = TokenTextSplitter(
    chunk_size=300,
    chunk_overlap=50
)

docs = text_splitter.create_documents([raw_text])

for i, doc in enumerate(docs):
    print(f"Chunk {i+1}:")
    print(doc.page_content)
    print("-" * 60)
