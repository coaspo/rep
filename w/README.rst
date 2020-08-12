Quizzer
=======
The 'w' is a static web site project.
It contains useful/interesting links/info and
the ability to search the contents of the site.

See `<./contents.html>`__ for more details

.. contents:: Contents:



Notes
-----
|  **Best practice, create virtual env**:
|    ``pip3 install virtualenv``
|  From the project directory run:
|    ``virtualenv venv``
|
|    **In pycharm:**
|     >File >Settings >Project:quizzer
|     Create ``venv`` in project folder and select project interpreter:
|     ``c:\..\quizzer\venv\Scripts\python.exe``
|
|    **Outside pycharm:**
|       . venv/bin/activate
|
|  **After using a new library**, update ``requirements.txt``:
|   ``pip install pipreqs``
|   ``pipreqs ltrans``

View site from github
---------------------
|To view ``br1/main`` branches in browser click:
| <https://htmlpreview.github.io/?https://github.com/coaspo/rep/blob/br1/w/index.html>
| <https://htmlpreview.github.io/?https://github.com/coaspo/rep/blob/master/w/index.html>
|respectfully.



Run python check-in tests
-------------------------
|  Run <./tests/test_script_check_into_br1.py>
|
|    This tests the script that creates/updates files
|    <./search_labels.txt> and <./search_file_paths.txt>
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

Run server tests
----------------
| Run <./tests/start_local_server__open__test_search.html.py>.
|
|   The script stops/runs local server using:
|    fuser -k 8080/tcp
|     python3 -m http.server 8080
|   And displays
|     <http://localhost:8080/w/tests/test_search.html>
|
|Open <https://li.netlify.app/w/tests/test_search.html>.
|
|   This runs unit and integration on the server.
|

Run tests and check into github
-------------------------------
|   In command window type  or in Pycharm run:
|   ``run_tests_and_check-in-br1.py``

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
|     Or run:
|       . venv/bin/activate
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
