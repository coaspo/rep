function unitTestsMain() {
   window.DEBUG = true
   console.log('-- unitTestsMain() started');
   const tStart = new Date().getTime();
   searchContentsMainTest()
   getFileUrlsTest()
   getUrlLabelTest()
   getSearchLabelsTest()
   readTextTest()
   
   searchUrlsTest()
   searchFileIndexTest() 
   findParagraphsTest();
   highLightTest();
    
   if (window.testFailed) {
      document.body.style.background = '#ff6666';
   } else {
      document.body.style.background = '#ccffcc';
   }
   const tEnd = new Date().getTime();
   const dt = tEnd - tStart;
   document.getElementById("search-results").innerHTML += '\n  ' + dt + ' msec';
   console.log('-- unitTestsMain() done');
}


function testUnitTest() {
   document.getElementById("inputText").innerHTML = '  '
   searchFileIndexTest()
}


function searchContentsMainTest() {
   document.getElementById('inputText').value = '  '
   searchContentsMain(true, '/tests/search_files_paths__t.txt', '/tests/search_labels__t.txt')
   const actual= document.getElementById("search-results").innerHTML
   updateTestMsg('0 searchContentsMain()  innerHTML ', '', actual);
}


function getFileUrlsTest() {
   const searchFileUrls = getFileUrls(window.BASE_URL, '/tests/search_files_paths__t.txt')
   const expected = [ window.BASE_URL + "/tests/search-files/links-2.html",
                window.BASE_URL + "/tests/search-files/links.html",
                window.BASE_URL + "/tests/search-files/problems-examples.html",
                window.BASE_URL + "/tests/search-files/problems-solutions.html",
                window.BASE_URL + "/tests/search-files/recipe.html" ]
   updateTestMsg('1 getFileUrls()', expected, searchFileUrls);
}


function getSearchLabelsTest() {
   const searchLabels = getSearchLabels(window.BASE_URL, '/tests/search_labels__t.txt')
   const expected = [["wolfram", "0", "https://www.wolfram.com/"],
            ["worldometers", "0", "https://www.worldometers.info/"],
            ["week in virology", "0", "https://www.microbe.tv/twiv/archive/"],
            ["internet archive", "1", "https://archive.org"],
            ["free books", "1", "https://www.freebookcentre.net/"],
            ["coursera- free course", "1", "https://www.coursera.org/"],
            ["edx - mit, harvard", "1", "https://www.edx.org/"]];
   updateTestMsg('2 searchFileIndex()', expected, searchLabels);
}


function getUrlLabelTest() {
   const name = getUrlLabel(window.BASE_URL + '/tests/search-files/recipe.html');
   updateTestMsg('3 getUrlLabel()', 'tests/search-files/recipe.html', name)
}


function readTextTest() {  
   const text = readText(window.BASE_URL + '/tests/search_labels__t.txt');
   const expected = 'wolfram$$0$$https://www.wolfram.com/\n\
worldometers$$0$$https://www.worldometers.info/\n\
week in virology$$0$$https://www.microbe.tv/twiv/archive/\n\
internet archive$$1$$https://archive.org\n\
free books$$1$$https://www.freebookcentre.net/\n\
coursera- free course$$1$$https://www.coursera.org/\n\
edx - mit, harvard$$1$$https://www.edx.org/'
   updateTestMsg('4 readText()', expected, text)
}


function searchUrlsTest() {  
   searchFileUrls = [ window.BASE_URL + "/tests/search-files/recipe.html",
                      window.BASE_URL + "/tests/search-files/links.html"]

   const result = searchUrls('recipe', searchFileUrls)
   console.log(result)
   const expected = '<a href="'+ window.BASE_URL + '/tests/search-files/recipe.html">tests/search-files/<id style=\'color:red\'>recipe</id>.html</a>';
   updateTestMsg('5 searchUrlsTest(),links html', expected, result.html)

   const expected1 = window.BASE_URL + '/tests/search-files/recipe.html';
   updateTestMsg('5 searchUrlsTest(),links 1 url', expected1, result.url )
   updateTestMsg('5 searchUrlsTest(),links numOfUrls', 1, result.numOfUrls)

   const result2 = searchUrls('tests', searchFileUrls)
   console.log(result)
   const expected2 = '<a href="'+window.BASE_URL+'/tests/search-files/recipe.html"><id style=\'color:red\'>tests</id>/search-files/recipe.html</a>\n\
<a href="'+window.BASE_URL+'/tests/search-files/links.html"><id style=\'color:red\'>tests</id>/search-files/links.html</a>';
   updateTestMsg('6 searchUrlsTest(),links html 2', expected2, result2.html)
   updateTestMsg('6 searchUrlsTest(),links url 2', 'NA', result2.url )
   updateTestMsg('6 searchUrlsTest(),links numOfUrls 2', 2, result2.numOfUrls)

   const result3 = searchUrls('xxxx', searchFileUrls)
   updateTestMsg('7 searchUrlsTest(),links html 0', '', result3.html)
}


function searchFileIndexTest() {
   const labels= [['smart search site', 0, '//www.wolfram.com/'],
      ['free books site', 1, 'https://www.freebookcentre.net'],
      ['coursera- free course site', 1, 'https://www.coursera.org/']];
   searchFileUrls =[window.BASE_URL+'/tests/search-files/etc.html',
                    window.BASE_URL+'/tests/search-files/misc.html'];
   const result = searchFileIndex('xxxx', searchFileUrls, labels)
   updateTestMsg('7 searchFileIndex(),no find', '', result.html)
   
   const result2 = searchFileIndex('smart', searchFileUrls, labels)
   const expected2 = '<a href="http://localhost:8080/w/tests/search-files/etc.html">tests/search-files/etc.html</a>: \
<a href="//www.wolfram.com/"><id style=\'color:red\'>smart</id> search site</a>'
   updateTestMsg('8 searchFileIndex(), html ', expected2, result2.html)
   updateTestMsg('8 searchFileIndex(), url ', '//www.wolfram.com/', result2.url)
   updateTestMsg('8 searchFileIndex(), numOfUrls ', 1, result2.urlCount)

   const result3 = searchFileIndex('free', searchFileUrls, labels)
   const expected3 = '<a href="http://localhost:8080/w/tests/search-files/misc.html">tests/search-files/misc.html</a>: \
<a href="https://www.freebookcentre.net"><id style=\'color:red\'>free</id> books site</a> \
<a href="https://www.coursera.org/">coursera- <id style=\'color:red\'>free</id> course site</a>'
   updateTestMsg('9 searchFileIndex(), html 2 ', expected3, result3.html)
   updateTestMsg('9 searchFileIndex(), url 2 ', 'NA', result3.url)
   updateTestMsg('9 searchFileIndex(), numOfUrls 2 ', 2, result3.urlCount)

   const result4 = searchFileIndex('site', searchFileUrls, labels)
   const expected4 = '<a href="http://localhost:8080/w/tests/search-files/etc.html">tests/search-files/etc.html</a>: <a href="//www.wolfram.com/">smart search <id style=\'color:red\'>site</id></a>\n\
\n\
<a href="http://localhost:8080/w/tests/search-files/misc.html">tests/search-files/misc.html</a>: <a href="https://www.freebookcentre.net">free books <id style=\'color:red\'>site</id></a> <a href="https://www.coursera.org/">coursera- free course <id style=\'color:red\'>site</id></a>'
   updateTestMsg('10 searchFileIndex(), html 2 ', expected4, result4.html)
   updateTestMsg('10 searchFileIndex(), url 2 ', 'NA', result4.url)
   updateTestMsg('10 searchFileIndex(), numOfUrls 2 ', 3, result4.urlCount)
}


function findParagraphsTest() {  
   text = readText(window.BASE_URL + '/tests/search-files/problems-solutions.html');

   file_search_result = findParagraphs('sudo', text)
   const expected = 'use fire wall\n'+
              'answer: <id style=\'color:red\'>sudo</id> gedit..\n'+
              '        add line..';
   updateTestMsg('11 findParagraphs(),problems', expected, file_search_result)

   file_search_result = findParagraphs('use', text)
   const expected2 = '<id style=\'color:red\'>use</id> snipping tool\n'+
              'answer: shift-prtscn\n'+
              '\n'+
              '<id style=\'color:red\'>use</id> fire wall\n'+
              'answer: sudo gedit..\n'+
              '        add line..';
   updateTestMsg('12 findParagraphs(),problems', expected2, file_search_result)
}


function highLightTest() {
   line = 'abAAbc'
   line = highLight(line, 'b') 
   const expected = "a<id style='color:red'>b</id>AA<id style='color:red'>b</id>c"
   updateTestMsg('11 highLightTest() no link', expected, line)

   line = 'A<a href="https:/aa/bbh.html">bb</a>Z'
   line = highLight(line, 'bb') 
   const expected2 = "A<a href=\"https:/aa/bbh.html\"><id style='color:red'>bb</id></a>Z"
   updateTestMsg('13 highLightTest() 2 link', expected2, line)

   line = "A<a href='https:/aa/bbh.html'>bb</a>Z"
   line = highLight(line, 'bb') 
   const expected3 = "A<a href='https:/aa/bbh.html'><id style='color:red'>bb</id></a>Z"
   updateTestMsg('14 highLightTest() 3 link single quote', expected3, line)

   line = "A<a href='https:/aa/bbh.html'>bb</a>Z--B<a href='https:/xx/bb.HTML'>bbx</a>W"
   line = highLight(line, 'bb') 
   const expected4 = "A<a href='https:/aa/bbh.html'><id style='color:red'>bb</id></a>Z--"+
              "B<a href='https:/xx/bb.HTML'><id style='color:red'>bb</id>x</a>W"
   updateTestMsg('15 highLightTest() 4 links', expected4, line)

   line = "A<a href='https:/aa/bbh.html'>bb</a>Z--B<a href='https:/xx/bb.HTML'>bbx</a>Wbb--"
   line = highLight(line, 'bb') 
   expected5 = "A<a href='https:/aa/bbh.html'><id style='color:red'>bb</id></a>Z--" +
              "B<a href='https:/xx/bb.HTML'><id style='color:red'>bb</id>x</a>W" +
              "<id style='color:red'>bb</id>--"
   updateTestMsg('16 highLightTest() 5links + text', expected5, line)
}


function updateTestMsg(testName, expected, actual) {
   console.log('* testName='+ testName)
   const isPass = expected == String(actual);
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
   var displayMsgs = document.getElementById("search-results").innerHTML;
   if (displayMsgs.length >  0) {
      displayMsgs += '\n';
   }
   displayMsgs += status ; 
   document.getElementById("search-results").innerHTML = displayMsgs
}


