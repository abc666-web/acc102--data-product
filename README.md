Smart Financial Analysis System
1. Project Purpose：
  This project analyzes corporate financial performance for clear business decision-making and learning purposes. The target audience is managers, financial analysts, and students.
2. Data Source
  （1）Data source: User-uploaded CSV/Excel files or manual input
  （2）Access date: Real-time processing
  （3）Key variables: Revenue, net profit, assets, liabilities, equity, inventory, accounts receivable, market cap
3. Methods (Python Workflow)
  （1）Data cleaning and calculation with Pandas
  （2）Financial indicator analysis and computation
  （3）Interactive visualization with Plotly
  （4）Frontend and backend separation with Streamlit + FastAPI
  （5）AI report generation using LangChain + ChromaDB (RAG)
4. Key Findings
  Automatically calculate 5 core financial dimensions
  Generate professional AI-supported financial reports
  Display intuitive radar charts and bar charts
  Support both file upload and manual data input
5. How to Run
  Clone this repository
  Install dependencies: pip install -r requirements_finance.txt
  Run one‑command startup: python start_finance_system.py
  Open the app at: http://localhost:8501
6. Limitations
  Requires Python 3.10.14 due to package compatibility
  Only supports local or cloud server deployment
  Static analysis without real-time market data
  Basic interface design
7. Demo / Product Link
  Local app: http://localhost:8501
  Demo video: [Your video link]
  GitHub repo: https://github.com/abc666-web/acc102--data-product.git
