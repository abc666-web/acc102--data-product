import logging
import os
import tempfile
import traceback
from datetime import datetime
from typing import Dict, Any

from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 导入财务分析模块
try:
    from financial_data_processor import FinancialDataProcessor
    from financial_report_generator import FinancialReportGenerator
    from financial_knowledge_base import FinancialKnowledgeBase
    
    # 初始化组件
    data_processor = FinancialDataProcessor()
    report_generator = FinancialReportGenerator()
    knowledge_base = FinancialKnowledgeBase()
    
    COMPONENTS_AVAILABLE = True
    logger.info("财务分析组件初始化成功")
except Exception as e:
    logger.error(f"初始化财务分析组件失败: {e}")
    COMPONENTS_AVAILABLE = False

# 创建FastAPI应用
app = FastAPI(
    title="智能财务分析系统API",
    description="基于RAG架构的智能财务分析系统",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局变量
upload_tasks = {}

@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "智能财务分析系统API",
        "version": "1.0.0",
        "components": {
            "data_processor": "available" if COMPONENTS_AVAILABLE else "unavailable",
            "report_generator": "available" if COMPONENTS_AVAILABLE else "unavailable",
            "knowledge_base": "available" if COMPONENTS_AVAILABLE else "unavailable"
        }
    }

@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "components": {
            "data_processor": "available" if COMPONENTS_AVAILABLE else "unavailable",
            "report_generator": "available" if COMPONENTS_AVAILABLE else "unavailable",
            "knowledge_base": "available" if COMPONENTS_AVAILABLE else "unavailable"
        }
    }


# UploadFile 已从 fastapi 导入


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """上传财务数据文件"""
    logger.info(f"上传文件请求: {file.filename}")
    
    if not COMPONENTS_AVAILABLE:
        raise HTTPException(status_code=500, detail="财务分析组件未初始化")
    
    try:
        # 检查文件类型
        file_ext = file.filename.split('.')[-1].lower()
        if file_ext not in ['csv', 'xlsx']:
            raise HTTPException(status_code=415, detail=f"不支持的文件类型: {file_ext}")
        
        # 读取文件内容
        content = await file.read()
        file_size = len(content)
        logger.info(f"文件读取完成: {file.filename}, 大小: {file_size} bytes")
        
        # 处理文件
        with tempfile.NamedTemporaryFile(mode='wb', suffix=f'.{file_ext}', delete=False) as temp_file:
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            # 使用数据处理器加载文件
            result = data_processor.load_file(temp_file_path, file_ext)
            
            if result["status"] == "success":
                # 计算指标
                metrics = data_processor.calculate_all_metrics()
                
                return {
                    "status": "success",
                    "message": "文件上传成功并已处理",
                    "filename": file.filename,
                    "file_size": file_size,
                    "metrics": metrics,
                    "data_summary": data_processor.get_data_summary()
                }
            else:
                return {
                    "status": "error",
                    "message": result["message"],
                    "filename": file.filename
                }
                
        finally:
            # 清理临时文件
            os.unlink(temp_file_path)
            
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"上传文件时出错: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"文件上传失败: {str(e)}")

@app.post("/upload-manual")
async def upload_manual_data(data: Dict[str, Any]):
    """上传手动输入的财务数据"""
    logger.info("上传手动财务数据")
    
    if not COMPONENTS_AVAILABLE:
        raise HTTPException(status_code=500, detail="财务分析组件未初始化")
    
    try:
        # 验证数据
        required_fields = ['revenue', 'net_profit', 'total_assets', 'total_liabilities', 'total_equity']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            raise HTTPException(status_code=400, detail=f"缺少必要字段: {', '.join(missing_fields)}")
        
        # 加载数据
        result = data_processor.load_manual_data(data)
        
        if result["status"] == "success":
            # 计算指标
            metrics = data_processor.calculate_all_metrics()
            
            return {
                "status": "success",
                "message": "数据上传成功",
                "metrics": metrics,
                "data_summary": data_processor.get_data_summary()
            }
        else:
            return {
                "status": "error",
                "message": result["message"]
            }
            
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"上传手动数据时出错: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"数据上传失败: {str(e)}")

@app.post("/generate")
async def generate_report(data: Dict[str, Any]):
    """生成财务分析报告"""
    logger.info("生成财务分析报告请求")
    
    if not COMPONENTS_AVAILABLE:
        raise HTTPException(status_code=500, detail="财务分析组件未初始化")
    
    try:
        # 获取参数
        financial_data = data.get("financial_data", {})
        query = data.get("query", "财务分析")
        report_type = data.get("report_type", "comprehensive")
        
        # 验证参数
        if not financial_data:
            raise HTTPException(status_code=400, detail="财务数据不能为空")
        
        # 生成报告
        result = report_generator.generate_report(financial_data, query, report_type)
        
        if result["status"] == "success":
            return {
                "status": "success",
                "report_content": result["report_content"],
                "metrics": result["metrics"],
                "data_quality": result["data_quality"]
            }
        else:
            return {
                "status": "error",
                "message": result["report_content"],
                "error": result.get("error", "未知错误")
            }
            
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"生成报告时出错: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"报告生成失败: {str(e)}")

@app.post("/kb/upload")
async def upload_to_knowledge_base(file: UploadFile = File(...)):
    """上传文档到财务知识库"""
    logger.info(f"上传文档到知识库: {file.filename}")
    
    if not COMPONENTS_AVAILABLE:
        raise HTTPException(status_code=500, detail="财务分析组件未初始化")
    
    try:
        # 检查文件类型
        file_ext = file.filename.split('.')[-1].lower()
        if file_ext not in ['txt', 'md', 'pdf']:
            raise HTTPException(status_code=415, detail=f"不支持的文件类型: {file_ext}")
        
        # 读取文件内容
        content = await file.read()
        file_size = len(content)
        logger.info(f"文件读取完成: {file.filename}, 大小: {file_size} bytes")
        
        # 根据文件类型提取文本
        text_content = ""
        
        if file_ext == 'pdf':
            # PDF处理
            try:
                from PyPDF2 import PdfReader
                import io
                
                pdf_reader = PdfReader(io.BytesIO(content))
                text_content = "\n".join([page.extract_text() for page in pdf_reader.pages])
                
                if not text_content.strip():
                    return {
                        "status": "warning",
                        "message": "PDF文件已上传，但无法提取文本内容",
                        "filename": file.filename,
                        "note": "可能是扫描版PDF或加密文件"
                    }
                    
            except Exception as e:
                logger.error(f"PDF处理失败: {e}")
                raise HTTPException(status_code=500, detail=f"PDF处理失败: {str(e)}")
                
        else:
            # 文本文件处理
            try:
                text_content = content.decode('utf-8', errors='ignore')
            except:
                text_content = content.decode('latin-1', errors='ignore')
        
        # 创建文档对象
        from langchain.schema import Document
        
        doc = Document(
            page_content=text_content,
            metadata={
                "source": file.filename,
                "file_type": file_ext,
                "upload_time": datetime.now().isoformat(),
                "file_size": file_size
            }
        )
        
        # 添加到知识库
        result = knowledge_base.add_documents([doc])
        
        return {
            "status": "success",
            "message": "文档上传成功并已添加到知识库",
            "filename": file.filename,
            "file_size": file_size,
            "extracted_text_length": len(text_content),
            "chunks_added": result.get("added", 0)
        }
        
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"上传文档到知识库时出错: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"文档上传失败: {str(e)}")

@app.get("/kb/info")
async def kb_info():
    """获取知识库信息"""
    if not COMPONENTS_AVAILABLE:
        raise HTTPException(status_code=500, detail="财务分析组件未初始化")
    
    try:
        info = knowledge_base.get_info()
        return info
    except Exception as e:
        logger.error(f"获取知识库信息失败: {e}")
        return {"error": f"获取知识库信息失败: {str(e)}", "document_count": 0}

@app.get("/templates")
async def get_templates():
    """获取报告模板列表"""
    templates = [
        {"id": "comprehensive", "name": "综合财务分析报告"},
        {"id": "profitability", "name": "盈利能力分析报告"},
        {"id": "solvency", "name": "偿债能力分析报告"},
        {"id": "operating", "name": "运营能力分析报告"},
        {"id": "growth", "name": "发展能力分析报告"},
        {"id": "valuation", "name": "估值分析报告"}
    ]
    return {"templates": templates}

@app.post("/calculate-metrics")
async def calculate_metrics(data: Dict[str, Any]):
    """计算财务指标"""
    logger.info("计算财务指标请求")
    
    if not COMPONENTS_AVAILABLE:
        raise HTTPException(status_code=500, detail="财务分析组件未初始化")
    
    try:
        # 加载数据
        result = data_processor.load_manual_data(data)
        
        if result["status"] == "success":
            # 计算指标
            metrics = data_processor.calculate_all_metrics()
            
            return {
                "status": "success",
                "metrics": metrics,
                "data_summary": data_processor.get_data_summary()
            }
        else:
            return {
                "status": "error",
                "message": result["message"]
            }
            
    except Exception as e:
        logger.error(f"计算指标时出错: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"指标计算失败: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    
    # 启动服务器
    uvicorn.run(
        "finance_api_server:app",
        host="0.0.0.0",
        port=8004,
        reload=True,
        log_level="info"
    )