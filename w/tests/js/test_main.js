function unitTestsMain() {
  window.DEBUG = true
  console.log('-- unitTestsMain() started');
  const tStart = new Date().getTime();
  try {
      testSearchMain();
      testSearchLabelsMain();
      testSearchPageSourceMain();
      testWeatherMain();
      if (window.testFailed) {
         document.body.style.background = '#ff6666';
      } else {
         document.body.style.background = '#ccffcc';
      }
      const tEnd = new Date().getTime();
      const dt = tEnd - tStart;
      document.getElementById("search-results").innerHTML += '\n  ' + dt + ' msec';
      console.log('-- unitTestsMain() done');
  } catch (err) {
    document.getElementById("search-results").innerHTML += '\n  ' + err
  }
}

function testUnitTest() {
   testWeatherMain()
}

function moon() {
   const full_moon_ms = new Date(2000, 1, 24, 16, 42, 0, 0).getTime();
  console.log(init_full_moon_dt)  //29 d 12 h 44 m 2.8016 s
    const synodic_month_ms = 29 * 24 * 60 * 60000 + 12 * 60 * 60000 + 44 * 60000 + 2802
    const moon_months = ((new Date()).getTime() - full_moon_ms) / synodic_month_ms
    const moon_month_fraction = moon_months - Math.trunc(moon_months)
    let moon_month_num = Math.trunc(moon_months)
    var new_moon_dt = new Date(full_moon_dt.getTime() + Math.round((moon_month_num + .5)* synodic_month_ms))
    if (moon_month_fraction > .5){
       moon_month_num += 1
    }
    d = new Date(init_full_moon_dt.getTime() + synodic_month_ms)
    
   console.log ('+ ++ ++'+ synodic_month_ms)
  console.log(init_full_moon_dt)  //29 d 12 h 44 m 2.8016 s
//new Date(milliseconds)   

// synodic month 29.530588853
// 29:12:44:02.8768992
//https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?begin_date=20200915 18:56&end_date=20200915 20:56&station=8443970&product=water_temperature&interval=h&units=english&time_zone=lst_ldt&application=web_services&format=json')

}


function validate(testName, expected, actual) {
   console.log('* testName='+ testName)
   const isPass = expected == String(actual);
   console.log('* validate() expected='+expected+'|')
   console.log('* validate() actual  ='+String(actual)+'|')
   if (isPass) {
      status = 'Pass: '+  testName;
   } else {
      window.testFailed =true;
      status = '<id style=\'color:red\'>Failed; '+  testName + '</id>' +
               '\n--expected: '+expected + 
               '\n----actual: ' + actual;
   }
   console.log('* validate() status=' + status);
   var displayMsgs = document.getElementById("search-results").innerHTML;
   if (displayMsgs.length >  0) {
      displayMsgs += '\n';
   }
   displayMsgs += status ; 
   document.getElementById("search-results").innerHTML = displayMsgs
}


