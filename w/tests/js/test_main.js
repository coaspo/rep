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


function sortTable(i_column) {
      console.log('- 00 00- - sortTable' )
      var table, rows, sorted, i, x, y, sortFlag;
      table = document.getElementById("table");
      sorted = true;
      document.getElementById("body").style.cursor = "wait";
      while (sorted) {
         sorted = false;
         rows = table.rows;
         for (i = 1; i < rows.length - 1; i++) {
            sortFlag = false;
            i_col = i_column
            if (rows[i].cells.length >4) {
                i_col++;
            }
            i_col2 = i_column
            if (rows[i+1].cells.length >4) {
                i_col2++;
            }
            x = rows[i].getElementsByTagName("TD")[i_col];
            y = rows[i + 1].getElementsByTagName("TD")[i_col2];
            x = x.innerHTML.toLowerCase()
            y = y.innerHTML.toLowerCase()
            if (i_column==3) {
              x = parseInt(x);
              y = parseInt(y);
             } else if (i_column==1) {
                // <a href="....">sample</a>
                 ii = x.indexOf(">")+ 1;
                 jj = x.indexOf("</");
                 x = x.substring(ii,jj)
                 ii = y.indexOf(">")+ 1;
                 jj = y.indexOf("</");
                 y = y.substring(ii,jj)
             }
            console.log(i_column+'==== ' + x+ '=='+y)
            if (x > y) {
               sortFlag = true;
               break;
            }
         }
         if (sortFlag) {
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            sorted = true;
         }
      }
      document.getElementById("body").style.cursor = "auto";
   }