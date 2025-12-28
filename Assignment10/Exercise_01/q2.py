from langchain_text_splitters import RecursiveCharacterTextSplitter

raw_text = """
LangChain is a framework for developing applications powered by large language models.

It supports prompt templates, chains, agents, memory, and retrieval systems.

• Easy to integrate
• Modular design
• Production ready
"""

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=100,
    separators=["\n\n", "\n", " ", ""]
)

docs = text_splitter.create_documents([raw_text])

for i, doc in enumerate(docs):
    print(f"Chunk {i+1}:")
    print(doc.page_content)
    print("-" * 60)
