import os
import hashlib
import struct
import math
from typing import List, Dict, Optional, Any
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
import chromadb
from chromadb.config import Settings
import logging

logger = logging.getLogger(__name__)

class FinancialKnowledgeBase:
    def __init__(self, persist_directory: str = "./finance_kb"):
        """初始化财务知识库"""
        self.persist_directory = persist_directory
        
        # 创建向量数据库客户端
        self.client = chromadb.PersistentClient(
            path=self.persist_directory,
            settings=Settings(
                anonymized_telemetry=False
            )
        )
        
        # 创建或获取集合
        self.collection = self.client.get_or_create_collection(
            name="financial_knowledge",
            metadata={"hnsw:space": "cosine"}
        )
        
        # 文本分割器
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            separators=["\n\n", "\n", "。", "；", "，", " ", ""]
        )
        
        # 初始化内置财务知识
        self._initialize_builtin_knowledge()
        
        logger.info("财务知识库初始化完成")
    
    def _initialize_builtin_knowledge(self):
        """初始化内置财务知识"""
        builtin_knowledge = [
            {
                "content": """杜邦分析是一种财务分析方法，通过将净资产收益率（ROE）分解为三个关键指标：销售净利率、总资产周转率和权益乘数。ROE = 销售净利率 × 总资产周转率 × 权益乘数。这种分解有助于识别公司盈利能力的来源和潜在问题。""",
                "metadata": {"source": "财务分析基础", "type": "杜邦分析"}
            },
            {
                "content": """财务比率分析是评估公司财务状况的重要工具。主要包括：盈利能力比率（如毛利率、净利率、ROE）、偿债能力比率（如流动比率、速动比率、资产负债率）、运营能力比率（如应收账款周转率、存货周转率）和发展能力比率（如营收增长率、净利润增长率）。""",
                "metadata": {"source": "财务分析基础", "type": "财务比率"}
            },
            {
                "content": """估值模型包括市盈率（PE）、市净率（PB）、市销率（PS）和现金流贴现（DCF）等方法。市盈率适用于盈利稳定的公司，市净率适用于金融和周期性行业，市销率适用于成长型公司，DCF适用于现金流稳定的公司。""",
                "metadata": {"source": "财务分析基础", "type": "估值模型"}
            },
            {
                "content": """盈利能力分析主要关注公司的盈利水平和盈利质量。核心指标包括：毛利率（反映产品定价能力）、净利率（反映整体盈利能力）、净资产收益率（ROE，反映股东回报）、总资产收益率（ROA，反映资产利用效率）。""",
                "metadata": {"source": "财务分析基础", "type": "盈利能力"}
            },
            {
                "content": """偿债能力分析评估公司偿还债务的能力。短期偿债能力指标包括流动比率（理想值2以上）和速动比率（理想值1以上）；长期偿债能力指标包括资产负债率（一般不超过70%）和利息保障倍数（理想值3以上）。""",
                "metadata": {"source": "财务分析基础", "type": "偿债能力"}
            },
            {
                "content": """运营能力分析评估公司资产的利用效率。关键指标包括：应收账款周转率（反映收款效率）、存货周转率（反映库存管理效率）、总资产周转率（反映整体资产利用效率）。周转率越高，表明资产利用效率越好。""",
                "metadata": {"source": "财务分析基础", "type": "运营能力"}
            },
            {
                "content": """发展能力分析评估公司的成长潜力。主要指标包括：营收增长率（反映市场扩张能力）、净利润增长率（反映盈利增长能力）、总资产增长率（反映规模扩张能力）。持续的高增长率通常意味着良好的发展前景。""",
                "metadata": {"source": "财务分析基础", "type": "发展能力"}
            },
            {
                "content": """财务报告分析需要结合行业特点和公司战略。不同行业的财务指标标准差异很大，例如制造业的资产负债率通常较高，而科技行业的研发费用比例较高。分析时应关注指标的变化趋势和行业对比。""",
                "metadata": {"source": "财务分析基础", "type": "行业分析"}
            }
        ]
        
        # 添加内置知识到知识库
        for knowledge in builtin_knowledge:
            doc = Document(
                page_content=knowledge["content"],
                metadata=knowledge["metadata"]
            )
            self.add_documents([doc])
    
    def _simple_embedding(self, text: str) -> List[float]:
        """使用哈希生成简单的向量嵌入"""
        hash_obj = hashlib.sha256(text.encode())
        hash_bytes = hash_obj.digest()
        
        # 生成384维向量
        vector = []
        for i in range(384):
            if i * 4 < len(hash_bytes):
                try:
                    value = struct.unpack('f', hash_bytes[i * 4:(i + 1) * 4])[0] / 1000.0
                except:
                    value = 0.0
            else:
                value = 0.0
            vector.append(value)
        
        # 归一化处理
        norm = math.sqrt(sum(v * v for v in vector))
        if norm > 0:
            vector = [v / norm for v in vector]
        
        return vector
    
    def add_documents(self, documents: List[Document], metadata: Optional[Dict] = None) -> Dict:
        """添加文档到知识库"""
        try:
            # 分割文档
            split_docs = self.text_splitter.split_documents(documents)
            
            # 准备数据
            ids = []
            embeddings = []
            texts = []
            metadatas = []
            
            for i, doc in enumerate(split_docs):
                doc_id = f"doc_{self.collection.count() + i}"
                ids.append(doc_id)
                
                embedding = self._simple_embedding(doc.page_content)
                embeddings.append(embedding)
                
                texts.append(doc.page_content)
                
                doc_metadata = doc.metadata.copy()
                if metadata:
                    doc_metadata.update(metadata)
                metadatas.append(doc_metadata)
            
            # 添加到数据库
            self.collection.add(
                ids=ids,
                embeddings=embeddings,
                metadatas=metadatas,
                documents=texts
            )
            
            logger.info(f"添加了 {len(split_docs)} 个文档块")
            
            # 返回添加的文档数量
            return {"added": len(split_docs)}
            
        except Exception as e:
            logger.error(f"添加文档失败: {e}")
            raise
    
    def search_similar(self, query: str, k: int = 3) -> List[Document]:
        """搜索相似文档"""
        try:
            # 生成查询向量
            query_embedding = self._simple_embedding(query)
            
            # 相似性搜索
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=k
            )
            
            # 转换为Document对象
            documents = []
            if results['documents']:
                for i in range(len(results['documents'][0])):
                    doc = Document(
                        page_content=results['documents'][0][i],
                        metadata=results['metadatas'][0][i] if results['metadatas'] else {}
                    )
                    documents.append(doc)
            
            return documents
            
        except Exception as e:
            logger.error(f"搜索相似文档失败: {e}")
            return []
    
    def get_info(self) -> Dict[str, Any]:
        """获取知识库信息"""
        try:
            count = self.collection.count()
            return {
                "document_count": count,
                "collection_name": self.collection.name,
                "persist_directory": self.persist_directory,
                "status": "active"
            }
        except Exception as e:
            logger.error(f"获取知识库信息失败: {e}")
            return {
                "document_count": 0,
                "error": str(e)
            }
    
    def clear(self):
        """清空知识库"""
        try:
            self.client.delete_collection(self.collection.name)
            self.collection = self.client.create_collection(
                name="financial_knowledge",
                metadata={"hnsw:space": "cosine"}
            )
            logger.info("知识库已清空")
            return {"status": "success", "message": "知识库已清空"}
        except Exception as e:
            logger.error(f"清空知识库失败: {e}")
            return {"status": "error", "message": str(e)}