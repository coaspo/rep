REM To run this in the Git Bash window type:
REM    cmd "/C check-in-br1.bat"
REM
REM NOTE this runs the tests, reports
REM "failed was unexpected at this time." and stops.
REM pystest works from the command line
REM but not from a bat file???
REM
REM For any errors, may need to update a pkg, for example:
REM    pip install -U pluggy
REM and recreate venv:
REM    virtualenv venv

@echo on
call .\venv\Scripts\activate.bat
echo --- venv activated
set PYTHONPATH=.
call pytest tests/
if ERRORLEVEL 1 (
    echo --- tests failed
    pause
	set errorflag=1
)
echo --- pytest done
call .\venv\Scripts\deactivate.bat
if ERRORLEVEL 1 (
	echo. & echo    Tests have failed - cannot do check-in & echo.
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

call .\venv\Scripts\activate.bat
set PYTHONPATH=.
pytest tests/
if ERRORLEVEL 1 (
	pause
)
