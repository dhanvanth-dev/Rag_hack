# loader.py

import os
import requests
from unstructured.partition.pdf import partition_pdf
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_and_chunk_document(url: str, chunk_size=750, chunk_overlap=50, cleanup=True):
    """
    Downloads a PDF from a URL, extracts structured content using `unstructured`,
    and returns split chunks using LangChain's RecursiveCharacterTextSplitter.
    """
    file_path = "temp.pdf"
    
    try:
        # Download PDF
        response = requests.get(url)
        response.raise_for_status()
        
        with open(file_path, "wb") as f:
            f.write(response.content)
        
        # Extract content
        elements = partition_pdf(filename=file_path,
                                 extract_images_in_pdf=False,
                                    infer_table_structure=False,
                                    ocr_strategy="no_ocr",)
        raw_text = "\n".join([el.text for el in elements if el.text])
        
        # Chunk text
        splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        chunks = splitter.split_text(raw_text)
        return chunks
    
    except Exception as e:
        raise RuntimeError(f"Error in loading/chunking document: {e}")
    
    finally:
        if cleanup and os.path.exists(file_path):
            os.remove(file_path)
