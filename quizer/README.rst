Quizzer
=======
Project illustrates MVC in python.
It may be used to make and practice quizzes.

.. contents:: Contents:


Run app
-------
|  Install python 3 and add it to path.
|  (Optional) Update pip:
|  ``python -m pip install --upgrade pip``
|
|  From project dir, run the commands:
|  ``pip install -r requirements.txt``
|  ``python cli.py``
|
|  May review info and error MSGs in:
|  ``logs\quizzer-YYYY-MM.log``

Run tests
---------
|  **In Pycharm:**
|   >File >Settings >Tools >Python-Integrated-Tools,
|   change >Default-test-runner to ``pytest``
|   select a test and > "run pytest"
|
|  **Outside pycharm:**
|   Double click ``c:\..\quizzer\run-tests.bat``

Notes
-----
|  **Best practice**, create virtual env:
|    ``pip install virtualenv``
|    ``virtualenv venv``
|
|    **Work in pycharm:**
|     >File >Settings >Project:quizzer
|     Should be able to select:
|     ``c:\..\quizzer\venv\Scripts\python.exe``
|
|    **Work outside pycharm:**
|     Activate venv (add bin to ``%PATH%``)
|       ``cd c:\..\quizzer``
|       ``.\venv\Scripts\activate.bat``
|       When done, deactivate Path. ``%PATH%``:
|       ``.\venv\Scripts\deactivate.bat``
|
|  **After using a new library**, update requirements.txt:
|   ``pip freeze > requirements.txt``

Problems/Solutions
------------------
| Cannot run pytest (rt click tests dir ..)
| **FIX:** >File >Settings >Tools >Python-Integrated-Tools,
| change >Default-test-runner to pytest
|
| on running pytest: ``found = cls._search_paths(context.pattern, context.path) AttributeError: 'str' object has no attribute 'pattern'``
| **FIX:** from project dir, run ``./venv/Scripts/activate.bat``