
function testTideIndex() {
   predictions = [
   {t:"2020-09-15 18:45", v:"4.632"},
   {t:"2020-09-15 22:15", v:"10.853"},
   {t:"2020-09-15 22:30", v:"10.831"},
   {t:"2020-09-16 04:45", v:"-0.404"},
   {t:"2020-09-16 05:00", v:"-0.330"}]
   highTideIndex = getHighTideIndex(0, predictions)
   validate('0 getHighTideIndex()   ', 1, highTideIndex);
   lowTideIndex = getLowTideIndex(highTideIndex+1, predictions)
   validate('0 getLowTideIndex()   ', 3, lowTideIndex);
}

function testGetTidesLink() {
   predictions = [
   {t:"2020-09-15 18:45", v:"4.632"},
   {t:"2020-09-15 22:15", v:"10.853"},
   {t:"2020-09-15 22:30", v:"10.831"},
   {t:"2020-09-16 04:45", v:"-0.404"},
   {t:"2020-09-16 05:00", v:"-0.330"}]
   link = getTidesLink(predictions)
   expected = '<a href="https://tidesandcurrents.noaa.gov/stationhome.html?id=8443970" title="High tide: 10.853 ft, at: 2020-09-15 22:15;  Low tide: -0.404 ft, at: 2020-09-16 04:45">22:15 H ⬆️</br>04:45 L</a>'
   validate('0 getTidesLink()   ', expected, link);
   predictions = [
   {t:"2020-09-15 18:45", v:"-0.599"},
   {t:"2020-09-15 22:15", v:"-0.643"},
   {t:"2020-09-15 22:30", v:"-0.565"},
   {t:"2020-09-16 04:45", v:"0.10"},
   {t:"2020-09-16 05:00", v:"0.05"}]
   link = getTidesLink(predictions)
   expected = '<a href="https://tidesandcurrents.noaa.gov/stationhome.html?id=8443970" title="Low tide: -0.643 ft, at: 2020-09-15 22:15;  High tide: 0.10 ft, at: 2020-09-16 04:45">22:15 L ⬇️</br>04:45 H</a>'
   validate('1 getTidesLink()   ', expected, link);
 }

function testReadText() {
  try {
     js = readText('https://api.weather.gov/gridpoints/BOX/68,81/forecast')
     var w = JSON.parse(js)
     console.log(w.properties.periods[0]['detailedForecast'])
  } catch (err) {
    validate('0 readText()   ', '', err);
  }
}

