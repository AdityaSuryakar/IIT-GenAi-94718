import streamlit as st
from config import RESUME_DIR, CHROMA_DIR
from vector_store import VectorStoreManager
from resume_service import ResumeService
from ui_components import ResumeUI

st.set_page_config(
    page_title="AI Resume Shortlisting",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI Resume Shortlisting System")

vector_manager = VectorStoreManager(CHROMA_DIR)
resume_service = ResumeService(RESUME_DIR, vector_manager)
ui = ResumeUI(resume_service)

with st.sidebar:
    st.header("⚙️ Menu")

    if st.button("🔄 Index All Resumes"):
        count = resume_service.index_resumes()
        st.success(f"Indexed {count} chunks")

    menu = st.radio(
        "Select Action",
        ["Upload Resume", "View Resumes", "Delete Resume", "Shortlist"]
    )

if menu == "Upload Resume":
    ui.upload_ui(RESUME_DIR)

elif menu == "View Resumes":
    ui.list_ui()

elif menu == "Delete Resume":
    ui.delete_ui()

elif menu == "Shortlist":
    ui.shortlist_ui()
