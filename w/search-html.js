	function match_text_in_lines(search_text, lines) {
		match = {};
		match.display_html = '';
		match.first_matched_link = ''
		match.title = false

		for (var j = 0; j < lines.length; j++) {
			var line = lines[j];
			console.log('---'+line)
			if (line.indexOf(search_text) > -1) {
			    if (line.indexOf('<title>') > -1) {
					continue
				}
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
