function getWeather() {
  const js = readText('https://api.weather.gov/gridpoints/BOX/68,81/forecast')
  const w = JSON.parse(js)
  console.log(w)
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


function weatherPeriod(i, periods) {
  const t = periods[i]['temperature']
  tColor = '#0000FF;'  // blue
  if (t > 78) {
    tColor = '#CC0000;' // dark red
  } else if (t > 65) {
    tColor = '#009900;'   // dark greem
  }
  
  const f = periods[i]['detailedForecast'].toLowerCase()
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
  const url = '<a href="https://forecast.weather.gov/MapClick.php?lat=42.482&lon=-71.0973&lg=english&&FcstType=text&bw=1" title="'+
               detailed+ '">' + fore + '</a>'
  return url
}


function getTides() {
  var today = new Date();
  time = today.toTimeString();
  ts1 = today.toISOString().replace(/-/g,'').substr(0,8) + ' ' + time.substr(0,5);
  var tommorow = new Date(new Date().getTime() + 24 * 60 * 60 * 1000);
  ts2 = tommorow.toISOString().replace(/-/g,'').substr(0,8) + ' ' + time.substr(0,5);
  url='https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?begin_date='+ ts1 +
  '&end_date=' + ts2 +'&station=8443970&product=predictions&interval=15&datum=mllw'+
  '&units=english&time_zone=lst_ldt&application=web_services&format=json';
  const js = readText(url)
  const w = JSON.parse(js)
  var isTideGoingOut = w.predictions[0].v > w.predictions[1].v;
  console.log(isTideGoingOut)
  console.log(w)
  if (isTideGoingOut) {
    lowTideIndex = getLowTideIndex(0, w.predictions)
    highTideIndex = getHighTideIndex(lowTideIndex+1, w.predictions)
    console.log('low '+lowTideIndex + ' high '+highTideIndex)
    nextTide =  w.predictions[lowTideIndex].t.substr(11) +
               ' low tide</br>'+ w.predictions[highTideIndex].t.substr(11) + ' high'
    details = 'Low tide: '+ w.predictions[lowTideIndex].v + ' ft, at: ' + w.predictions[lowTideIndex].t +
               ';  High tide: '+ w.predictions[highTideIndex].v + ' ft, at: ' + w.predictions[highTideIndex].t 
  } else {  
    highTideIndex = getHighTideIndex(0, w.predictions)
    lowTideIndex = getLowTideIndex(highTideIndex+1, w.predictions)
    console.log('high '+highTideIndex + ' low '+lowTideIndex)
    nextTide =  w.predictions[highTideIndex].t.substr(11) +
               ' high tide</br>'+ w.predictions[lowTideIndex].t.substr(11) + ' low'
    details = 'High tide: '+ w.predictions[highTideIndex].v + ' ft, at: ' + w.predictions[highTideIndex].t +
               ';  Low tide: '+ w.predictions[lowTideIndex].v + ' ft, at: ' + w.predictions[lowTideIndex].t 
  }
  console.log(nextTide)
  let url2 = '<a href="https://tidesandcurrents.noaa.gov/stationhome.html?id=8443970" title="'+
        details + '">' + nextTide + '</a>'
  return url2
}

function getLowTideIndex(iStart, ar) {
  var minHeight = ar[iStart].v;
  for (var i=iStart+1; i < ar.length; i++) {
      if (ar[i].v < minHeight)
        minHeight = ar[i].v;
      else
        return i;
  }
}

function getHighTideIndex(iStart, ar) {
  var maxHeight = ar[iStart].v;
  for (var i=iStart+1; i < ar.length; i++) {
      if (ar[i].v > maxHeight)
        maxHeight = ar[i].v;
      else
        return i;
  }
}

try {
  var html = '<table><tr><td>'+getWeather()+
             '</td><td> &emsp; &emsp; </td><td>'+getTides()+'</br>graphic</td></tr></table>'
  self.postMessage(html);
}
catch(err) {
  self.postMessage(err.message);
}


