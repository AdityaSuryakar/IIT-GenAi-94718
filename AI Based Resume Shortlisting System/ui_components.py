#Minimal UI
import streamlit as st
import os


class ResumeUI:
    def __init__(self, resume_service):
        self.service = resume_service

    def upload_ui(self, resume_dir):
        st.subheader("📤 Upload Resume")
        file = st.file_uploader("Upload PDF", type=["pdf"])

        if file:
            path = os.path.join(resume_dir, file.name)
            with open(path, "wb") as f:
                f.write(file.read())

            count = self.service.index_resumes(path)
            st.success(f"{file.name} indexed ({count} chunks)")

    def list_ui(self):
        st.subheader("📋 Stored Resumes")
        resumes = self.service.list_resumes()

        if not resumes:
            st.info("No resumes found")
        for r in resumes:
            st.markdown(f"• **{r}**")

    def delete_ui(self):
        st.subheader("🗑 Delete Resume")
        resumes = self.service.list_resumes()

        if resumes:
            resume = st.selectbox("Select Resume", resumes)
            if st.button("Delete"):
                self.service.delete_resume(resume)
                st.success(f"{resume} deleted")

    def shortlist_ui(self):
        st.subheader("🎯 Shortlist Resumes")

        jd = st.text_area("Paste Job Description", height=200)
        k = st.slider("Top Results", 1, 10, 3)

        if st.button("Shortlist") and jd.strip():
            results = self.service.vector_manager.similarity_search(jd, k)

            scores = {}
            for doc in results:
                r = doc.metadata["resume"]
                scores[r] = scores.get(r, 0) + 1

            st.divider()
            for r, s in scores.items():
                st.success(f"{r} → matched chunks: {s}")
 