window.DEBUG = true;
x = window.location.href ;
iEnd = x.indexOf('/w/')+3;
PFX  = '<a href="'
BASE = x.substring(0,iEnd);

function integrationTestsMain() {
   window.DEBUG = true
   console.log('-- integrationTestsMain() started');
   const tStart = new Date().getTime();
   blankTest();
   oneFileTest();
   multipleFileTest();
   urlTest();
   urlsTest();

   if (window.testFailed) {
      document.body.style.background = '#ff6666';
   } else {
      document.body.style.background = '#ccffcc';
   }
   const tEnd = new Date().getTime();
   dt = tEnd - tStart;
   document.getElementById("search-results").innerHTML += '\n  ' + dt + ' msec';
   console.log('-- integrationTestsMain() done');
}

function testIntegrationTest() {
   multipleFileTest()
}

function blankTest() {
   search = searchFiles('  ','/tests/search_files_file_paths__t.txt')
   updateTestMsg('searchFiles() 0 blank', '', search.html+search.hitUrl)
}

function oneFileTest() {
   search = searchFiles('recipe', '/tests/search_files_file_paths__t.txt')
   expected = PFX + BASE + 'tests/search-files/recipe.html">tests/search-files/<id style=\'color:red\'>recipe</id>.html</a>' 
   updateTestMsg('searchFiles() 1 one file',  expected, search.html)
   updateTestMsg('searchFiles() 2 one file', 'http://localhost:8080/w/tests/search-files/recipe.html', search.hitUrl)
}


function multipleFileTest() {
   search = searchFiles('use','/tests/search_files_file_paths__t.txt')
   expected = PFX + BASE + 'tests/search-files/problems-solutions.html">tests/search-files/problems-solutions.html</a>: <id style=\'color:red\'>use</id> snipping tool\n'+
              'answer: shift-prtscn\n'+
              '\n'+
              '<id style=\'color:red\'>use</id> fire wall\n'+
              'answer: sudo gedit..\n' +
              '        add line..\n' +
              '\n'+
              PFX + BASE + 'tests/search-files/problems-examples.html">tests/search-files/problems-examples.html</a>: <id style=\'color:red\'>use</id> linux tool\n'+
              'answer: check apps' 
   updateTestMsg('searchFiles() 3 problem', expected, search.html)
   updateTestMsg('searchFiles() 4 problem', '', search.hitUrl)
}

function urlTest() {
   search = searchFiles('Problem','/tests/search_files_file_paths__t.txt')
   expected = PFX + BASE + 'tests/search-files/problems-solutions.html">tests/search-files/<id style=\'color:red\'>problem</id>s-solutions.html</a>\n'+
                  PFX + BASE + 'tests/search-files/problems-examples.html">tests/search-files/<id style=\'color:red\'>problem</id>s-examples.html</a>\n'+
                  '\n'+
                  PFX + BASE + 'tests/search-files/problems-solutions.html">tests/search-files/problems-solutions.html</a>: oz in 1 cup\n'+
                  'answer: 8 oz no <id style=\'color:red\'>problem</id>'
   updateTestMsg('searchFiles() 5 file name + text, Problem', expected, search.html)
   updateTestMsg('searchFiles() 6 file name + text, Problem', '', search.hitUrl)
}

function urlsTest() {
   search = searchFiles('solution','/tests/search_files_file_paths__t.txt')
   expected = PFX + BASE + 'tests/search-files/problems-solutions.html">tests/search-files/problems-<id style=\'color:red\'>solution</id>s.html</a>'
   updateTestMsg('searchFiles() 7  2 files, solution', expected, search.html)
   updateTestMsg('searchFiles() 8 2 files, solution', 'http://localhost:8080/w/tests/search-files/problems-solutions.html', search.hitUrl)
}

