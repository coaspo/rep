function testSearchMain() {
   testReadText();
   searchContentsMainTest();
   getFileUrlsTest();
   readTextTest();
   getSearchLabelsTest();
}

function testReadText() {
  try {
     js = readText('https://api.weather.gov/gridpoints/BOX/68,81/forecast')
     var w = JSON.parse(js)
     console.log(w.properties.periods[0]['detailedForecast'])
     validate('0 search.js:readText()   ', 'readforcast', 'readforcast');
  } catch (err) {
    validate('0 search.js:readText()   ', '', err);
  }
}

function searchContentsMainTest() {
   document.getElementById('inputText').value = '  '
   searchContentsMain(true, '/tests/search_file_paths__t.txt', '/tests/search_labels__t.txt')
   const actual= document.getElementById("search-results").innerHTML
   validate('1 search.js:searchContentsMain()  innerHTML ', '', actual);
}


function getFileUrlsTest() {
   const searchFileUrls = getFileUrls(window.BASE_URL, '/tests/search_file_paths__t.txt')
   const expected = [ window.BASE_URL + "/tests/search-files/category/words.html",
                window.BASE_URL + "/tests/search-files/links-2.html",
                window.BASE_URL + "/tests/search-files/links.html",
                window.BASE_URL + "/tests/search-files/problems-examples.html",
                window.BASE_URL + "/tests/search-files/problems-solutions.html",
                window.BASE_URL + "/tests/search-files/recipe.html" ]
   validate('2 search.js:getFileUrls()', expected, searchFileUrls);
}


function readTextTest() {  
   const text = readText(window.BASE_URL + '/tests/search_labels__t.txt');
   const expected = 'wolfram$$1$$https://www.wolfram.com/\n\
worldometers$$1$$https://www.worldometers.info/\n\
week in virology$$1$$https://www.microbe.tv/twiv/archive/\n\
internet archive$$2$$https://archive.org\n\
free books$$2$$https://www.freebookcentre.net/\n\
coursera- free course$$2$$https://www.coursera.org/\n\
edx - mit, harvard$$2$$https://www.edx.org/\n\
pizza$$5\n\
serve done$$5'
   validate('3 search.js:readText()', expected, text)
}

function getSearchLabelsTest() {
   const searchLabels = getSearchLabels(window.BASE_URL, '/tests/search_labels__t.txt')
   const expected = [["wolfram", "1", "https://www.wolfram.com/"],
            ["worldometers", "1", "https://www.worldometers.info/"],
            ["week in virology", "1", "https://www.microbe.tv/twiv/archive/"],
            ["internet archive", "2", "https://archive.org"],
            ["free books", "2", "https://www.freebookcentre.net/"],
            ["coursera- free course", "2", "https://www.coursera.org/"],
            ["edx - mit, harvard", "2", "https://www.edx.org/"],
            ["pizza", "5"],
            ["serve done", "5"]];
   validate('4 search.js:getSearchLabels()', expected, searchLabels);
}


