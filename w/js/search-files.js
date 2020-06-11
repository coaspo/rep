function searchContentsMain(debug, filePathsFile) {
  'use strict';
  window.debug = debug;
  window.inputText = document.getElementById('inputText').value.trim();
  if (window.debug) console.log('*searchContentsMain() window.inputText= ' + window.inputText);
  document.getElementById("search-results").innerHTML = 'Wait... searching web pages'
  
  const search = searchFiles(inputText, filePathsFile);
  if (window.debug) console.log('*searchContentsMain() search.html= ' + search.html);     
  if (window.debug) console.log('*searchContentsMain() search.hitUrl= ' + search.hitUrl);     
  document.getElementById("search-results").innerHTML = search.html;
  if (search.hitUrl != '') {
    window.open(search.hitUrl, "_self");
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
  const url = baseUrl + searchFilesPathsFile;
  if (window.debug) console.log('*getFileUrls() url= ' + url);
  const html = readText(url);

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
   const baseUrl = getBaseUrl()
   const fileUrls = getFileUrls(baseUrl, filePathsFile)
   window.numOfmatchedLines = 0
   if (window.debug) console.log('*searchFiles() inputText = '+inputText)  
   if (inputText.length === 0) {
     search = {};
     search.html = '';   
     search.hitUrl = '';   
     return search;
   }

  result = scanProblemfiles(fileUrls, inputText)
  search = annotateResults(result, inputText)

  if (search.html.length === 0) {
    search.html = 'Did not find: "' + inputText + '"';
  } 
  return search;
}

function scanProblemfiles(fileUrls, inputText) {
  result = {};
  result.urls = '';
  result.html = '';   
  for (i = 0; i < fileUrls.length; i++) {
    var url = fileUrls[i];
    if (window.debug) console.log('*scanProblemfiles() url = '+url)  
    if (url.indexOf(inputText) > -1) {
      result.urls += (result.urls.length > 0 ? '##' : '') + url; 
    }
    if (url.indexOf('problem') < 0) {
       continue;
    }
    // scan text of problem files.
    var text = readText(url);
    const iStart = text.indexOf('<body');
    text = text.substr(iStart).trim().replace(/\r/, '');
    fileSearchResult = findTextInParagraphs(inputText, text)

    if (fileSearchResult.length > 0) {
      if (result.html.length > 0) {
        result.html += '\n\n';
      }
      result.html = result.html  + '<a href="' + url + '">' + fileName(url) + '</a>: ' + fileSearchResult;
    }
    if (window.debug) console.log('*scanProblemfiles() finished search in url= '+url);
  }
  return result;
}


function annotateResults(result, inputText) {
  search = {};
  search.html = result.html;   
  search.hitUrl = '';   
  if (result.urls.length > 0) {
    urls = result.urls.split('##');
    if (urls.length == 1 && (result.html.length === 0 || window.numOfmatchedLines == 1)) {
      search.hitUrl = urls[0]
    }
    html = ''
    for (var i=0; i<urls.length; i++) {
      name = fileName(urls[i])
      name = name.replace(inputText, "<id style='color:red'>" + inputText + "</id>");
      html = html + '\n<a href="' + urls[i] + '">' + name + '</a>';
    }
    html = html.trim()
    if (result.html.length > 0) {
      search.html = html + '\n\n'+ result.html;
    } else {
      search.html = html
    }
  } 
  if (window.debug) console.log('*annotateResults() search.html= ' + search.html+'\nsearch.hitUrl= '+search.hitUrl);
  return search;
}

  function readText(url) {
    var req = new XMLHttpRequest();
    req.open('GET', url, false); // `false` makes the request synchronous
    req.send(null);
    if (req.status === 200) {
      text = req.responseText.trim();
    } else {
      text = req.status + ' on reading: ' + url;
      console.log('*readText() text= ' + text)
    }
    if (window.debug) console.log('*readText() text= ' + text)
    return text
  }


  function fileName(url) {
    const i1 = url.lastIndexOf('/w/') + 3;
    const name = url.substring(i1);
    return name;
  }

  function getAnchors(baseUrl, filePath) {
    const url = baseUrl + filePath;
    if (window.debug) console.log('*getAnchors() url= ' + url)
    const text = readText(url)
    return text;
  }
  
  function scanAnchors(linksText, inputText) {
    result = {};
    result.html = '';   
    result.hitUrl = '';   
    if (linksText.indexOf(inputText) < 0) {
      return result;
    }
    lines = linksText.split('\n');
    for (var i=0; i<lines.length; i++) {
      if (lines[i].indexOf(inputText) < 0) {
        continue;
      }
      fields = lines[i].split('$$').toLowerCase()
      anchors = fields[0].split('##')
      //if (links.indexOf(inputText) > -1
      filepath = fields[1]
      console.log(i+' ' + filepath)
    }
  }

  function getAnchorLabels(anchors) {
    labels = new Array(anchors.length);
    for (var i=0; i<anchors.length; i++) {
      iStart = anchors[i].indexOf('>') + 1
      deltaI = anchors[i].indexOf('<', iStart) -iStart
      console.log(iStart + '  ' + iEnd)
      labels[i] = anchors[i].substr(iStart, deltaI);
    }
    return labels;
  }
