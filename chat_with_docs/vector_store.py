import os
import pickle
from typing import List, Dict, Any, Optional
import faiss
import numpy as np
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_core.vectorstores import VectorStore

from config import Config

class VectorStoreManager:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=Config.OPENAI_API_KEY,
            model=Config.EMBEDDING_MODEL
        )
        self.vector_store: Optional[FAISS] = None
        self.store_path = Config.VECTOR_DB_PATH
        
    def create_vector_store(self, documents: List[Document]) -> FAISS:
        """Create a new vector store from documents"""
        if not documents:
            raise ValueError("No documents provided to create vector store")
        
        self.vector_store = FAISS.from_documents(documents, self.embeddings)
        return self.vector_store
    
    def add_documents(self, documents: List[Document]) -> None:
        """Add documents to existing vector store"""
        if not documents:
            return
        
        if self.vector_store is None:
            self.vector_store = self.create_vector_store(documents)
        else:
            self.vector_store.add_documents(documents)
    
    def save_vector_store(self) -> None:
        """Save vector store to disk"""
        if self.vector_store is None:
            raise ValueError("No vector store to save")
        
        os.makedirs(self.store_path, exist_ok=True)
        self.vector_store.save_local(self.store_path)
        print(f"Vector store saved to {self.store_path}")
    
    def load_vector_store(self) -> bool:
        """Load vector store from disk"""
        try:
            if os.path.exists(self.store_path):
                self.vector_store = FAISS.load_local(
                    self.store_path, 
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
                print(f"Vector store loaded from {self.store_path}")
                return True
            return False
        except Exception as e:
            print(f"Error loading vector store: {e}")
            return False
    
    def similarity_search(self, query: str, k: int = None) -> List[Document]:
        """Search for similar documents"""
        if self.vector_store is None:
            raise ValueError("No vector store available for search")
        
        k = k or Config.TOP_K_RESULTS
        return self.vector_store.similarity_search(query, k=k)
    
    def similarity_search_with_score(self, query: str, k: int = None) -> List[tuple]:
        """Search for similar documents with similarity scores"""
        if self.vector_store is None:
            raise ValueError("No vector store available for search")
        
        k = k or Config.TOP_K_RESULTS
        return self.vector_store.similarity_search_with_score(query, k=k)
    
    def get_retriever(self, search_kwargs: Dict[str, Any] = None):
        """Get a retriever object for the vector store"""
        if self.vector_store is None:
            raise ValueError("No vector store available")
        
        search_kwargs = search_kwargs or {"k": Config.TOP_K_RESULTS}
        return self.vector_store.as_retriever(search_kwargs=search_kwargs)
    
    def delete_vector_store(self) -> None:
        """Delete the vector store from disk"""
        if os.path.exists(self.store_path):
            import shutil
            shutil.rmtree(self.store_path)
            print(f"Vector store deleted from {self.store_path}")
        self.vector_store = None
    
    def get_document_count(self) -> int:
        """Get the number of documents in the vector store"""
        if self.vector_store is None:
            return 0
        return self.vector_store.index.ntotal
    
    def get_all_documents(self) -> List[Document]:
        """Get all documents from the vector store"""
        if self.vector_store is None:
            return []
        
        # This is a simplified approach - in practice, you might want to store
        # document metadata separately for more efficient retrieval
        return list(self.vector_store.docstore._dict.values())
