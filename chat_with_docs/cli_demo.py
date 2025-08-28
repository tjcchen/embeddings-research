#!/usr/bin/env python3
"""
Command Line Interface for Chat with Documents System
Simple demo without web interface
"""

import os
import sys
from pathlib import Path

from document_processor import DocumentProcessor
from vector_store import VectorStoreManager
from qa_system import QASystem
from config import Config

class CLIDemo:
    def __init__(self):
        self.document_processor = DocumentProcessor()
        self.vector_store_manager = VectorStoreManager()
        self.qa_system = QASystem(self.vector_store_manager)
        self.chat_history = []
    
    def run(self):
        print("📚 文档问答系统 - Chat with Documents")
        print("=" * 50)
        
        # Check API key
        if not Config.OPENAI_API_KEY:
            print("❌ 错误：请设置 OPENAI_API_KEY 环境变量")
            print("💡 提示：创建 .env 文件并添加：OPENAI_API_KEY=your_api_key_here")
            return
        
        # Try to load existing vector store
        if self.vector_store_manager.load_vector_store():
            doc_count = self.vector_store_manager.get_document_count()
            print(f"✅ 已加载现有向量数据库，包含 {doc_count} 个文档块")
        else:
            print("📁 未找到现有数据库，请先添加文档")
        
        while True:
            print("\n" + "=" * 50)
            print("选择操作：")
            print("1. 添加文档文件")
            print("2. 添加网页URL")
            print("3. 开始问答")
            print("4. 查看文档统计")
            print("5. 清空数据库")
            print("6. 退出")
            
            choice = input("\n请输入选项 (1-6): ").strip()
            
            if choice == "1":
                self.add_documents()
            elif choice == "2":
                self.add_url()
            elif choice == "3":
                self.start_qa()
            elif choice == "4":
                self.show_stats()
            elif choice == "5":
                self.clear_database()
            elif choice == "6":
                print("👋 再见！")
                break
            else:
                print("❌ 无效选项，请重新选择")
    
    def add_documents(self):
        """Add document files"""
        print("\n📁 添加文档文件")
        print("支持的格式：.pdf, .docx, .txt, .html, .md")
        
        file_path = input("请输入文件路径: ").strip()
        
        if not file_path:
            print("❌ 文件路径不能为空")
            return
        
        if not os.path.exists(file_path):
            print("❌ 文件不存在")
            return
        
        try:
            print("⏳ 正在处理文档...")
            documents = self.document_processor.process_file(file_path)
            
            self.vector_store_manager.add_documents(documents)
            self.vector_store_manager.save_vector_store()
            
            print(f"✅ 成功添加 {len(documents)} 个文档块")
            
        except Exception as e:
            print(f"❌ 处理文档失败：{str(e)}")
    
    def add_url(self):
        """Add web page URL"""
        print("\n🌐 添加网页URL")
        
        url = input("请输入网页URL: ").strip()
        
        if not url:
            print("❌ URL不能为空")
            return
        
        try:
            print("⏳ 正在处理网页...")
            documents = self.document_processor.process_url(url)
            
            self.vector_store_manager.add_documents(documents)
            self.vector_store_manager.save_vector_store()
            
            print(f"✅ 成功添加 {len(documents)} 个文档块")
            
        except Exception as e:
            print(f"❌ 处理网页失败：{str(e)}")
    
    def start_qa(self):
        """Start Q&A session"""
        if self.vector_store_manager.vector_store is None:
            print("❌ 请先添加文档！")
            return
        
        print("\n💬 开始问答会话")
        print("输入 'quit' 退出问答模式")
        print("输入 'clear' 清空对话历史")
        print("-" * 30)
        
        while True:
            question = input("\n🤔 请输入问题: ").strip()
            
            if question.lower() == 'quit':
                break
            elif question.lower() == 'clear':
                self.chat_history = []
                print("✅ 对话历史已清空")
                continue
            elif not question:
                continue
            
            try:
                print("⏳ 正在思考...")
                response = self.qa_system.chat_with_history(question, self.chat_history)
                
                print(f"\n🤖 回答：{response['answer']}")
                
                # Show source documents
                if response.get('source_documents'):
                    print("\n📚 相关文档来源：")
                    for i, doc in enumerate(response['source_documents'], 1):
                        source = doc['metadata'].get('file_name', doc['metadata'].get('source', 'Unknown'))
                        print(f"  {i}. {source}")
                        print(f"     {doc['content'][:100]}...")
                
                # Add to history
                self.chat_history.append({
                    'question': question,
                    'answer': response['answer']
                })
                
            except Exception as e:
                print(f"❌ 回答问题失败：{str(e)}")
    
    def show_stats(self):
        """Show database statistics"""
        print("\n📊 数据库统计")
        
        if self.vector_store_manager.vector_store is None:
            print("❌ 暂无数据")
            return
        
        doc_count = self.vector_store_manager.get_document_count()
        print(f"📄 文档块数量: {doc_count}")
        
        # Show sample documents
        try:
            sample_docs = self.vector_store_manager.similarity_search("sample", k=3)
            print(f"📋 示例文档片段:")
            for i, doc in enumerate(sample_docs, 1):
                source = doc.metadata.get('file_name', doc.metadata.get('source', 'Unknown'))
                print(f"  {i}. 来源: {source}")
                print(f"     内容: {doc.page_content[:100]}...")
        except:
            pass
    
    def clear_database(self):
        """Clear the vector database"""
        confirm = input("\n⚠️  确定要清空数据库吗？(y/N): ").strip().lower()
        
        if confirm == 'y':
            try:
                self.vector_store_manager.delete_vector_store()
                self.chat_history = []
                print("✅ 数据库已清空")
            except Exception as e:
                print(f"❌ 清空失败：{str(e)}")
        else:
            print("❌ 操作已取消")

def main():
    demo = CLIDemo()
    demo.run()

if __name__ == "__main__":
    main()
