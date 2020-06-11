function findTextInParagraphs(search_text, text) {
  console.log(text)
  text = text.toString().toLowerCase();
  if (text.indexOf(search_text) < 0) {
    return '';
  }
  var fileSearchResult = '';
  paragraphs = text.split('\n\n');
  
  for (var j = 0; j < paragraphs.length; j++) {
    var paragraph = paragraphs[j].toLowerCase();
    if (paragraph.indexOf(search_text) > -1) {
      paragraph = paragraph.replace(/<br>/g, '');
      paragraph = paragraph.replace(/<li>/g, '');
      paragraph = paragraph.replace(/<\/li>/g, '');
      if (fileSearchResult.length > 0) {
        fileSearchResult += '\n\n';
      }
      paragraph = paragraph.replace('<br>', "").replace('<p>', "");
      paragraph = paragraph = highLight(paragraph, search_text) 
      fileSearchResult += paragraph;
      window.numOfmatchedLines++;
    }
  }
  if (window.debug) console.log('*matchTextInLines() fileSearchResult=' + fileSearchResult)
  return fileSearchResult;
}


const urlRe = new RegExp('<a href(.+?)##(.+?)@@(.+?)>', 'g');

function highLight(text, search_text) {
   var count = (text.match(/href/g) || []).length;
   const re = new RegExp(search_text, 'g');
   if (count == 0) {
     text = text.replace(re, "<id style='color:red'>" + search_text + "</id>");
     return text;
   }
   // highlight text that is not in href="..."
   text = text.replace(re, "##" + search_text + "@@");
   if (window.debug) console.log('*highLight() text='+text)
   text = text.replace(urlRe,  '<a href$1$2$3>')
   if (window.debug) console.log('*highLight() text='+text)
   text = text.split("##").join("<id style='color:red'>"); 
   text = text.split("@@").join("</id>"); 
   if (window.debug) console.log('*highLight() text='+text)
   return text;
}

function toParagraphs(lines) {
  text = '';
  for (var i = 0; i < lines.length; i++) {
    var line = lines[i];
    if (line.length == 0) {
      text += '?$';
    } else {
      if (text.length > 0) { 
        text += '\n';
      }
    }
    text += line;
  }
  paragraphs = text.split('?$');
  for (var i = 0; i < paragraphs.length; i++) {
    paragraphs[i] = paragraphs[i].trim();
  }
  if (window.debug) console.log('*toParagraphs() paragraphs=' + paragraphs);
  return paragraphs
}
