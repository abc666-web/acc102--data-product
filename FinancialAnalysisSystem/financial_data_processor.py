import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any
import json

class FinancialDataProcessor:
    def __init__(self):
        self.financial_data = {}
        self.metrics = {}
    
    def load_file(self, file_content, file_type):
        """加载财务数据文件"""
        try:
            if file_type == 'csv':
                df = pd.read_csv(file_content)
            elif file_type == 'xlsx':
                df = pd.read_excel(file_content)
            else:
                raise ValueError(f"不支持的文件类型: {file_type}")
            
            # 处理数据，提取财务指标
            self.financial_data = self._process_dataframe(df)
            return {"status": "success", "message": "文件加载成功"}
            
        except Exception as e:
            return {"status": "error", "message": f"文件加载失败: {str(e)}"}
    
    def load_manual_data(self, data: Dict):
        """加载手动输入的财务数据"""
        self.financial_data = data
        return {"status": "success", "message": "数据加载成功"}
    
    def _process_dataframe(self, df: pd.DataFrame) -> Dict:
        """处理数据框，提取财务指标"""
        result = {}
        
        # 尝试识别常见的财务指标列
        numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
        
        for col in numeric_columns:
            col_lower = col.lower()
            
            # 识别收入相关指标
            if any(keyword in col_lower for keyword in ['revenue', 'income', 'sales', '营收', '收入', '销售额']):
                value = df[col].iloc[-1] if len(df) > 0 else None
                result['revenue'] = float(value) if value is not None else None
            
            # 识别净利润相关指标
            elif any(keyword in col_lower for keyword in ['profit', 'net', '净利润', '利润']):
                value = df[col].iloc[-1] if len(df) > 0 else None
                result['net_profit'] = float(value) if value is not None else None
            
            # 识别总资产相关指标
            elif any(keyword in col_lower for keyword in ['asset', '总资产', '资产']):
                value = df[col].iloc[-1] if len(df) > 0 else None
                result['total_assets'] = float(value) if value is not None else None
            
            # 识别总负债相关指标
            elif any(keyword in col_lower for keyword in ['liability', 'debt', '总负债', '负债']):
                value = df[col].iloc[-1] if len(df) > 0 else None
                result['total_liabilities'] = float(value) if value is not None else None
            
            # 识别股东权益相关指标
            elif any(keyword in col_lower for keyword in ['equity', '股东权益', '净资产']):
                value = df[col].iloc[-1] if len(df) > 0 else None
                result['total_equity'] = float(value) if value is not None else None
            
            # 识别成本相关指标
            elif any(keyword in col_lower for keyword in ['cost', '成本']):
                value = df[col].iloc[-1] if len(df) > 0 else None
                result['cost'] = float(value) if value is not None else None
        
        return result
    
    def calculate_all_metrics(self) -> Dict:
        """计算所有财务指标"""
        metrics = {}
        
        # 盈利能力指标
        metrics['profitability'] = self._calculate_profitability()
        
        # 偿债能力指标
        metrics['solvency'] = self._calculate_solvency()
        
        # 运营能力指标
        metrics['operating'] = self._calculate_operating()
        
        # 发展能力指标
        metrics['growth'] = self._calculate_growth()
        
        # 估值指标
        metrics['valuation'] = self._calculate_valuation()
        
        self.metrics = metrics
        return metrics
    
    def _calculate_profitability(self) -> Dict:
        """计算盈利能力指标"""
        metrics = {}
        
        # 毛利率
        if 'revenue' in self.financial_data and 'cost' in self.financial_data:
            revenue = self.financial_data['revenue']
            cost = self.financial_data['cost']
            if revenue and revenue != 0:
                metrics['gross_margin'] = (revenue - cost) / revenue * 100
        
        # 净利率
        if 'revenue' in self.financial_data and 'net_profit' in self.financial_data:
            revenue = self.financial_data['revenue']
            net_profit = self.financial_data['net_profit']
            if revenue and revenue != 0:
                metrics['net_margin'] = net_profit / revenue * 100
        
        # 净资产收益率 (ROE)
        if 'net_profit' in self.financial_data and 'total_equity' in self.financial_data:
            net_profit = self.financial_data['net_profit']
            total_equity = self.financial_data['total_equity']
            if total_equity and total_equity != 0:
                metrics['roe'] = net_profit / total_equity * 100
        
        # 总资产收益率 (ROA)
        if 'net_profit' in self.financial_data and 'total_assets' in self.financial_data:
            net_profit = self.financial_data['net_profit']
            total_assets = self.financial_data['total_assets']
            if total_assets and total_assets != 0:
                metrics['roa'] = net_profit / total_assets * 100
        
        return metrics
    
    def _calculate_solvency(self) -> Dict:
        """计算偿债能力指标"""
        metrics = {}
        
        # 流动比率
        if 'current_assets' in self.financial_data and 'current_liabilities' in self.financial_data:
            current_assets = self.financial_data['current_assets']
            current_liabilities = self.financial_data['current_liabilities']
            if current_liabilities and current_liabilities != 0:
                metrics['current_ratio'] = current_assets / current_liabilities
        
        # 速动比率
        if 'quick_assets' in self.financial_data and 'current_liabilities' in self.financial_data:
            quick_assets = self.financial_data['quick_assets']
            current_liabilities = self.financial_data['current_liabilities']
            if current_liabilities and current_liabilities != 0:
                metrics['quick_ratio'] = quick_assets / current_liabilities
        
        # 资产负债率
        if 'total_assets' in self.financial_data and 'total_liabilities' in self.financial_data:
            total_assets = self.financial_data['total_assets']
            total_liabilities = self.financial_data['total_liabilities']
            if total_assets and total_assets != 0:
                metrics['asset_liability_ratio'] = total_liabilities / total_assets * 100
        
        return metrics
    
    def _calculate_operating(self) -> Dict:
        """计算运营能力指标"""
        metrics = {}
        
        # 应收账款周转率
        if 'revenue' in self.financial_data and 'accounts_receivable' in self.financial_data:
            revenue = self.financial_data['revenue']
            accounts_receivable = self.financial_data['accounts_receivable']
            if accounts_receivable and accounts_receivable != 0:
                metrics['accounts_receivable_turnover'] = revenue / accounts_receivable
        
        # 存货周转率
        if 'cost' in self.financial_data and 'inventory' in self.financial_data:
            cost = self.financial_data['cost']
            inventory = self.financial_data['inventory']
            if inventory and inventory != 0:
                metrics['inventory_turnover'] = cost / inventory
        
        return metrics
    
    def _calculate_growth(self) -> Dict:
        """计算发展能力指标"""
        metrics = {}
        
        # 营收增长率
        if 'revenue' in self.financial_data and 'previous_revenue' in self.financial_data:
            revenue = self.financial_data['revenue']
            previous_revenue = self.financial_data['previous_revenue']
            if previous_revenue and previous_revenue != 0:
                metrics['revenue_growth'] = (revenue - previous_revenue) / previous_revenue * 100
        
        # 净利润增长率
        if 'net_profit' in self.financial_data and 'previous_net_profit' in self.financial_data:
            net_profit = self.financial_data['net_profit']
            previous_net_profit = self.financial_data['previous_net_profit']
            if previous_net_profit and previous_net_profit != 0:
                metrics['net_profit_growth'] = (net_profit - previous_net_profit) / previous_net_profit * 100
        
        return metrics
    
    def _calculate_valuation(self) -> Dict:
        """计算估值指标"""
        metrics = {}
        
        # 市盈率 (PE)
        if 'market_cap' in self.financial_data and 'net_profit' in self.financial_data:
            market_cap = self.financial_data['market_cap']
            net_profit = self.financial_data['net_profit']
            if net_profit and net_profit != 0:
                metrics['pe_ratio'] = market_cap / net_profit
        
        # 市净率 (PB)
        if 'market_cap' in self.financial_data and 'total_equity' in self.financial_data:
            market_cap = self.financial_data['market_cap']
            total_equity = self.financial_data['total_equity']
            if total_equity and total_equity != 0:
                metrics['pb_ratio'] = market_cap / total_equity
        
        # 市销率 (PS)
        if 'market_cap' in self.financial_data and 'revenue' in self.financial_data:
            market_cap = self.financial_data['market_cap']
            revenue = self.financial_data['revenue']
            if revenue and revenue != 0:
                metrics['ps_ratio'] = market_cap / revenue
        
        return metrics
    
    def get_data_summary(self) -> Dict:
        """获取数据摘要"""
        return {
            "financial_data": self.financial_data,
            "metrics": self.metrics,
            "data_quality": self._assess_data_quality()
        }
    
    def _assess_data_quality(self) -> Dict:
        """评估数据质量"""
        quality = {
            "completeness": 0,
            "accuracy": 100,
            "missing_fields": []
        }
        
        required_fields = ['revenue', 'net_profit', 'total_assets', 'total_liabilities', 'total_equity']
        available_fields = [field for field in required_fields if field in self.financial_data and self.financial_data[field] is not None]
        
        quality['completeness'] = len(available_fields) / len(required_fields) * 100
        quality['missing_fields'] = [field for field in required_fields if field not in available_fields]
        
        return quality