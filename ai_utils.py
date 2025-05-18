# ai_utils.py

import os
import pdfplumber
import docx
from keybert import KeyBERT

kw_model = KeyBERT()

# Read file content (basic text extraction)
def extract_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    try:
        if ext == '.txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        elif ext == '.pdf':
            with pdfplumber.open(file_path) as pdf:
                return '\n'.join([page.extract_text() or '' for page in pdf.pages])
        elif ext in ['.doc', '.docx']:
            doc = docx.Document(file_path)
            return '\n'.join([para.text for para in doc.paragraphs])
        else:
            return ""
    except:
        return ""

# Generate tags from text using KeyBERT
def generate_tags(text, num_tags=5):
    if not text.strip():
        return []
    keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), stop_words='english', top_n=num_tags)
    return [kw[0] for kw in keywords]

# Basic rule-based category detection
def generate_category(file_path, text):
    ext = os.path.splitext(file_path)[1].lower()
    if ext in ['.jpg', '.png', '.jpeg', '.gif']:
        return "Image"
    elif ext in ['.mp4', '.avi', '.mov']:
        return "Video"
    elif ext in ['.pdf', '.doc', '.docx', '.txt']:
        return "Document"
    elif ext in ['.py', '.js', '.html', '.css']:
        return "Code"
    elif 'resume' in file_path.lower():
        return "Resume"
    elif 'invoice' in file_path.lower():
        return "Finance"
    elif len(text.split()) > 1000:
        return "Large Document"
    else:
        return "Others"
