#!/usr/bin/env python3
"""
Sample test script to demonstrate the Chat with Documents system
"""

import os
import tempfile
from pathlib import Path

from document_processor import DocumentProcessor
from vector_store import VectorStoreManager
from qa_system import QASystem

def create_sample_documents():
    """Create sample documents for testing"""
    sample_docs = []
    
    # Create a temporary directory for sample files
    temp_dir = tempfile.mkdtemp()
    
    # Sample 1: AI and Machine Learning
    ai_content = """
    人工智能与机器学习

    人工智能（Artificial Intelligence, AI）是计算机科学的一个分支，致力于创建能够执行通常需要人类智能的任务的系统。

    机器学习是人工智能的一个子集，它使计算机能够在没有明确编程的情况下学习和改进。主要类型包括：

    1. 监督学习：使用标记数据训练模型
    2. 无监督学习：从未标记数据中发现模式
    3. 强化学习：通过与环境交互学习最优行为

    深度学习是机器学习的一个分支，使用神经网络来模拟人脑的学习过程。它在图像识别、自然语言处理和语音识别等领域取得了突破性进展。

    应用领域：
    - 自动驾驶汽车
    - 医疗诊断
    - 金融风险评估
    - 推荐系统
    - 语音助手
    """
    
    ai_file = os.path.join(temp_dir, "ai_ml_intro.txt")
    with open(ai_file, 'w', encoding='utf-8') as f:
        f.write(ai_content)
    sample_docs.append(ai_file)
    
    # Sample 2: Python Programming
    python_content = """
    Python编程语言基础

    Python是一种高级、解释型的编程语言，以其简洁和可读性而闻名。

    主要特点：
    - 语法简洁明了
    - 跨平台兼容
    - 丰富的标准库
    - 强大的第三方生态系统

    数据类型：
    1. 基本类型：int, float, str, bool
    2. 集合类型：list, tuple, dict, set
    3. 高级类型：class, function, module

    常用库：
    - NumPy：数值计算
    - Pandas：数据分析
    - Matplotlib：数据可视化
    - Scikit-learn：机器学习
    - Django/Flask：Web开发
    - TensorFlow/PyTorch：深度学习

    Python在以下领域广泛应用：
    - 数据科学和分析
    - 人工智能和机器学习
    - Web开发
    - 自动化脚本
    - 科学计算
    """
    
    python_file = os.path.join(temp_dir, "python_basics.txt")
    with open(python_file, 'w', encoding='utf-8') as f:
        f.write(python_content)
    sample_docs.append(python_file)
    
    # Sample 3: Data Science Process
    ds_content = """
    数据科学流程

    数据科学是一个跨学科领域，结合了统计学、计算机科学和领域专业知识来从数据中提取洞察。

    典型的数据科学流程包括：

    1. 问题定义
       - 明确业务目标
       - 定义成功指标
       - 确定数据需求

    2. 数据收集
       - 内部数据源
       - 外部数据源
       - API和网络爬虫
       - 传感器数据

    3. 数据清理和预处理
       - 处理缺失值
       - 异常值检测
       - 数据格式标准化
       - 特征工程

    4. 探索性数据分析（EDA）
       - 数据分布分析
       - 相关性分析
       - 可视化探索
       - 假设验证

    5. 模型建立
       - 算法选择
       - 特征选择
       - 模型训练
       - 超参数调优

    6. 模型评估
       - 交叉验证
       - 性能指标
       - 模型解释性
       - 业务价值评估

    7. 部署和监控
       - 模型部署
       - 性能监控
       - 模型更新
       - A/B测试
    """
    
    ds_file = os.path.join(temp_dir, "data_science_process.txt")
    with open(ds_file, 'w', encoding='utf-8') as f:
        f.write(ds_content)
    sample_docs.append(ds_file)
    
    return sample_docs, temp_dir

def test_system():
    """Test the complete system"""
    print("🧪 开始测试文档问答系统")
    print("=" * 50)
    
    # Create sample documents
    print("📝 创建示例文档...")
    sample_files, temp_dir = create_sample_documents()
    
    # Initialize components
    print("🔧 初始化系统组件...")
    doc_processor = DocumentProcessor()
    vector_store = VectorStoreManager()
    qa_system = QASystem(vector_store)
    
    # Process documents
    print("📚 处理文档...")
    all_documents = []
    for file_path in sample_files:
        print(f"  处理: {Path(file_path).name}")
        documents = doc_processor.process_file(file_path)
        all_documents.extend(documents)
        print(f"    生成 {len(documents)} 个文档块")
    
    # Create vector store
    print("🔍 创建向量数据库...")
    vector_store.create_vector_store(all_documents)
    print(f"✅ 向量数据库创建完成，包含 {len(all_documents)} 个文档块")
    
    # Test questions
    test_questions = [
        "什么是机器学习？",
        "Python有哪些主要特点？",
        "数据科学流程包括哪些步骤？",
        "深度学习在哪些领域有应用？",
        "数据预处理包括什么内容？"
    ]
    
    print("\n💬 开始问答测试")
    print("-" * 30)
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n🤔 问题 {i}: {question}")
        
        try:
            response = qa_system.ask_question(question)
            print(f"🤖 回答: {response['answer']}")
            
            if response.get('source_documents'):
                print("📚 相关文档:")
                for j, doc in enumerate(response['source_documents'][:2], 1):
                    source = doc['metadata'].get('file_name', 'Unknown')
                    print(f"  {j}. 来源: {source}")
                    print(f"     内容: {doc['content'][:100]}...")
        
        except Exception as e:
            print(f"❌ 错误: {str(e)}")
    
    # Test similarity search
    print(f"\n🔍 测试相似度搜索")
    print("-" * 30)
    
    search_query = "机器学习算法"
    similar_docs = vector_store.similarity_search_with_score(search_query, k=3)
    
    print(f"查询: {search_query}")
    for i, (doc, score) in enumerate(similar_docs, 1):
        source = doc.metadata.get('file_name', 'Unknown')
        print(f"{i}. 相似度: {score:.3f} | 来源: {source}")
        print(f"   内容: {doc.page_content[:100]}...")
    
    # Cleanup
    print(f"\n🧹 清理临时文件...")
    import shutil
    shutil.rmtree(temp_dir)
    
    print("\n✅ 测试完成！")

def main():
    """Main function"""
    from config import Config
    
    # Check API key
    if not Config.OPENAI_API_KEY:
        print("❌ 错误：请设置 OPENAI_API_KEY 环境变量")
        print("💡 提示：创建 .env 文件并添加：OPENAI_API_KEY=your_api_key_here")
        return
    
    test_system()

if __name__ == "__main__":
    main()
