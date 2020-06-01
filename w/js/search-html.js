function findTextInLines(search_text, lines, useParagraphs) {
        if (useParagraphs) {
                lines = toParagraphs(lines)
        }
        fileSearchResult = '';
        var re = new RegExp(search_text, 'g');
        
        for (var j = 0; j < lines.length; j++) {
                var line = lines[j].toLowerCase();
                if (line.indexOf(search_text) > -1) {
                        line = line.replace(/<br>/g, '');
                        line = line.replace(/<li>/g, '');
                        line = line.replace(/<\/li>/g, '');
                        if (fileSearchResult.length > 0) {
                           fileSearchResult += '\n'; 
                           if (useParagraphs) {
                              fileSearchResult += '\n';
                           }
                        }
                        line = line.replace('<br>', "").replace('<p>', "");
                        line = line = highLight(line, search_text) 
                        fileSearchResult += line;
                        window.numOfmatchedLines++;
                }
        }
        if (window.debug) console.log('*matchTextInLines() fileSearchResult=' + fileSearchResult)
        return fileSearchResult;
}


const urlRe = new RegExp('<a href(.+?)##(.+?)@@(.+?)>', 'g');

function highLight(line, search_text) {
   var count = (line.match(/href/g) || []).length;
   const re = new RegExp(search_text, 'g');
   if (count == 0) {
     line = line.replace(re, "<id style='color:red'>" + search_text + "</id>");
     return line;
   }
   // highlight text that is not in href="..."
   line = line.replace(re, "##" + search_text + "@@");
   if (window.debug) console.log('*highLight() line='+line)
   line = line.replace(urlRe,  '<a href$1$2$3>')
   if (window.debug) console.log('*highLight() line='+line)
   line = line.split("##").join("<id style='color:red'>"); 
   line = line.split("@@").join("</id>"); 
   if (window.debug) console.log('*highLight() line='+line)
   return line;
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
