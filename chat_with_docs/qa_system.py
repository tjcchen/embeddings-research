from typing import List, Dict, Any, Optional
from langchain_openai import OpenAI, ChatOpenAI
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document

from config import Config
from vector_store import VectorStoreManager

class QASystem:
    def __init__(self, vector_store_manager: VectorStoreManager):
        self.vector_store_manager = vector_store_manager
        self.llm = ChatOpenAI(
            openai_api_key=Config.OPENAI_API_KEY,
            model_name=Config.CHAT_MODEL,
            temperature=0.1
        )
        
        # Custom prompt template for better responses
        self.prompt_template = PromptTemplate(
            template="""使用以下上下文信息来回答问题。如果你不知道答案，就说你不知道，不要试图编造答案。

上下文信息:
{context}

问题: {question}

请提供详细且准确的答案，并在可能的情况下引用相关的文档来源：""",
            input_variables=["context", "question"]
        )
        
        self.english_prompt_template = PromptTemplate(
            template="""Use the following pieces of context to answer the question. If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context:
{context}

Question: {question}

Please provide a detailed and accurate answer, citing relevant document sources when possible:""",
            input_variables=["context", "question"]
        )
    
    def setup_qa_chain(self, language: str = "chinese"):
        """Setup the QA chain with retriever"""
        if self.vector_store_manager.vector_store is None:
            raise ValueError("No vector store available. Please add documents first.")
        
        retriever = self.vector_store_manager.get_retriever()
        
        prompt = self.prompt_template if language == "chinese" else self.english_prompt_template
        
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever,
            chain_type_kwargs={"prompt": prompt},
            return_source_documents=True
        )
        
        return qa_chain
    
    def ask_question(self, question: str, language: str = "chinese") -> Dict[str, Any]:
        """Ask a question and get an answer with source documents"""
        try:
            qa_chain = self.setup_qa_chain(language)
            result = qa_chain({"query": question})
            
            # Format the response
            response = {
                "answer": result["result"],
                "source_documents": [],
                "question": question
            }
            
            # Process source documents
            for doc in result["source_documents"]:
                source_info = {
                    "content": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
                    "metadata": doc.metadata
                }
                response["source_documents"].append(source_info)
            
            return response
            
        except Exception as e:
            return {
                "answer": f"抱歉，处理您的问题时出现错误：{str(e)}",
                "source_documents": [],
                "question": question,
                "error": str(e)
            }
    
    def get_relevant_documents(self, query: str, k: int = None) -> List[Document]:
        """Get relevant documents for a query"""
        return self.vector_store_manager.similarity_search(query, k)
    
    def get_relevant_documents_with_scores(self, query: str, k: int = None) -> List[tuple]:
        """Get relevant documents with similarity scores"""
        return self.vector_store_manager.similarity_search_with_score(query, k)
    
    def chat_with_history(self, question: str, chat_history: List[Dict[str, str]] = None, language: str = "chinese") -> Dict[str, Any]:
        """Chat with conversation history context"""
        if chat_history is None:
            chat_history = []
        
        # Build context from chat history
        history_context = ""
        for chat in chat_history[-3:]:  # Only use last 3 exchanges
            history_context += f"Q: {chat.get('question', '')}\nA: {chat.get('answer', '')}\n\n"
        
        # Enhance the question with history context if available
        enhanced_question = question
        if history_context:
            enhanced_question = f"基于以下对话历史：\n{history_context}\n当前问题：{question}"
        
        return self.ask_question(enhanced_question, language)
