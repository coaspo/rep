translator
==========
Project illustrates MVC in python.

It uses **googletranslate** and saves translated words into
a local json file to improve performance.

.. contents:: Contents:


Run app
-------
|  From project dir, run:
|  ``pip install -r requirements.txt``
|  then
|  ``python cli.py``

Run tests
---------
|  ``set PYTHONPATH .``
|  ``pytest tests/``

Notes
-----
|  Update requirements.txt:
|  ``pip freeze > requirements.txt``


|  If not in a Pychram, use virtual env:

|  Create virtual env:
|    ``virtualenv venv``
|    Activate venv (adds bin to ``%PATH%``)
|    ``source venv/bin/activate``
|    Restore ``%PATH%``:
|    ``decactivate``
