      console.log(document.getElementById('sunrise').innerHTML + '------')
      var buttonWorker

      function startWorker(type, increment) {
        if (type == 'month') {
          f = nextMonth
          timeout = 800
        } else if (type == 'day') {
          f = nextDay
          timeout = 200
        } else if (type == 'hour') {
          f = nextHour
          timeout = 500
        } else if (type == 'minute') {
          f = nextMinute
          timeout = 500
        }
        if (typeof (Worker) !== "undefined") {
          if (typeof (buttonWorker) == "undefined") {
            buttonWorker = new Worker("button-worker.js");
          }
          buttonWorker.onmessage = function (event) {
            f(increment)
          };
          buttonWorker.postMessage({ 'timeout': timeout });
        } else {
          f(increment)
          console.log("Sorry, your browser does not support Web Workers...");
        }
      }

      function stopWorker() {
        buttonWorker.terminate();
        buttonWorker = undefined;
      }


      // using sky.js
      update_screen(new Date())

      function nextMinute(increment) {
        date = new Date(date.getFullYear(), date.getMonth(), date.getDate(), date.getHours(), date.getMinutes() + increment, 0, 0)
        update_screen(date)
      }
      function nextHour(increment) {
        date = new Date(date.getFullYear(), date.getMonth(), date.getDate(), date.getHours() + increment, date.getMinutes(), 0, 0)
        update_screen(date)
      }
      function nextDay(increment) {
        date = new Date(date.getFullYear(), date.getMonth(), date.getDate(), date.getHours() + increment * 24, date.getMinutes(), 0, 0)
        update_screen(date)
      }
      function nextMonth(increment) {
        let year = date.getFullYear()
        let month = date.getMonth()
        month = month + increment
        if (month > 11) {
          year += 1
          month = 0
        } else if (month < 0) {
          year -= 1
          month = 11
        }
        date = new Date(year, month, date.getDate(), date.getHours(), 0, 0, 0)
        update_screen(date)
      }
      function update_screen(date) {
        sun = new Sun(date)
        NorthSky.update(date, sun)
        SouthSky.update(date, sun)
        document.getElementById('sunrise').innerHTML = '🌅 ' + sun.sunriseTime
        console.log(document.getElementById('sunrise').innerHTML + '------')
        document.getElementById('sunset').innerHTML = '🌇 ' + sun.sunsetTime
      }

      window.onload = function () {
        const img = document.getElementById('stars2')
        img.style.display = "none";
        const c = document.getElementById("starWindow");
        const ctx = c.getContext("2d");
        ctx.drawImage(img, 250, 0, 1104, 375, 0, 0, 1104, 375);
      }
