Static Website
==============
'w' is a static web site project.
It contains useful/interesting links/info and
the ability to search the contents of the site.
See <./content.html> for more details.


Test
----
Run <./tests/test_script_check_into_br1.py>

  This tests the script that creates/updates files
  <./search_labels.txt> and <./search_file_paths.txt>


Run <./tests/start_local_server__open__test_search.html.py>. 

  The script stops/runs local server using:
    fuser -k 8080/tcp
    python3 -m http.server 8080
  And displays 
    <http://localhost:8080/w/tests/test_search.html>

Open <https://li.netlify.app/w/tests/test_search.html>. 

  This runs unit and integration on the server.

View site from github
---------------------
To view ``br1/main`` branches in browser click:  
 <https://htmlpreview.github.io/?https://github.com/coaspo/rep/blob/br1/w/index.html> 
 <https://htmlpreview.github.io/?https://github.com/coaspo/rep/blob/master/w/index.html>  
respectfully.  

