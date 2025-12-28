from langchain_text_splitters import RecursiveCharacterTextSplitter, Language

code_text = """
def add(a, b):
    return a + b

class Calculator:
    def multiply(self, x, y):
        return x * y

    def divide(self, x, y):
        if y == 0:
            return None
        return x / y
"""

code_splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.PYTHON,
    chunk_size=1000,
    chunk_overlap=100
)

docs = code_splitter.create_documents([code_text])

for i, doc in enumerate(docs):
    print(f"Chunk {i+1}:")
    print(doc.page_content)
    print("-" * 60)
