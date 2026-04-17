import os
import json
from typing import Dict, Optional, Any
import logging
from financial_knowledge_base import FinancialKnowledgeBase
from financial_data_processor import FinancialDataProcessor

logger = logging.getLogger(__name__)

class FinancialReportGenerator:
    def __init__(self):
        """Initialize financial report generator"""
        self.kb = FinancialKnowledgeBase()
        self.data_processor = FinancialDataProcessor()
        self.system_prompt = """You are a professional financial analyst. Please generate a detailed financial analysis report based on the provided financial data and analysis framework.

Analysis Framework:
1. Profitability Analysis (Gross Margin, Net Margin, ROE, ROA, etc.)
2. Solvency Analysis (Current Ratio, Quick Ratio, Debt-to-Asset Ratio, etc.)
3. Operating Efficiency Analysis (Accounts Receivable Turnover, Inventory Turnover, etc.)
4. Growth Capacity Analysis (Revenue Growth Rate, Net Profit Growth Rate, etc.)
5. Valuation Analysis (PE, PB, PS, etc.)

Please provide in-depth data analysis and professional insights."""
    
    def generate_report(self, financial_data: Dict, query: str, report_type: str = "comprehensive") -> Dict:
        """生成财务分析报告"""
        try:
            # 加载财务数据
            self.data_processor.load_manual_data(financial_data)
            
            # 计算财务指标
            metrics = self.data_processor.calculate_all_metrics()
            
            # 构建查询
            enhanced_query = self._build_enhanced_query(query, financial_data, metrics)
            
            # 检索相关知识
            context_docs = self.kb.search_similar(enhanced_query, k=5)
            
            # 构建上下文
            context_text = self._build_context(context_docs)
            
            # 根据报告类型生成报告
            if report_type == "comprehensive":
                report_content = self._generate_comprehensive_report(financial_data, metrics, context_text)
            elif report_type == "profitability":
                report_content = self._generate_profitability_report(financial_data, metrics, context_text)
            elif report_type == "solvency":
                report_content = self._generate_solvency_report(financial_data, metrics, context_text)
            elif report_type == "operating":
                report_content = self._generate_operating_report(financial_data, metrics, context_text)
            elif report_type == "growth":
                report_content = self._generate_growth_report(financial_data, metrics, context_text)
            elif report_type == "valuation":
                report_content = self._generate_valuation_report(financial_data, metrics, context_text)
            else:
                report_content = self._generate_comprehensive_report(financial_data, metrics, context_text)
            
            return {
                "report_content": report_content,
                "status": "success",
                "metrics": metrics,
                "data_quality": self.data_processor.get_data_summary()["data_quality"]
            }
            
        except Exception as e:
            logger.error(f"生成报告时出错: {e}")
            return {
                "report_content": f"报告生成失败: {str(e)}",
                "status": "error",
                "error": str(e)
            }
    
    def _build_enhanced_query(self, query: str, financial_data: Dict, metrics: Dict) -> str:
        """Build enhanced query"""
        query_parts = [query]
        
        # Add key financial data
        if 'revenue' in financial_data:
            query_parts.append(f"Revenue: {financial_data['revenue']}")
        if 'net_profit' in financial_data:
            query_parts.append(f"Net Profit: {financial_data['net_profit']}")
        
        # Add key metrics
        if 'profitability' in metrics and metrics['profitability']:
            profitability = metrics['profitability']
            if 'roe' in profitability:
                query_parts.append(f"ROE: {profitability['roe']}%")
            if 'net_margin' in profitability:
                query_parts.append(f"Net Margin: {profitability['net_margin']}%")
        
        return " ".join(query_parts)
    
    def _build_context(self, docs) -> str:
        """Build context"""
        context_text = ""
        for i, doc in enumerate(docs, 1):
            source = doc.metadata.get("source", "Unknown Source")
            context_text += f"[Knowledge {i} - {source}]: {doc.page_content}\n\n"
        return context_text
    
    def _generate_comprehensive_report(self, financial_data: Dict, metrics: Dict, context_text: str) -> str:
        """Generate comprehensive financial analysis report"""
        report = "# Comprehensive Financial Analysis Report\n\n"
        
        # Data Overview
        report += "## I. Data Overview\n"
        report += "### 1.1 Core Financial Data\n"
        report += f"- **Revenue**: {financial_data.get('revenue', 'N/A')}\n"
        report += f"- **Net Profit**: {financial_data.get('net_profit', 'N/A')}\n"
        report += f"- **Total Assets**: {financial_data.get('total_assets', 'N/A')}\n"
        report += f"- **Total Liabilities**: {financial_data.get('total_liabilities', 'N/A')}\n"
        report += f"- **Total Equity**: {financial_data.get('total_equity', 'N/A')}\n"
        report += f"- **Cost**: {financial_data.get('cost', 'N/A')}\n\n"
        
        # Profitability Analysis
        report += "## II. In-depth Profitability Analysis\n"
        profitability = metrics.get('profitability', {})
        
        if profitability:
            report += "### 2.1 Core Profitability Metrics\n"
            report += f"- **Gross Margin**: {profitability.get('gross_margin', 'N/A')}%\n"
            report += f"- **Net Margin**: {profitability.get('net_margin', 'N/A')}%\n"
            report += f"- **ROE (Return on Equity)**: {profitability.get('roe', 'N/A')}%\n"
            report += f"- **ROA (Return on Assets)**: {profitability.get('roa', 'N/A')}%\n\n"
            
            report += "### 2.2 Profitability Evaluation\n"
            roe = profitability.get('roe', 0)
            net_margin = profitability.get('net_margin', 0)
            gross_margin = profitability.get('gross_margin', 0)
            
            if roe > 15:
                report += "**ROE Analysis**: ROE exceeds 15%, indicating excellent profitability and strong ability to generate returns for shareholders. This typically means the company has strong competitive advantages and high operational efficiency.\n"
            elif roe > 10:
                report += "**ROE Analysis**: ROE is between 10%-15%, showing good profitability and stable returns for shareholders. The company's operational condition is healthy but still has room for improvement.\n"
            elif roe > 5:
                report += "**ROE Analysis**: ROE is between 5%-10%, indicating average profitability with room for improvement in shareholder returns. The company needs to focus on operational efficiency and cost control.\n"
            else:
                report += "**ROE Analysis**: ROE is below 5%, showing weak profitability and low shareholder returns. The company needs to analyze the reasons for profit decline and take effective measures to improve profitability.\n"
            
            if gross_margin > 30:
                report += "**Gross Margin Analysis**: Gross margin exceeds 30%, indicating strong pricing power and cost control capabilities, with certain competitive advantages in the market.\n"
            elif gross_margin > 20:
                report += "**Gross Margin Analysis**: Gross margin is between 20%-30%, showing good pricing power and cost control capabilities with certain market competitiveness.\n"
            elif gross_margin > 10:
                report += "**Gross Margin Analysis**: Gross margin is between 10%-20%, indicating average pricing power and cost control capabilities. Need to focus on cost structure optimization.\n"
            else:
                report += "**Gross Margin Analysis**: Gross margin is below 10%, showing weak pricing power and cost control issues. Need to focus on cost optimization and product structure adjustment.\n"
            
            if net_margin > 15:
                report += "**Net Margin Analysis**: Net margin exceeds 15%, indicating strong overall profitability and good period expense control, with high profit quality.\n"
            elif net_margin > 8:
                report += "**Net Margin Analysis**: Net margin is between 8%-15%, showing good overall profitability and reasonable period expense control.\n"
            elif net_margin > 3:
                report += "**Net Margin Analysis**: Net margin is between 3%-8%, indicating average overall profitability with room for improvement in period expense control.\n"
            else:
                report += "**Net Margin Analysis**: Net margin is below 3%, showing weak overall profitability and period expense control issues. Need to focus on expense management.\n"
        else:
            report += "- Insufficient data to calculate profitability metrics\n"
        report += "\n"
        
        # Solvency Analysis
        report += "## III. Comprehensive Solvency Assessment\n"
        solvency = metrics.get('solvency', {})
        
        if solvency:
            report += "### 3.1 Core Solvency Metrics\n"
            report += f"- **Current Ratio**: {solvency.get('current_ratio', 'N/A')}\n"
            report += f"- **Quick Ratio**: {solvency.get('quick_ratio', 'N/A')}\n"
            report += f"- **Debt-to-Asset Ratio**: {solvency.get('asset_liability_ratio', 'N/A')}%\n\n"
            
            report += "### 3.2 Short-term Solvency Analysis\n"
            current_ratio = solvency.get('current_ratio', 0)
            quick_ratio = solvency.get('quick_ratio', 0)
            
            if current_ratio > 2:
                report += "**Current Ratio Analysis**: Current ratio exceeds 2, indicating excellent short-term solvency. The company has sufficient current assets to cover current liabilities, with low short-term financial risk.\n"
            elif current_ratio > 1.5:
                report += "**Current Ratio Analysis**: Current ratio is between 1.5-2, showing good short-term solvency. Current assets can adequately cover current liabilities.\n"
            elif current_ratio > 1:
                report += "**Current Ratio Analysis**: Current ratio is between 1-1.5, indicating average short-term solvency. Need to monitor the quality and liquidity of current assets.\n"
            else:
                report += "**Current Ratio Analysis**: Current ratio is below 1, showing weak short-term solvency and potential liquidity risk. Need to focus on cash flow management.\n"
            
            if quick_ratio > 1.5:
                report += "**Quick Ratio Analysis**: Quick ratio exceeds 1.5, indicating excellent immediate solvency. The company has sufficient quick assets to meet short-term obligations.\n"
            elif quick_ratio > 1:
                report += "**Quick Ratio Analysis**: Quick ratio is between 1-1.5, showing good immediate solvency. Quick assets can adequately cover current liabilities.\n"
            elif quick_ratio > 0.7:
                report += "**Quick Ratio Analysis**: Quick ratio is between 0.7-1, indicating average immediate solvency. Need to monitor accounts receivable collection.\n"
            else:
                report += "**Quick Ratio Analysis**: Quick ratio is below 0.7, showing weak immediate solvency with significant short-term debt pressure.\n"
            
            report += "\n### 3.3 Long-term Solvency Analysis\n"
            debt_ratio = solvency.get('asset_liability_ratio', 100)
            
            if debt_ratio < 40:
                report += "**Debt-to-Asset Ratio Analysis**: Debt-to-asset ratio is below 40%, indicating excellent long-term solvency with a robust financial structure and low financial risk.\n"
            elif debt_ratio < 60:
                report += "**Debt-to-Asset Ratio Analysis**: Debt-to-asset ratio is between 40%-60%, showing good long-term solvency with a reasonably balanced financial structure.\n"
            elif debt_ratio < 75:
                report += "**Debt-to-Asset Ratio Analysis**: Debt-to-asset ratio is between 60%-75%, indicating average long-term solvency with relatively high financial leverage.\n"
            else:
                report += "**Debt-to-Asset Ratio Analysis**: Debt-to-asset ratio exceeds 75%, showing weak long-term solvency with high financial risk. Need to focus on debt structure optimization.\n"
        else:
            report += "- Insufficient data to calculate solvency metrics\n"
        report += "\n"
        
        # Operating Efficiency Analysis
        report += "## IV. In-depth Operating Efficiency Analysis\n"
        operating = metrics.get('operating', {})
        
        if operating:
            report += "### 4.1 Core Operating Metrics\n"
            report += f"- **Accounts Receivable Turnover**: {operating.get('accounts_receivable_turnover', 'N/A')}\n"
            report += f"- **Inventory Turnover**: {operating.get('inventory_turnover', 'N/A')}\n\n"
            
            report += "### 4.2 Accounts Receivable Management Analysis\n"
            ar_turnover = operating.get('accounts_receivable_turnover', 0)
            
            if ar_turnover > 10:
                report += "**Accounts Receivable Turnover Analysis**: Accounts receivable turnover exceeds 10, indicating excellent receivables management with fast collection and high capital efficiency.\n"
            elif ar_turnover > 6:
                report += "**Accounts Receivable Turnover Analysis**: Accounts receivable turnover is between 6-10, showing good receivables management with reasonably fast collection.\n"
            elif ar_turnover > 3:
                report += "**Accounts Receivable Turnover Analysis**: Accounts receivable turnover is between 3-6, indicating average receivables management with room for improvement in collection speed.\n"
            else:
                report += "**Accounts Receivable Turnover Analysis**: Accounts receivable turnover is below 3, showing weak receivables management with slow collection and potential bad debt risk.\n"
            
            report += "\n### 4.3 Inventory Management Analysis\n"
            inventory_turnover = operating.get('inventory_turnover', 0)
            
            if inventory_turnover > 12:
                report += "**Inventory Turnover Analysis**: Inventory turnover exceeds 12, indicating excellent inventory management with fast turnover and minimal capital occupation.\n"
            elif inventory_turnover > 8:
                report += "**Inventory Turnover Analysis**: Inventory turnover is between 8-12, showing good inventory management with reasonably fast turnover.\n"
            elif inventory_turnover > 4:
                report += "**Inventory Turnover Analysis**: Inventory turnover is between 4-8, indicating average inventory management with room for improvement in turnover speed.\n"
            else:
                report += "**Inventory Turnover Analysis**: Inventory turnover is below 4, showing weak inventory management with severe inventory backlog and high capital occupation.\n"
        else:
            report += "- Insufficient data to calculate operating efficiency metrics\n"
        report += "\n"
        
        # Growth Capacity Analysis
        report += "## V. Comprehensive Growth Capacity Assessment\n"
        growth = metrics.get('growth', {})
        
        if growth:
            report += "### 5.1 Core Growth Metrics\n"
            report += f"- **Revenue Growth Rate**: {growth.get('revenue_growth', 'N/A')}%\n"
            report += f"- **Net Profit Growth Rate**: {growth.get('net_profit_growth', 'N/A')}%\n\n"
            
            report += "### 5.2 Growth Quality Analysis\n"
            revenue_growth = growth.get('revenue_growth', 0)
            profit_growth = growth.get('net_profit_growth', 0)
            
            if revenue_growth > 25:
                report += "**Revenue Growth Analysis**: Revenue growth rate exceeds 25%, showing very fast growth. The company is in a high-speed development stage with strong market expansion capabilities.\n"
            elif revenue_growth > 15:
                report += "**Revenue Growth Analysis**: Revenue growth rate is between 15%-25%, showing fast growth with good development momentum.\n"
            elif revenue_growth > 8:
                report += "**Revenue Growth Analysis**: Revenue growth rate is between 8%-15%, showing moderate growth with stable development.\n"
            elif revenue_growth > 0:
                report += "**Revenue Growth Analysis**: Revenue growth rate is between 0%-8%, showing slow growth with insufficient development momentum.\n"
            else:
                report += "**Revenue Growth Analysis**: Revenue shows negative growth. The company faces development challenges and needs to analyze the reasons for decline and take countermeasures.\n"
            
            if profit_growth > revenue_growth + 10:
                report += "**Profit Growth Analysis**: Profit growth significantly outpaces revenue growth, indicating strong cost control capabilities, evident scale effects, and high profit quality.\n"
            elif profit_growth > revenue_growth + 3:
                report += "**Profit Growth Analysis**: Profit growth outpaces revenue growth, indicating good cost control and relatively high profit quality.\n"
            elif profit_growth > revenue_growth - 3:
                report += "**Profit Growth Analysis**: Profit growth basically matches revenue growth, indicating stable cost control.\n"
            else:
                report += "**Profit Growth Analysis**: Profit growth lags behind revenue growth, indicating cost control issues and room for improvement in profit quality.\n"
        else:
            report += "- Insufficient data to calculate growth capacity metrics\n"
        report += "\n"
        
        # Valuation Analysis
        report += "## VI. Comprehensive Valuation Analysis\n"
        valuation = metrics.get('valuation', {})
        
        if valuation:
            report += "### 6.1 Core Valuation Metrics\n"
            report += f"- **Price-to-Earnings Ratio (PE)**: {valuation.get('pe_ratio', 'N/A')}\n"
            report += f"- **Price-to-Book Ratio (PB)**: {valuation.get('pb_ratio', 'N/A')}\n"
            report += f"- **Price-to-Sales Ratio (PS)**: {valuation.get('ps_ratio', 'N/A')}\n\n"
            
            report += "### 6.2 Valuation Rationality Analysis\n"
            pe = valuation.get('pe_ratio', 0)
            pb = valuation.get('pb_ratio', 0)
            ps = valuation.get('ps_ratio', 0)
            
            if pe < 12:
                report += "**PE Ratio Analysis**: PE is below 12, indicating a relatively low valuation. There may be investment value, but company growth should be monitored.\n"
            elif pe < 25:
                report += "**PE Ratio Analysis**: PE is between 12-25, indicating a reasonable valuation that matches the company's fundamentals.\n"
            elif pe < 40:
                report += "**PE Ratio Analysis**: PE is between 25-40, indicating a relatively high valuation. Need to assess whether future growth can support current valuation.\n"
            else:
                report += "**PE Ratio Analysis**: PE exceeds 40, indicating a high valuation with potential valuation correction risk.\n"
            
            if pb < 1.5:
                report += "**PB Ratio Analysis**: PB is below 1.5, indicating low asset valuation with higher investment safety.\n"
            elif pb < 3:
                report += "**PB Ratio Analysis**: PB is between 1.5-3, indicating reasonable asset valuation that matches the company's asset quality.\n"
            elif pb < 5:
                report += "**PB Ratio Analysis**: PB is between 3-5, indicating relatively high asset valuation. Need to focus on asset quality and profitability.\n"
            else:
                report += "**PB Ratio Analysis**: PB exceeds 5, indicating high asset valuation with potential valuation risk.\n"
            
            if ps < 1:
                report += "**PS Ratio Analysis**: PS is below 1, indicating low revenue valuation. Suitable for focusing on the company's revenue growth potential.\n"
            elif ps < 3:
                report += "**PS Ratio Analysis**: PS is between 1-3, indicating reasonable revenue valuation that matches the company's revenue scale.\n"
            else:
                report += "**PS Ratio Analysis**: PS exceeds 3, indicating high revenue valuation. Need to monitor the sustainability of revenue growth.\n"
        else:
            report += "- Insufficient data to calculate valuation metrics\n"
        report += "\n"
        
        # Comprehensive Analysis and Strategic Recommendations
        report += "## VII. Comprehensive Analysis and Strategic Recommendations\n"
        report += "### 7.1 Comprehensive Evaluation\n"
        report += "Based on the multi-dimensional financial analysis above, we conduct a comprehensive evaluation of the company's overall financial condition:\n\n"
        
        # Profitability Evaluation
        if 'profitability' in metrics and metrics['profitability']:
            roe = metrics['profitability'].get('roe', 0)
            if roe > 15:
                report += "- **Profitability**: Excellent, with strong market competitiveness and profit level\n"
            elif roe > 10:
                report += "- **Profitability**: Good, with above-average industry profit level\n"
            elif roe > 5:
                report += "- **Profitability**: Average, with room for improvement\n"
            else:
                report += "- **Profitability**: Weak, requires focused attention on profit improvement\n"
        
        # Financial Health Evaluation
        if 'solvency' in metrics and metrics['solvency']:
            debt_ratio = metrics['solvency'].get('asset_liability_ratio', 100)
            current_ratio = metrics['solvency'].get('current_ratio', 0)
            
            if debt_ratio < 50 and current_ratio > 1.5:
                report += "- **Financial Health**: Excellent, with robust financial structure and strong solvency\n"
            elif debt_ratio < 70 and current_ratio > 1:
                report += "- **Financial Health**: Good, with reasonably balanced financial structure\n"
            else:
                report += "- **Financial Health**: Average, with certain financial risks\n"
        
        # Operating Efficiency Evaluation
        if 'operating' in metrics and metrics['operating']:
            ar_turnover = metrics['operating'].get('accounts_receivable_turnover', 0)
            inventory_turnover = metrics['operating'].get('inventory_turnover', 0)
            
            if ar_turnover > 8 and inventory_turnover > 8:
                report += "- **Operating Efficiency**: Excellent, with high asset utilization efficiency\n"
            elif ar_turnover > 4 and inventory_turnover > 4:
                report += "- **Operating Efficiency**: Good, with reasonably balanced asset utilization\n"
            else:
                report += "- **Operating Efficiency**: Average, with room for improvement in asset utilization\n"
        
        # Growth Potential Evaluation
        if 'growth' in metrics and metrics['growth']:
            revenue_growth = metrics['growth'].get('revenue_growth', 0)
            profit_growth = metrics['growth'].get('net_profit_growth', 0)
            
            if revenue_growth > 20 and profit_growth > revenue_growth:
                report += "- **Growth Potential**: Excellent, with strong growth momentum and high profit quality\n"
            elif revenue_growth > 10 and profit_growth > 0:
                report += "- **Growth Potential**: Good, with certain growth capabilities\n"
            elif revenue_growth > 0:
                report += "- **Growth Potential**: Average, with insufficient growth momentum\n"
            else:
                report += "- **Growth Potential**: Weak, facing growth bottlenecks\n"
        
        report += "\n### 7.2 Strategic Recommendations\n"
        
        # Profitability-based Recommendations
        if 'profitability' in metrics and metrics['profitability']:
            roe = metrics['profitability'].get('roe', 0)
            if roe < 10:
                report += "**Profit Improvement Recommendations**:\n"
                report += "- Optimize product structure, increase sales proportion of high-margin products\n"
                report += "- Strengthen cost control, reduce operating costs and period expenses\n"
                report += "- Improve asset utilization efficiency, optimize asset allocation\n"
                report += "- Enhance supply chain management, reduce procurement costs\n\n"
        
        # Solvency-based Recommendations
        if 'solvency' in metrics and metrics['solvency']:
            debt_ratio = metrics['solvency'].get('asset_liability_ratio', 100)
            current_ratio = metrics['solvency'].get('current_ratio', 0)
            
            if debt_ratio > 70 or current_ratio < 1:
                report += "**Financial Structure Optimization Recommendations**:\n"
                report += "- Optimize debt structure, reduce short-term debt proportion\n"
                report += "- Strengthen cash flow management, improve capital utilization efficiency\n"
                report += "- Consider equity financing, optimize capital structure\n"
                report += "- Establish comprehensive capital warning mechanism\n\n"
        
        # Operating Efficiency-based Recommendations
        if 'operating' in metrics and metrics['operating']:
            ar_turnover = metrics['operating'].get('accounts_receivable_turnover', 0)
            inventory_turnover = metrics['operating'].get('inventory_turnover', 0)
            
            if ar_turnover < 6 or inventory_turnover < 6:
                report += "**Operating Efficiency Improvement Recommendations**:\n"
                report += "- Optimize accounts receivable management, shorten collection cycle\n"
                report += "- Strengthen inventory management, reduce inventory backlog\n"
                report += "- Introduce advanced inventory management systems\n"
                report += "- Optimize supply chain, improve operational efficiency\n\n"
        
        # Growth Capacity-based Recommendations
        if 'growth' in metrics and metrics['growth']:
            revenue_growth = metrics['growth'].get('revenue_growth', 0)
            
            if revenue_growth < 10:
                report += "**Growth Momentum Enhancement Recommendations**:\n"
                report += "- Expand into new markets, identify new growth drivers\n"
                report += "- Strengthen product innovation, enhance product competitiveness\n"
                report += "- Optimize marketing strategies, increase market share\n"
                report += "- Consider mergers and acquisitions, achieve leapfrog development\n\n"
        
        # Valuation-based Recommendations
        if 'valuation' in metrics and metrics['valuation']:
            pe = metrics['valuation'].get('pe_ratio', 0)
            
            if pe > 30:
                report += "**Valuation Management Recommendations**:\n"
                report += "- Strengthen investor relations management, enhance market recognition\n"
                report += "- Improve information disclosure quality, enhance transparency\n"
                report += "- Monitor valuation rationality, avoid overvaluation\n"
                report += "- Strengthen performance management, ensure earnings growth supports valuation\n\n"
        
        report += "## VIII. Risk Warning and Risk Mitigation Strategies\n"
        report += "### 8.1 Key Risk Factors\n"
        
        # Financial Risk
        if 'solvency' in metrics and metrics['solvency']:
            debt_ratio = metrics['solvency'].get('asset_liability_ratio', 100)
            if debt_ratio > 70:
                report += "- **Financial Risk**: High debt-to-asset ratio, with financial pressure and debt repayment risks\n"
        
        # Profitability Risk
        if 'profitability' in metrics and metrics['profitability']:
            roe = metrics['profitability'].get('roe', 0)
            if roe < 5:
                report += "- **Profitability Risk**: Weak profitability, with potential profit decline risks\n"
        
        # Operational Risk
        if 'operating' in metrics and metrics['operating']:
            inventory_turnover = metrics['operating'].get('inventory_turnover', 0)
            if inventory_turnover < 4:
                report += "- **Operational Risk**: Slow inventory turnover, with potential inventory backlog risks\n"
        
        # Growth Risk
        if 'growth' in metrics and metrics['growth']:
            revenue_growth = metrics['growth'].get('revenue_growth', 0)
            if revenue_growth < 0:
                report += "- **Growth Risk**: Negative revenue growth, with potential market share decline risks\n"
        
        # Valuation Risk
        if 'valuation' in metrics and metrics['valuation']:
            pe = metrics['valuation'].get('pe_ratio', 0)
            if pe > 40:
                report += "- **Valuation Risk**: High valuation, with potential valuation correction risks\n"
        
        report += "\n### 8.2 Risk Mitigation Strategies\n"
        report += "- **Establish Risk Warning Mechanism**: Regularly monitor key financial indicators, promptly identify risk signals\n"
        report += "- **Optimize Financial Structure**: Reasonably control debt scale, optimize capital structure\n"
        report += "- **Strengthen Cash Flow Management**: Ensure stable cash flow, improve risk resistance capability\n"
        report += "- **Diversified Development**: Reduce dependence on single business, diversify risks\n"
        report += "- **Enhance Internal Control**: Establish sound internal control systems, prevent risks\n"
        
        report += "\n## IX. Conclusion\n"
        report += "Based on the above analysis, we believe the company's overall financial condition"
        
        # Provide comprehensive conclusion based on indicators
        has_excellent = False
        has_poor = False
        
        if 'profitability' in metrics and metrics['profitability']:
            if metrics['profitability'].get('roe', 0) > 15:
                has_excellent = True
            elif metrics['profitability'].get('roe', 0) < 5:
                has_poor = True
        
        if 'solvency' in metrics and metrics['solvency']:
            if metrics['solvency'].get('asset_liability_ratio', 100) < 50:
                has_excellent = True
            elif metrics['solvency'].get('asset_liability_ratio', 100) > 70:
                has_poor = True
        
        if 'growth' in metrics and metrics['growth']:
            if metrics['growth'].get('revenue_growth', 0) > 20:
                has_excellent = True
            elif metrics['growth'].get('revenue_growth', 0) < 0:
                has_poor = True
        
        if has_excellent and not has_poor:
            report += " is excellent, with strong profitability, robust financial structure, and good development potential. The company has strong competitiveness in the industry with optimistic future prospects."
        elif has_excellent or not has_poor:
            report += " is good, with relatively healthy overall financial condition but still has some areas for improvement. It is recommended that the company continues to optimize its financial structure, enhance operational efficiency, and strengthen development momentum."
        elif has_poor:
            report += " is average, with some obvious problems and risks. It is recommended that the company highly values the current issues and takes effective measures to improve financial condition, enhance profitability and operational efficiency."
        else:
            report += " requires further observation and analysis. It is recommended that the company strengthens financial management and enhances comprehensive competitiveness."
        
        report += "\n\n"
        report += "This report is based on the provided financial data for analysis and is for reference only. Actual investment decisions should consider multiple factors including the company's industry position, market environment, macroeconomic conditions, etc."
        
        return report
    
    def _generate_profitability_report(self, financial_data: Dict, metrics: Dict, context_text: str) -> str:
        """生成盈利能力分析报告"""
        report = "# 盈利能力深度分析报告\n\n"
        
        # 核心盈利指标
        report += "## 一、核心盈利指标概览\n"
        profitability = metrics.get('profitability', {})
        
        if profitability:
            report += "### 1.1 关键指标\n"
            report += f"- **毛利率**: {profitability.get('gross_margin', 'N/A')}%\n"
            report += f"- **净利率**: {profitability.get('net_margin', 'N/A')}%\n"
            report += f"- **ROE (净资产收益率)**: {profitability.get('roe', 'N/A')}%\n"
            report += f"- **ROA (总资产收益率)**: {profitability.get('roa', 'N/A')}%\n\n"
            
            # 盈利能力评分
            report += "### 1.2 盈利能力评分\n"
            score = 0
            
            roe = profitability.get('roe', 0)
            if roe > 15:
                score += 3
            elif roe > 10:
                score += 2
            elif roe > 5:
                score += 1
            
            net_margin = profitability.get('net_margin', 0)
            if net_margin > 15:
                score += 3
            elif net_margin > 8:
                score += 2
            elif net_margin > 3:
                score += 1
            
            gross_margin = profitability.get('gross_margin', 0)
            if gross_margin > 30:
                score += 3
            elif gross_margin > 20:
                score += 2
            elif gross_margin > 10:
                score += 1
            
            if score >= 7:
                report += f"**盈利能力评分**: {score}/9 - 优秀\n"
            elif score >= 5:
                report += f"**盈利能力评分**: {score}/9 - 良好\n"
            elif score >= 3:
                report += f"**盈利能力评分**: {score}/9 - 一般\n"
            else:
                report += f"**盈利能力评分**: {score}/9 - 较弱\n"
        else:
            report += "- 数据不足，无法计算盈利能力指标\n"
        report += "\n"
        
        # 盈利能力深度分析
        report += "## 二、盈利能力深度分析\n"
        
        if 'profitability' in metrics and metrics['profitability']:
            roe = metrics['profitability'].get('roe', 0)
            net_margin = metrics['profitability'].get('net_margin', 0)
            gross_margin = metrics['profitability'].get('gross_margin', 0)
            roa = metrics['profitability'].get('roa', 0)
            
            report += "### 2.1 ROE分析\n"
            if roe > 15:
                report += "**评估**: ROE超过15%，表明公司具有优秀的盈利能力，能够为股东创造较高的投资回报。这通常意味着公司在行业中具有较强的竞争优势，经营效率较高，产品定价能力强，成本控制良好。\n"
                report += "**优势**: 股东回报率高，投资吸引力强，公司价值创造能力突出。\n"
            elif roe > 10:
                report += "**评估**: ROE在10%-15%之间，盈利能力良好，能够为股东提供稳定的回报。公司的经营状况较为健康，但仍有提升空间。\n"
                report += "**优势**: 股东回报稳定，公司经营状况健康。\n"
            elif roe > 5:
                report += "**评估**: ROE在5%-10%之间，盈利能力一般，股东回报水平有待提升。公司需要关注经营效率的改善和成本控制。\n"
                report += "**挑战**: 股东回报水平不高，需要提升盈利能力。\n"
            else:
                report += "**评估**: ROE低于5%，盈利能力较弱，股东回报水平较低。公司需要深入分析盈利下滑的原因，采取有效措施提升盈利能力。\n"
                report += "**风险**: 股东回报水平低，可能影响投资者信心和公司估值。\n"
            
            report += "\n### 2.2 毛利率分析\n"
            if gross_margin > 30:
                report += "**评估**: 毛利率超过30%，表明公司产品具有较强的定价能力和成本控制能力，在市场上具有一定的竞争优势。\n"
                report += "**优势**: 产品附加值高，定价能力强，成本控制有效。\n"
            elif gross_margin > 20:
                report += "**评估**: 毛利率在20%-30%之间，产品定价能力和成本控制能力良好，具有一定的市场竞争力。\n"
                report += "**优势**: 产品具有一定的定价能力，成本控制较为合理。\n"
            elif gross_margin > 10:
                report += "**评估**: 毛利率在10%-20%之间，产品定价能力和成本控制能力一般，需要关注成本结构优化。\n"
                report += "**挑战**: 产品定价能力有限，成本控制有待改善。\n"
            else:
                report += "**评估**: 毛利率低于10%，产品定价能力较弱，成本控制存在问题，需要重点关注成本优化和产品结构调整。\n"
                report += "**风险**: 产品竞争力弱，成本控制不佳，盈利空间有限。\n"
            
            report += "\n### 2.3 净利率分析\n"
            if net_margin > 15:
                report += "**评估**: 净利率超过15%，表明公司整体盈利能力强，期间费用控制良好，具有较高的盈利质量。\n"
                report += "**优势**: 期间费用控制优秀，盈利质量高。\n"
            elif net_margin > 8:
                report += "**评估**: 净利率在8%-15%之间，整体盈利能力良好，期间费用控制较为合理。\n"
                report += "**优势**: 期间费用控制良好，盈利质量较高。\n"
            elif net_margin > 3:
                report += "**评估**: 净利率在3%-8%之间，整体盈利能力一般，期间费用控制有待改善。\n"
                report += "**挑战**: 期间费用控制有待提升，盈利质量一般。\n"
            else:
                report += "**评估**: 净利率低于3%，整体盈利能力较弱，期间费用控制存在问题，需要重点关注费用管理。\n"
                report += "**风险**: 期间费用过高，侵蚀利润，盈利质量差。\n"
            
            report += "\n### 2.4 ROA分析\n"
            if roa > 10:
                report += "**评估**: ROA超过10%，表明公司资产利用效率高，总资产盈利能力强。\n"
                report += "**优势**: 资产利用效率高，投资回报好。\n"
            elif roa > 5:
                report += "**评估**: ROA在5%-10%之间，资产利用效率良好，总资产盈利能力较为稳定。\n"
                report += "**优势**: 资产利用效率良好。\n"
            elif roa > 2:
                report += "**评估**: ROA在2%-5%之间，资产利用效率一般，总资产盈利能力有待提升。\n"
                report += "**挑战**: 资产利用效率有待提升。\n"
            else:
                report += "**评估**: ROA低于2%，资产利用效率较低，总资产盈利能力较弱。\n"
                report += "**风险**: 资产利用效率低，投资回报差。\n"
        
        report += "\n## 三、盈利驱动因素分析\n"
        
        if 'profitability' in metrics and metrics['profitability']:
            report += "### 3.1 盈利构成分析\n"
            report += "- **产品结构**: 分析不同产品的盈利贡献，识别高毛利产品\n"
            report += "- **客户结构**: 分析不同客户群体的盈利贡献\n"
            report += "- **区域结构**: 分析不同区域市场的盈利表现\n"
            report += "- **销售渠道**: 分析不同销售渠道的盈利贡献\n\n"
            
            report += "### 3.2 成本结构分析\n"
            report += "- **原材料成本**: 分析原材料价格波动对毛利率的影响\n"
            report += "- **人工成本**: 分析人工成本变化对盈利能力的影响\n"
            report += "- **制造费用**: 分析制造费用的合理性和控制效果\n"
            report += "- **期间费用**: 分析销售费用、管理费用、财务费用的合理性\n\n"
        
        report += "## 四、行业对比分析\n"
        report += "### 4.1 盈利能力行业对比\n"
        report += "- **毛利率对比**: 与行业平均水平对比，评估产品定价能力\n"
        report += "- **净利率对比**: 与行业平均水平对比，评估整体盈利能力\n"
        report += "- **ROE对比**: 与行业平均水平对比，评估股东回报水平\n"
        report += "- **盈利质量对比**: 与行业平均水平对比，评估盈利的可持续性\n\n"
        
        report += "## 五、盈利趋势分析\n"
        report += "### 5.1 历史趋势分析\n"
        report += "- **毛利率趋势**: 分析毛利率的历史变化趋势\n"
        report += "- **净利率趋势**: 分析净利率的历史变化趋势\n"
        report += "- **ROE趋势**: 分析ROE的历史变化趋势\n"
        report += "- **盈利波动性**: 分析盈利的稳定性和波动性\n\n"
        
        report += "## 六、改进建议与策略\n"
        
        if 'profitability' in metrics and metrics['profitability']:
            roe = metrics['profitability'].get('roe', 0)
            net_margin = metrics['profitability'].get('net_margin', 0)
            gross_margin = metrics['profitability'].get('gross_margin', 0)
            
            if roe < 10 or net_margin < 8 or gross_margin < 20:
                report += "### 6.1 短期改进建议\n"
                
                if gross_margin < 20:
                    report += "**产品策略优化**:\n"
                    report += "- 优化产品结构，提高高毛利产品的销售占比\n"
                    report += "- 加强产品创新，提升产品附加值\n"
                    report += "- 优化定价策略，提升产品定价能力\n"
                    report += "- 加强品牌建设，提升品牌溢价能力\n\n"
                
                if net_margin < 8:
                    report += "**成本费用控制**:\n"
                    report += "- 加强供应链管理，降低采购成本\n"
                    report += "- 优化生产流程，提高生产效率\n"
                    report += "- 控制期间费用，优化费用结构\n"
                    report += "- 加强成本核算，落实成本责任\n\n"
                
                if roe < 10:
                    report += "**资产利用效率提升**:\n"
                    report += "- 优化资产配置，提高资产利用效率\n"
                    report += "- 处置低效资产，盘活存量资产\n"
                    report += "- 优化资本结构，合理使用财务杠杆\n"
                    report += "- 加强投资管理，提高投资回报率\n\n"
            
            report += "### 6.2 长期战略建议\n"
            report += "**业务结构优化**:\n"
            report += "- 聚焦核心业务，提升核心竞争力\n"
            report += "- 发展高盈利业务，优化业务结构\n"
            report += "- 加强研发投入，提升产品竞争力\n"
            report += "- 拓展新业务领域，培育新的盈利增长点\n\n"
            
            report += "**运营模式创新**:\n"
            report += "- 探索新的商业模式，提升盈利能力\n"
            report += "- 加强数字化转型，提升运营效率\n"
            report += "- 优化客户结构，提升客户价值\n"
            report += "- 加强供应链协同，降低整体成本\n\n"
        
        report += "## 七、风险提示\n"
        report += "### 7.1 盈利风险因素\n"
        report += "- **市场竞争风险**: 市场竞争加剧可能导致毛利率下降\n"
        report += "- **成本上涨风险**: 原材料、人工等成本上涨可能侵蚀利润\n"
        report += "- **需求波动风险**: 市场需求波动可能影响营收和利润\n"
        report += "- **政策变化风险**: 政策变化可能影响公司盈利能力\n\n"
        
        report += "### 7.2 风险应对策略\n"
        report += "- **建立成本预警机制**: 密切监控成本变化，及时调整经营策略\n"
        report += "- **优化产品结构**: 降低对单一产品的依赖，分散风险\n"
        report += "- **加强客户管理**: 维护核心客户，提高客户忠诚度\n"
        report += "- **提升运营效率**: 通过数字化手段提升运营效率，降低成本\n\n"
        
        report += "## 八、结论\n"
        if 'profitability' in metrics and metrics['profitability']:
            roe = metrics['profitability'].get('roe', 0)
            
            if roe > 15:
                report += "综合以上分析，公司的盈利能力优秀，具有较强的市场竞争力和盈利水平。建议公司继续保持优势，进一步提升盈利质量和可持续性。"
            elif roe > 10:
                report += "综合以上分析，公司的盈利能力良好，经营状况较为健康。建议公司继续优化成本结构，提升运营效率，进一步增强盈利能力。"
            elif roe > 5:
                report += "综合以上分析，公司的盈利能力一般，存在一定的提升空间。建议公司重点关注成本控制和运营效率提升，采取有效措施改善盈利能力。"
            else:
                report += "综合以上分析，公司的盈利能力较弱，面临较大的挑战。建议公司高度重视盈利能力提升，制定切实可行的改进措施，改善盈利状况。"
        else:
            report += "由于数据不足，无法对盈利能力进行全面分析。建议公司完善财务数据，为盈利能力分析提供更多信息。"
        
        report += "\n\n"
        report += "本报告基于提供的财务数据进行分析，仅供参考。实际经营决策还需结合公司战略、市场环境等多方面因素综合考虑。"
        
        return report
    
    def _generate_solvency_report(self, financial_data: Dict, metrics: Dict, context_text: str) -> str:
        """生成偿债能力分析报告"""
        report = "# 偿债能力全面评估报告\n\n"
        
        # 核心偿债指标
        report += "## 一、核心偿债指标概览\n"
        solvency = metrics.get('solvency', {})
        
        if solvency:
            report += "### 1.1 关键指标\n"
            report += f"- **流动比率**: {solvency.get('current_ratio', 'N/A')}\n"
            report += f"- **速动比率**: {solvency.get('quick_ratio', 'N/A')}\n"
            report += f"- **资产负债率**: {solvency.get('asset_liability_ratio', 'N/A')}%\n\n"
            
            # 偿债能力评分
            report += "### 1.2 偿债能力评分\n"
            score = 0
            
            debt_ratio = solvency.get('asset_liability_ratio', 100)
            if debt_ratio < 40:
                score += 3
            elif debt_ratio < 60:
                score += 2
            elif debt_ratio < 75:
                score += 1
            
            current_ratio = solvency.get('current_ratio', 0)
            if current_ratio > 2:
                score += 3
            elif current_ratio > 1.5:
                score += 2
            elif current_ratio > 1:
                score += 1
            
            quick_ratio = solvency.get('quick_ratio', 0)
            if quick_ratio > 1.5:
                score += 3
            elif quick_ratio > 1:
                score += 2
            elif quick_ratio > 0.7:
                score += 1
            
            if score >= 7:
                report += f"**偿债能力评分**: {score}/9 - 优秀\n"
            elif score >= 5:
                report += f"**偿债能力评分**: {score}/9 - 良好\n"
            elif score >= 3:
                report += f"**偿债能力评分**: {score}/9 - 一般\n"
            else:
                report += f"**偿债能力评分**: {score}/9 - 较弱\n"
        else:
            report += "- 数据不足，无法计算偿债能力指标\n"
        report += "\n"
        
        # 短期偿债能力分析
        report += "## 二、短期偿债能力深度分析\n"
        
        if 'solvency' in metrics and metrics['solvency']:
            current_ratio = metrics['solvency'].get('current_ratio', 0)
            quick_ratio = metrics['solvency'].get('quick_ratio', 0)
            
            report += "### 2.1 流动比率分析\n"
            if current_ratio > 2:
                report += "**评估**: 流动比率超过2，短期偿债能力优秀，公司有足够的流动资产覆盖流动负债，短期财务风险较低。\n"
                report += "**优势**: 短期偿债能力强，流动性充足，抗风险能力强。\n"
            elif current_ratio > 1.5:
                report += "**评估**: 流动比率在1.5-2之间，短期偿债能力良好，流动资产能够较好地覆盖流动负债。\n"
                report += "**优势**: 短期偿债能力良好，流动性较为充足。\n"
            elif current_ratio > 1:
                report += "**评估**: 流动比率在1-1.5之间，短期偿债能力一般，需要关注流动资产的质量和变现能力。\n"
                report += "**挑战**: 短期偿债能力一般，需要关注流动资产质量。\n"
            else:
                report += "**评估**: 流动比率低于1，短期偿债能力较弱，存在短期流动性风险，需要关注现金流管理。\n"
                report += "**风险**: 短期偿债能力不足，可能面临流动性危机。\n"
            
            report += "\n### 2.2 速动比率分析\n"
            if quick_ratio > 1.5:
                report += "**评估**: 速动比率超过1.5，即时偿债能力优秀，公司有足够的速动资产应对短期债务。\n"
                report += "**优势**: 即时偿债能力强，无需依赖存货变现。\n"
            elif quick_ratio > 1:
                report += "**评估**: 速动比率在1-1.5之间，即时偿债能力良好，速动资产能够较好地覆盖流动负债。\n"
                report += "**优势**: 即时偿债能力良好。\n"
            elif quick_ratio > 0.7:
                report += "**评估**: 速动比率在0.7-1之间，即时偿债能力一般，需要关注应收账款的回收情况。\n"
                report += "**挑战**: 即时偿债能力一般，需要关注应收账款质量。\n"
            else:
                report += "**评估**: 速动比率低于0.7，即时偿债能力较弱，存在较大的短期偿债压力。\n"
                report += "**风险**: 即时偿债能力不足，可能面临短期债务违约风险。\n"
        
        report += "\n## 三、长期偿债能力深度分析\n"
        
        if 'solvency' in metrics and metrics['solvency']:
            debt_ratio = metrics['solvency'].get('asset_liability_ratio', 100)
            
            report += "### 3.1 资产负债率分析\n"
            if debt_ratio < 40:
                report += "**评估**: 资产负债率低于40%，长期偿债能力优秀，财务结构稳健，财务风险较低。\n"
                report += "**优势**: 财务结构稳健，财务风险低，融资能力强。\n"
            elif debt_ratio < 60:
                report += "**评估**: 资产负债率在40%-60%之间，长期偿债能力良好，财务结构较为合理。\n"
                report += "**优势**: 财务结构合理，财务杠杆使用适度。\n"
            elif debt_ratio < 75:
                report += "**评估**: 资产负债率在60%-75%之间，长期偿债能力一般，财务杠杆水平较高。\n"
                report += "**挑战**: 财务杠杆水平较高，财务风险有所增加。\n"
            else:
                report += "**评估**: 资产负债率超过75%，长期偿债能力较弱，财务风险较高，需要关注债务结构优化。\n"
                report += "**风险**: 财务风险高，可能面临债务违约风险，融资成本上升。\n"
        
        report += "\n## 四、债务结构分析\n"
        
        if 'solvency' in metrics and metrics['solvency']:
            report += "### 4.1 债务期限结构\n"
            report += "- **短期债务占比**: 分析短期债务占总债务的比例\n"
            report += "- **长期债务占比**: 分析长期债务占总债务的比例\n"
            report += "- **债务期限匹配**: 评估债务期限与资产期限的匹配程度\n"
            report += "- **再融资风险**: 评估短期债务集中到期带来的再融资压力\n\n"
            
            report += "### 4.2 债务类型结构\n"
            report += "- **银行贷款**: 分析银行贷款占总债务的比例\n"
            report += "- **债券融资**: 分析债券融资占总债务的比例\n"
            report += "- **应付账款**: 分析应付账款占总债务的比例\n"
            report += "- **其他债务**: 分析其他类型债务的构成\n\n"
        
        report += "## 五、现金流与偿债能力分析\n"
        report += "### 5.1 经营活动现金流分析\n"
        report += "- **经营现金流规模**: 评估经营活动产生的现金流量\n"
        report += "- **现金流稳定性**: 分析经营现金流的稳定性\n"
        report += "- **现金流覆盖能力**: 评估经营现金流对债务的覆盖能力\n"
        report += "- **现金流质量**: 分析经营现金流的质量和可持续性\n\n"
        
        report += "### 5.2 偿债保障比率\n"
        report += "- **利息保障倍数**: 评估利润对利息支出的保障程度\n"
        report += "- **现金流量利息保障倍数**: 评估经营现金流对利息支出的保障程度\n"
        report += "- **债务保障比率**: 评估经营现金流对债务的保障程度\n"
        report += "- **自由现金流**: 评估可用于偿还债务的自由现金流量\n\n"
        
        report += "## 六、行业对比分析\n"
        report += "### 6.1 偿债能力行业对比\n"
        report += "- **资产负债率对比**: 与行业平均水平对比，评估财务杠杆水平\n"
        report += "- **流动比率对比**: 与行业平均水平对比，评估短期偿债能力\n"
        report += "- **速动比率对比**: 与行业平均水平对比，评估即时偿债能力\n"
        report += "- **偿债能力排名**: 在行业中的偿债能力排名\n\n"
        
        report += "## 七、财务弹性分析\n"
        report += "### 7.1 融资能力评估\n"
        report += "- **银行授信额度**: 评估可用的银行授信额度\n"
        report += "- **债券发行能力**: 评估债券发行的可能性和成本\n"
        report += "- **股权融资能力**: 评估股权融资的可能性\n"
        report += "- **融资渠道多样性**: 评估融资渠道的多样性和稳定性\n\n"
        
        report += "### 7.2 资产变现能力\n"
        report += "- **流动资产变现能力**: 评估流动资产的变现速度和价值\n"
        report += "- **非流动资产变现能力**: 评估非流动资产的变现可能性\n"
        report += "- **资产流动性**: 评估整体资产的流动性水平\n"
        report += "- **资产质量**: 评估资产的质量和可变现性\n\n"
        
        report += "## 八、风险评估与应对策略\n"
        
        if 'solvency' in metrics and metrics['solvency']:
            debt_ratio = metrics['solvency'].get('asset_liability_ratio', 100)
            current_ratio = metrics['solvency'].get('current_ratio', 0)
            quick_ratio = metrics['solvency'].get('quick_ratio', 0)
            
            if debt_ratio > 70 or current_ratio < 1 or quick_ratio < 0.7:
                report += "### 8.1 主要风险因素\n"
                
                if debt_ratio > 70:
                    report += "**财务杠杆风险**:\n"
                    report += "- 资产负债率过高，财务风险大\n"
                    report += "- 利息支出负担重，影响盈利能力\n"
                    report += "- 债务到期集中，再融资压力大\n"
                    report += "- 融资成本上升，影响公司价值\n\n"
                
                if current_ratio < 1 or quick_ratio < 0.7:
                    report += "**流动性风险**:\n"
                    report += "- 短期偿债能力不足，可能面临流动性危机\n"
                    report += "- 现金流管理压力大\n"
                    report += "- 资产变现能力不足\n"
                    report += "- 供应商信用风险增加\n\n"
            
            report += "### 8.2 风险应对策略\n"
            
            if debt_ratio > 60:
                report += "**债务结构优化策略**:\n"
                report += "- 优化债务期限结构，降低短期债务比例\n"
                report += "- 提前偿还高成本债务，降低融资成本\n"
                report += "- 争取债务展期，缓解短期偿债压力\n"
                report += "- 考虑股权融资，优化资本结构\n\n"
            
            if current_ratio < 1.5 or quick_ratio < 1:
                report += "**流动性管理策略**:\n"
                report += "- 加强现金流预测和管理\n"
                report += "- 优化应收账款管理，加快回款速度\n"
                report += "- 控制存货水平，减少资金占用\n"
                report += "- 建立流动性储备，应对突发情况\n\n"
        
        report += "## 九、改进建议\n"
        
        if 'solvency' in metrics and metrics['solvency']:
            debt_ratio = metrics['solvency'].get('asset_liability_ratio', 100)
            current_ratio = metrics['solvency'].get('current_ratio', 0)
            
            if debt_ratio > 60:
                report += "### 9.1 长期财务结构优化建议\n"
                report += "- **优化资本结构**: 合理控制债务规模，降低资产负债率\n"
                report += "- **延长债务期限**: 将短期债务转换为长期债务，降低再融资风险\n"
                report += "- **优化债务类型**: 选择成本更低、期限更长的融资方式\n"
                report += "- **加强财务管理**: 建立健全财务管理制度，提高资金使用效率\n\n"
            
            if current_ratio < 1.5:
                report += "### 9.2 短期流动性改善建议\n"
                report += "- **优化营运资金管理**: 缩短应收账款周转天数，加快回款\n"
                report += "- **控制存货水平**: 优化库存管理，减少库存积压\n"
                report += "- **延长应付账款周期**: 在不影响供应商关系的前提下，合理延长付款周期\n"
                report += "- **建立现金储备**: 保持一定的现金储备，应对短期流动性需求\n\n"
        
        report += "## 十、结论\n"
        if 'solvency' in metrics and metrics['solvency']:
            debt_ratio = metrics['solvency'].get('asset_liability_ratio', 100)
            current_ratio = metrics['solvency'].get('current_ratio', 0)
            
            if debt_ratio < 50 and current_ratio > 1.5:
                report += "综合以上分析，公司的偿债能力优秀，财务结构稳健，流动性充足。建议公司继续保持良好的财务状况，合理使用财务杠杆，优化资本结构。"
            elif debt_ratio < 70 and current_ratio > 1:
                report += "综合以上分析，公司的偿债能力良好，财务结构较为合理。建议公司继续优化债务结构，加强现金流管理，进一步提升偿债能力。"
            elif debt_ratio < 75:
                report += "综合以上分析，公司的偿债能力一般，存在一定的财务风险。建议公司重点关注债务结构优化和流动性管理，采取有效措施改善偿债能力。"
            else:
                report += "综合以上分析，公司的偿债能力较弱，面临较大的财务风险。建议公司高度重视偿债能力改善，制定切实可行的财务优化方案，降低财务风险。"
        else:
            report += "由于数据不足，无法对偿债能力进行全面分析。建议公司完善财务数据，为偿债能力分析提供更多信息。"
        
        report += "\n\n"
        report += "本报告基于提供的财务数据进行分析，仅供参考。实际财务决策还需结合公司战略、市场环境等多方面因素综合考虑。"
        
        return report
    
    def _generate_operating_report(self, financial_data: Dict, metrics: Dict, context_text: str) -> str:
        """生成运营能力分析报告"""
        report = "# 运营能力深度剖析报告\n\n"
        
        # 核心运营指标
        report += "## 一、核心运营指标概览\n"
        operating = metrics.get('operating', {})
        
        if operating:
            report += "### 1.1 关键指标\n"
            report += f"- **应收账款周转率**: {operating.get('accounts_receivable_turnover', 'N/A')}\n"
            report += f"- **存货周转率**: {operating.get('inventory_turnover', 'N/A')}\n\n"
            
            # 运营能力评分
            report += "### 1.2 运营能力评分\n"
            score = 0
            
            ar_turnover = operating.get('accounts_receivable_turnover', 0)
            if ar_turnover > 10:
                score += 3
            elif ar_turnover > 6:
                score += 2
            elif ar_turnover > 3:
                score += 1
            
            inventory_turnover = operating.get('inventory_turnover', 0)
            if inventory_turnover > 12:
                score += 3
            elif inventory_turnover > 8:
                score += 2
            elif inventory_turnover > 4:
                score += 1
            
            if score >= 5:
                report += f"**运营能力评分**: {score}/6 - 优秀\n"
            elif score >= 3:
                report += f"**运营能力评分**: {score}/6 - 良好\n"
            elif score >= 2:
                report += f"**运营能力评分**: {score}/6 - 一般\n"
            else:
                report += f"**运营能力评分**: {score}/6 - 较弱\n"
        else:
            report += "- 数据不足，无法计算运营能力指标\n"
        report += "\n"
        
        # 应收账款管理分析
        report += "## 二、应收账款管理深度分析\n"
        
        if 'operating' in metrics and metrics['operating']:
            ar_turnover = metrics['operating'].get('accounts_receivable_turnover', 0)
            
            report += "### 2.1 应收账款周转率分析\n"
            if ar_turnover > 10:
                report += "**评估**: 应收账款周转率超过10，应收账款管理优秀，回款速度快，资金使用效率高。\n"
                report += "**优势**: 回款速度快，资金占用少，坏账风险低，资金使用效率高。\n"
            elif ar_turnover > 6:
                report += "**评估**: 应收账款周转率在6-10之间，应收账款管理良好，回款速度较为合理。\n"
                report += "**优势**: 回款速度较为合理，资金占用适中。\n"
            elif ar_turnover > 3:
                report += "**评估**: 应收账款周转率在3-6之间，应收账款管理一般，回款速度有待提升。\n"
                report += "**挑战**: 回款速度较慢，资金占用较多，坏账风险有所增加。\n"
            else:
                report += "**评估**: 应收账款周转率低于3，应收账款管理较弱，回款速度慢，存在坏账风险。\n"
                report += "**风险**: 回款速度慢，资金占用多，坏账风险高，影响资金周转。\n"
            
            report += "\n### 2.2 应收账款质量分析\n"
            report += "- **账龄分析**: 分析应收账款的账龄结构，识别逾期账款\n"
            report += "- **客户集中度**: 分析应收账款的客户分布，评估客户集中度风险\n"
            report += "- **坏账准备**: 评估坏账准备的充足性\n"
            report += "- **回款周期**: 计算平均回款天数，评估回款效率\n\n"
        
        # 存货管理分析
        report += "## 三、存货管理深度分析\n"
        
        if 'operating' in metrics and metrics['operating']:
            inventory_turnover = metrics['operating'].get('inventory_turnover', 0)
            
            report += "### 3.1 存货周转率分析\n"
            if inventory_turnover > 12:
                report += "**评估**: 存货周转率超过12，存货管理优秀，库存周转速度快，资金占用少。\n"
                report += "**优势**: 库存周转快，资金占用少，库存成本低，产品新鲜度高。\n"
            elif inventory_turnover > 8:
                report += "**评估**: 存货周转率在8-12之间，存货管理良好，库存周转速度较为合理。\n"
                report += "**优势**: 库存周转较为合理，资金占用适中。\n"
            elif inventory_turnover > 4:
                report += "**评估**: 存货周转率在4-8之间，存货管理一般，库存周转速度有待提升。\n"
                report += "**挑战**: 库存周转较慢，资金占用较多，库存成本较高。\n"
            else:
                report += "**评估**: 存货周转率低于4，存货管理较弱，库存积压严重，资金占用较多。\n"
                report += "**风险**: 库存积压严重，资金占用多，库存成本高，可能存在滞销风险。\n"
            
            report += "\n### 3.2 存货结构分析\n"
            report += "- **存货分类**: 分析原材料、在产品、产成品的结构\n"
            report += "- **库存水平**: 评估库存水平的合理性\n"
            report += "- **库存周转率**: 分析不同类别存货的周转情况\n"
            report += "- **库存成本**: 评估库存持有成本和缺货成本\n\n"
        
        report += "## 四、总资产运营效率分析\n"
        report += "### 4.1 总资产周转率分析\n"
        report += "- **总资产周转率**: 评估总资产的利用效率\n"
        report += "- **固定资产周转率**: 评估固定资产的利用效率\n"
        report += "- **流动资产周转率**: 评估流动资产的利用效率\n"
        report += "- **运营周期**: 计算从投入资金到收回资金的周期\n\n"
        
        report += "### 4.2 资产利用效率分析\n"
        report += "- **闲置资产**: 识别闲置或低效使用的资产\n"
        report += "- **资产配置**: 评估资产配置的合理性\n"
        report += "- **资产回报率**: 评估资产的回报率\n"
        report += "- **资产更新**: 评估资产更新和技术升级的必要性\n\n"
        
        report += "## 五、供应链管理分析\n"
        report += "### 5.1 供应链效率评估\n"
        report += "- **采购效率**: 评估采购流程的效率和成本\n"
        report += "- **供应商管理**: 评估供应商关系管理和供应链稳定性\n"
        report += "- **库存管理**: 评估库存管理策略的有效性\n"
        report += "- **物流效率**: 评估物流配送的效率和成本\n\n"
        
        report += "### 5.2 供应链风险评估\n"
        report += "- **供应链集中度**: 评估供应商集中度风险\n"
        report += "- **供应链中断风险**: 评估供应链中断的可能性和影响\n"
        report += "- **价格波动风险**: 评估原材料价格波动的风险\n"
        report += "- **供应链韧性**: 评估供应链的韧性和应对能力\n\n"
        
        report += "## 六、运营模式分析\n"
        report += "### 6.1 业务流程分析\n"
        report += "- **流程效率**: 评估核心业务流程的效率\n"
        report += "- **流程优化**: 识别流程优化的机会\n"
        report += "- **数字化程度**: 评估业务流程的数字化程度\n"
        report += "- **自动化水平**: 评估业务流程的自动化水平\n\n"
        
        report += "### 6.2 运营策略评估\n"
        report += "- **库存策略**: 评估库存管理策略的合理性\n"
        report += "- **信用政策**: 评估应收账款管理政策的合理性\n"
        report += "- **定价策略**: 评估产品定价策略的有效性\n"
        report += "- **营销策略**: 评估营销策略的效果和效率\n\n"
        
        report += "## 七、行业对比分析\n"
        report += "### 7.1 运营效率行业对比\n"
        report += "- **应收账款周转率对比**: 与行业平均水平对比\n"
        report += "- **存货周转率对比**: 与行业平均水平对比\n"
        report += "- **总资产周转率对比**: 与行业平均水平对比\n"
        report += "- **运营效率排名**: 在行业中的运营效率排名\n\n"
        
        report += "### 7.2 最佳实践借鉴\n"
        report += "- **行业标杆**: 分析行业内运营效率高的企业\n"
        report += "- **最佳实践**: 借鉴行业最佳实践\n"
        report += "- **差距分析**: 分析与行业标杆的差距\n"
        report += "- **改进方向**: 确定改进方向和重点\n\n"
        
        report += "## 八、改进建议与策略\n"
        
        if 'operating' in metrics and metrics['operating']:
            ar_turnover = metrics['operating'].get('accounts_receivable_turnover', 0)
            inventory_turnover = metrics['operating'].get('inventory_turnover', 0)
            
            if ar_turnover < 6 or inventory_turnover < 8:
                report += "### 8.1 短期改进建议\n"
                
                if ar_turnover < 6:
                    report += "**应收账款管理优化**:\n"
                    report += "- 优化信用政策，加强客户信用评估\n"
                    report += "- 建立应收账款跟踪系统，加强回款监控\n"
                    report += "- 实施应收账款保理或资产证券化\n"
                    report += "- 加强销售与财务部门的协作，提高回款效率\n\n"
                
                if inventory_turnover < 8:
                    report += "**存货管理优化**:\n"
                    report += "- 实施ABC分类管理，重点管理高价值存货\n"
                    report += "- 优化采购计划，减少库存积压\n"
                    report += "- 建立库存预警机制，及时处理滞销品\n"
                    report += "- 优化生产计划，减少在产品库存\n\n"
            
            report += "### 8.2 长期战略建议\n"
            report += "**运营模式创新**:\n"
            report += "- 推进数字化转型，提升运营效率\n"
            report += "- 实施精益管理，消除浪费\n"
            report += "- 优化供应链管理，提升供应链效率\n"
            report += "- 建立运营数据监控体系，持续优化运营效率\n\n"
            
            report += "**资产结构优化**:\n"
            report += "- 处置低效资产，盘活存量资产\n"
            report += "- 优化资产配置，提高资产利用效率\n"
            report += "- 加强固定资产管理，提高固定资产利用率\n"
            report += "- 优化流动资产结构，提高流动性\n\n"
        
        report += "## 九、风险提示\n"
        report += "### 9.1 运营风险因素\n"
        report += "- **应收账款风险**: 应收账款回款困难，坏账风险增加\n"
        report += "- **存货风险**: 库存积压，资金占用过多\n"
        report += "- **供应链风险**: 供应链中断，影响生产经营\n"
        report += "- **运营效率风险**: 运营效率低下，影响盈利能力\n\n"
        
        report += "### 9.2 风险应对策略\n"
        report += "- **建立风险预警机制**: 定期监控运营指标，及时发现风险信号\n"
        report += "- **优化信用管理**: 加强客户信用评估，降低坏账风险\n"
        report += "- **优化库存管理**: 实施精细化库存管理，减少库存积压\n"
        report += "- **加强供应链管理**: 建立供应链风险应对机制\n\n"
        
        report += "## 十、结论\n"
        if 'operating' in metrics and metrics['operating']:
            ar_turnover = metrics['operating'].get('accounts_receivable_turnover', 0)
            inventory_turnover = metrics['operating'].get('inventory_turnover', 0)
            
            if ar_turnover > 8 and inventory_turnover > 8:
                report += "综合以上分析，公司的运营能力优秀，资产利用效率高，运营管理水平良好。建议公司继续保持优势，进一步提升运营效率和管理水平。"
            elif ar_turnover > 4 and inventory_turnover > 4:
                report += "综合以上分析，公司的运营能力良好，资产利用效率较为合理。建议公司继续优化运营管理，进一步提升运营效率。"
            else:
                report += "综合以上分析，公司的运营能力一般，存在一定的提升空间。建议公司重点关注应收账款管理和存货管理，采取有效措施提升运营效率。"
        else:
            report += "由于数据不足，无法对运营能力进行全面分析。建议公司完善财务数据，为运营能力分析提供更多信息。"
        
        report += "\n\n"
        report += "本报告基于提供的财务数据进行分析，仅供参考。实际运营决策还需结合公司战略、市场环境等多方面因素综合考虑。"
        
        return report
    
    def _generate_growth_report(self, financial_data: Dict, metrics: Dict, context_text: str) -> str:
        """生成发展能力分析报告"""
        report = "# 发展能力全面评估报告\n\n"
        
        # 核心发展指标
        report += "## 一、核心发展指标概览\n"
        growth = metrics.get('growth', {})
        
        if growth:
            report += "### 1.1 关键指标\n"
            report += f"- **营收增长率**: {growth.get('revenue_growth', 'N/A')}%\n"
            report += f"- **净利润增长率**: {growth.get('net_profit_growth', 'N/A')}%\n\n"
            
            # 发展能力评分
            report += "### 1.2 发展能力评分\n"
            score = 0
            
            revenue_growth = growth.get('revenue_growth', 0)
            if revenue_growth > 25:
                score += 3
            elif revenue_growth > 15:
                score += 2
            elif revenue_growth > 8:
                score += 1
            
            profit_growth = growth.get('net_profit_growth', 0)
            if profit_growth > revenue_growth + 10:
                score += 3
            elif profit_growth > revenue_growth + 3:
                score += 2
            elif profit_growth > revenue_growth - 3:
                score += 1
            
            if score >= 5:
                report += f"**发展能力评分**: {score}/6 - 优秀\n"
            elif score >= 3:
                report += f"**发展能力评分**: {score}/6 - 良好\n"
            elif score >= 2:
                report += f"**发展能力评分**: {score}/6 - 一般\n"
            else:
                report += f"**发展能力评分**: {score}/6 - 较弱\n"
        else:
            report += "- 数据不足，无法计算发展能力指标\n"
        report += "\n"
        
        # 营收增长分析
        report += "## 二、营收增长深度分析\n"
        
        if 'growth' in metrics and metrics['growth']:
            revenue_growth = metrics['growth'].get('revenue_growth', 0)
            
            report += "### 2.1 营收增长率分析\n"
            if revenue_growth > 25:
                report += "**评估**: 营收增长率超过25%，增长速度非常快，公司处于高速发展阶段，市场扩张能力强。\n"
                report += "**优势**: 增长速度快，市场份额提升明显，发展潜力大。\n"
            elif revenue_growth > 15:
                report += "**评估**: 营收增长率在15%-25%之间，增长速度较快，公司发展势头良好。\n"
                report += "**优势**: 增长速度较快，发展势头良好。\n"
            elif revenue_growth > 8:
                report += "**评估**: 营收增长率在8%-15%之间，增长速度适中，公司发展较为稳定。\n"
                report += "**优势**: 增长速度适中，发展较为稳定。\n"
            elif revenue_growth > 0:
                report += "**评估**: 营收增长率在0%-8%之间，增长速度较慢，公司发展动力不足。\n"
                report += "**挑战**: 增长速度较慢，发展动力不足。\n"
            else:
                report += "**评估**: 营收出现负增长，公司发展面临挑战，需要分析下滑原因并采取应对措施。\n"
                report += "**风险**: 营收下滑，市场份额可能下降。\n"
            
            report += "\n### 2.2 营收增长质量分析\n"
            report += "- **增长可持续性**: 分析营收增长的可持续性\n"
            report += "- **增长来源**: 分析营收增长的主要来源\n"
            report += "- **增长质量**: 评估营收增长的质量和真实性\n"
            report += "- **增长波动性**: 分析营收增长的稳定性\n\n"
        
        # 利润增长分析
        report += "## 三、利润增长深度分析\n"
        
        if 'growth' in metrics and metrics['growth']:
            revenue_growth = metrics['growth'].get('revenue_growth', 0)
            profit_growth = metrics['growth'].get('net_profit_growth', 0)
            
            report += "### 3.1 利润增长率分析\n"
            if profit_growth > revenue_growth + 10:
                report += "**评估**: 利润增长显著快于营收增长，表明公司成本控制能力强，规模效应明显，盈利质量高。\n"
                report += "**优势**: 成本控制优秀，盈利质量高，规模效应明显。\n"
            elif profit_growth > revenue_growth + 3:
                report += "**评估**: 利润增长快于营收增长，表明公司成本控制良好，盈利质量较高。\n"
                report += "**优势**: 成本控制良好，盈利质量较高。\n"
            elif profit_growth > revenue_growth - 3:
                report += "**评估**: 利润增长与营收增长基本匹配，公司成本控制较为稳定。\n"
                report += "**优势**: 成本控制稳定，盈利质量一般。\n"
            else:
                report += "**评估**: 利润增长慢于营收增长，表明公司成本控制存在问题，盈利质量有待提升。\n"
                report += "**风险**: 成本控制不佳，盈利质量差。\n"
            
            report += "\n### 3.2 利润增长驱动因素分析\n"
            report += "- **成本控制**: 分析成本控制对利润增长的贡献\n"
            report += "- **产品结构**: 分析产品结构优化对利润增长的贡献\n"
            report += "- **价格策略**: 分析价格调整对利润增长的影响\n"
            report += "- **费用管理**: 分析期间费用控制对利润增长的影响\n\n"
        
        report += "## 四、增长动力分析\n"
        report += "### 4.1 市场拓展分析\n"
        report += "- **市场份额**: 分析市场份额的变化趋势\n"
        report += "- **新市场开拓**: 评估新市场开拓的成效\n"
        report += "- **客户增长**: 分析客户数量和质量的变化\n"
        report += "- **市场渗透率**: 评估市场渗透率的提升情况\n\n"
        
        report += "### 4.2 产品创新分析\n"
        report += "- **新产品贡献**: 分析新产品对营收增长的贡献\n"
        report += "- **产品升级**: 评估产品升级对增长的推动作用\n"
        report += "- **研发投入**: 分析研发投入与增长的关系\n"
        report += "- **技术创新**: 评估技术创新对增长的影响\n\n"
        
        report += "### 4.3 并购重组分析\n"
        report += "- **并购贡献**: 分析并购活动对增长的贡献\n"
        report += "- **整合效果**: 评估并购后的整合效果\n"
        report += "- **协同效应**: 分析并购带来的协同效应\n"
        report += "- **并购战略**: 评估并购战略的有效性\n\n"
        
        report += "## 五、行业对比分析\n"
        report += "### 5.1 增长速度行业对比\n"
        report += "- **营收增长率对比**: 与行业平均水平对比\n"
        report += "- **利润增长率对比**: 与行业平均水平对比\n"
        report += "- **增长排名**: 在行业中的增长排名\n"
        report += "- **增长潜力对比**: 与行业标杆企业对比\n\n"
        
        report += "### 5.2 增长模式对比\n"
        report += "- **内生增长**: 评估内生增长的贡献\n"
        report += "- **外延增长**: 评估外延增长的贡献\n"
        report += "- **增长模式**: 分析增长模式的合理性\n"
        report += "- **可持续性**: 评估增长模式的可持续性\n\n"
        
        report += "## 六、增长质量评估\n"
        report += "### 6.1 增长可持续性分析\n"
        report += "- **增长动力**: 分析增长的主要动力来源\n"
        report += "- **增长基础**: 评估增长的基础是否牢固\n"
        report += "- **增长风险**: 分析增长面临的风险\n"
        report += "- **增长韧性**: 评估增长的韧性和抗风险能力\n\n"
        
        report += "### 6.2 增长效率分析\n"
        report += "- **投入产出比**: 评估增长的投入产出效率\n"
        report += "- **资源利用**: 分析资源利用效率\n"
        report += "- **增长成本**: 评估增长的成本\n"
        report += "- **增长质量**: 评估增长的质量和效益\n\n"
        
        report += "## 七、发展战略分析\n"
        report += "### 7.1 发展战略评估\n"
        report += "- **战略定位**: 评估公司的战略定位\n"
        report += "- **战略执行**: 评估战略执行的效果\n"
        report += "- **战略调整**: 分析战略调整的必要性\n"
        report += "- **战略目标**: 评估战略目标的合理性\n\n"
        
        report += "### 7.2 竞争优势分析\n"
        report += "- **核心竞争力**: 分析公司的核心竞争力\n"
        report += "- **竞争优势**: 评估竞争优势的可持续性\n"
        report += "- **竞争地位**: 分析公司在行业中的竞争地位\n"
        report += "- **竞争策略**: 评估竞争策略的有效性\n\n"
        
        report += "## 八、风险评估\n"
        report += "### 8.1 增长风险因素\n"
        report += "- **增长放缓风险**: 增长速度可能放缓\n"
        report += "- **增长质量风险**: 增长质量不高\n"
        report += "- **市场风险**: 市场需求变化风险\n"
        report += "- **竞争风险**: 竞争加剧风险\n\n"
        
        report += "### 8.2 风险应对策略\n"
        report += "- **多元化发展**: 降低单一业务依赖\n"
        report += "- **创新驱动**: 加强创新能力建设\n"
        report += "- **风险管理**: 建立风险预警机制\n"
        report += "- **战略调整**: 适时调整发展战略\n\n"
        
        report += "## 九、改进建议与策略\n"
        
        if 'growth' in metrics and metrics['growth']:
            revenue_growth = metrics['growth'].get('revenue_growth', 0)
            profit_growth = metrics['growth'].get('net_profit_growth', 0)
            
            if revenue_growth < 15 or profit_growth < revenue_growth:
                report += "### 9.1 短期增长策略\n"
                
                if revenue_growth < 15:
                    report += "**市场拓展策略**:\n"
                    report += "- 拓展新市场，寻找新的增长点\n"
                    report += "- 加强市场营销，提高品牌知名度\n"
                    report += "- 优化销售渠道，提升销售效率\n"
                    report += "- 开发新客户，扩大客户群体\n\n"
                
                if profit_growth < revenue_growth:
                    report += "**成本优化策略**:\n"
                    report += "- 加强成本控制，降低运营成本\n"
                    report += "- 优化产品结构，提高高毛利产品占比\n"
                    report += "- 提升运营效率，降低期间费用\n"
                    report += "- 加强供应链管理，降低采购成本\n\n"
            
            report += "### 9.2 长期发展战略\n"
            report += "**创新驱动战略**:\n"
            report += "- 加强研发投入，提升创新能力\n"
            report += "- 开发新产品，培育新的增长点\n"
            report += "- 推进技术创新，提升核心竞争力\n"
            report += "- 建立创新激励机制，激发创新活力\n\n"
            
            report += "**战略转型策略**:\n"
            report += "- 优化业务结构，聚焦核心业务\n"
            report += "- 探索新的商业模式，提升增长潜力\n"
            report += "- 推进数字化转型，提升运营效率\n"
            report += "- 加强人才培养，提升组织能力\n\n"
        
        report += "## 十、结论\n"
        if 'growth' in metrics and metrics['growth']:
            revenue_growth = metrics['growth'].get('revenue_growth', 0)
            profit_growth = metrics['growth'].get('net_profit_growth', 0)
            
            if revenue_growth > 20 and profit_growth > revenue_growth:
                report += "综合以上分析，公司的发展能力优秀，具有较强的增长动力和良好的盈利质量。建议公司继续保持创新驱动，优化发展战略，实现可持续增长。"
            elif revenue_growth > 10 and profit_growth > 0:
                report += "综合以上分析，公司的发展能力良好，具备一定的增长能力。建议公司继续优化发展策略，提升增长质量和可持续性。"
            elif revenue_growth > 0:
                report += "综合以上分析，公司的发展能力一般，增长动力不足。建议公司重点关注增长动力提升，采取有效措施改善发展状况。"
            else:
                report += "综合以上分析，公司的发展能力较弱，面临增长瓶颈。建议公司高度重视发展能力提升，制定切实可行的发展战略，实现可持续增长。"
        else:
            report += "由于数据不足，无法对发展能力进行全面分析。建议公司完善财务数据，为发展能力分析提供更多信息。"
        
        report += "\n\n"
        report += "本报告基于提供的财务数据进行分析，仅供参考。实际发展决策还需结合公司战略、市场环境等多方面因素综合考虑。"
        
        return report
    
    def _generate_valuation_report(self, financial_data: Dict, metrics: Dict, context_text: str) -> str:
        """生成估值分析报告"""
        report = "# 估值水平综合分析报告\n\n"
        
        # 核心估值指标
        report += "## 一、核心估值指标概览\n"
        valuation = metrics.get('valuation', {})
        
        if valuation:
            report += "### 1.1 关键指标\n"
            report += f"- **市盈率 (PE)**: {valuation.get('pe_ratio', 'N/A')}\n"
            report += f"- **市净率 (PB)**: {valuation.get('pb_ratio', 'N/A')}\n"
            report += f"- **市销率 (PS)**: {valuation.get('ps_ratio', 'N/A')}\n\n"
            
            # 估值合理性评分
            report += "### 1.2 估值合理性评分\n"
            score = 0
            
            pe = valuation.get('pe_ratio', 0)
            if pe < 12:
                score += 3
            elif pe < 25:
                score += 2
            elif pe < 40:
                score += 1
            
            pb = valuation.get('pb_ratio', 0)
            if pb < 1.5:
                score += 3
            elif pb < 3:
                score += 2
            elif pb < 5:
                score += 1
            
            ps = valuation.get('ps_ratio', 0)
            if ps < 1:
                score += 3
            elif ps < 3:
                score += 2
            elif ps < 5:
                score += 1
            
            if score >= 7:
                report += f"**估值合理性评分**: {score}/9 - 低估\n"
            elif score >= 5:
                report += f"**估值合理性评分**: {score}/9 - 合理\n"
            elif score >= 3:
                report += f"**估值合理性评分**: {score}/9 - 偏高\n"
            else:
                report += f"**估值合理性评分**: {score}/9 - 高估\n"
        else:
            report += "- 数据不足，无法计算估值指标\n"
        report += "\n"
        
        # 市盈率分析
        report += "## 二、市盈率深度分析\n"
        
        if 'valuation' in metrics and metrics['valuation']:
            pe = metrics['valuation'].get('pe_ratio', 0)
            
            report += "### 2.1 市盈率水平分析\n"
            if pe < 12:
                report += "**评估**: PE低于12，估值处于较低水平，可能存在投资价值，但需要关注公司成长性。\n"
                report += "**优势**: 估值较低，安全边际较高，上涨空间较大。\n"
            elif pe < 25:
                report += "**评估**: PE在12-25之间，估值处于合理水平，与公司基本面较为匹配。\n"
                report += "**优势**: 估值合理，与基本面匹配，风险适中。\n"
            elif pe < 40:
                report += "**评估**: PE在25-40之间，估值处于较高水平，需要关注公司未来成长性是否支撑当前估值。\n"
                report += "**挑战**: 估值较高，需要较高的成长性支撑。\n"
            else:
                report += "**评估**: PE超过40，估值处于较高水平，存在估值回调风险。\n"
                report += "**风险**: 估值过高，存在回调风险，需要谨慎对待。\n"
            
            report += "\n### 2.2 市盈率影响因素分析\n"
            report += "- **盈利质量**: 分析盈利的质量和可持续性\n"
            report += "- **增长预期**: 评估市场对公司未来增长的预期\n"
            report += "- **行业特性**: 考虑行业特性对市盈率的影响\n"
            report += "- **市场情绪**: 分析市场情绪对市盈率的影响\n\n"
        
        # 市净率分析
        report += "## 三、市净率深度分析\n"
        
        if 'valuation' in metrics and metrics['valuation']:
            pb = metrics['valuation'].get('pb_ratio', 0)
            
            report += "### 3.1 市净率水平分析\n"
            if pb < 1.5:
                report += "**评估**: PB低于1.5，资产估值较低，投资安全性较高。\n"
                report += "**优势**: 资产估值低，安全边际高，投资风险小。\n"
            elif pb < 3:
                report += "**评估**: PB在1.5-3之间，资产估值合理，与公司资产质量较为匹配。\n"
                report += "**优势**: 资产估值合理，风险适中。\n"
            elif pb < 5:
                report += "**评估**: PB在3-5之间，资产估值较高，需要关注资产质量和盈利能力。\n"
                report += "**挑战**: 资产估值较高，需要关注资产质量。\n"
            else:
                report += "**评估**: PB超过5，资产估值较高，存在估值风险。\n"
                report += "**风险**: 资产估值过高，存在回调风险。\n"
            
            report += "\n### 3.2 市净率影响因素分析\n"
            report += "- **资产质量**: 评估资产的质量和盈利能力\n"
            report += "- **无形资产**: 考虑无形资产对估值的影响\n"
            report += "- **资产结构**: 分析资产结构对市净率的影响\n"
            report += "- **行业特性**: 考虑行业特性对市净率的影响\n\n"
        
        # 市销率分析
        report += "## 四、市销率深度分析\n"
        
        if 'valuation' in metrics and metrics['valuation']:
            ps = metrics['valuation'].get('ps_ratio', 0)
            
            report += "### 4.1 市销率水平分析\n"
            if ps < 1:
                report += "**评估**: PS低于1，营收估值较低，适合关注公司的营收增长潜力。\n"
                report += "**优势**: 营收估值低，适合关注成长股。\n"
            elif ps < 3:
                report += "**评估**: PS在1-3之间，营收估值合理，与公司营收规模较为匹配。\n"
                report += "**优势**: 营收估值合理，风险适中。\n"
            else:
                report += "**评估**: PS超过3，营收估值较高，需要关注营收增长的可持续性。\n"
                report += "**风险**: 营收估值过高，需要较高的营收增长支撑。\n"
            
            report += "\n### 4.2 市销率影响因素分析\n"
            report += "- **营收质量**: 分析营收的质量和可持续性\n"
            report += "- **增长潜力**: 评估营收增长的潜力\n"
            report += "- **行业特性**: 考虑行业特性对市销率的影响\n"
            report += "- **商业模式**: 分析商业模式对市销率的影响\n\n"
        
        report += "## 五、估值模型分析\n"
        report += "### 5.1 相对估值法分析\n"
        report += "- **市盈率法**: 基于市盈率的估值分析\n"
        report += "- **市净率法**: 基于市净率的估值分析\n"
        report += "- **市销率法**: 基于市销率的估值分析\n"
        report += "- **EV/EBITDA**: 基于企业价值与息税折旧摊销前利润的估值分析\n\n"
        
        report += "### 5.2 绝对估值法分析\n"
        report += "- **DCF模型**: 基于现金流折现模型的估值分析\n"
        report += "- **DDM模型**: 基于股息折现模型的估值分析\n"
        report += "- **剩余收益模型**: 基于剩余收益模型的估值分析\n"
        report += "- **经济增加值**: 基于经济增加值的估值分析\n\n"
        
        report += "## 六、行业对比分析\n"
        report += "### 6.1 估值水平行业对比\n"
        report += "- **市盈率对比**: 与行业平均市盈率对比\n"
        report += "- **市净率对比**: 与行业平均市净率对比\n"
        report += "- **市销率对比**: 与行业平均市销率对比\n"
        report += "- **估值排名**: 在行业中的估值排名\n\n"
        
        report += "### 6.2 估值溢价分析\n"
        report += "- **估值溢价**: 分析相对于行业平均估值的溢价或折价\n"
        report += "- **溢价原因**: 分析估值溢价的原因\n"
        report += "- **溢价合理性**: 评估估值溢价的合理性\n"
        report += "- **溢价可持续性**: 评估估值溢价的可持续性\n\n"
        
        report += "## 七、成长性与估值匹配分析\n"
        report += "### 7.1 PEG比率分析\n"
        report += "- **PEG比率**: 计算市盈率与增长率的比率\n"
        report += "- **PEG评估**: 评估PEG比率的合理性\n"
        report += "- **成长性验证**: 验证公司的成长性是否支撑当前估值\n"
        report += "- **增长可持续性**: 评估增长的可持续性\n\n"
        
        report += "### 7.2 估值与基本面匹配分析\n"
        report += "- **盈利能力匹配**: 评估盈利能力与估值的匹配度\n"
        report += "- **成长性匹配**: 评估成长性与估值的匹配度\n"
        report += "- **资产质量匹配**: 评估资产质量与估值的匹配度\n"
        report += "- **风险匹配**: 评估风险与估值的匹配度\n\n"
        
        report += "## 八、估值风险评估\n"
        report += "### 8.1 估值风险因素\n"
        report += "- **估值过高风险**: 当前估值过高，存在回调风险\n"
        report += "- **成长性不及预期风险**: 公司成长性不及市场预期\n"
        report += "- **盈利下滑风险**: 公司盈利能力下滑\n"
        report += "- **市场风格切换风险**: 市场风格切换导致估值调整\n\n"
        
        report += "### 8.2 风险应对策略\n"
        report += "- **分散投资**: 降低单一股票的风险\n"
        report += "- **关注基本面**: 密切关注公司基本面变化\n"
        report += "- **设置止损**: 设置合理的止损位\n"
        report += "- **定期评估**: 定期评估估值的合理性\n\n"
        
        report += "## 九、投资建议\n"
        
        if 'valuation' in metrics and metrics['valuation']:
            pe = metrics['valuation'].get('pe_ratio', 0)
            pb = metrics['valuation'].get('pb_ratio', 0)
            
            report += "### 9.1 投资策略建议\n"
            
            if pe < 15 and pb < 2:
                report += "**投资策略**: 价值投资策略\n"
                report += "- 估值较低，具有较高的安全边际\n"
                report += "- 适合长期持有，关注基本面改善\n"
                report += "- 分批建仓，降低短期波动风险\n"
                report += "- 关注催化剂事件，等待估值修复\n\n"
            
            elif pe < 25 and pb < 3:
                report += "**投资策略**: 均衡投资策略\n"
                report += "- 估值合理，与基本面匹配\n"
                report += "- 关注成长性，持有为主\n"
                report += "- 适量配置，控制仓位\n"
                report += "- 定期评估，动态调整\n\n"
            
            else:
                report += "**投资策略**: 谨慎投资策略\n"
                report += "- 估值较高，需要较高的成长性支撑\n"
                report += "- 控制仓位，避免重仓\n"
                report += "- 设置止损，防范风险\n"
                report += "- 关注催化剂事件，及时调整\n\n"
        
        report += "### 9.2 投资时机建议\n"
        report += "- **入场时机**: 选择合适的入场时机，避免追高\n"
        report += "- **仓位控制**: 根据估值水平控制仓位\n"
        report += "- **持有周期**: 根据公司成长性确定持有周期\n"
        report += "- **退出策略**: 制定明确的退出策略\n\n"
        
        report += "## 十、结论\n"
        if 'valuation' in metrics and metrics['valuation']:
            pe = metrics['valuation'].get('pe_ratio', 0)
            pb = metrics['valuation'].get('pb_ratio', 0)
            
            if pe < 15 and pb < 2:
                report += "综合以上分析，公司当前估值处于较低水平，具有较高的投资价值。建议采取价值投资策略，关注公司基本面改善，长期持有。"
            elif pe < 25 and pb < 3:
                report += "综合以上分析，公司当前估值处于合理水平，与基本面较为匹配。建议采取均衡投资策略，关注公司成长性，适量配置。"
            elif pe < 40 and pb < 5:
                report += "综合以上分析，公司当前估值处于较高水平，需要关注成长性是否支撑当前估值。建议采取谨慎投资策略，控制仓位，防范风险。"
            else:
                report += "综合以上分析，公司当前估值处于较高水平，存在回调风险。建议保持谨慎，控制仓位，密切关注公司基本面变化。"
        else:
            report += "由于数据不足，无法对估值进行全面分析。建议公司完善财务数据，为估值分析提供更多信息。"
        
        report += "\n\n"
        report += "本报告基于提供的财务数据进行分析，仅供参考。实际投资决策还需结合公司基本面、行业前景、宏观经济等多方面因素综合考虑。"
        
        return report