@echo off

cd /d "C:\Users\ethan\portfolio\sql _Normalisations_project\crypto-incremental-etl-pipeline"

echo ============================================== >> task_scheduler.log
echo Started: %date% %time% >> task_scheduler.log

venv\Scripts\python.exe src\pipeline.py >> task_scheduler.log 2>&1

echo Pipeline exit code: %errorlevel% >> task_scheduler.log

git add crypto_prices.db >> task_scheduler.log 2>&1

git diff --cached --quiet
if errorlevel 1 (
    git commit -m "data: scheduled database update" >> task_scheduler.log 2>&1
    git push origin main >> task_scheduler.log 2>&1
) else (
    echo No database changes to commit. >> task_scheduler.log
)

echo Finished: %date% %time% >> task_scheduler.log