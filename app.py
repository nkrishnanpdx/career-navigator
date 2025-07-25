import streamlit as st
import fitz  # PyMuPDF
import io
from agents.job_planner import JobPlannerAgent
from agents.tailor import TailorAgent
from agents.email_agent import EmailAgent
from agents.tracker import TrackerAgent
from tools.pdf_utils import extract_text_from_pdf
from tools.db import initialize_db, insert_application

st.set_page_config(page_title="Intelligent Career Navigator", layout="centered")
st.title("🧭 Intelligent Career Navigator")

initialize_db()

st.sidebar.header("Upload Resume")
resume_file = st.sidebar.file_uploader("Choose a PDF resume", type=["pdf"])

if resume_file:
    pdf_bytes = resume_file.read()
    resume_text = extract_text_from_pdf(io.BytesIO(pdf_bytes))

    st.subheader("Extracted Resume Text")
    with st.expander("View text"):
        st.write(resume_text)

    if st.button("🔍 Run Career Navigator"):
        with st.spinner("Analyzing profile and generating applications..."):
            planner = JobPlannerAgent()
            queries = planner.run(resume_text)

            tailor = TailorAgent()
            tailored = tailor.run({"resume_text": resume_text, "job_description": queries[0]})

            st.subheader("🎯 Search Query")
            st.code(queries[0])

            st.subheader("📄 Tailored Resume")
            st.code(tailored.get("tailored_resume"))

            st.subheader("✉️ Cover Letter")
            st.code(tailored.get("cover_letter"))

            tracker = TrackerAgent()
            tracker.run({"job": queries[0], "status": "Applied"})

            st.success("Application processed and tracked.")

else:
    st.info("Please upload your resume to begin.")
