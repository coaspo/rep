REM To run this in the Git Bash window type:
REM    cmd "/C check-in-br1.bat"
REM
REM For any errors, may need to update a pkg, for example:
REM    pip install -U pluggy
REM and recreate venv:
REM    virtualenv venv

@echo on
call .\venv\Scripts\activate.bat
if ERRORLEVEL 1 (
    echo --- activate venv failed
    pause
	exit 1
)
echo --- venv activated
set PYTHONPATH=.
call pytest tests/
if ERRORLEVEL 1 (
    echo --- tests failed
    pause
	exit 1
)
echo --- pytest done
call .\venv\Scripts\deactivate.bat
if ERRORLEVEL 1 (
	echo --- deactivate venv failed
	pause
	exit 1
)
echo --- venv deactivated
@echo on
git add *
git status
echo.
set /p msg=Enter git commit msg:
git commit -m "%msg%"
git push origin br1
pause

