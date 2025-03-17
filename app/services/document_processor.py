import os
from typing import List, Any
from langchain.document_loaders import (
    DirectoryLoader, 
    PyMuPDFLoader,
    UnstructuredFileLoader,
    TextLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter

class DocumentProcessor:
    """Document processor, optimized for Chinese documents"""
    
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
    def load_documents(self, directory_path: str) -> List[Any]:
        """Load all documents from the specified directory"""
        loaders = {
            ".pdf": PyMuPDFLoader,
            ".txt": TextLoader,
            ".md": TextLoader,
            ".docx": UnstructuredFileLoader,
            ".doc": UnstructuredFileLoader,
            ".xlsx": UnstructuredFileLoader,
            ".xls": UnstructuredFileLoader,
        }
        
        documents = []
        
        # Iterate through all files in the directory
        for root, _, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_ext = os.path.splitext(file)[1].lower()
                
                if file_ext in loaders:
                    try:
                        loader_cls = loaders[file_ext]
                        loader = loader_cls(file_path)
                        documents.extend(loader.load())
                        print(f"Successfully loaded document: {file_path}")
                    except Exception as e:
                        print(f"Error loading document {file_path}: {e}")
        
        print(f"Loaded {len(documents)} documents")
        return documents
    
    def split_documents(self, documents: List[Any]) -> List[Any]:
        """Split documents into chunks suitable for vectorization, optimized for Chinese"""
        # Use splitter optimized for Chinese
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", "。", "！", "？", "；", "，", " ", ""]
        )
        
        splits = text_splitter.split_documents(documents)
        print(f"Documents split into {len(splits)} chunks")
        return splits
