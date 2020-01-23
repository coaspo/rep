set TEST_ERR=1

	if %TEST_ERR%==2(
		echo --- tests failed
		pause
		exit 1
	)
