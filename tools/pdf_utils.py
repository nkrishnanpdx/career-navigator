import fitz  # PyMuPDF

def extract_text_from_pdf(path: str) -> str:
    """Extract raw text from a PDF file"""
    doc = fitz.open(path)
    text = "\n".join(page.get_text() for page in doc)
    doc.close()
    return text



