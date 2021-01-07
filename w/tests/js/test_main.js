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
   moon()
}


function moon() {
   const new_moon_ms = new Date(2019, 4, 4, 18, 45, 0, 0).getTime();
    // May 4	6:45 pm;  selected arbitrarily from  https://www.timeanddate.com/moon/phases/usa/boston
    const synodic_month_ms = 29 * 24 * 60 * 60000 + 12 * 60 * 60000 + 44 * 60000 + 2802; 
    //29 d 12 h 44 m 2.8016 s   https://en.wikipedia.org/wiki/Lunar_month
    const periods = ((new Date()).getTime() - new_moon_ms) / synodic_month_ms
    const fraction = periods - Math.trunc(periods)
    console.log(fraction)
    if (fraction <= .12) {
       icon = '🌑'
    } else if (fraction <= .21) {
       icon = '️🌒'
    } else if (fraction <= .31) {
       icon = '🌓'
    } else if (fraction <= .38) {
       icon = '🌔️'
    } else if (fraction <= .62) {
       icon = '🌕️'
    } else if (fraction <= .69) {
       icon = '🌖'
    } else if (fraction <= .79) {
       icon = '️🌗'
    } else if (fraction <= .88) {
       icon = '🌘'
    } else {
       icon = '🌑'
    }
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


