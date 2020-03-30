Quizzer
=======
Application creates multiple choice quizzes using simple marked-up text.

See `help <./quz/help.html>`__ for more details

.. contents:: Contents:


Get application
----------------
| Use git-bash to clone the repo:
|    ``git clone https://github.com/coaspo/rep``
|   To get a brach, for example ``br1``:
|    ``git pull origin br1``
| Or download zip file from github.

Run app
-------
|  Install python 3 and add it to path.
|  (Optional) Update pip:
|    ``python -m pip install --upgrade pip``
|
|  Run ``python cli.py``
|  or create a short cut to it and double click it.
|
|  May review info and error MSGs in:
|    ``logs\quizzer-YYYY-MM.log``''

Run tests
---------
|  From project dir, install pytest:
|    ``pip install -r requirements.txt``
|  May need to activate venv (see below) before doing this.
|
|  **In Pycharm:**
|   >File >Settings >Tools >Python-Integrated-Tools,
|   change >Default-test-runner to ``pytest``
|   select a test and > "run pytest"
|
|  **Outside pycharm:**
|   In command window type  ``run_tests.py``
|   Double clicking the file does not work (!)

Tests/check-in automation
-------------------------------
<<<<<<< HEAD
|   Run ``run_tests_and_check-in-br1.bat``
|   If a test fails, code will not be checked in.
=======
|   In command window type  or in Pycharm run:
|   ``run_tests_and_check-in-br1.py``
>>>>>>> br1

Notes
-----
|  **Best practice, create virtual env**:
|    ``pip install virtualenv``
|  From the project directory run:
|    ``virtualenv venv``
|
|    **In pycharm:**
|     >File >Settings >Project:quizzer
|     Create ``venv`` in project folder and select project interpreter:
|     ``c:\..\quizzer\venv\Scripts\python.exe``
|
|    **Outside pycharm:**
|     Activate venv (add bin to ``%PATH%``)
|       ``cd c:\..\quizzer``
|       ``.\venv\Scripts\activate.bat``
|       When done, deactivate Path. ``%PATH%``:
|       ``.\venv\Scripts\deactivate.bat``
|
|  **After using a new library**, update ``requirements.txt``:
|   ``pip install pipreqs``
|   ``pipreqs ltrans``

Problems/Solutions
------------------
| Cannot run pytest (rt click tests dir ..)
| **FIX:** >File >Settings >Tools >Python-Integrated-Tools,
| change >Default-test-runner to pytest
|
| on running pytest: ``found = cls._search_paths(context.pattern, context.path) AttributeError: 'str' object has no attribute 'pattern'``
| **FIX:** from project dir, run ``./venv/Scripts/activate.bat``
|