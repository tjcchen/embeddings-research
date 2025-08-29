import os
import requests
from typing import List, Dict, Any
from pathlib import Path

import PyPDF2
from docx import Document
from bs4 import BeautifulSoup
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document as LangChainDocument

from config import Config

class DocumentProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=Config.CHUNK_SIZE,
            chunk_overlap=Config.CHUNK_OVERLAP,
            length_function=len,
        )
        
    def process_file(self, file_path: str) -> List[LangChainDocument]:
        """Process a file and return chunked documents"""
        file_extension = Path(file_path).suffix.lower()
        
        if file_extension == '.pdf':
            text = self._extract_pdf_text(file_path)
        elif file_extension == '.docx':
            text = self._extract_docx_text(file_path)
        elif file_extension in ['.txt', '.md']:
            text = self._extract_text_file(file_path)
        elif file_extension == '.html':
            text = self._extract_html_text(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")
        
        # Create metadata
        metadata = {
            "source": file_path,
            "file_type": file_extension,
            "file_name": Path(file_path).name
        }
        
        # Split text into chunks
        chunks = self.text_splitter.split_text(text)
        
        # Create LangChain documents
        documents = []
        for i, chunk in enumerate(chunks):
            doc_metadata = metadata.copy()
            doc_metadata["chunk_id"] = i
            documents.append(LangChainDocument(page_content=chunk, metadata=doc_metadata))
        
        return documents
    
    def process_url(self, url: str) -> List[LangChainDocument]:
        """Process a web page URL and return chunked documents"""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Extract text
            text = soup.get_text()
            
            # Clean up text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            # Create metadata
            metadata = {
                "source": url,
                "file_type": "web_page",
                "title": soup.title.string if soup.title else "Unknown"
            }
            
            # Split text into chunks
            text_chunks = self.text_splitter.split_text(text)
            
            # Create LangChain documents
            documents = []
            for i, chunk in enumerate(text_chunks):
                doc_metadata = metadata.copy()
                doc_metadata["chunk_id"] = i
                documents.append(LangChainDocument(page_content=chunk, metadata=doc_metadata))
            
            return documents
            
        except Exception as e:
            raise Exception(f"Error processing URL {url}: {str(e)}")
    
    def _extract_pdf_text(self, file_path: str) -> str:
        """Extract text from PDF file"""
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text
    
    def _extract_docx_text(self, file_path: str) -> str:
        """Extract text from DOCX file"""
        doc = Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    
    def _extract_text_file(self, file_path: str) -> str:
        """Extract text from plain text file"""
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    
    def _extract_html_text(self, file_path: str) -> str:
        """Extract text from HTML file"""
        with open(file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file.read(), 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            return soup.get_text()
    
    def get_supported_extensions(self) -> List[str]:
        """Return list of supported file extensions"""
        return Config.SUPPORTED_EXTENSIONS
