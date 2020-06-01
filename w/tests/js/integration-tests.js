window.debug = true;
function integrationTestsMain() {
   console.log('-- integrationTestsMain() started');
   blankTest();
   oneFileTest();
   multipleFileTest();
   urlTest();
   urlTest2();
   if (window.testFailed) {
      document.body.style.background = '#ff6666';
   } else {
      document.body.style.background = '#ccffcc';
   }
   console.log('-- integrationTestsMain() done');
}


function blankTest() {
   search = searchFiles('  ','/tests/test_search_files_file_paths.txt')
   updateTestMsg('searchFiles() 0 blank', '', search.html+search.urls)
}

function oneFileTest() {
   search = searchFiles('pizza','/tests/test_search_files_file_paths.txt')
   expected = '<a href="http://localhost:8080/w/tests/search-files/recipe.html">tests/search-files/recipe.html</a>: <b><id style=\'color:red\'>pizza</id></b>' 
   updateTestMsg('searchFiles() 1 one file', expected, search.html)
   updateTestMsg('searchFiles() 2 one file', '', search.hitUrl)
}


function multipleFileTest() {
   search = searchFiles('cup','/tests/test_search_files_file_paths.txt')
   expected = '<a href="http://localhost:8080/w/tests/search-files/recipe.html">tests/search-files/recipe.html</a>: 3 <id style=\'color:red\'>cup</id>s flour\n'+
              '1 <id style=\'color:red\'>cup</id> water\n'+
              '\n'+
              '<a href="http://localhost:8080/w/tests/search-files/problems-solutions.html">tests/search-files/problems-solutions.html</a>: oz in 1 <id style=\'color:red\'>cup</id>' 
   updateTestMsg('searchFiles() 3 multi file', expected, search.html)
    updateTestMsg('searchFiles() 4 multi file', '', search.hitUrl)
}

function urlTest() {
   search = searchFiles('recipe','/tests/test_search_files_file_paths.txt')
   expectedHtml = '<a href="http://localhost:8080/w/tests/search-files/recipe.html">tests/search-files/<id style=\'color:red\'>recipe</id>.html</a>'
   expectedUrl = 'http://localhost:8080/w/tests/search-files/recipe.html'
   updateTestMsg('searchFiles() 5 file name, recipe', expectedHtml, search.html)
   updateTestMsg('searchFiles() 6 file name, recipe', expectedUrl, search.hitUrl)

   search = searchFiles('Problem','/tests/test_search_files_file_paths.txt')
   expectedHtml = '<a href="http://localhost:8080/w/tests/search-files/problems-solutions.html">tests/search-files/<id style=\'color:red\'>problem</id>s-solutions.html</a>\n'+
                  '\n'+
                  '<a href="http://localhost:8080/w/tests/search-files/problems-solutions.html">tests/search-files/problems-solutions.html</a>: answer: 8 oz no <id style=\'color:red\'>problem</id>'
   updateTestMsg('searchFiles() 7 file name + text, Problem', expectedHtml, search.html)
   updateTestMsg('searchFiles() 8 file name + text, Problem', '', search.hitUrl)
}

function urlTest2() {
   search = searchFiles('solution','/tests/test_search_files_file_paths.txt')
   expectedHtml = '<a href="http://localhost:8080/w/tests/search-files/problems-solutions.html">tests/search-files/problems-<id style=\'color:red\'>solution</id>s.html</a>\n'+
                  '<a href="http://localhost:8080/w/tests/search-files/misc-solutions.html">tests/search-files/misc-<id style=\'color:red\'>solution</id>s.html</a>'
   updateTestMsg('searchFiles() 9  2 files, solution', expectedHtml, search.html)
   updateTestMsg('searchFiles() 10 2 files, solution', '', search.hitUrl)

}

