function searchContentsMain(debug) {
	'use strict';
        window.debug = debug;
        window.inputText = document.getElementById('inputText').value.trim();
	if (window.debug) console.log('window.inputText= ' + window.inputText);
	const base_url = getBaseUrl()
        const fileUrls = getFileUrls(base_url, '/searcn_file_paths.txt')
	const search = searchFiles(window.inputText, fileUrls);
        if (window.debug) console.log('search= ' + search);	
        
	document.getElementById("search-results").innerHTML = search.html;
	possiblyShowDoc(search.docLink)
}


function searchFiles(inputText, fileUrls) {
	if (window.debug) console.log('inputText = '+inputText)	
	if (inputText.length === 0) {
		var search = {}
		search.html = ''
		search.docLink = '';
		return search;
	}
	var search = doSearch(inputText, fileUrls);
	return search
}

function possiblyShowDoc(docLink) {
	if (search.docLink.length === 0) {
		return
	}
}


function getBaseUrl() {
	const url = String(document.URL);
	const i_base = url.indexOf('/w/') + 2;
	const base_url = url.substr(0, i_base);
	if (window.debug) console.log('base_url= ' + base_url)
	return base_url;
}


function getFileUrls(base_url, searchFilesPathsFile) {
	var req = new XMLHttpRequest();
	const url = base_url + searchFilesPathsFile;
	if (window.debug) console.log('url= ' + url);
	req.open("GET", url, false); // synchronous - browser may disable this???
	req.send();
	const html = req.responseText;

	const lines = html.trim().split('\n');
	var fileUrls = [];

	for (var i = 0; i < lines.length; i++) {
		fileUrls[i] = base_url + lines[i];
	}
	if (window.debug) console.log('paths=\n' + String(fileUrls).replace(/,/g, '\n'));
	return fileUrls;
}


function doSearch(inputText, fileUrls) {
	search = {};
	search.docLink = '';
	search.html = '';

	for (i = 0; i < fileUrls.length; i++) {
		url = fileUrls[i];
		if (search.docLink === '' && url.indexOf(url) > -1) {
			search.docLink = '<a href="' + url + '">' + url +' </a>'
		}

		const lines = readLines(url);
		match = matchTextInLines(inputText, lines)

		if (match.display_html.length > 0) {
			if (search.html.length > 0) {
				search.html += '<br>';
			}
			search.html = search.html + '<a href="' + url + '">' + fileName(url) + '</a>:' + match.display_html;
		}
		if (search.docLink === '' && match.first_matched_link.length > 0) {
			search.docLink = match.first_matched_link
		}
		if (window.debug && search.docLink.length > 0) console.log('text in: url= '+url);
	}
	
	if (search.html.length === 0) {
		search.html = 'Did not find: "' + inputText + '"';
	}
	if (window.debug) console.log('search=\n' + search);
	return search;
}


	function readLines(url) {
		var req = new XMLHttpRequest();
		req.open('GET', url, false); // `false` makes the request synchronous
		req.send(null);

		if (req.status === 200) {
			const iStart = req.responseText.indexOf('<body>');
                        console.log('=======>')
                       console.log(req.responseText)
                       console.log('<=======')
                       lines = req.responseText.substr(iStart).trim().split('\n');
                       lines.splice(0, 1);
                        console.log('=======>')
                       console.log(lines)
                       console.log('<=======')
			return lines;
		}
		return [req.status + ' on reading:' + url];
	}


	function matchTextInLines2(inputText, lines) {
		match = {};
		match.display_html = '';
		match.first_matched_link = ''

		for (var j = 0; j < lines.length; j++) {
			var line = lines[j];
			
			if (line.indexOf(inputText) > -1) {
				line = line.replace(/<br>/g, '');
				line = line.replace(/<li>/g, '');
				line = line.replace(/<\/li>/g, '');
				match.display_html += '<br>' + j + ': ' + line;

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
		const i1 = url.lastIndexOf('/') + 1;
		const i2 = url.length - 5;
		const name = url.substring(i1, i2);
		return name;
	}
