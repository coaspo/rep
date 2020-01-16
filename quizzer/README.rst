Quizzer
=======
Project illustrates MVC in python.
It may be used to make and practice quizzes.

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
|
|  May review info and error MSGs in:
|    ``logs\quizzer-YYYY-MM.log``''

Run tests
---------
|  From project dir, install pytest:
|    ``pip install -r requirements.txt``
|
|  **In Pycharm:**
|   >File >Settings >Tools >Python-Integrated-Tools,
|   change >Default-test-runner to ``pytest``
|   select a test and > "run pytest"
|
|  **Outside pycharm:**
|   Double click ``c:\..\quizzer\run-tests.bat``

Notes
-----
|  **Best practice, create virtual env**:
|    ``pip install virtualenv``
|  From the project directory run:
|    ``virtualenv venv``
|
|    **In pycharm:**
|     >File >Settings >Project:quizzer
|     Should be able to select:
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