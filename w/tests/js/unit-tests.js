function unitTestsMain() {
   window.debug = true
   console.log('-- unitTestsMain() started');
   functionTests();
   recipeTests();
   linksTests();
   problemTests();
   highLightTest();
   if (window.testFailed) {
      document.body.style.background = '#ff6666';
   } else {
      document.body.style.background = '#ccffcc';
   }
   console.log('-- unitTestsMain() done');
}

function functionTests() {
   baseUrl = getBaseUrl()
   updateTestMsg('1 getBaseUrl()', 'http://localhost:8080/w', baseUrl)

   fileUrls = getFileUrls(baseUrl, '/tests/test_search_files_file_paths.txt')
   expected = ['http://localhost:8080/w/tests/search-files/recipe.html',
         'http://localhost:8080/w/tests/search-files/problems-solutions.html',
         'http://localhost:8080/w/tests/search-files/links.html',
          'http://localhost:8080/w/tests/search-files/misc-solutions.html']
   updateTestMsg('2 getFileUrls()', expected, fileUrls);

   name = fileName('http://localhost:8080/w/tests/search-files/recipe.html');
   updateTestMsg('3 fileName()', 'tests/search-files/recipe.html', name)
   
   lines = ['a','b', '','cc','', 'eee','fff']
   paragraphs = toParagraphs(lines)
   expected = ['a\nb','cc', 'eee\nfff'];
   updateTestMsg('3 toParagraphs()', expected, paragraphs)
}

function recipeTests() {  
   lines = readLines('http://localhost:8080/w/tests/search-files/recipe.html');
   expected = ['<b>pizza</b>', 
            '3 cups flour', 
            '1/2 tsp salt', 
            '1 cup water', 
            '    450 °F']
   updateTestMsg('4 readLines()', expected, lines)

   file_search_result = findTextInLines('cup', lines, false)
   expected = '3 <id style=\'color:red\'>cup</id>s flour\n1 <id style=\'color:red\'>cup</id> water'
   updateTestMsg('5 findTextInLines(),reg', expected, file_search_result)

   file_search_result = findTextInLines('pizza', lines, false)
   expected = "<b><id style='color:red'>pizza</id></b>";
   updateTestMsg('6 findTextInLines(),bold', expected, file_search_result)
}

function linksTests() {  
   lines = readLines('http://localhost:8080/w/tests/search-files/links.html');

   file_search_result = findTextInLines('reference', lines, false)
   expected = '<id style=\'color:red\'>reference</id>:';
   updateTestMsg('7 findTextInLines(),links', expected, file_search_result)

   file_search_result = findTextInLines('free', lines, false)
   expected = '  <a href="https://www.freebookcentre.net/"><id style=\'color:red\'>free</id> books</a>?\n'+
              '  <a href="https://www.coursera.org/">coursera</a> <id style=\'color:red\'>free</id> courses'
   updateTestMsg('8 findTextInLines(),links', expected, file_search_result)
}

function problemTests() {  
   lines = readLines('http://localhost:8080/w/tests/search-files/problems-solutions.html');

   file_search_result = findTextInLines('sudo', lines, true)
   expected = 'use fire wall\n'+
              'answer: <id style=\'color:red\'>sudo</id> gedit..\n'+
              '        add line..';
   updateTestMsg('9 findTextInLines(),problems', expected, file_search_result)

   file_search_result = findTextInLines('use', lines, true)
   expected = '<id style=\'color:red\'>use</id> snipping tool\n'+
              'answer: shift-prtscn\n'+
              '\n'+
              '<id style=\'color:red\'>use</id> fire wall\n'+
              'answer: sudo gedit..\n'+
              '        add line..';
   updateTestMsg('10 findTextInLines(),problems', expected, file_search_result)
}

function highLightTest() {
   line = 'abAAbc'
   line = highLight(line, 'b') 
   expected = "a<id style='color:red'>b</id>AA<id style='color:red'>b</id>c"
   updateTestMsg('11 highLightTest() no link', expected, line)

   line = 'A<a href="https:/aa/bbh.html">bb</a>Z'
   line = highLight(line, 'bb') 
   expected = "A<a href=\"https:/aa/bbh.html\"><id style='color:red'>bb</id></a>Z"
   updateTestMsg('12 highLightTest() 12 link', expected, line)

   line = "A<a href='https:/aa/bbh.html'>bb</a>Z"
   line = highLight(line, 'bb') 
   expected = "A<a href='https:/aa/bbh.html'><id style='color:red'>bb</id></a>Z"
   updateTestMsg('13 highLightTest() link single quote', expected, line)

   line = "A<a href='https:/aa/bbh.html'>bb</a>Z--B<a href='https:/xx/bb.HTML'>bbx</a>W"
   line = highLight(line, 'bb') 
   expected = "A<a href='https:/aa/bbh.html'><id style='color:red'>bb</id></a>Z--"+
              "B<a href='https:/xx/bb.HTML'><id style='color:red'>bb</id>x</a>W"
   updateTestMsg('14 highLightTest() links', expected, line)

   line = "A<a href='https:/aa/bbh.html'>bb</a>Z--B<a href='https:/xx/bb.HTML'>bbx</a>Wbb--"
   line = highLight(line, 'bb') 
   expected = "A<a href='https:/aa/bbh.html'><id style='color:red'>bb</id></a>Z--" +
              "B<a href='https:/xx/bb.HTML'><id style='color:red'>bb</id>x</a>W" +
              "<id style='color:red'>bb</id>--"
   updateTestMsg('15 highLightTest() links + text', expected, line)
}

function updateTestMsg(testName, expected, actual) {
   console.log('* testName='+ testName)
   isPass = expected == String(actual);
   console.log('* updateTestMsg() expected='+expected+'|')
   console.log('* updateTestMsg() actual  ='+String(actual)+'|')
   if (isPass) {
      status = 'Pass: '+  testName;
   } else {
      window.testFailed =true;
      status = '<id style=\'color:red\'>Failed; '+  testName + '</id>' +
               '\n--expected: '+expected + 
               '\n----actual: ' + actual
   }
   console.log('* updateTestMsg() status=' + status);
   displayMsgs = document.getElementById("search-results").innerHTML;
   if (displayMsgs.length >  0) {
      displayMsgs += '\n';
   }
   displayMsgs += status ; 
   document.getElementById("search-results").innerHTML = displayMsgs
}


