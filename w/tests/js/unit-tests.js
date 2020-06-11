x = window.location.href ;
iEnd = x.indexOf('/w/')+2;
ROOT = x.substring(0,iEnd);
baseUrl = getBaseUrl() 

function unitTestsMain() {
   window.debug = true
   console.log('-- unitTestsMain() started');
   const tStart = new Date().getTime();
   functionTests();
   problemTests();
   highLightTest();
   getAnchorsTest();
   if (window.testFailed) {
      document.body.style.background = '#ff6666';
   } else {
      document.body.style.background = '#ccffcc';
   }
   const tEnd = new Date().getTime();
   dt = tEnd - tStart;
   document.getElementById("search-results").innerHTML += '\n  ' + dt + ' msec';
   console.log('-- unitTestsMain() done');
}

function testUnitTest() {
   baseUrl = getBaseUrl()
   console.log(baseUrl)
   fileUrls = getFileUrls(baseUrl, '/tests/files_paths__t.txt')
   expected = [ROOT + '/tests/search-files/links-2.html',
          ROOT + '/tests/search-files/links.html',
          ROOT + '/tests/search-files/problems-examples.html',
          ROOT + '/tests/search-files/problems-solutions.html',
          ROOT + '/tests/search-files/recipe.html']
   updateTestMsg('2 getFileUrls()', expected, fileUrls);
}

function functionTests() {
   baseUrl = getBaseUrl()
   updateTestMsg('1 getBaseUrl()', ROOT, baseUrl)

   fileUrls = getFileUrls(baseUrl, '/tests/search_files_file_paths__t.txt')
   expected = [ROOT + '/tests/search-files/recipe.html',
          ROOT + '/tests/search-files/problems-solutions.html',
          ROOT + '/tests/search-files/links.html',
          ROOT + '/tests/search-files/problems-examples.html']
   updateTestMsg('2 getFileUrls()', expected, fileUrls);

   name = fileName(ROOT + '/tests/search-files/recipe.html');
   updateTestMsg('3 fileName()', 'tests/search-files/recipe.html', name)
   
   lines = ['a','b', '','cc','', 'eee','fff']
   paragraphs = toParagraphs(lines)
   expected = ['a\nb','cc', 'eee\nfff'];
   updateTestMsg('3 toParagraphs()', expected, paragraphs)
}


function linksTests() {  
   lines = readLines(ROOT + '/tests/search-files/links.html');

   file_search_result = findTextInLines('reference', lines, false)
   expected = '<id style=\'color:red\'>reference</id>:';
   updateTestMsg('7 findTextInLines(),links', expected, file_search_result)

   file_search_result = findTextInLines('free', lines, false)
   expected = '  <a href="https://www.freebookcentre.net/"><id style=\'color:red\'>free</id> books</a>?\n'+
              '  <a href="https://www.coursera.org/">coursera- free course</a>'
   updateTestMsg('8 findTextInLines(),links', expected, file_search_result)
}

function problemTests() {  
   text = readText(ROOT + '/tests/search-files/problems-solutions.html');

   file_search_result = findTextInParagraphs('sudo', text)
   expected = 'use fire wall\n'+
              'answer: <id style=\'color:red\'>sudo</id> gedit..\n'+
              '        add line..';
   updateTestMsg('9 findTextInLines(),problems', expected, file_search_result)

   file_search_result = findTextInParagraphs('use', text)
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

function getAnchorsTest() {
   text = getAnchors(getBaseUrl(), '/tests/search_labels__t.txt');
   expected ='<a href="https://archive.org">Internet archive</a>##\
<a href="https://www.freebookcentre.net/">Free books</a>##\
<a href="https://www.coursera.org/">Coursera- Free course</a>##\
<a href="https://www.edx.org/">edX - MIT, Harvard</a>$$\
search-files/links.html\n\
<a href="https://www.wolfram.com/">Wolfram</a>##\
<a href="https://www.worldometers.info/">worldometers</a>##\
<a href="https://www.microbe.tv/twiv/archive/">Week in virology</a>\
$$search-files/links-2.html'
   updateTestMsg('16 getAnchors()', expected, text)
   links = ['<a href="https://www.freebookcentre.net/">Free books</a>', '<a href="https://www.edx.org/">edX - MIT, Harvard</a>'];
   labels = getAnchorLabels(links)
   console.log(labels)
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
               '\n----actual: ' + actual;
   }
   console.log('* updateTestMsg() status=' + status);
   displayMsgs = document.getElementById("search-results").innerHTML;
   if (displayMsgs.length >  0) {
      displayMsgs += '\n';
   }
   displayMsgs += status ; 
   document.getElementById("search-results").innerHTML = displayMsgs
}


