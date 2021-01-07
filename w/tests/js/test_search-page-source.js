function testSearchPageSourceMain() {
   findParagraphsTest();
   highLightTest();
}


function findParagraphsTest() {  
   text = readText(window.BASE_URL + '/tests/search-files/problems-solutions.html');

   file_search_result = findParagraphs('sudo', text)
   const expected = 'use fire wall\n'+
              'answer: <id style=\'color:red\'>sudo</id> gedit..\n'+
              '        add line..';
   validate('0 search-page-source.js:findParagraphs(),problems', expected, file_search_result)

   file_search_result = findParagraphs('use', text)
   const expected2 = '<id style=\'color:red\'>use</id> snipping tool\n'+
              'answer: shift-prtscn\n'+
              '\n'+
              '<id style=\'color:red\'>use</id> fire wall\n'+
              'answer: sudo gedit..\n'+
              '        add line..';
   validate('1 search-page-source.js:findParagraphs(),problems', expected2, file_search_result)
}


function highLightTest() {
   line = 'abAAbc'
   line = highLight(line, 'b') 
   const expected = "a<id style='color:red'>b</id>AA<id style='color:red'>b</id>c"
   validate('3 search-page-source.js:highLight() no link', expected, line)

   line = 'A<a href="https:/aa/bbh.html">bb</a>Z'
   line = highLight(line, 'bb') 
   const expected2 = "A<a href=\"https:/aa/bbh.html\"><id style='color:red'>bb</id></a>Z"
   validate('4 search-page-source.js:highLight() 2 link', expected2, line)

   line = "A<a href='https:/aa/bbh.html'>bb</a>Z"
   line = highLight(line, 'bb') 
   const expected3 = "A<a href='https:/aa/bbh.html'><id style='color:red'>bb</id></a>Z"
   validate('5 search-page-source.js:highLight() 3 link single quote', expected3, line)

   line = "A<a href='https:/aa/bbh.html'>bb</a>Z--B<a href='https:/xx/bb.HTML'>bbx</a>W"
   line = highLight(line, 'bb') 
   const expected4 = "A<a href='https:/aa/bbh.html'><id style='color:red'>bb</id></a>Z--"+
              "B<a href='https:/xx/bb.HTML'><id style='color:red'>bb</id>x</a>W"
   validate('6 search-page-source.js:highLight() 4 links', expected4, line)

   line = "A<a href='https:/aa/bbh.html'>bb</a>Z--B<a href='https:/xx/bb.HTML'>bbx</a>Wbb--"
   line = highLight(line, 'bb') 
   expected5 = "A<a href='https:/aa/bbh.html'><id style='color:red'>bb</id></a>Z--" +
              "B<a href='https:/xx/bb.HTML'><id style='color:red'>bb</id>x</a>W" +
              "<id style='color:red'>bb</id>--"
   validate('7 search-page-source.js:highLight() 5links + text', expected5, line)
}
