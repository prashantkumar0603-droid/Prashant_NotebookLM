
from pypdf import PdfReader
from docx import Document
from io import BytesIO

def parse_pdf(file):
    """
    Parse different document types (PDF, DOCX, DOC, TXT)
    """
    filename = getattr(file, 'filename', '').lower()
    
    try:
        if filename.endswith('.pdf'):
            return parse_pdf_file(file)
        elif filename.endswith(('.docx', '.doc')):
            return parse_docx_file(file)
        elif filename.endswith('.txt'):
            return parse_txt_file(file)
        else:
            # Try PDF first, then fallback to DOCX
            try:
                return parse_pdf_file(file)
            except:
                file.seek(0)  # Reset file pointer
                return parse_docx_file(file)
    except Exception as e:
        raise ValueError(f"Error parsing file: {str(e)}")

def parse_pdf_file(file):
    """Parse PDF files"""
    try:
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        raise ValueError(f"Error parsing PDF: {str(e)}")

def parse_docx_file(file):
    """Parse DOCX files"""
    try:
        doc = Document(file)
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text
    except Exception as e:
        raise ValueError(f"Error parsing DOCX: {str(e)}")

def parse_txt_file(file):
    """Parse TXT files"""
    try:
        content = file.read()
        if isinstance(content, bytes):
            return content.decode('utf-8')
        return content
    except Exception as e:
        raise ValueError(f"Error parsing TXT: {str(e)}")
