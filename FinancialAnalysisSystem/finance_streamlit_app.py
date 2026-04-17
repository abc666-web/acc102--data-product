import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# API配置
API_BASE_URL = "http://localhost:8004"

# Page Configuration
st.set_page_config(
    page_title="Smart Financial Analysis System",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义样式
st.markdown("""
    <style>
    /* 导入Inter字体 */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* 全局样式 */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    
    /* 页面背景 - 浅色肌理感渐变 */
    body {
        background: 
            radial-gradient(circle at 20% 80%, rgba(42, 63, 95, 0.03) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(76, 175, 80, 0.03) 0%, transparent 50%),
            radial-gradient(circle at 40% 40%, rgba(255, 193, 7, 0.03) 0%, transparent 50%),
            linear-gradient(135deg, #F8F9FA 0%, #E9ECEF 50%, #F8F9FA 100%);
        min-height: 100vh;
        margin: 0;
        padding: 0;
        color: #2A3F5F;
        background-attachment: fixed;
    }
    
    /* Streamlit容器背景 - 透明以显示肌理感背景 */
    .stApp {
        background-color: transparent;
        padding: 2rem 0;
    }
    
    /* 主标题样式 */
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #2A3F5F;
        text-align: center;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.75rem;
    }
    
    .main-title::after {
        content: '';
        display: block;
        width: 60px;
        height: 3px;
        background-color: #2A3F5F;
        margin: 1rem auto 0;
        border-radius: 2px;
    }
    
    /* 副标题样式 */
    .sub-header {
        font-size: 1.75rem;
        font-weight: 600;
        color: #2A3F5F;
        margin-top: 2rem;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* 导航按钮样式 */
    .nav-button {
        background-color: white;
        color: #2A3F5F;
        border: 2px solid #E2E8F0;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .nav-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(42, 63, 95, 0.15);
        border-color: #2A3F5F;
    }
    
    .nav-button.active {
        background-color: #2A3F5F;
        color: white;
        border-color: #2A3F5F;
        box-shadow: 0 4px 12px rgba(42, 63, 95, 0.2);
    }
    
    /* 卡片样式 */
    .metric-card {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border: 1px solid #E2E8F0;
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.12);
    }
    
    /* 按钮样式 */
    .stButton>button {
        background-color: #2A3F5F;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 12px rgba(42, 63, 95, 0.2);
    }
    
    .stButton>button:hover {
        background-color: #1E2F49;
        transform: translateY(-1px);
        box-shadow: 0 6px 16px rgba(42, 63, 95, 0.3);
    }
    
    /* 表单样式 */
    .stTextInput>div>div>input,
    .stNumberInput>div>div>input,
    .stSelectbox>div>div>select {
        background-color: white;
        border-radius: 8px;
        border: 2px solid #E2E8F0;
        padding: 0.75rem 1rem;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        color: #2A3F5F;
    }
    
    .stTextInput>div>div>input:focus,
    .stNumberInput>div>div>input:focus,
    .stSelectbox>div>div>select:focus {
        border-color: #2A3F5F;
        box-shadow: 0 0 0 3px rgba(42, 63, 95, 0.1);
        outline: none;
    }
    
    /* 文件上传器样式 */
    .stFileUploader>div>div {
        background-color: white;
        border: 2px dashed #E2E8F0;
        border-radius: 16px;
        padding: 3rem;
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .stFileUploader>div>div:hover {
        border-color: #2A3F5F;
        background-color: #F8FAFC;
        border-style: solid;
    }
    
    /* 成功消息样式 */
    .stSuccess {
        background-color: #F0FDF4;
        border-left: 4px solid #4CAF50;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(76, 175, 80, 0.1);
    }
    
    /* 警告消息样式 */
    .stWarning {
        background-color: #FFFBEB;
        border-left: 4px solid #FFC107;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(255, 193, 7, 0.1);
    }
    
    /* 错误消息样式 */
    .stError {
        background-color: #FEF2F2;
        border-left: 4px solid #F44336;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(244, 67, 54, 0.1);
    }
    
    /* 信息框样式 */
    .stInfo {
        background-color: #EFF6FF;
        border-left: 4px solid #3B82F6;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.1);
    }
    
    /* 数据表格样式 */
    .stDataFrame {
        background-color: white;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border: 1px solid #E2E8F0;
    }
    
    /* 展开器样式 */
    [data-testid="stExpander"] {
        background-color: white;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border: 1px solid #E2E8F0;
    }
    
    [data-testid="stExpander"] > div:first-child {
        border-radius: 12px;
        padding: 1rem 1.5rem;
        background-color: white;
    }
    
    /* 加载状态样式 */
    .stSpinner {
        color: #2A3F5F;
    }
    
    /* 进度条样式 */
    .stProgress > div > div {
        background-color: #2A3F5F;
        border-radius: 4px;
    }
    
    /* 表格样式优化 */
    .dataframe {
        border-collapse: separate;
        border-spacing: 0;
        width: 100%;
    }
    
    .dataframe th {
        background-color: #2A3F5F;
        color: white;
        padding: 0.75rem 1rem;
        text-align: left;
        font-weight: 600;
    }
    
    .dataframe td {
        padding: 0.75rem 1rem;
        border-bottom: 1px solid #E2E8F0;
    }
    
    .dataframe tr:hover {
        background-color: #F8FAFC;
    }
    
    /* 响应式设计 */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2rem;
        }
        
        .nav-button {
            padding: 0.6rem 1rem;
            font-size: 0.85rem;
        }
        
        .metric-card {
            padding: 1.5rem;
        }
    }
    
    /* 滚动条样式 */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #F8F9FA;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #CBD5E1;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #94A3B8;
    }
    
    /* 输入框标签样式 */
    label {
        font-weight: 500;
        color: #2A3F5F;
        margin-bottom: 0.5rem;
        display: block;
    }
    
    /* 分组标题样式 */
    .group-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #2A3F5F;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #E2E8F0;
    }
    </style>
""", unsafe_allow_html=True)

# 全局变量
if "financial_data" not in st.session_state:
    st.session_state.financial_data = {}
    
if "metrics" not in st.session_state:
    st.session_state.metrics = {}
    
if "report_history" not in st.session_state:
    st.session_state.report_history = []

def main():
    """Main function"""
    # Page Title
    st.markdown('<h1 class="main-title">📊 Smart Financial Analysis System</h1>', unsafe_allow_html=True)
    
    # Initialize current page
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Data Input"
    
    # Create horizontal navigation bar - use column layout to ensure horizontal alignment
    col1, col2, col3, col4 = st.columns(4)
    
    # Navigation button configuration
    nav_buttons = [
        {"id": "Data Input", "icon": "💰", "label": "Data Input", "col": col1},
        {"id": "Metrics Analysis", "icon": "📈", "label": "Metrics Analysis", "col": col2},
        {"id": "Report Generation", "icon": "📋", "label": "Report Generation", "col": col3},
        {"id": "Knowledge Base", "icon": "📚", "label": "Knowledge Base", "col": col4}
    ]
    
    for btn in nav_buttons:
        with btn["col"]:
            if st.button(
                f"{btn['icon']} {btn['label']}",
                use_container_width=True,
                key=f"nav_{btn['id']}",
                on_click=lambda page=btn["id"]: setattr(st.session_state, "current_page", page)
            ):
                st.session_state.current_page = btn["id"]
    
    # 获取当前页面
    page = st.session_state.current_page
    
    # Page navigation
    if page == "Data Input":
        data_input_page()
    elif page == "Metrics Analysis":
        metrics_analysis_page()
    elif page == "Report Generation":
        report_generation_page()
    elif page == "Knowledge Base":
        knowledge_base_page()

def data_input_page():
    """Data Input Page"""
    st.markdown('<h2 class="sub-header">💰 Financial Data Input</h2>', unsafe_allow_html=True)
    
    # Create data input method selection card
    st.markdown('<div style="background: white; border-radius: 16px; padding: 2rem; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08); margin-bottom: 2rem;">', unsafe_allow_html=True)
    
    # Data input method selection
    st.markdown('<h4 style="color: #2A3F5F; font-weight: 600; margin-bottom: 1.5rem;">🔄 Select Data Input Method</h4>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        file_upload_btn = st.button(
            "📁 File Upload",
            use_container_width=True,
            key="file_upload_btn"
        )
    
    with col2:
        manual_input_btn = st.button(
            "✍️ Manual Input",
            use_container_width=True,
            key="manual_input_btn"
        )
    
    # Initialize input method state
    if "input_method" not in st.session_state:
        st.session_state.input_method = "File Upload"
    
    # Update input method
    if file_upload_btn:
        st.session_state.input_method = "File Upload"
    elif manual_input_btn:
        st.session_state.input_method = "Manual Input"
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Display corresponding input section based on selection
    if st.session_state.input_method == "File Upload":
        file_upload_section()
    else:
        manual_input_section()

def file_upload_section():
    """File Upload Section"""
    # Create file upload card
    st.markdown('<div style="background: white; border-radius: 16px; padding: 2rem; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);">', unsafe_allow_html=True)
    
    st.markdown('<h4 style="color: #2A3F5F; font-weight: 600; margin-bottom: 1.5rem;">📁 File Upload</h4>', unsafe_allow_html=True)
    
    # File upload instructions
    st.markdown('<div style="background: #EFF6FF; border-radius: 8px; padding: 1rem; margin-bottom: 1.5rem;">', unsafe_allow_html=True)
    st.markdown('<p style="color: #2A3F5F; margin: 0;">💡 <strong>Supported Formats</strong>: CSV, Excel (.xlsx)</p>', unsafe_allow_html=True)
    st.markdown('<p style="color: #2A3F5F; margin: 0;">📋 <strong>Recommended Fields</strong>: Revenue, Net Profit, Total Assets, Total Liabilities, Equity, etc.</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # File upload area
    uploaded_file = st.file_uploader(
        "",
        type=["csv", "xlsx"],
        label_visibility="collapsed",
        help="Drag and drop file here or click to upload"
    )
    
    if uploaded_file is not None:
        with st.spinner("🔄 Processing file..."):
            try:
                files = {"file": uploaded_file}
                response = requests.post(f"{API_BASE_URL}/upload", files=files)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # 成功消息
                    st.markdown(f"""
                        <div class="stSuccess">
                            <strong>✅ {result["message"]}</strong>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # 保存数据到会话状态
                    st.session_state.financial_data = result.get("data_summary", {}).get("financial_data", {})
                    st.session_state.metrics = result.get("metrics", {})
                    st.session_state.unit = result.get("unit", "Million")  # Save unit information
                    
                    # Display data overview
                    if st.session_state.financial_data:
                        st.markdown(f'<h4 style="color: #2A3F5F; font-weight: 600; margin-top: 2rem; margin-bottom: 1rem;">📊 Data Overview (Unit: {st.session_state.unit})</h4>', unsafe_allow_html=True)
                        
                        # 创建美观的数据表格
                        df = pd.DataFrame([st.session_state.financial_data])
                        st.dataframe(
                            df,
                            use_container_width=True,
                            hide_index=True
                        )
                
                else:
                    st.markdown(f"""
                        <div class="stError">
                            <strong>❌ 上传失败</strong>: {response.status_code} - {response.text}
                        </div>
                    """, unsafe_allow_html=True)
                    
            except Exception as e:
                st.markdown(f"""
                    <div class="stError">
                        <strong>❌ 上传失败</strong>: {str(e)}
                    </div>
                """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def manual_input_section():
    """Manual Input Section"""
    # Create manual input card
    st.markdown('<div style="background: white; border-radius: 16px; padding: 2rem; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);">', unsafe_allow_html=True)
    
    st.markdown('<h4 style="color: #2A3F5F; font-weight: 600; margin-bottom: 1.5rem;">✍️ Manual Financial Data Input</h4>', unsafe_allow_html=True)
    
    # Form instructions and unit selection
    st.markdown('<div style="background: #EFF6FF; border-radius: 8px; padding: 1rem; margin-bottom: 2rem;">', unsafe_allow_html=True)
    st.markdown('<p style="color: #2A3F5F; margin: 0;">💡 <strong>Note</strong>: Fields marked with * are required, other fields are optional</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Unit selection
    unit = st.selectbox(
        "Select data unit",
        ["CNY", "Million CNY"],
        index=1,  # Default to Million CNY
        help="Select the unit for input data"
    )
    
    # Create form
    with st.form("manual_input_form"):
        # Core financial data (required)
        st.markdown('<div class="group-title">🔍 Core Financial Data *</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            revenue = st.number_input("Revenue *", value=0.0, format="%.2f", key="revenue", help="Company's operating revenue")
            net_profit = st.number_input("Net Profit *", value=0.0, format="%.2f", key="net_profit", help="Company's net profit")
            total_assets = st.number_input("Total Assets *", value=0.0, format="%.2f", key="total_assets", help="Company's total assets")
            
        with col2:
            total_liabilities = st.number_input("Total Liabilities *", value=0.0, format="%.2f", key="total_liabilities", help="Company's total liabilities")
            total_equity = st.number_input("Equity *", value=0.0, format="%.2f", key="total_equity", help="Company's shareholders' equity")
            cost = st.number_input("Cost", value=0.0, format="%.2f", key="cost", help="Company's operating cost")
        
        # Optional fields
        st.markdown('<div class="group-title">📋 Operating Data (Optional)</div>', unsafe_allow_html=True)
        
        col3, col4 = st.columns(2)
        
        with col3:
            current_assets = st.number_input("Current Assets", value=0.0, format="%.2f", key="current_assets", help="Company's current assets")
            current_liabilities = st.number_input("Current Liabilities", value=0.0, format="%.2f", key="current_liabilities", help="Company's current liabilities")
            quick_assets = st.number_input("Quick Assets", value=0.0, format="%.2f", key="quick_assets", help="Company's quick assets")
            
        with col4:
            accounts_receivable = st.number_input("Accounts Receivable", value=0.0, format="%.2f", key="accounts_receivable", help="Company's accounts receivable")
            inventory = st.number_input("Inventory", value=0.0, format="%.2f", key="inventory", help="Company's inventory")
            market_cap = st.number_input("Market Cap", value=0.0, format="%.2f", key="market_cap", help="Company's market capitalization")
        
        # YoY data
        st.markdown('<div class="group-title">📈 Year-over-Year Data (Optional)</div>', unsafe_allow_html=True)
        
        col5, col6 = st.columns(2)
        
        with col5:
            previous_revenue = st.number_input("Previous Revenue", value=0.0, format="%.2f", key="previous_revenue", help="Previous period's revenue")
            previous_net_profit = st.number_input("Previous Net Profit", value=0.0, format="%.2f", key="previous_net_profit", help="Previous period's net profit")
        
        # Submit button
        st.markdown("<br>", unsafe_allow_html=True)
        col_center = st.columns([3, 2, 3])
        with col_center[1]:
            submitted = st.form_submit_button("📤 Submit Data", use_container_width=True)
        
        if submitted:
            # Validate required fields
            if revenue == 0 or net_profit == 0 or total_assets == 0 or total_liabilities == 0 or total_equity == 0:
                st.markdown("""
                    <div class="stError">
                        <strong>❌ Please fill in all required fields</strong>
                    </div>
                """, unsafe_allow_html=True)
            else:
                # 构建数据字典，包含单位信息
                financial_data = {
                    "revenue": revenue,
                    "net_profit": net_profit,
                    "total_assets": total_assets,
                    "total_liabilities": total_liabilities,
                    "total_equity": total_equity,
                    "cost": cost,
                    "current_assets": current_assets,
                    "current_liabilities": current_liabilities,
                    "quick_assets": quick_assets,
                    "accounts_receivable": accounts_receivable,
                    "inventory": inventory,
                    "market_cap": market_cap,
                    "previous_revenue": previous_revenue,
                    "previous_net_profit": previous_net_profit,
                    "unit": unit  # 添加单位信息
                }
                
                with st.spinner("🔄 Processing data..."):
                    try:
                        response = requests.post(
                            f"{API_BASE_URL}/upload-manual",
                            json=financial_data
                        )
                        
                        if response.status_code == 200:
                            result = response.json()
                            
                            st.markdown(f"""
                                <div class="stSuccess">
                                    <strong>✅ {result["message"]}</strong>
                                </div>
                            """, unsafe_allow_html=True)
                            
                            # 保存数据到会话状态
                            st.session_state.financial_data = financial_data
                            st.session_state.metrics = result.get("metrics", {})
                            st.session_state.unit = unit  # 保存单位信息
                            
                        else:
                            st.markdown(f"""
                                <div class="stError">
                                    <strong>❌ 数据提交失败</strong>: {response.status_code} - {response.text}
                                </div>
                            """, unsafe_allow_html=True)
                            
                    except Exception as e:
                        st.markdown(f"""
                            <div class="stError">
                                <strong>❌ 数据提交失败</strong>: {str(e)}
                            </div>
                        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def metrics_analysis_page():
    """Metrics Analysis Page"""
    st.markdown('<h2 class="sub-header">📈 Financial Metrics Analysis</h2>', unsafe_allow_html=True)
    
    # Check if data exists
    if not st.session_state.metrics:
        st.markdown("""
            <div class="stWarning">
                <strong>⚠️ Data Notice</strong>
                <p>Please input financial data in the 'Data Input' page first</p>
            </div>
        """, unsafe_allow_html=True)
        return
    
    # Display metrics overview
    st.markdown('<h4 style="color: #2A3F5F; font-weight: 600; margin-bottom: 2rem;">📊 Metrics Overview</h4>', unsafe_allow_html=True)
    
    # 创建指标卡片
    metrics = st.session_state.metrics
    
    # Profitability metrics
    if "profitability" in metrics and metrics["profitability"]:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown('<h4 style="color: #2A3F5F; font-weight: 600; margin-bottom: 1.5rem;">💹 Profitability</h4>', unsafe_allow_html=True)
        
        profit_metrics = metrics["profitability"]
        cols = st.columns(len(profit_metrics))
        
        for i, (key, value) in enumerate(profit_metrics.items()):
            with cols[i]:
                metric_name = {
                    "gross_margin": "Gross Margin",
                    "net_margin": "Net Margin",
                    "roe": "ROE",
                    "roa": "ROA"
                }.get(key, key)
                
                # Set color based on metric value
                if key == "roe":
                    if value > 15:
                        color = "#4CAF50"
                        status = "Excellent"
                    elif value > 10:
                        color = "#FFC107"
                        status = "Good"
                    else:
                        color = "#F44336"
                        status = "Weak"
                elif key in ["gross_margin", "net_margin"]:
                    if value > 20:
                        color = "#4CAF50"
                        status = "Excellent"
                    elif value > 10:
                        color = "#FFC107"
                        status = "Good"
                    else:
                        color = "#F44336"
                        status = "Weak"
                else:
                    color = "#2A3F5F"
                    status = ""
                
                st.markdown(f"""
                    <div style="text-align: center; padding: 1rem; border-radius: 8px; background-color: #F8FAFC;">
                        <p style="color: #2A3F5F; margin-bottom: 0.5rem; font-weight: 500;">{metric_name}</p>
                        <p style="font-size: 1.75rem; font-weight: 700; color: {color}; margin-bottom: 0.25rem;">{value:.2f}%</p>
                        <p style="font-size: 0.85rem; color: {color}; font-weight: 500;">{status}</p>
                    </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Solvency metrics
    if "solvency" in metrics and metrics["solvency"]:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown('<h4 style="color: #2A3F5F; font-weight: 600; margin-bottom: 1.5rem;">🛡️ Solvency</h4>', unsafe_allow_html=True)
        
        solvency_metrics = metrics["solvency"]
        cols = st.columns(len(solvency_metrics))
        
        for i, (key, value) in enumerate(solvency_metrics.items()):
            with cols[i]:
                metric_name = {
                    "current_ratio": "Current Ratio",
                    "quick_ratio": "Quick Ratio",
                    "asset_liability_ratio": "Debt-to-Asset Ratio"
                }.get(key, key)
                
                # Set color based on metric value
                if key == "current_ratio":
                    if value > 2:
                        color = "#4CAF50"
                        status = "Excellent"
                    elif value > 1:
                        color = "#FFC107"
                        status = "Good"
                    else:
                        color = "#F44336"
                        status = "Weak"
                elif key == "quick_ratio":
                    if value > 1:
                        color = "#4CAF50"
                        status = "Excellent"
                    elif value > 0.5:
                        color = "#FFC107"
                        status = "Good"
                    else:
                        color = "#F44336"
                        status = "Weak"
                elif key == "asset_liability_ratio":
                    if value < 50:
                        color = "#4CAF50"
                        status = "Excellent"
                    elif value < 70:
                        color = "#FFC107"
                        status = "Good"
                    else:
                        color = "#F44336"
                        status = "Weak"
                else:
                    color = "#2A3F5F"
                    status = ""
                
                unit = "%" if key == "asset_liability_ratio" else ""
                st.markdown(f"""
                    <div style="text-align: center; padding: 1rem; border-radius: 8px; background-color: #F8FAFC;">
                        <p style="color: #2A3F5F; margin-bottom: 0.5rem; font-weight: 500;">{metric_name}</p>
                        <p style="font-size: 1.75rem; font-weight: 700; color: {color}; margin-bottom: 0.25rem;">{value:.2f}{unit}</p>
                        <p style="font-size: 0.85rem; color: {color}; font-weight: 500;">{status}</p>
                    </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Operating efficiency metrics
    if "operating" in metrics and metrics["operating"]:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown('<h4 style="color: #2A3F5F; font-weight: 600; margin-bottom: 1.5rem;">⚡ Operating Efficiency</h4>', unsafe_allow_html=True)
        
        operating_metrics = metrics["operating"]
        cols = st.columns(len(operating_metrics))
        
        for i, (key, value) in enumerate(operating_metrics.items()):
            with cols[i]:
                metric_name = {
                    "accounts_receivable_turnover": "Accounts Receivable Turnover",
                    "inventory_turnover": "Inventory Turnover"
                }.get(key, key)
                
                # Set color based on metric value
                if key == "accounts_receivable_turnover":
                    if value > 8:
                        color = "#4CAF50"
                        status = "Excellent"
                    elif value > 5:
                        color = "#FFC107"
                        status = "Good"
                    else:
                        color = "#F44336"
                        status = "Weak"
                elif key == "inventory_turnover":
                    if value > 10:
                        color = "#4CAF50"
                        status = "Excellent"
                    elif value > 5:
                        color = "#FFC107"
                        status = "Good"
                    else:
                        color = "#F44336"
                        status = "Weak"
                else:
                    color = "#2A3F5F"
                    status = ""
                
                st.markdown(f"""
                    <div style="text-align: center; padding: 1rem; border-radius: 8px; background-color: #F8FAFC;">
                        <p style="color: #2A3F5F; margin-bottom: 0.5rem; font-weight: 500;">{metric_name}</p>
                        <p style="font-size: 1.75rem; font-weight: 700; color: {color}; margin-bottom: 0.25rem;">{value:.2f}</p>
                        <p style="font-size: 0.85rem; color: {color}; font-weight: 500;">{status}</p>
                    </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Growth metrics
    if "growth" in metrics and metrics["growth"]:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown('<h4 style="color: #2A3F5F; font-weight: 600; margin-bottom: 1.5rem;">📊 Growth Potential</h4>', unsafe_allow_html=True)
        
        growth_metrics = metrics["growth"]
        cols = st.columns(len(growth_metrics))
        
        for i, (key, value) in enumerate(growth_metrics.items()):
            with cols[i]:
                metric_name = {
                    "revenue_growth": "Revenue Growth",
                    "net_profit_growth": "Net Profit Growth"
                }.get(key, key)
                
                # Set color based on metric value
                if value > 20:
                    color = "#4CAF50"
                    status = "Excellent"
                elif value > 10:
                    color = "#FFC107"
                    status = "Good"
                elif value > 0:
                    color = "#3B82F6"
                    status = "Average"
                else:
                    color = "#F44336"
                    status = "Weak"
                
                st.markdown(f"""
                    <div style="text-align: center; padding: 1rem; border-radius: 8px; background-color: #F8FAFC;">
                        <p style="color: #2A3F5F; margin-bottom: 0.5rem; font-weight: 500;">{metric_name}</p>
                        <p style="font-size: 1.75rem; font-weight: 700; color: {color}; margin-bottom: 0.25rem;">{value:.2f}%</p>
                        <p style="font-size: 0.85rem; color: {color}; font-weight: 500;">{status}</p>
                    </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Valuation metrics
    if "valuation" in metrics and metrics["valuation"]:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown('<h4 style="color: #2A3F5F; font-weight: 600; margin-bottom: 1.5rem;">💰 Valuation Metrics</h4>', unsafe_allow_html=True)
        
        valuation_metrics = metrics["valuation"]
        cols = st.columns(len(valuation_metrics))
        
        for i, (key, value) in enumerate(valuation_metrics.items()):
            with cols[i]:
                metric_name = {
                    "pe_ratio": "P/E Ratio",
                    "pb_ratio": "P/B Ratio",
                    "ps_ratio": "P/S Ratio"
                }.get(key, key)
                
                # Set color based on metric value
                if key == "pe_ratio":
                    if value < 15:
                        color = "#4CAF50"
                        status = "Undervalued"
                    elif value < 30:
                        color = "#FFC107"
                        status = "Fair Value"
                    else:
                        color = "#F44336"
                        status = "Overvalued"
                elif key == "pb_ratio":
                    if value < 2:
                        color = "#4CAF50"
                        status = "Undervalued"
                    elif value < 5:
                        color = "#FFC107"
                        status = "Fair Value"
                    else:
                        color = "#F44336"
                        status = "Overvalued"
                else:
                    color = "#2A3F5F"
                    status = ""
                
                st.markdown(f"""
                    <div style="text-align: center; padding: 1rem; border-radius: 8px; background-color: #F8FAFC;">
                        <p style="color: #2A3F5F; margin-bottom: 0.5rem; font-weight: 500;">{metric_name}</p>
                        <p style="font-size: 1.75rem; font-weight: 700; color: {color}; margin-bottom: 0.25rem;">{value:.2f}</p>
                        <p style="font-size: 0.85rem; color: {color}; font-weight: 500;">{status}</p>
                    </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Visualization charts
    st.markdown('<h4 style="color: #2A3F5F; font-weight: 600; margin-top: 2rem; margin-bottom: 1.5rem;">📉 Metrics Visualization</h4>', unsafe_allow_html=True)
    
    # 创建雷达图
    if metrics:
        radar_data = []
        categories = []
        
        # 收集指标数据
        if "profitability" in metrics:
            profit = metrics["profitability"]
            if "roe" in profit:
                radar_data.append(profit["roe"])
                categories.append("ROE")
            if "net_margin" in profit:
                radar_data.append(profit["net_margin"])
                categories.append("Net Margin")
    
        if "solvency" in metrics:
            solvency = metrics["solvency"]
            if "asset_liability_ratio" in solvency:
                # Debt-to-asset ratio needs reverse processing (lower is better)
                radar_data.append(100 - solvency["asset_liability_ratio"])
                categories.append("Solvency")
    
        if "growth" in metrics:
            growth = metrics["growth"]
            if "revenue_growth" in growth:
                radar_data.append(growth["revenue_growth"])
                categories.append("Revenue Growth")
    
        # 如果没有数据，使用默认值
        if not radar_data:
            # 添加默认数据以确保雷达图显示
            radar_data = [50, 50, 50]
            categories = ["ROE", "Solvency", "Growth"]
    
        if radar_data and categories:
            # 创建美观的雷达图
            fig = go.Figure(data=go.Scatterpolar(
                r=radar_data,
                theta=categories,
                fill='toself',
                line=dict(color='#2A3F5F', width=2),
                fillcolor='rgba(42, 63, 95, 0.15)',
                marker=dict(color='#2A3F5F', size=6)
            ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, max(radar_data) * 1.2],
                        gridcolor='#E2E8F0',
                        gridwidth=1,
                        tickfont=dict(color='#2A3F5F', size=10)
                    ),
                    angularaxis=dict(
                        gridcolor='#E2E8F0',
                        gridwidth=1,
                        tickfont=dict(color='#2A3F5F', size=11)
                    ),
                    bgcolor='#FFFFFF'
                ),
                showlegend=False,
                title={
                    'text': 'Financial Metrics Radar Chart',
                    'font': {'size': 18, 'color': '#2A3F5F'},
                    'x': 0.5,
                    'y': 0.95
                },
                paper_bgcolor='white',
                plot_bgcolor='white',
                height=450,
                margin=dict(l=50, r=50, t=80, b=50)
            )
            
            # 创建图表容器
            st.markdown('<div style="background: white; border-radius: 16px; padding: 2rem; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);">', unsafe_allow_html=True)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Add financial metrics bar chart
        st.markdown('<h4 style="color: #2A3F5F; font-weight: 600; margin-top: 2rem; margin-bottom: 1.5rem;">📊 Financial Metrics Comparison</h4>', unsafe_allow_html=True)
        
        # 准备柱状图数据
        bar_data = []
        bar_labels = []
        
        # Profitability metrics
        if "profitability" in metrics:
            profit = metrics["profitability"]
            if "roe" in profit:
                bar_data.append(profit["roe"])
                bar_labels.append("ROE")
            if "net_margin" in profit:
                bar_data.append(profit["net_margin"])
                bar_labels.append("Net Margin")
        
        # Solvency metrics
        if "solvency" in metrics:
            solvency = metrics["solvency"]
            if "asset_liability_ratio" in solvency:
                # Reverse debt-to-asset ratio for comparison
                bar_data.append(100 - solvency["asset_liability_ratio"])
                bar_labels.append("Solvency")
        
        # Growth metrics
        if "growth" in metrics:
            growth = metrics["growth"]
            if "revenue_growth" in growth:
                bar_data.append(growth["revenue_growth"])
                bar_labels.append("Revenue Growth")
        
        if bar_data:
            # 创建柱状图
            bar_fig = go.Figure(data=go.Bar(
                x=bar_labels,
                y=bar_data,
                marker=dict(color=['#4CAF50', '#2A3F5F', '#FFC107', '#3B82F6'][:len(bar_data)]),
                text=[f'{val:.2f}%' for val in bar_data],
                textposition='auto'
            ))
            
            bar_fig.update_layout(
                title={
                    'text': 'Core Financial Metrics Comparison',
                    'font': {'size': 16, 'color': '#2A3F5F'},
                    'x': 0.5,
                    'y': 0.95
                },
                xaxis=dict(
                    title='Metric Name',
                    tickfont=dict(color='#2A3F5F', size=11),
                    gridcolor='#E2E8F0'
                ),
                yaxis=dict(
                    title='Metric Value (%)',
                    tickfont=dict(color='#2A3F5F', size=11),
                    gridcolor='#E2E8F0'
                ),
                paper_bgcolor='white',
                plot_bgcolor='white',
                height=400,
                margin=dict(l=50, r=50, t=80, b=50)
            )
            
            # 创建图表容器
            st.markdown('<div style="background: white; border-radius: 16px; padding: 2rem; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);">', unsafe_allow_html=True)
            st.plotly_chart(bar_fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Add metrics score chart
        st.markdown('<h4 style="color: #2A3F5F; font-weight: 600; margin-top: 2rem; margin-bottom: 1.5rem;">📈 Metrics Score Analysis</h4>', unsafe_allow_html=True)
        
        # 准备评分数据
        scores = []
        score_labels = []
        
        # Profitability score
        if "profitability" in metrics:
            profit = metrics["profitability"]
            roe = profit.get("roe", 0)
            if roe > 15:
                scores.append(95)
            elif roe > 10:
                scores.append(85)
            elif roe > 5:
                scores.append(70)
            else:
                scores.append(50)
            score_labels.append("Profitability")
        
        # Solvency score
        if "solvency" in metrics:
            solvency = metrics["solvency"]
            debt_ratio = solvency.get("asset_liability_ratio", 100)
            if debt_ratio < 50:
                scores.append(90)
            elif debt_ratio < 70:
                scores.append(75)
            else:
                scores.append(60)
            score_labels.append("Solvency")
        
        # Operating efficiency score
        if "operating" in metrics:
            operating = metrics["operating"]
            inventory_turnover = operating.get("inventory_turnover", 0)
            if inventory_turnover > 10:
                scores.append(90)
            elif inventory_turnover > 5:
                scores.append(75)
            else:
                scores.append(60)
            score_labels.append("Operating Efficiency")
        
        # Growth potential score
        if "growth" in metrics:
            growth = metrics["growth"]
            revenue_growth = growth.get("revenue_growth", 0)
            if revenue_growth > 20:
                scores.append(95)
            elif revenue_growth > 10:
                scores.append(80)
            elif revenue_growth > 0:
                scores.append(65)
            else:
                scores.append(50)
            score_labels.append("Growth Potential")
        
        if scores:
            # 创建评分雷达图
            score_fig = go.Figure(data=go.Scatterpolar(
                r=scores + [scores[0]],
                theta=score_labels + [score_labels[0]],
                fill='toself',
                line=dict(color='#2A3F5F', width=2),
                fillcolor='rgba(42, 63, 95, 0.15)',
                marker=dict(color='#2A3F5F', size=6)
            ))
            
            score_fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100],
                        gridcolor='#E2E8F0',
                        gridwidth=1,
                        tickfont=dict(color='#2A3F5F', size=10)
                    ),
                    angularaxis=dict(
                        gridcolor='#E2E8F0',
                        gridwidth=1,
                        tickfont=dict(color='#2A3F5F', size=11)
                    ),
                    bgcolor='#FFFFFF'
                ),
                showlegend=False,
                title={
                    'text': 'Financial Capability Score Radar Chart',
                    'font': {'size': 16, 'color': '#2A3F5F'},
                    'x': 0.5,
                    'y': 0.95
                },
                paper_bgcolor='white',
                plot_bgcolor='white',
                height=450,
                margin=dict(l=50, r=50, t=80, b=50)
            )
            
            # 创建图表容器
            st.markdown('<div style="background: white; border-radius: 16px; padding: 2rem; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);">', unsafe_allow_html=True)
            st.plotly_chart(score_fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

def report_generation_page():
    """Report Generation Page"""
    st.markdown('<h2 class="sub-header">📋 Financial Analysis Report Generation</h2>', unsafe_allow_html=True)
    
    # Check if data exists
    if not st.session_state.financial_data:
        st.markdown("""
            <div class="stWarning">
                <strong>⚠️ Data Notice</strong>
                <p>Please input financial data in the 'Data Input' page first</p>
            </div>
        """, unsafe_allow_html=True)
        return
    
    # 创建报告生成卡片
    st.markdown('<div style="background: white; border-radius: 16px; padding: 2rem; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);">', unsafe_allow_html=True)
    
    # 获取报告模板
    try:
        response = requests.get(f"{API_BASE_URL}/templates")
        if response.status_code == 200:
            templates = response.json().get("templates", [])
        else:
            templates = [
                {"id": "comprehensive", "name": "Comprehensive Financial Analysis Report"},
                {"id": "profitability", "name": "Profitability Analysis Report"},
                {"id": "solvency", "name": "Solvency Analysis Report"},
                {"id": "operating", "name": "Operating Efficiency Analysis Report"},
                {"id": "growth", "name": "Growth Potential Analysis Report"},
                {"id": "valuation", "name": "Valuation Analysis Report"}
            ]
    except:
        templates = [
            {"id": "comprehensive", "name": "Comprehensive Financial Analysis Report"},
            {"id": "profitability", "name": "Profitability Analysis Report"},
            {"id": "solvency", "name": "Solvency Analysis Report"},
            {"id": "operating", "name": "Operating Efficiency Analysis Report"},
            {"id": "growth", "name": "Growth Potential Analysis Report"},
            {"id": "valuation", "name": "Valuation Analysis Report"}
        ]
    
    # Select report type
    st.markdown('<h4 style="color: #2A3F5F; font-weight: 600; margin-bottom: 1.5rem;">📄 Select Report Type</h4>', unsafe_allow_html=True)
    
    # 创建美观的选择框
    report_type = st.selectbox(
        "",
        templates,
        format_func=lambda x: x["name"],
        label_visibility="collapsed"
    )
    
    # User query
    st.markdown('<h4 style="color: #2A3F5F; font-weight: 600; margin-bottom: 1.5rem;">🔍 Analysis Requirements (Optional)</h4>', unsafe_allow_html=True)
    
    # Create beautiful text input
    query = st.text_input(
        "",
        placeholder="e.g., Focus on profitability and solvency analysis, provide improvement suggestions",
        label_visibility="collapsed",
        help="You can specify areas for focused analysis"
    )
    
    # Generate report button
    st.markdown("<br>", unsafe_allow_html=True)
    col_center = st.columns([3, 2, 3])
    with col_center[1]:
        if st.button("🚀 Generate Report", use_container_width=True):
            with st.spinner("🔄 Generating report..."):
                try:
                    payload = {
                        "financial_data": st.session_state.financial_data,
                        "query": query if query else "Financial analysis",
                        "report_type": report_type["id"]
                    }
                    
                    response = requests.post(
                        f"{API_BASE_URL}/generate",
                        json=payload
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        if result["status"] == "success":
                            report_content = result["report_content"]
                            
                            # 显示报告
                            st.markdown('<div style="margin-top: 3rem;">', unsafe_allow_html=True)
                            st.markdown(f'<h4 style="color: #2A3F5F; font-weight: 600; margin-bottom: 1.5rem;">📝 {report_type["name"]}</h4>', unsafe_allow_html=True)
                            
                            # 创建美观的报告展示区域 - 进一步增加宽度
                            st.markdown('<div style="background: #F8FAFC; border-radius: 16px; padding: 3rem; border: 1px solid #E2E8F0; max-width: 1200px; margin: 0 auto;">', unsafe_allow_html=True)
                            st.markdown(report_content)
                            st.markdown('</div>', unsafe_allow_html=True)
                            
                            # 保存到历史记录
                            st.session_state.report_history.append({
                                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "report_type": report_type["name"],
                                "content": report_content
                            })
                            
                            # Download button
                            st.markdown("<br>", unsafe_allow_html=True)
                            col_download = st.columns([3, 2, 3])
                            with col_download[1]:
                                st.download_button(
                                    label="💾 Download Report",
                                    data=report_content,
                                    file_name=f"Financial_Analysis_Report_{report_type['id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                                    mime="text/markdown",
                                    use_container_width=True
                                )
                            
                            st.markdown('</div>', unsafe_allow_html=True)
                            
                        else:
                            st.markdown(f"""
                                <div class="stError">
                                    <strong>❌ Report generation failed</strong>: {result.get('message', 'Unknown error')}
                                </div>
                            """, unsafe_allow_html=True)
                            
                    else:
                        st.markdown(f"""
                            <div class="stError">
                                <strong>❌ Report generation failed</strong>: {response.status_code} - {response.text}
                            </div>
                        """, unsafe_allow_html=True)
                        
                except Exception as e:
                    st.markdown(f"""
                        <div class="stError">
                            <strong>❌ Report generation failed</strong>: {str(e)}
                        </div>
                    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Show report history
    if st.session_state.report_history:
        st.markdown('<h4 style="color: #2A3F5F; font-weight: 600; margin-top: 2rem; margin-bottom: 1.5rem;">📚 Report History</h4>', unsafe_allow_html=True)
        
        for i, report in enumerate(reversed(st.session_state.report_history), 1):
            with st.expander(f"📄 {report['timestamp']} - {report['report_type']}", expanded=False):
                    st.markdown('<div style="background: #F8FAFC; border-radius: 16px; padding: 3rem; border: 1px solid #E2E8F0; max-width: 1200px; margin: 0 auto;">', unsafe_allow_html=True)
                    st.markdown(report['content'])
                    st.markdown('</div>', unsafe_allow_html=True)

def knowledge_base_page():
    """Knowledge Base Management Page"""
    st.markdown('<h2 class="sub-header">📚 Financial Knowledge Base Management</h2>', unsafe_allow_html=True)
    
    # Create knowledge base status card
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    
    # Get knowledge base information
    st.markdown('<h4 style="color: #2A3F5F; font-weight: 600; margin-bottom: 1.5rem;">📊 Knowledge Base Status</h4>', unsafe_allow_html=True)
    
    try:
        response = requests.get(f"{API_BASE_URL}/kb/info")
        if response.status_code == 200:
            info = response.json()
            doc_count = info.get("document_count", 0)
            
            # Create beautiful metric card
            st.markdown('<div style="display: flex; align-items: center; gap: 1.5rem;">', unsafe_allow_html=True)
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #2A3F5F 0%, #4A6FA5 100%); color: white; padding: 2rem; border-radius: 16px; text-align: center; flex: 1; box-shadow: 0 4px 12px rgba(42, 63, 95, 0.2);">
                    <p style="font-size: 1rem; margin-bottom: 0.5rem; font-weight: 500;">Document Count</p>
                    <p style="font-size: 3rem; font-weight: 700;">{doc_count}</p>
                </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        else:
            st.markdown(f"""
                <div class="stError">
                    <strong>❌ Failed to get knowledge base information</strong>: {response.status_code}
                </div>
            """, unsafe_allow_html=True)
    except Exception as e:
        st.markdown(f"""
            <div class="stError">
                <strong>❌ Failed to get knowledge base information</strong>: {str(e)}
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Upload document card
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    
    st.markdown('<h4 style="color: #2A3F5F; font-weight: 600; margin-bottom: 1.5rem;">📁 Upload Documents to Knowledge Base</h4>', unsafe_allow_html=True)
    
    # File upload instructions
    st.markdown('<div style="background: #EFF6FF; border-radius: 8px; padding: 1rem; margin-bottom: 1.5rem;">', unsafe_allow_html=True)
    st.markdown('<p style="color: #2A3F5F; margin: 0;">💡 <strong>Supported Formats</strong>: TXT, Markdown (.md), PDF</p>', unsafe_allow_html=True)
    st.markdown('<p style="color: #2A3F5F; margin: 0;">📋 <strong>Recommended Content</strong>: Financial analysis methods, industry standards, valuation models, and other professional documents</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # File upload area
    uploaded_file = st.file_uploader(
        "",
        type=["txt", "md", "pdf"],
        label_visibility="collapsed",
        help="Drag and drop files here or click to upload"
    )
    
    if uploaded_file is not None:
        with st.spinner("🔄 Uploading document..."):
            try:
                files = {"file": uploaded_file}
                response = requests.post(f"{API_BASE_URL}/kb/upload", files=files)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    st.markdown(f"""
                        <div class="stSuccess">
                            <strong>✅ {result["message"]}</strong>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                        <div class="stError">
                            <strong>❌ Upload failed</strong>: {response.status_code} - {response.text}
                        </div>
                    """, unsafe_allow_html=True)
                    
            except Exception as e:
                st.markdown(f"""
                    <div class="stError">
                        <strong>❌ Upload failed</strong>: {str(e)}
                    </div>
                """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Knowledge base description card
    st.markdown('<div style="background: #EFF6FF; border-radius: 16px; padding: 2rem; border-left: 4px solid #3B82F6;">', unsafe_allow_html=True)
    st.markdown('<h4 style="color: #2A3F5F; font-weight: 600; margin-bottom: 1.5rem;">📖 Knowledge Base Description</h4>', unsafe_allow_html=True)
    st.markdown("""
    <div style="line-height: 1.8; color: #2A3F5F;">
        <div style="margin-bottom: 1.5rem;">
            <strong>🎯 Knowledge Base Content</strong>
            <ul>
                <li><strong>Financial Analysis Methods and Frameworks</strong>: Professional methods such as DuPont analysis and financial ratio analysis</li>
                <li><strong>Financial Ratio Analysis Standards</strong>: Reasonable ranges and evaluation standards for financial indicators across industries</li>
                <li><strong>Valuation Models and Methods</strong>: Application of valuation models like PE, PB, PS, DCF, etc.</li>
                <li><strong>Industry Analysis Guides</strong>: Focus areas and characteristics for financial analysis in different industries</li>
            </ul>
        </div>
        <div>
            <strong>💡 Important Note</strong>
            <p>Uploaded documents will be used to enhance the professionalism and accuracy of financial analysis reports, helping the system provide more precise analysis and recommendations. It is recommended to upload high-quality, professional financial analysis materials.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()