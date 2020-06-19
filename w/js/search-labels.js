function searchFileIndex(inputText, searchFileUrls, searchLabels) {
  const result = {};
  result.html = '';   
  result.url = '';   
  result.urlCount = 0;   
  prevFileIndex = -1
  for (var i=0; i<searchLabels.length; i++) {
    const fields = searchLabels[i]
    var label = fields[0]
    if (label.indexOf(inputText) < 0) {
      continue;
    }
    const fileIndex = fields[1]
    if (prevFileIndex != fileIndex) {
      prevFileIndex = fileIndex
      if (result.html.length >0) {
        result.html += '\n\n'
      }
      result.html += getLink(searchFileUrls[fileIndex]) + ':'
    }
    label = highLight(label, inputText) 
    if (fields.length ==3) {
      result.urlCount++;
      url = fields[2]
      result.html += ' <a href="' + url + '">' + label + '</a>'
      result.url = url 
    } else {
      result.html += label 
    }
  }
  if (result.urlCount > 1 && result.html.length > 0) {
    result.url = 'NA'
  }
  console.log('*searchIndexedLabels() ====1=' + result.urlCount)
  console.log('*searchIndexedLabels() r===2=' + result.html.length)
  console.log('*searchIndexedLabels() ===3=' + result.html)
  console.log('*searchIndexedLabels() ===4=' + result.url)
  if (window.DEBUG) console.log('*searchIndexedLabels() result.html=' + result.html)
  return result
}


function searchUrls(inputText, searchFileUrls) {
  const result = {};
  result.html = '';   
  result.url = '';   
  result.numOfUrls = 0;
  for (var i=0; i<searchFileUrls.length; i++) {
    const url = searchFileUrls[i]
    var label = getUrlLabel(url).toLowerCase()
    if (label.indexOf(inputText) > -1) {
      if (result.html.length > 0) {
        result.html += '\n'
      }
      result.numOfUrls++;
      label = highLight(label, inputText)
      result.html += '<a href="' + url + '">' + label+ '</a>'
      result.url = url
    }
  }
  if (result.numOfUrls > 1 && result.html.length > 0) {
    result.url = 'NA'
  }
  if (window.DEBUG) console.log('*searchUrlLabels() result=' + result)
  return result
}
  
  
function getUrlLabel(url) {
  const i1 = url.lastIndexOf('/w/') + 3;
  const label = url.substring(i1);
  return label;
}


function getLink(url) {
  const label = getUrlLabel(url)
  const link = '<a href="' + url + '">' + label + '</a>'
  return link;
}

