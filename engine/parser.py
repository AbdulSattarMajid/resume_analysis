from pdfminer.high_level import extract_text
import docx2txt

def extract_content(file_path):
    """Step 1: Universal Reader"""
    try:
        if file_path.endswith('.pdf'):
            return extract_text(file_path)
        elif file_path.endswith('.docx') or file_path.endswith('.temp_resume'):
            # Note: We add .temp_resume because Streamlit saves it as a temp file
            return docx2txt.process(file_path)
        else:
            # Default fallback: try reading as text
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
    except Exception as e:
        return f"Error reading file: {e}"