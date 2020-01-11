Title Run pytest in translator
call ./venv/Scripts/activate.bat
set PYTHONPATH=.
pytest tests/
if ERRORLEVEL 1 (
	pause 
)
call ./venv/Scripts/deactivate.bat
