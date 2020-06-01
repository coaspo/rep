function searchContentsMain(debug, filePathsFile) {
  'use strict';
  window.debug = debug;
  window.inputText = document.getElementById('inputText').value.trim();
  if (window.debug) console.log('*searchContentsMain() window.inputText= ' + window.inputText);
  document.getElementById("search-results").innerHTML = 'Wait... searching web pages'
  
  const search = searchFiles(inputText, filePathsFile);
  if (window.debug) console.log('*searchContentsMain() search.html= ' + search.html);     
  if (window.debug) console.log('*searchContentsMain() search.url= ' + search.url);     
  document.getElementById("search-results").innerHTML = search.html;
  if (search.hitUrl != '') {
    window.open(search.hitUrl, "_self");
  }
}


function possiblyShowDoc(url) {
  if (search.url.length === 0) {
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
   inputText = inputText.trim().toLowerCase();
   search = {};
   search.urls = '';
   search.html = '';   
   search.hitUrl = '';   
   const baseUrl = getBaseUrl()
   const fileUrls = getFileUrls(baseUrl, filePathsFile)
   if (window.debug) console.log('*searchFiles() inputText = '+inputText)  
   if (inputText.length === 0) {
     return search;
   }

  for (i = 0; i < fileUrls.length; i++) {
    url = fileUrls[i];
    if (url.indexOf(inputText) > -1) {
      search.urls += (search.urls.length > 0 ? '##' : '') + url; 
    }

    const lines = readLines(url);
    useParagraphs = url.indexOf('problem') > -1
    fileSearchResult = findTextInLines(inputText, lines, useParagraphs)

    if (fileSearchResult.length > 0) {
      if (search.html .length > 0) {
        search.html  += '\n\n';
      }
      search.html  = search.html  + '<a href="' + url + '">' + fileName(url) + '</a>: ' + fileSearchResult;
    }
    if (window.debug) console.log('*searchFiles() finishe search in url= '+url);
  }
  
  if (window.debug) console.log('*searchFiles() search.urls= ' + search.urls);

  if (search.urls.length > 0) {
      urls = search.urls.split('##');
      if (urls.length == 1 && search.html.length === 0) {
        search.hitUrl = urls[0]
      }
      html = ''
      for (var i=0; i<urls.length; i++) {
        name = fileName(urls[i])
        name = name.replace(inputText, "<id style='color:red'>" + inputText + "</id>");
        html = html + '\n<a href="' + urls[i] + '">' + name + '</a>';
      }
      html = html.trim()
      if (search.html.length > 0) {
         search.html  = html + '\n\n'+ search.html;
      } else {
        
         search.html  = html
      }
  } 
  if (search.html.length === 0) {
    search.html  = 'Did not find: "' + inputText + '"';
  } 
  if (window.debug) console.log('*searchFiles() search.html= ' + search.html+'\nsearch.urls= '+search.urls);
  return search;
}


  function readLines(url) {
    var req = new XMLHttpRequest();
    req.open('GET', url, false); // `false` makes the request synchronous
    req.send(null);

    if (req.status === 200) {
      const iStart = req.responseText.indexOf('<body');
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


  function fileName(url) {
    const i1 = url.lastIndexOf('/w/') + 3;
    const name = url.substring(i1);
    return name;
  }
