function getWeather() {
  try {
    const js = readText('https://api.weather.gov/gridpoints/BOX/68,81/forecast')
    const w = JSON.parse(js)
    console.log(w)
    // 0/1/2 is for current/next/next 12 hours
    const url1 = weatherPeriod(0, w.properties.periods)
    const url2 = weatherPeriod(1, w.properties.periods)
    const url3 = weatherPeriod(2, w.properties.periods)
    const html = url1+ '<br>' + url2 + '<br>' + url3
    return html
  } catch (err) {
    console.log('ERR1 '+ err.message)
    console.log(err.stack)
    return  ''
  }
}

function readText(url) {
  const req = new XMLHttpRequest();
  req.open('GET', url, false); // `false` makes the request synchronous
  try {
    req.send(null);
  } catch (err) {
    throw err + ' on reading: ' + url;
  }
  if (req.status === 200) {
    var text = req.responseText.trim();
  } else {
    var text = req.status + ' on reading: ' + url;
    throw text
  }
  return text
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
  let fore = "<span style='font-weight: bold; color:" + tColor + "'>" + t + 'Â°</span> '
  if (f.includes('partly sun')) {
    fore += 'đ¤ī¸ '
  } else if (f.includes('sun')) {
    fore += 'đ '
  }
  if (f.includes('cloud')) {
    fore += 'âī¸ '
  } 
  if (f.includes('rain') || f.includes('shower')) {
    fore += 'đ§ī¸ '
  } 
  if (f.includes('thunderstorm')) {
    fore += 'đŠī¸ '
  } else if (f.includes('thunder ')) {
    fore += 'âĄ '
  } 
  if (f.includes('fog')) {
    fore += 'đĢī¸ '
  }
  if (f.includes('windy') || f.includes('gusts')) {
    fore += 'đŦī¸ '
  }
  if (f.includes('hurricane')) {
    fore += 'đ '
  }
  if (f.includes('snow')) {
    fore += 'âī¸ '
  }
  let detailed
  if (i == 0) {
    detailed = 'Current 12-hr period:  '
  } else if (i == 1) {
    detailed = '12-hr period after 12 hrs:  '
  } else if (i == 2) {
    detailed = '12-hr period after 24 hrs:  '
  }
  detailed += periods[i]['detailedForecast']
  const url = '<a href="https://forecast.weather.gov/MapClick.php?lat=42.482&lon=-71.0973&lg=english&&FcstType=text&bw=1" title="'+
               detailed+ '">' + fore + '</a>'
  return url
}



try {
  const html = '<table><tr><td>graphicWeather</td><td>'+getWeather()+'</tr></table>'
  self.postMessage(html);
} catch(err) {
  console.log(err.message)
  console.log(err.stack)
  self.postMessage('weather ERR: '+ err.message)
}
