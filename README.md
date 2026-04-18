Smart Financial Analysis System
1. Problem & User
  This project helps managers, financial analysts and students conduct fast, standard financial analysis, solving low efficiency and inconsistent reporting issues.
2. Data
  Source: User-uploaded CSV/Excel files or manual input
  Access date: Real-time processing
  Key fields: Revenue, net profit, assets, liabilities, equity, inventory, accounts receivable,       market cap
3. Methods
  Data cleaning and calculation with Pandas
  Interactive charts with Plotly
  Frontend: Streamlit; Backend: FastAPI
  RAG report generation using LangChain + ChromaDB
4. Key Findings
  Automatically computes 5 core financial dimensions
  Generates professional reports supported by AI & RAG
  Provides interactive radar and bar charts
  Supports file upload and manual input
5. How to Run
  This application is designed to run locally with a separate backend API (FastAPI) and frontend (Streamlit), so it is not deployed on Streamlit Cloud. Please follow the steps below     to start it on your own computer.
  Important Note: This project must run on Python 3.10.14.Due to package compatibility constraints, other Python versions (especially 3.12+) will cause installation failures and         prevent the code from running successfully.
  One‑Command Startup (Recommended)
  This project supports one‑command startup that automatically installs dependencies, launches the backend API, and starts the frontend interface.
      bash
      # Clone the repository
      git clone https://github.com/abc666-web/acc102--data-product.git
      cd acc102--data-product
      # Install dependencies
      pip install -r requirements_finance.txt
      # One‑command full system start
      python start_finance_system.py
   
  After running, open your browser and access the app at: http://localhost:8501

7. Product link / Demo
  Local app: http://localhost:8501
  Demo video: [Your video link]
  GitHub repo: [Your GitHub link]
8. Limitations & next steps
  Limitations: Static analysis only; basic interface; no real-time market data; large files may affect speed
  Next steps: Add time-series analysis; support more industries; add real-time data; optimize AI reports
