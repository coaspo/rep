function getWeather() {
  const js = readText('https://api.weather.gov/gridpoints/BOX/68,81/forecast')
  const w = JSON.parse(js)
  const url1 = weatherPeriod(0, w.properties.periods)
  const url2 = weatherPeriod(1, w.properties.periods)
  const url3 = weatherPeriod(2, w.properties.periods)
  graphLink = "<a href='https://forecast.weather.gov/MapClick.php?lat=42.48&lon=-71.1&unit=0&lg=english&FcstType=graphical'>Graphical weather</a>"
  ref = ' &nbsp; &nbsp; <id style="font-size: 70%">' + graphLink + '</id>'
  html = url1+ '<br>' + url2 + '<br>' + url3  + ref 
  try {
    return html
  } catch (err) {
    return 'weather ERR; refresh page or browse '+ graphLink
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


function weatherPeriod(i, periods) {
  const forecast = periods[i]['detailedForecast']
  t = periods[i]['temperature']
  tColor = '#0000FF;'  // blue
  if (t > 78) {
    tColor = '#CC0000;' // dark red
  } else if (t > 65) {
    tColor = '#009900;'   // dark greem
  }
  f = forecast.toLowerCase()
  fore = "<span style='font-weight: bold; color:" + tColor + "'>" + t + '</span> '
  if (f.includes('partly sun')) {
    fore += '🌤️ '
  } else if (f.includes('sun')) {
    fore += '🌞 '
  }
  if (f.includes('cloud')) {
    fore += '☁️ '
  } 
  if (f.includes('rain') || f.includes('shower')) {
    fore += '🌧️ '
  } 
  if (f.includes('thunderstorm')) {
    fore += '🌩️ '
  } else if (f.includes('thunder ')) {
    fore += '⚡ '
  } 
  if (f.includes('fog')) {
    fore += '🌫️ '
  }
  if (f.includes('snow')) {
    fore += '❄️ '
  }
  const detailed = periods[i]['detailedForecast']
  const url = '<a href="https://forecast.weather.gov/MapClick.php?lat=42.482&lon=-71.0973&lg=english&&FcstType=text&bw=1" title="'+detailed+ '">' +
         fore + '</a>'
  return url
}


try {
  self.postMessage(getWeather());
}
catch(err) {
  self.postMessage(err.message);
}


