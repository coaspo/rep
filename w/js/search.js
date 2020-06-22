// Globals to minimize reading reference URLs; used only in the first function below.  
window.SEARCH_FILE_URLS
window.SEARCH_LABELS
window.BASE_URL


function searchContentsMain(debug, filePathsFilePath, labelsFilePath) {
  'use strict';
  window.DEBUG = debug;
  const inputText = document.getElementById('inputText').value.toLowerCase().trim();
  if (window.DEBUG) console.log('*searchContentsMain() inputText= ' + inputText);     
  if (typeof window.BASE_URL === 'undefined') {
    window.BASE_URL = getBaseUrl()
    window.SEARCH_FILE_URLS = getFileUrls(window.BASE_URL, filePathsFilePath)
    window.SEARCH_LABELS = getSearchLabels(window.BASE_URL,labelsFilePath)
  }
  if (inputText.length == 0) {
    document.getElementById("search-results").innerHTML = ''
    return;
  }

  if (window.DEBUG) console.log('*searchContentsMain() window.inputText= ' + inputText);
  document.getElementById("search-results").innerHTML = 'Wait... searching web pages'
  
  const result = searchContents(inputText, window.SEARCH_FILE_URLS, window.SEARCH_LABELS);
  if (window.DEBUG) console.log('*searchContentsMain() search.html= ' + result.html);     
  if (window.DEBUG) console.log('*searchContentsMain() search.hitUrl= ' + result.hitUrl);     
  document.getElementById("search-results").innerHTML = result.html;
  if (result.hitUrl != '') {
    window.open(result.hitUrl, "_self");
  }
}


function getBaseUrl() {
  const url = String(document.URL);
  const i_base = url.indexOf('/w/') + 2;
  baseUrl = url.substr(0, i_base);
  if (window.DEBUG) console.log('*getBaseUrl() baseUrl= ' + baseUrl)
  return baseUrl
}


function getFileUrls(baseUrl, filePathsFilePath) {
  const url = baseUrl +filePathsFilePath
  if (window.DEBUG) console.log('*getFileUrls() url= ' + url);
  const html = readText(url);

  const lines = html.trim().split('\n');
  var fileUrls = [];

  for (var i = 0; i < lines.length; i++) {
    fileUrls[i] = window.BASE_URL + lines[i];
  }
  if (window.DEBUG) console.log('*getFileUrls() paths=\n' + 
                    String(fileUrls).replace(/,/g, '\n'));
  return fileUrls;
}


function getSearchLabels(baseUrl, labelsFilePath) {
  const url = baseUrl + labelsFilePath
  if (window.DEBUG) console.log('*getSearchLabels() url= ' + url);
  const labelText = readText(url);

  const lines = labelText.trim().split('\n');
  var labels = [];

  for (var i = 0; i < lines.length; i++) {
    var fields = lines[i].split('$$')
    labels[i] = fields;
  }
  if (window.DEBUG) console.log('*getSearchLabels() labels=\n' + String(labels));
  return labels;
}


function readText(url) {
  if (window.DEBUG) console.log('*readText() url= ' + url);
  var req = new XMLHttpRequest();
  req.open('GET', url, false); // `false` makes the request synchronous
  try {
    req.send(null);
  } catch (err) {
    throw err + ' on reading: ' + url;
  }
  if (req.status === 200) {
    text = req.responseText.trim();
  } else {
    text = req.status + ' on reading: ' + url;
    console.log('*readText() ERR text= ' + text)
    throw text
  }
  if (window.DEBUG) console.log('*readText() text= ' + text)
  return text
}


function searchContents(inputText, searchFileUrls, searchLabels) {
  if (window.DEBUG) console.log('*searchFiles() inputText = '+inputText)  

  const problemsHtml = scanProblemfiles(searchFileUrls, inputText)
  const urlResult = searchUrls(inputText, searchFileUrls)
  const indexResult = searchFileIndex(inputText, searchFileUrls, searchLabels) 
  
  var result = {};
  result.html = urlResult.html + '\n\n' + indexResult.html + '\n\n' + problemsHtml
  result.html = result.html.replace('\n\n\n\n','')   
  if (result.html.length === 0) {
    result.html = 'Did not find: "' + inputText + '"';
  } else  if ((problemsHtml.length + urlResult.numOfUrls + indexResult.urlCount) == 1) {
     result.hitUrl = urlResult.url + indexResult.url
  }
  return result;
}


function weather() {
  const js = readText('https://api.weather.gov/gridpoints/BOX/68,81/forecast')
  console.log('*weather() js = '+js)  
  const w = JSON.parse(js)
  const url = weatherPeriod(0, w.properties.periods)
  const url2 = weatherPeriod(1, w.properties.periods)
  return url + '<br>'+url2
}

function weatherPeriod(i, periods) {
  const forecast = periods[i]['shortForecast']
  const temp = periods[i]['temperature']
  const detailed = periods[i]['detailedForecast']
  const url = '<a href="https://forecast.weather.gov/MapClick.php?lat=42.482&amp;lon=-71.0973&amp;unit=0&amp;lg=english&amp;FcstType=graphical"  title="'+detailed+ '">' +
         temp+ ' '+forecast + '</a>'
  return url
}

try {
  document.getElementById("weather").innerHTML = weather()
} catch (err) {
  document.getElementById("search-results").innerHTML = err
}


