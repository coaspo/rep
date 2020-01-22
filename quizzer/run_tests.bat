Title Run pytest in quizzer
call .\venv\Scripts\activate.bat
set PYTHONPATH=.
pytest tests/
if ERRORLEVEL 1 (
	pause 
)
call .\venv\Scripts\deactivate.bat
