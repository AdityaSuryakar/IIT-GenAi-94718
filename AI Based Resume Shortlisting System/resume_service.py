import os
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


class ResumeService:
    def __init__(self, resume_dir, vector_manager):
        self.resume_dir = resume_dir
        self.vector_manager = vector_manager

    def list_resumes(self):
        return os.listdir(self.resume_dir)

    def delete_resume(self, resume_name):
        path = os.path.join(self.resume_dir, resume_name)
        if os.path.exists(path):
            os.remove(path)
        self.vector_manager.delete_resume_embeddings(resume_name)

    def index_resumes(self, pdf_path=None):
        loader = (
            PyPDFLoader(pdf_path)
            if pdf_path
            else DirectoryLoader(self.resume_dir, glob="*.pdf", loader_cls=PyPDFLoader)
        )

        documents = loader.load()
        if not documents:
            return 0

        splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)

        chunks, metadatas = [], []
        resume_names = set()

        for doc in documents:
            resume_names.add(os.path.basename(doc.metadata["source"]))

        for resume in resume_names:
            self.vector_manager.delete_resume_embeddings(resume)

        for doc in documents:
            resume_name = os.path.basename(doc.metadata["source"])
            texts = splitter.split_text(doc.page_content)

            for text in texts:
                chunks.append(text)
                metadatas.append({
                    "resume": resume_name,
                    "page": doc.metadata.get("page", -1)
                })

        ids = [f"{m['resume']}_{i}" for i, m in enumerate(metadatas)]
        self.vector_manager.add_embeddings(chunks, metadatas, ids)

        return len(chunks)
