function unitTestsMain() {
  window.DEBUG = true
  console.log('-- unitTestsMain() started');
  const tStart = new Date().getTime();
  try {
      testSearchMain();
      testSearchLabelsMain();
      testSearchPageSourceMain();
      testSearchPageSourceMain;
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


