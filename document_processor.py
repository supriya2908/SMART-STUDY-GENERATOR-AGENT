
"""
Document processing utilities.
Handles PDF, TXT, and DOCX extraction, plus basic preprocessing.
"""

import io
import re


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract text from a PDF file using pdfplumber (preferred) with PyPDF2 fallback."""
    text = ""
    try:
        import pdfplumber
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        if text.strip():
            return clean_text(text)
    except Exception:
        pass

    # Fallback to PyPDF2
    try:
        import PyPDF2
        reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        for page in reader.pages:
            text += (page.extract_text() or "") + "\n"
    except Exception as e:
        return f"[PDF extraction failed: {e}]"

    return clean_text(text)


def extract_text_from_docx(file_bytes: bytes) -> str:
    """Extract text from a DOCX file."""
    try:
        from docx import Document
        doc = Document(io.BytesIO(file_bytes))
        paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]
        return clean_text("\n".join(paragraphs))
    except Exception as e:
        return f"[DOCX extraction failed: {e}]"


def extract_text_from_txt(file_bytes: bytes) -> str:
    """Decode a plain-text file."""
    for encoding in ("utf-8", "latin-1", "cp1252"):
        try:
            return clean_text(file_bytes.decode(encoding))
        except UnicodeDecodeError:
            continue
    return "[Text decoding failed]"


def clean_text(text: str) -> str:
    """Remove excessive whitespace and non-printable characters."""
    text = re.sub(r'\s+', ' ', text)          # collapse whitespace
    text = re.sub(r'[^\x20-\x7E\n]', '', text)  # strip non-ASCII control chars
    return text.strip()


def chunk_text(text: str, chunk_size: int = 3000, overlap: int = 200) -> list[str]:
    """Split long text into overlapping chunks for LLM processing."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks


def extract_topics_from_text(text: str) -> list[str]:
    """Heuristically extract candidate topic headings from raw text."""
    lines = text.split('\n')
    topics = []
    for line in lines:
        line = line.strip()
        # Short title-case lines are likely headings
        if 3 < len(line) < 80 and line[0].isupper() and not line.endswith('.'):
            topics.append(line)
    # Deduplicate while preserving order
    seen = set()
    unique = []
    for t in topics:
        if t.lower() not in seen:
            seen.add(t.lower())
            unique.append(t)
    return unique[:20]


def summarise_for_context(text: str, max_chars: int = 1500) -> str:
    """Return the first max_chars characters as a quick context preview."""
    return text[:max_chars] + ("…" if len(text) > max_chars else "")
