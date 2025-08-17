@echo off
setlocal

pip install openai pyyaml 

set /p api_key="Please enter OpenRouter API key or press Enter to skip:"
echo|set /p=%api_key% > _includes\settings\api_key.txt

pause
