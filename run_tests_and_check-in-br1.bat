REM To run this in the Git Bash window type:
REM    cmd "/C run_tests_and_check-in-br1.bat"
REM
REM For any errors, may need to update a pkg, for example:
REM    pip install -U pluggy
REM and recreate venv:
REM    virtualenv venv

Title Run pytest and git add/commit/push
echo off
set PYTHONPATH=.

set is_br1_branch=false
	FOR /F "usebackq delims==" %%i IN (`git status`) DO (
		if "%%i"=="On branch br1" (
			set is_br1_branch=true
		)
	)
	if %is_br1_branch%==false (
	   git status
	   echo --- Current branch is not br1.
	   echo --- Only br1 check-ins are allowed.
	   pause
	   exit /B 1
	)


call .\python-venv\Scripts\activate.bat
	if ERRORLEVEL 1 (
		echo --- activate venv failed
		pause
		exit 1
	)
	echo --- venv activated

set TEST_ERR=0
cd quizzer
call pytest tests/
	if ERRORLEVEL 1 (
		echo --- quizzer tests failed
		set TEST_ERR=1
	)
cd ../translator
call pytest tests/
	if ERRORLEVEL 1 (
		echo --- translator tests failed
		set TEST_ERR=1
	)
	echo --- pytest done

cd ..
call .\python-venv\Scripts\deactivate.bat
	if ERRORLEVEL 1 (
		echo --- deactivate venv failed
	)
	echo --- venv deactivated

	if %TEST_ERR%==1 (
		echo --- tests failed
		pause
		exit 1
	)
call git status
	
git add *
git status
	echo.
set /p msg=Enter git commit msg:
git commit -m "%msg%"
git push origin br1

pause

