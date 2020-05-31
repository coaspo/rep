window.debug = true;
function integrationTestsMain() {
   console.log('-- integrationTestsMain() started');
   oneFileTest();
   multipleFileTest();
   docLinkTest();
   if (window.testFailed) {
      document.body.style.background = '#ff6666';
   } else {
      document.body.style.background = '#ccffcc';
   }
   console.log('-- integrationTestsMain() done');
}


function oneFileTest() {
   search = searchFiles('pizza','/tests/test_search_files_file_paths.txt')
   expected = '<a href="http://localhost:8080/w/tests/search-files/recipe.html">tests/search-files/recipe.html</a>: <b><id style=\'color:red\'>pizza</id></b>' 
   updateTestMsg('searchFiles() 1 one file', expected, search.html)
   updateTestMsg('searchFiles() 2 one file', '', search.docLink)
}


function multipleFileTest() {
   search = searchFiles('cup','/tests/test_search_files_file_paths.txt')
   expected = '<a href="http://localhost:8080/w/tests/search-files/recipe.html">tests/search-files/recipe.html</a>: 3 <id style=\'color:red\'>cup</id>s flour\n'+
              '1 <id style=\'color:red\'>cup</id> water\n'+
              '\n'+
              '<a href="http://localhost:8080/w/tests/search-files/problems-solutions.html">tests/search-files/problems-solutions.html</a>: oz in 1 <id style=\'color:red\'>cup</id>' 
   updateTestMsg('searchFiles() 3 multi file', expected, search.html)
   updateTestMsg('searchFiles() 4 multi file', '', search.docLink)
}

function docLinkTest() {
   search = searchFiles('recipe','/tests/test_search_files_file_paths.txt')
   expectedHtml = 'Found text in one file name; <a href="http://localhost:8080/w/tests/search-files/recipe.html">tests/search-files/recipe.html</a>'
   expectedDoc = '<a href="http://localhost:8080/w/tests/search-files/recipe.html">tests/search-files/recipe.html</a>'
   updateTestMsg('searchFiles() 5 docLink', expectedHtml, search.html)
   updateTestMsg('searchFiles() 6 docLink', expectedDoc, search.docLink)
}

function docLinkTest2() {
   search = searchFiles('Problem','/tests/test_search_files_file_paths.txt')
   expectedHtml = 'Found text in one file name; <a href="http://localhost:8080/w/tests/search-files/problems-solutions.html">tests/search-files/problems-solutions.html</a>'
   expectedDoc = '<a href="http://localhost:8080/w/tests/search-files/problems-solutions.html">tests/search-files/problems-solutions.html</a>'
   updateTestMsg('searchFiles() 7 hybrid', expectedHtml, search.html)
   updateTestMsg('searchFiles() 8 hybrid', expectedDoc, search.docLink)
}

