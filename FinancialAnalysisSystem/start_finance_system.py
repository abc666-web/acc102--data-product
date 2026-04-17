#!/usr/bin/env python3
"""
智能财务分析系统启动脚本
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def check_environment():
    """检查环境"""
    print("检查环境...")
    
    # 检查Python版本
    if sys.version_info < (3, 8):
        print("❌ Python版本需要3.8或更高")
        return False
    
    # 检查必要文件
    required_files = [
        "financial_data_processor.py",
        "financial_knowledge_base.py", 
        "financial_report_generator.py",
        "finance_api_server.py",
        "finance_streamlit_app.py"
    ]
    
    missing_files = [f for f in required_files if not Path(f).exists()]
    if missing_files:
        print(f"❌ 缺少必要文件: {', '.join(missing_files)}")
        return False
    
    print("✅ 环境检查通过")
    return True

def install_dependencies():
    """安装依赖"""
    print("\n安装依赖包...")
    
    try:
        # 检查requirements文件
        if Path("requirements_finance.txt").exists():
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "-r", "requirements_finance.txt"
            ])
            print("✅ 依赖安装成功")
        else:
            print("⚠️  requirements_finance.txt不存在，跳过依赖安装")
            
    except subprocess.CalledProcessError as e:
        print(f"❌ 依赖安装失败: {e}")
        return False
    
    return True

def start_api_server():
    """启动API服务器"""
    print("\n启动API服务器...")
    
    api_process = subprocess.Popen(
        [sys.executable, "finance_api_server.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # 等待服务器启动
    time.sleep(3)
    
    # 检查是否成功启动
    returncode = api_process.poll()
    if returncode is not None:
        stderr = api_process.stderr.read() if api_process.stderr else ""
        print(f"❌ API服务器启动失败")
        if stderr:
            print(f"错误信息: {stderr}")
        return None
    
    print("✅ API服务器启动成功")
    return api_process

def start_frontend():
    """启动前端界面"""
    print("\n启动前端界面...")
    
    frontend_process = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "finance_streamlit_app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # 等待前端启动
    time.sleep(3)
    
    # 检查是否成功启动
    returncode = frontend_process.poll()
    if returncode is not None:
        stderr = frontend_process.stderr.read() if frontend_process.stderr else ""
        print(f"❌ 前端界面启动失败")
        if stderr:
            print(f"错误信息: {stderr}")
        return None
    
    print("✅ 前端界面启动成功")
    return frontend_process

def show_status(api_process, frontend_process):
    """显示系统状态"""
    print("\n" + "="*60)
    print("智能财务分析系统 - 状态信息")
    print("="*60)
    print(f"API服务器: {'运行中' if api_process and api_process.poll() is None else '未运行'}")
    print(f"前端界面: {'运行中' if frontend_process and frontend_process.poll() is None else '未运行'}")
    print("\n访问地址:")
    print(f"  API服务: http://localhost:8004")
    print(f"  API文档: http://localhost:8004/docs")
    print(f"  前端界面: http://localhost:8502")
    print("\n按 Ctrl+C 停止系统")
    print("="*60)

def main():
    """主函数"""
    print("="*60)
    print("智能财务分析系统启动脚本")
    print("="*60)
    
    # 检查环境
    if not check_environment():
        sys.exit(1)
    
    # 安装依赖
    install_dependencies()
    
    # 启动服务
    api_process = start_api_server()
    frontend_process = start_frontend()
    
    # 显示状态
    show_status(api_process, frontend_process)
    
    # 等待用户中断
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n正在停止系统...")
        
        # 停止前端
        if frontend_process:
            frontend_process.terminate()
            frontend_process.wait()
        
        # 停止API服务器
        if api_process:
            api_process.terminate()
            api_process.wait()
        
        print("✅ 系统已停止")

if __name__ == "__main__":
    # 切换到脚本所在目录
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # 运行主函数
    main()