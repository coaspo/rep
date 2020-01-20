REM To run this in the Git Bash window type:
REM    cmd "/C check-in-br1.bat"
REM For any errors, may need to update a pkg, for example:
REM    pip install -U pluggy
REM and recreate venv:
REM    virtualenv venv

@echo on
call ./venv/Scripts/activate.bat
echo --- venv activated
set PYTHONPATH=.
pytest tests/
if ERRORLEVEL 1 (
    echo === test(s) failed
	set errorflag=1
)
call ./venv/Scripts/deactivate.bat
if ERRORLEVEL 1 (
	echo. & echo    Tests have failed - cannot do check-in & echo.
	pause
	exit 1
)
@echo on
git add *
git status
echo.
set /p msg=Enter git commit msg:
git commit -m "%msg%"
git push origin br1
pause