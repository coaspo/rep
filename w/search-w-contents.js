function search() {
  search_paths = search_file_paths();
  //alert('file_list=\n' + String(search_paths).replace(/,/g,'\n'));
  var search_text = document.getElementById('inputText').value.trim()
  //alert('search_text = '+search_text)
  if (search_text.length == 0) {
	  document.getElementById("search-results").innerHTML = "";
	  return;
  }
  html = search_text_in_files(search_text, search_paths)
  //alert('html='+html)

  if (html.length == 0) {
	  html = 'Did not find: "'+ search_text + '"';
  }
  document.getElementById("search-results").innerHTML = html
}


function search_file_paths() {
  url = String(document.URL)
  i_base = url.indexOf('/w/') + 3
  base_url = url.substr(0, i_base)
   
  all_paths = file_paths(base_url, 'tech');
  paths = file_paths(base_url, 'food')
  all_paths = all_paths.concat(paths);
  paths = file_paths(base_url, 'excercise')
  all_paths = all_paths.concat(paths);
  paths = file_paths(base_url, 'artScience')
  all_paths = all_paths.concat(paths);
  return all_paths
}


function search_text_in_files(search_text, search_paths) {
  html = ''
  for (i = 0; i < search_paths.length; i++) {
	  url = search_paths[i]
	  lines = read_lines(url) 
	  matched_text = ''
	  
	  for (j = 0; j < lines.length; j++) {
		  line = lines[j];
		  if (line.indexOf('<a href') < 0) {			  
	         line = lines[j].replace(/</g, '&lt;').replace(/>/g, '&gt;')
	      }
		  if (line.indexOf(search_text) > -1) {
		    matched_text = j + ': ' + line 
		    if (line.indexOf('<br>') < 0) {
		      matched_text = matched_text + '<br>'
		    }
		  }
      }
      
      if (matched_text.length > 0) {
		  html = html+ '<a href="' + url + '">' + file_name(url) + '</a>:<br>' + matched_text+'\n'
      }
  }
  return html
}


function read_lines(url) {
  var req = new XMLHttpRequest();
  req.open('GET', url, false);  // `false` makes the request synchronous
  req.send(null);
  
  if (req.status === 200) {
	i_start = req.responseText.indexOf('<pre>') + 5
    return req.responseText.substr(i_start).split('\n');
  }
  return [req.status+ ' on reading:' + url]
}	    


function file_name(url) {
	i1 = url.lastIndexOf('/') + 1
	i2 = url.length - 5
    name = url.substring(i1, i2)
    return name
}

	
function file_paths(base_url, dir_name) {
    req = new XMLHttpRequest(); 
    url = base_url + dir_name
    req.open("GET", url, false);
    req.send();
    html = req.responseText
    
    lines = html.split('\n')
	var paths = []
	var j = 0;
	
	for (i = 0; i < lines.length; i++) {
	  var i1 = lines[i].indexOf('href=')
	  if (i1 > 0) {
		var i2 = lines[i].indexOf('>', i1) - 1
		var file_name = lines[i].substring(i1+6, i2)
		  paths[j]= base_url + dir_name + '/' + file_name
		  j++
	  }
	}
	return paths
}

