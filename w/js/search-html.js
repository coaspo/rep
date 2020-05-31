function matchTextInLines(search_text, lines, useParagraphs) {
        if (useParagraphs) {
                lines = toParagraphs(lines)
        }
        search_text = search_text.toLowerCase();
        file_search_result = '';
        var re = new RegExp(search_text, 'g');
        
        for (var j = 0; j < lines.length; j++) {
                var line = lines[j].toLowerCase();
                if (line.indexOf(search_text) > -1) {
                        line = line.replace(/<br>/g, '');
                        line = line.replace(/<li>/g, '');
                        line = line.replace(/<\/li>/g, '');
                        //line = line.replace(/</g, '&lt;')
                        if (file_search_result.length > 0) {
                           file_search_result += '\n'; 
                           if (useParagraphs) {
                              file_search_result += '\n';
                           }
                        }
                        line = line.replace('<br>', "").replace('<p>', "");
                        line = line = highLight(line, search_text) 
                        file_search_result += line;
                }
        }
        if (window.debug) console.log('*file_search_result=' + file_search_result)
        return file_search_result;
}


function highLight(line, search_text) {
   var count = (line.match(/href/g) || []).length;
   if (count == 0) {
     const re = new RegExp(search_text, 'g');
     line = line.replace(re, "<id style='color:red'>" + search_text + "</id>");
     return line;
   }
   const re = new RegExp(search_text, 'g');
   line = line.replace(re, "##" + search_text + "@@");
   if (window.debug) console.log('*highLight() line='+line)
   const re2 = new RegExp('<a href(.+?)##(.+?)@@(.+?)>', 'g');// /<a href(.*)##(.*)@@">/g; 
   line = line.replace(re2,  '<a href$1$2$3>')
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
