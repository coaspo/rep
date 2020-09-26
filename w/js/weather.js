function getWeather() {
  const js = readText('https://api.weather.gov/gridpoints/BOX/68,81/forecast')
  const w = JSON.parse(js)
  console.log(w)
  const url1 = weatherPeriod(0, w.properties.periods)
  const url2 = weatherPeriod(1, w.properties.periods)
  const url3 = weatherPeriod(2, w.properties.periods)
  const html = url1+ '<br>' + url2 + '<br>' + url3
  try {
    return html
  } catch (err) {
    console.log(err.message)
    console.log(err.stack)
    return 'get weather ERR, press F12'
  }
}


function weatherPeriod(i, periods) {
  const t = periods[i]['temperature']
  let tColor = '#0000FF;'  // blue
  if (t > 78) {
    tColor = '#CC0000;' // dark red
  } else if (t > 65) {
    tColor = '#009900;'   // dark greem
  }
  
  const f = periods[i]['detailedForecast'].toLowerCase()
  let fore = "<span style='font-weight: bold; color:" + tColor + "'>" + t + '°</span> '
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

function getTS(date) {
  const time = date.toTimeString();
  const ts = date.toISOString().replace(/-/g,'').substr(0,8) + ' ' + time.substr(0,5);
  return ts
}

function getTides() {
  const today = new Date();
  const ts1 = getTS(today);
  const tomorrow = new Date(today.getTime() + 24 * 60 * 60 * 1000);
  const ts2 = getTS(tomorrow);
  const url='https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?begin_date='+ ts1 +
  '&end_date=' + ts2 +'&station=8443970&product=predictions&interval=15&datum=mllw'+
  '&units=english&time_zone=lst_ldt&application=web_services&format=json';
  console.log(url)
  const js = readText(url)
  const w = JSON.parse(js)
  const predictions = w.predictions
  const link = getTidesLink(predictions)
  console.log(link)
  return link
}

function getTidesLink(predictions) {
  const isTideBecomingLow = Number(predictions[0].v) > Number(predictions[1].v);
  console.log(isTideBecomingLow)
  console.log(predictions)
  if (isTideBecomingLow) {
    const lowTideIndex = getLowTideIndex(0, predictions)
    const highTideIndex = getHighTideIndex(lowTideIndex+1, predictions)
    console.log('low '+lowTideIndex + ' high '+highTideIndex)
    let lowTideTime = removeLeadingZero(predictions[lowTideIndex].t.substr(11)); 
    let highTideTime = removeLeadingZero(predictions[highTideIndex].t.substr(11));
    var nextTide =  lowTideTime +
               ' L ⬇️</br>'+ highTideTime + ' H'
    var details = 'Low tide: '+ predictions[lowTideIndex].v + ' ft, @ ' + predictions[lowTideIndex].t +
               ';  High tide: '+ predictions[highTideIndex].v + ' ft, @ ' + predictions[highTideIndex].t
  } else {  
    const highTideIndex = getHighTideIndex(0, predictions)
    const lowTideIndex = getLowTideIndex(highTideIndex+1, predictions)
    console.log('high '+highTideIndex + ' low '+lowTideIndex)
    let lowTideTime = removeLeadingZero(predictions[lowTideIndex].t.substr(11)); 
    let highTideTime = removeLeadingZero(predictions[highTideIndex].t.substr(11));
    var nextTide =  highTideTime +
               ' H ⬆️</br>'+ lowTideTime + ' L'
    var details = 'High tide: '+ predictions[highTideIndex].v + ' ft, @ ' + predictions[highTideIndex].t +
               ';  Low tide: '+ predictions[lowTideIndex].v + ' ft, @ ' + predictions[lowTideIndex].t 
  }
  console.log(nextTide)
  const link = '<a href="https://tidesandcurrents.noaa.gov/stationhome.html?id=8443970" title="'+
        details + '">' + nextTide + '</a>'
  return link
}


function removeLeadingZero(time) {
  if (time.charAt(0) == '0') {
    time = '&nbsp;' + time.substr(1);
  }
  return time;
}


function getLowTideIndex(iStart, ar) {
  let minHeight =  Number(ar[iStart].v);
  for (var i=iStart+1; i < ar.length; i++) {
      const waterHeight = Number(ar[i].v)
      if (waterHeight < minHeight)
        minHeight = waterHeight;
      else
        return i-1;
  }
  return ar.length;
}

function getHighTideIndex(iStart, ar) {
  let maxHeight = Number(ar[iStart].v);
  console.log(maxHeight)
  for (var i=iStart+1; i < ar.length; i++) {
     const waterHeight = Number(ar[i].v)
     console.log(i + ' ' + ar[i].v + ' ' + maxHeight + ' '+(ar[i].v > maxHeight))
     if (waterHeight > maxHeight)
        maxHeight = waterHeight;
      else
        return i-1;
  }
  return ar.length;
}

function getWaterTemperature() {
  const today = new Date();
  const ts2 = getTS(today);
  const yesterday = new Date(today.getTime() - 24 * 60 * 60 * 1000);
  const ts1 = getTS(yesterday);
  const url='https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?begin_date='+ ts1 +
  '&end_date=' + ts2 +'&station=8443970&product=water_temperature&interval=h'+
  '&units=english&time_zone=lst_ldt&application=web_services&format=json';

  console.log(url)
  const js = readText(url)
  const w = JSON.parse(js)
  const data = w.data
  if (typeof data == 'undefined')
    return ''
  const link = getWaterTemperatureLink(data)
  return link
}

function getWaterTemperatureLink(data) {
  let min =  100;
  let max =  -100;
  let total = 0.0;
  for (var i = 0; i < data.length; i++) {
      const t = Number(data[i].v)
      total = total + t
      if (t < min)
        min = t;
      if (t > max)
        max = t;
  }
  const average = Math.round(total / data.length)
  const details = 'Last 24 hr. min/max/ave water temp: ' + Math.round(min) + 
                  '/' + Math.round(max) + '/'+ average 
  const link = '<a href="https://tidesandcurrents.noaa.gov/stationhome.html?id=8443970" title="'+
               details + '°">' + average + '°</a>'
  return link
}


try {
  var html = '<table><tr><td>'+getWeather()+
             '</td><td> &emsp; &emsp; </td><td>'+getTides()+'</br>' +getWaterTemperature()+
             '</td><td> &emsp; &emsp; </td><td>graphic</td></tr></table>'
  console.log('========')
             console.log(html)
  self.postMessage(html);
} catch(err) {
  console.log(err.message)
  console.log(err.stack)
  self.postMessage('weather ERR, press F12')
}
//new Date(milliseconds)

// synodic month 29.530588853
// 29:12:44:02.8768992
//https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?begin_date=20200915 18:56&end_date=20200915 20:56&station=8443970&product=water_temperature&interval=h&units=english&time_zone=lst_ldt&application=web_services&format=json')

