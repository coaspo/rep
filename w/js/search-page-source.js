function scanProblemFiles(fileUrls, inputText) {
  let html = '';   
  for (i = 0; i < fileUrls.length; i++) {
    const url = fileUrls[i];
    if (window.DEBUG) console.log('*scanProblemFiles() url = '+url)
    if (url.indexOf('problem') < 0) {
       continue;
    }
    // scan text of problem files.
    let text = readText(url);
    const iStart = text.indexOf('<body');
    text = text.substr(iStart).trim().replace(/\r/, '');
    const foundParagraphs = findParagraphs(inputText, text)

    if (foundParagraphs.length > 0) {
      if (html.length > 0) {
        html += '\n\n';
      }
      html = html  + '<a href="' + url + '">' + getUrlLabel(url) + '</a>: ' + foundParagraphs;
    }
    if (window.DEBUG) console.log('*scanProblemFiles() finished search in url= '+url);
  }
  return html;
}


function findParagraphs(inputText, text) {
  if (window.DEBUG) console.log('*findParagraphs() text.length='+ text.length+ ' inputText=' +inputText)
  text = text.toString().toLowerCase();
  if (text.indexOf(inputText) < 0) {
    return '';
  }
  var foundParagraphs = '';
  const paragraphs = text.split('\n\n');
  
  for (let j = 0; j < paragraphs.length; j++) {
    let paragraph = paragraphs[j].toLowerCase();
    if (paragraph.indexOf(inputText) > -1) {
      paragraph = paragraph.replace(/<br>/g, '');
      paragraph = paragraph.replace(/<li>/g, '');
      paragraph = paragraph.replace(/<\/li>/g, '');
      if (foundParagraphs.length > 0) {
        foundParagraphs += '\n\n';
      }
      paragraph = paragraph.replace('<br>', "").replace('<p>', "");
      paragraph = paragraph = highLight(paragraph, inputText) 
      foundParagraphs += paragraph;
      window.numOfmatchedLines++;
    }
  }
  if (window.DEBUG) console.log('*findParagraphs() foundParagraphs=' + foundParagraphs)
  return foundParagraphs;
}


const urlRe = new RegExp('<a href(.+?)##(.+?)@@(.+?)>', 'g');


function highLight(html, inputText) {
   const count = (html.match(/href/g) || []).length;
   const re = new RegExp(inputText, 'g');
   if (count == 0) {
     html = html.replace(re, "<id style='color:red'>" + inputText + "</id>");
     return html;
   }
   // highlight html that is not in href="..."
   html = html.replace(re, "##" + inputText + "@@");
   if (window.DEBUG) console.log('*highLight() html='+html)
   html = html.replace(urlRe,  '<a href$1$2$3>')
   if (window.DEBUG) console.log('*highLight() html='+html)
   html = html.split("##").join("<id style='color:red'>"); 
   html = html.split("@@").join("</id>"); 
   if (window.DEBUG) console.log('*highLight() html='+html)
   return html;
}

