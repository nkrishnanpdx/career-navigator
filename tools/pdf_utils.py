import fitz # PyMuPDF
import io 
import os 

def extract_text_from_pdf(file_or_path: str | io.BytesIO) -> str:
    """
    Extract raw text from a PDF, which can be provided either as a file path (string)
    or a file-like object (io.BytesIO).
    """
    doc = None
    try:
        if isinstance(file_or_path, str):
            # If it's a string, assume it's a file path
            if not os.path.exists(file_or_path):
                print(f"Error: File not found at path: {file_or_path}")
                return ""
            doc = fitz.open(file_or_path)
        elif isinstance(file_or_path, io.BytesIO):
            # If it's a BytesIO object, read its content as a stream
            doc = fitz.open(stream=file_or_path.read(), filetype="pdf")
        else:
            print(f"Error: Unsupported input type for PDF extraction: {type(file_or_path)}")
            return ""

        if doc:
            text = "\n".join(page.get_text() for page in doc)
            doc.close()
            return text
        else:
            return "" 
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        if doc:
            doc.close() 
        return ""

