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
  //https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?begin_date=20200915 18:56&end_date=20200916 18:56&station=8443970&product=predictions&interval=15&datum=mllw&units=english&time_zone=lst_ldt&application=web_services&format=json weather.js:84:11

  console.log(url)
  const js = readText(url)
  const w = JSON.parse(js)
  const predictions = w.predictions
  link = getTidesLink(predictions)
  console.log(link)
  return link
}

function getTidesLink(predictions) {
  var isTideBecomingLow = Number(predictions[0].v) > Number(predictions[1].v);
  console.log(isTideBecomingLow)
  console.log(predictions)
  if (isTideBecomingLow) {
    lowTideIndex = getLowTideIndex(0, predictions)
    highTideIndex = getHighTideIndex(lowTideIndex+1, predictions)
    console.log('low '+lowTideIndex + ' high '+highTideIndex)
    nextTide =  predictions[lowTideIndex].t.substr(11) +
               ' L ⬇️</br>'+ predictions[highTideIndex].t.substr(11) + ' H'
    details = 'Low tide: '+ predictions[lowTideIndex].v + ' ft, at: ' + predictions[lowTideIndex].t +
               ';  High tide: '+ predictions[highTideIndex].v + ' ft, at: ' + predictions[highTideIndex].t 
  } else {  
    highTideIndex = getHighTideIndex(0, predictions)
    lowTideIndex = getLowTideIndex(highTideIndex+1, predictions)
    console.log('high '+highTideIndex + ' low '+lowTideIndex)
    nextTide =  predictions[highTideIndex].t.substr(11) +
               ' H ⬆️</br>'+ predictions[lowTideIndex].t.substr(11) + ' L'
    details = 'High tide: '+ predictions[highTideIndex].v + ' ft, at: ' + predictions[highTideIndex].t +
               ';  Low tide: '+ predictions[lowTideIndex].v + ' ft, at: ' + predictions[lowTideIndex].t 
  }
  console.log(nextTide)
  let link = '<a href="https://tidesandcurrents.noaa.gov/stationhome.html?id=8443970" title="'+
        details + '">' + nextTide + '</a>'
  return link
}

function getLowTideIndex(iStart, ar) {
  var minHeight =  Number(ar[iStart].v);
  for (var i=iStart+1; i < ar.length; i++) {
      waterHeight = Number(ar[i].v)
      if (waterHeight < minHeight)
        minHeight = waterHeight;
      else
        return i-1;
  }
}

function getHighTideIndex(iStart, ar) {
  var maxHeight = Number(ar[iStart].v);
  console.log(maxHeight)
  for (var i=iStart+1; i < ar.length; i++) {
     waterHeight = Number(ar[i].v)
   console.log(i + ' ' + ar[i].v + ' ' + maxHeight + ' '+(ar[i].v > maxHeight))
     if (waterHeight > maxHeight)
        maxHeight = waterHeight;
      else
        return i-1;
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
//new Date(milliseconds)

// synodic month 29.530588853
// 29:12:44:02.8768992

