@echo off

cd /d "C:\Users\ethan\portfolio\sql _Normalisations_project\crypto-incremental-etl-pipeline"

"venv\Scripts\python.exe" src\pipeline.py

git add crypto_prices.db

git diff --cached --quiet
if errorlevel 1 (
    git commit -m "data: scheduled database update"
    git push origin main
)