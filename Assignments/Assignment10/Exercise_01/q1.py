from langchain_text_splitters import CharacterTextSplitter

raw_text = """
LangChain is a framework for developing applications powered by large language models.
It helps with prompt management, chains, agents, memory, and retrieval.
"""

text_splitter = CharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

docs = text_splitter.create_documents([raw_text])

for i, doc in enumerate(docs):
    print(f"Chunk {i+1}:")
    print(doc.page_content)
    print("-" * 50)
