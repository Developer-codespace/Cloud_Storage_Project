import os
os.environ["USE_TF"] = "0"  # Disable TensorFlow for KeyBERT backend

print("Starting script...")

from keybert import KeyBERT

print("Loading KeyBERT model...")
try:
    model = KeyBERT("all-MiniLM-L6-v2")
    print("Model loaded successfully.")
except Exception as e:
    print("Error while loading model:", e)
    exit()

# Sample text for keyword extraction
text = """
Invoice Number: INV-2025-001
Date: May 18, 2025
Due Date: June 1, 2025

**Bill To:**  
Niladri Tech Solutions  
123 AI Lane, Singur, WB, India  

**Description** | **Quantity** | **Unit Price** | **Total**
-----------------------------------------------------------
AI Model Training | 10 Hours | ₹1000 | ₹10,000  
Data Preprocessing | 5 Hours | ₹800 | ₹4,000  
Feature Engineering | 3 Hours | ₹1200 | ₹3,600  

**Subtotal:** ₹17,600  
**Tax (18% GST):** ₹3,168  
**Total Amount Due:** ₹20,768  

Payment Method: Bank Transfer  
Account No: 987654321  
SWIFT Code: ABCD12345  

Thank you for your business!
"""


print("Extracting keywords...")
try:
    keywords = model.extract_keywords(
        text,
        keyphrase_ngram_range=(1, 2),
        stop_words='english',
        top_n=5
    )
    tags = [kw[0] for kw in keywords]
    print("Tags extracted:", tags)
except Exception as e:
    print("Error during keyword extraction:", e)

