import os
import streamlit as st
from pathlib import Path
from typing import List, Dict, Any

from document_processor import DocumentProcessor
from vector_store import VectorStoreManager
from qa_system import QASystem
from config import Config

class ChatWithDocsApp:
    def __init__(self):
        self.document_processor = DocumentProcessor()
        self.vector_store_manager = VectorStoreManager()
        self.qa_system = QASystem(self.vector_store_manager)
        
        # Initialize session state
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        if 'documents_loaded' not in st.session_state:
            st.session_state.documents_loaded = False
        if 'vector_store_ready' not in st.session_state:
            st.session_state.vector_store_ready = False
    
    def run(self):
        st.set_page_config(
            page_title="文档问答系统 - Chat with Documents",
            page_icon="📚",
            layout="wide"
        )
        
        st.title("📚 文档问答系统 (Chat with Documents)")
        st.markdown("---")
        
        # Sidebar for document management
        with st.sidebar:
            st.header("📁 文档管理")
            
            # Check if vector store exists
            if self.vector_store_manager.load_vector_store():
                st.session_state.vector_store_ready = True
                doc_count = self.vector_store_manager.get_document_count()
                st.success(f"已加载向量数据库，包含 {doc_count} 个文档块")
            
            # File upload section
            st.subheader("上传文档")
            uploaded_files = st.file_uploader(
                "选择文件",
                type=['pdf', 'docx', 'txt', 'html', 'md'],
                accept_multiple_files=True
            )
            
            # Process documents button
            if st.button("处理文档", type="primary"):
                if uploaded_files:
                    self.process_documents(uploaded_files)
            
            # Clear vector store button
            if st.button("清空数据库", type="secondary"):
                self.clear_vector_store()
        
        # Main chat interface
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.header("💬 对话界面")
            
            # Language selection
            language = st.selectbox("选择语言 / Select Language", ["chinese", "english"])
            
            # Question input form
            with st.form("question_form", clear_on_submit=True):
                question = st.text_input("请输入您的问题：")
                submit_button = st.form_submit_button("提问", type="primary")
                
                if submit_button:
                    if question and st.session_state.vector_store_ready:
                        self.handle_question(question, language)
                    elif not st.session_state.vector_store_ready:
                        st.error("请先上传并处理文档！")
                    else:
                        st.warning("请输入问题！")
            
            # Display chat history
            self.display_chat_history()
        
        with col2:
            st.header("📊 系统信息")
            
            if st.session_state.vector_store_ready:
                doc_count = self.vector_store_manager.get_document_count()
                st.metric("文档块数量", doc_count)
                
                # Display recent documents
                st.subheader("最近处理的文档")
                if hasattr(st.session_state, 'recent_docs'):
                    for doc_info in st.session_state.recent_docs[-5:]:
                        st.text(f"📄 {doc_info}")
            else:
                st.info("暂无文档数据")
    
    def process_documents(self, uploaded_files: List):
        """Process uploaded files"""
        with st.spinner("正在处理文档..."):
            try:
                all_documents = []
                processed_docs = []
                
                # Create upload directory
                os.makedirs(Config.UPLOAD_DIR, exist_ok=True)
                
                # Process uploaded files
                if uploaded_files:
                    for uploaded_file in uploaded_files:
                        # Save uploaded file
                        file_path = os.path.join(Config.UPLOAD_DIR, uploaded_file.name)
                        with open(file_path, "wb") as f:
                            f.write(uploaded_file.getvalue())
                        
                        # Process file
                        documents = self.document_processor.process_file(file_path)
                        all_documents.extend(documents)
                        processed_docs.append(uploaded_file.name)
                
                # Add to vector store
                if all_documents:
                    self.vector_store_manager.add_documents(all_documents)
                    self.vector_store_manager.save_vector_store()
                    
                    st.session_state.vector_store_ready = True
                    st.session_state.recent_docs = getattr(st.session_state, 'recent_docs', []) + processed_docs
                    
                    st.success(f"成功处理 {len(all_documents)} 个文档块！")
                else:
                    st.warning("没有找到可处理的文档内容。")
                    
            except Exception as e:
                st.error(f"处理文档时出错：{str(e)}")
    
    def handle_question(self, question: str, language: str):
        """Handle user question"""
        with st.spinner("正在思考..."):
            try:
                response = self.qa_system.chat_with_history(
                    question, 
                    st.session_state.chat_history,
                    language
                )
                
                # Add to chat history
                chat_entry = {
                    "question": question,
                    "answer": response["answer"],
                    "source_documents": response["source_documents"]
                }
                st.session_state.chat_history.append(chat_entry)
                
                # Note: Cannot clear input field due to Streamlit widget limitations
                # The input will be cleared on next rerun
                
            except Exception as e:
                st.error(f"回答问题时出错：{str(e)}")
    
    def display_chat_history(self):
        """Display chat history"""
        if st.session_state.chat_history:
            st.subheader("对话历史")
            
            for i, chat in enumerate(reversed(st.session_state.chat_history)):
                with st.expander(f"Q{len(st.session_state.chat_history)-i}: {chat['question'][:50]}..."):
                    st.markdown(f"**问题：** {chat['question']}")
                    st.markdown(f"**回答：** {chat['answer']}")
                    
                    if chat.get('source_documents'):
                        st.markdown("**相关文档：**")
                        for j, doc in enumerate(chat['source_documents']):
                            st.markdown(f"📄 **来源 {j+1}：** {doc['metadata'].get('file_name', 'Unknown')}")
                            st.markdown(f"```\n{doc['content']}\n```")
    
    def clear_vector_store(self):
        """Clear the vector store"""
        try:
            self.vector_store_manager.delete_vector_store()
            st.session_state.vector_store_ready = False
            st.session_state.chat_history = []
            st.session_state.recent_docs = []
            st.success("数据库已清空！")
        except Exception as e:
            st.error(f"清空数据库时出错：{str(e)}")

def main():
    # Check for OpenAI API key
    if not Config.OPENAI_API_KEY:
        st.error("请设置 OPENAI_API_KEY 环境变量！")
        st.info("您可以创建一个 .env 文件并添加：OPENAI_API_KEY=your_api_key_here")
        return
    
    app = ChatWithDocsApp()
    app.run()

if __name__ == "__main__":
    main()
