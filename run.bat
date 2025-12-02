@echo off
REM 桌面寵物啟動腳本
REM Desktop Pet Launch Script
REM 
REM 使用方式 / Usage:
REM 1. cd 到專案目錄 / Navigate to project directory
REM 2. 啟動虛擬環境（如需要）/ Activate virtual environment (if needed)
REM 3. 執行此腳本 / Run this script

echo ====================================
echo 桌面寵物 Desktop Pet
echo ====================================
echo.

python main.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo 執行失敗，請確認：
    echo 1. 已安裝 Python
    echo 2. 已安裝依賴套件：pip install -r requirements.txt
    echo 3. 已啟動虛擬環境（如使用）
    pause
)
