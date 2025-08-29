# 文档问答系统 (Chat with Documents)

一个基于 LangChain 和向量数据库的智能文档问答系统，支持上传 PDF、Word、网页等多种格式的文档，并通过自然语言进行问答交互。

## 🚀 功能特性

- **多格式文档支持**: PDF、Word (.docx)、文本文件 (.txt, .md)、HTML、网页URL
- **智能文本分块**: 使用 RecursiveCharacterTextSplitter 进行智能文本切分
- **向量化存储**: 基于 OpenAI Embeddings 和 FAISS 向量数据库
- **检索增强生成**: 结合相似度搜索和大语言模型的 RAG 架构
- **双语支持**: 支持中文和英文问答
- **对话历史**: 支持上下文相关的多轮对话
- **Web界面**: 基于 Streamlit 的友好用户界面
- **命令行工具**: 提供 CLI 版本用于快速测试

## 📋 应用场景

- **法律合同问答**: 上传法律文档，快速查询条款内容
- **学术论文解读**: 分析研究论文，提取关键信息
- **公司知识库助手**: 构建企业内部知识问答系统
- **技术文档查询**: 快速检索技术手册和API文档
- **教育辅助工具**: 帮助学生理解复杂教材内容

## 🛠 系统架构

```
文档输入 → 文本提取 → 智能分块 → 向量化 → FAISS存储
                                                    ↓
用户问题 → 向量检索 → 相关文档片段 → LLM生成答案 → 返回结果
```

## 📦 安装依赖

```bash
cd chat_with_docs
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

## ⚙️ 配置设置
python3 cli_demo.py
1. 复制环境变量模板：
```bash
cp .env.example .env
```

2. 编辑 `.env` 文件，添加您的 OpenAI API Key：
```
OPENAI_API_KEY=your_openai_api_key_here
```

## 🚀 使用方法

### Web界面版本

启动 Streamlit 应用：
```bash
python3 -m streamlit run main.py
```

然后在浏览器中打开 `http://localhost:8501`

### 命令行版本

运行 CLI 演示：
```bash

```

## 📁 项目结构

```
chat_with_docs/
├── config.py              # 配置文件
├── document_processor.py  # 文档处理模块
├── vector_store.py        # 向量数据库管理
├── qa_system.py           # 问答系统核心
├── main.py                # Streamlit Web应用
├── cli_demo.py            # 命令行演示
├── requirements.txt       # 依赖包列表
├── .env.example           # 环境变量模板
└── README.md              # 项目文档
```

## 🔧 核心组件

### DocumentProcessor
- 支持多种文档格式的文本提取
- 智能文本分块和元数据管理
- 网页内容抓取和清理

### VectorStoreManager
- FAISS 向量数据库管理
- 文档向量化和存储
- 相似度搜索和检索

### QASystem
- 基于检索的问答生成
- 支持对话历史上下文
- 自定义提示模板

## 📊 配置参数

在 `config.py` 中可以调整以下参数：

- `CHUNK_SIZE`: 文本分块大小 (默认: 1000)
- `CHUNK_OVERLAP`: 分块重叠长度 (默认: 200)
- `TOP_K_RESULTS`: 检索结果数量 (默认: 4)
- `EMBEDDING_MODEL`: 嵌入模型 (默认: text-embedding-ada-002)
- `CHAT_MODEL`: 对话模型 (默认: gpt-3.5-turbo)

## 🎯 使用示例

### 1. 上传文档
- 通过 Web 界面上传 PDF、Word 等文档
- 或者输入网页 URL 直接处理网页内容

### 2. 开始问答
```
问题: 这份合同的违约责任条款是什么？
回答: 根据合同第8条违约责任条款，如果一方违反合同约定...

来源文档: contract.pdf (第3页)
```

### 3. 多轮对话
```
问题1: 什么是机器学习？
回答1: 机器学习是人工智能的一个分支...

问题2: 它有哪些主要类型？
回答2: 基于前面提到的机器学习概念，主要有三种类型：监督学习、无监督学习和强化学习...
```

## 🔍 技术细节

### 文本处理流程
1. **文档解析**: 使用专门的库提取不同格式的文本内容
2. **文本清理**: 去除无关字符和格式信息
3. **智能分块**: 保持语义完整性的文本切分
4. **元数据管理**: 记录文档来源、页码等信息

### 向量化存储
1. **嵌入生成**: 使用 OpenAI text-embedding-ada-002 模型
2. **向量存储**: FAISS 高效向量数据库
3. **相似度计算**: 余弦相似度匹配
4. **检索优化**: Top-K 检索和阈值过滤

### 问答生成
1. **查询理解**: 分析用户问题意图
2. **文档检索**: 基于向量相似度的文档片段检索
3. **上下文构建**: 结合检索结果和对话历史
4. **答案生成**: 使用 GPT 模型生成准确回答

## 🚨 注意事项

1. **API 费用**: 使用 OpenAI API 会产生费用，请注意用量控制
2. **文档大小**: 建议单个文档不超过 10MB
3. **语言支持**: 主要优化中文和英文，其他语言可能效果有限
4. **网络连接**: 需要稳定的网络连接访问 OpenAI API

## 🔧 故障排除

### 常见问题

**Q: 提示 "No module named 'xxx'"**
A: 请确保已安装所有依赖：`pip install -r requirements.txt`

**Q: OpenAI API 错误**
A: 检查 API Key 是否正确设置，账户是否有足够余额

**Q: 文档处理失败**
A: 确认文档格式正确，文件未损坏

**Q: 搜索结果不准确**
A: 尝试调整 `CHUNK_SIZE` 和 `TOP_K_RESULTS` 参数

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本项目
2. 创建特性分支
3. 提交更改
4. 发起 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](../LICENSE) 文件

## 🙏 致谢

- [LangChain](https://github.com/langchain-ai/langchain) - 强大的 LLM 应用开发框架
- [FAISS](https://github.com/facebookresearch/faiss) - 高效的向量相似度搜索库
- [Streamlit](https://streamlit.io/) - 快速构建数据应用的框架
- [OpenAI](https://openai.com/) - 提供优秀的嵌入和语言模型

---

**Happy Chatting with Documents! 📚✨**
