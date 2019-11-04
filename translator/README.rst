translator
==========
Project illustrates MVC in python.

It uses **googletranslate** and saves translated words into
a local json file to improve performance.

.. contents:: Contents:


Run app
-------
|  Install python 3 and add it to path.
|  (Optional) Update pip:
|  ``python -m pip install --upgrade pip``
|
|  From project dir, **run**:
|  ``pip install -r requirements.txt``
|  ``python cli.py``

Run tests
---------
|  **In Pycharm:**
|   >File >Settings >Tools >Python-Integrated-Tools,
|   change >Default-test-runner to pytest
|   select a test and >"run pytest"
|
|  **Outside pycharm:**
|   Follow **Work outside pycharm:** labeled instructions below,
    and run:
|   ``set PYTHONPATH=.``
|   ``pytest tests/``

Notes
-----
|  **Best practice**, create virtual env:
|    ``pip install virtualenv``
|    ``virtualenv venv``
|
|    **Work in pycharm:**
|     >File >Settings >Project:translator
|     Should be able to select:
|     ``c:\..\translator\venv\Scripts\python.exe``
|
|    **Work outside pycharm:**
|     Activate venv (add bin to ``%PATH%``)
|       ``cd c:\..\translator``
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
| ``E   ModuleNotFoundError: No module named 'googletrans'``
| Click on ``import googletrans`` and slect fix
| Cause(?) venv created before running  ``pip install -r requirements.txt``