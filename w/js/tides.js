function getTides() {
  var today = new Date();
  time = today.toTimeString();
  ts1 = today.toISOString().replace(/-/g,'').substr(0,8) + ' ' + time.substr(0,5);
  var tommorow = new Date(new Date().getTime() + 24 * 60 * 60 * 1000);
  ts2 = tommorow.toISOString().replace(/-/g,'').substr(0,8) + ' ' + time.substr(0,5);
  url='https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?begin_date='+ ts1 +
  '&end_date=' + ts2 +'&station=8443970&product=predictions&interval=15&datum=mllw'+
  '&units=english&time_zone=lst_ldt&application=web_services&format=json';
  const js = readText('url')
  const w = JSON.parse(js)
  const url1 = weatherPeriod(0, w.properties.periods)
  const url2 = weatherPeriod(1, w.properties.periods)
  const url3 = weatherPeriod(2, w.properties.periods)
  html = url1+ '<br>' + url2 + '<br>' + url3
  try {
    return html
  } catch (err) {
    return 'get weather ERR '
  }
}


function readText(url) {
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
    throw text
  }
  return text
}
data:text/html,<script>
var today = new Date();
time = today.toTimeString();
ts1 = today.toISOString().replace(/-/g,'').substr(0,8) + ' ' + time.substr(0,5);
var tommorow = new Date(new Date().getTime() + 24 * 60 * 60 * 1000);
ts2 = tommorow.toISOString().replace(/-/g,'').substr(0,8) + ' ' + time.substr(0,5);
url='https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?begin_date='+ ts1 +
'&end_date=' + ts2 +'&station=8443970&product=predictions&interval=15&datum=mllw'+
'&units=english&time_zone=lst_ldt&application=web_services&format=json';
alert(url);</script>

