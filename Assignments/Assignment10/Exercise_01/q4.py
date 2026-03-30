from langchain_text_splitters import MarkdownHeaderTextSplitter

markdown_text = """
# LangChain

LangChain is a framework for building LLM-powered applications.

## Features
- Chains
- Agents
- Memory

## Use Cases
- Chatbots
- RAG systems

### RAG
Retrieval-Augmented Generation combines search with generation.
"""

headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
]

text_splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=headers_to_split_on
)

docs = text_splitter.split_text(markdown_text)

for i, doc in enumerate(docs):
    print(f"Chunk {i+1}")
    print("Metadata:", doc.metadata)
    print(doc.page_content)
    print("-" * 60)
