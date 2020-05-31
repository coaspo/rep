function searchContentsMain(debug, filePathsFile) {
  'use strict';
  window.debug = debug;
  window.inputText = document.getElementById('inputText').value.trim();
  if (window.debug) console.log('*searchContentsMain() window.inputText= ' + window.inputText);
  
  const search = searchFiles(inputText, filePathsFile);
  if (window.debug) console.log('*searchContentsMain() search= ' + search);     
  document.getElementById("search-results").innerHTML = search.html;
  return search;
}


function possiblyShowDoc(docLink) {
  if (search.docLink.length === 0) {
    return
  }
}


function getBaseUrl() {
  const url = String(document.URL);
  const i_base = url.indexOf('/w/') + 2;
  const baseUrl = url.substr(0, i_base);
  if (window.debug) console.log('*getBaseUrl() baseUrl= ' + baseUrl)
  return baseUrl;
}


function getFileUrls(baseUrl, searchFilesPathsFile) {
  var req = new XMLHttpRequest();
  const url = baseUrl + searchFilesPathsFile;
  if (window.debug) console.log('*getFileUrls() url= ' + url);
  req.open("GET", url, false); // synchronous - browser may disable this???
  req.send();
  const html = req.responseText;

  const lines = html.trim().split('\n');
  var fileUrls = [];

  for (var i = 0; i < lines.length; i++) {
    fileUrls[i] = baseUrl + lines[i];
  }
  if (window.debug) console.log('*getFileUrls() paths=\n' + String(fileUrls).replace(/,/g, '\n'));
  return fileUrls;
}


function searchFiles(inputText, filePathsFile) {
   search = {};
   search.docLink = '';
   search.html = '';   
   const baseUrl = getBaseUrl()
   const fileUrls = getFileUrls(baseUrl, filePathsFile)
   if (window.debug) console.log('*searchFiles() inputText = '+inputText)  
   if (inputText.length === 0) {
     return search;
   }
   numOfUrlMatches = 0;

  for (i = 0; i < fileUrls.length; i++) {
    url = fileUrls[i];
    if (url.indexOf(inputText) > -1) {
      search.docLink = '<a href="' + url + '">' + fileName(url) + '</a>'
      numOfUrlMatches++;
    }

    const lines = readLines(url);
    fileSearchResult = matchTextInLines(inputText, lines)

    if (fileSearchResult.length > 0) {
      if (search.html .length > 0) {
        search.html  += '\n\n';
      }
      search.html  = search.html  + '<a href="' + url + '">' + fileName(url) + '</a>: ' + fileSearchResult;
    }
    if (window.debug) console.log('*searchFiles() found text in: url= '+url);
  }
  
  if (window.debug) ('*searchFiles() numOfUrlMatches= '+numOfUrlMatches+ " search.docLink= " + search.docLink);
  if (numOfUrlMatches > 1) {
     search.docLink = '';
  }

  if (search.html .length === 0) {
    if (search.docLink == '') {
      search.html  = 'Did not find: "' + inputText + '"';
    } else {
      search.html  = 'Found text in one file name; ' + search.docLink;
    }
  }
  if (window.debug) console.log('*searchFiles() search.html= ' + search.html+'\nsearch.docLink= '+search.docLink);
  return search;
}


  function readLines(url) {
    var req = new XMLHttpRequest();
    req.open('GET', url, false); // `false` makes the request synchronous
    req.send(null);

    if (req.status === 200) {
      const iStart = req.responseText.indexOf('<body>');
      if (window.debug) console.log('*readLines()responseText=' + req.responseText)
      lines = req.responseText.substr(iStart).trim().replace(/\r/, '');
      lines = lines.split('\n');
      lines.splice(0, 1);
      if (window.debug) console.log('*readLines() lines= ' + lines)
    } else {
      lines = [req.status + ' on reading: ' + url];
      console.log('*readLines() lines= ' + lines[0])
    }
    return lines
  }


  function matchTextInLines2(inputText, lines) {
    match = {};
    match.fileSearchResult = '';
    match.first_matched_link = ''

    for (var j = 0; j < lines.length; j++) {
      var line = lines[j];
      
      if (line.indexOf(inputText) > -1) {
        line = line.replace(/<br>/g, '');
        line = line.replace(/<li>/g, '');
        line = line.replace(/<\/li>/g, '');
        match.fileSearchResult += '<br>' + j + ': ' + line;

        var k1 = line.indexOf('<a href');
        if (k1 < 0) {
          line = lines[j].replace(/</g, '&lt;').replace(/>/g, '&gt;');
          if (match.first_matched_link === '') {
            var k2 = line.indexOf('>', k1);
            match.first_matched_link = line.substring(k1 + 7, k2);
          }
        }
      }
    }
    return match  
  }


  function fileName(url) {
    const i1 = url.lastIndexOf('/w/') + 3;
    const name = url.substring(i1);
    return name;
  }
