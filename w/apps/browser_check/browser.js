/**  how-to-find-the-operating-system-details-using-javascript
 * JavaScript Client Detection
 * (C) viazenetti GmbH (Christian Ludwig)
 */
(function (window) {
    {
        var unknown = '-';

        // screen
        var screenSize = '';
        if (screen.width) {
            width = (screen.width) ? screen.width : '';
            height = (screen.height) ? screen.height : '';
            screenSize += '' + width + " x " + height;
        }

        // browser
        var nVer = navigator.appVersion;
        var nAgt = navigator.userAgent;
        var browser = navigator.appName;
        var version = '' + parseFloat(navigator.appVersion);
        var majorVersion = parseInt(navigator.appVersion, 10);
        var nameOffset, verOffset, ix;

        // Opera
        if ((verOffset = nAgt.indexOf('Opera')) != -1) {
            browser = 'Opera';
            version = nAgt.substring(verOffset + 6);
            if ((verOffset = nAgt.indexOf('Version')) != -1) {
                version = nAgt.substring(verOffset + 8);
            }
        }
        // Opera Next
        if ((verOffset = nAgt.indexOf('OPR')) != -1) {
            browser = 'Opera';
            version = nAgt.substring(verOffset + 4);
        }
        // Legacy Edge
        else if ((verOffset = nAgt.indexOf('Edge')) != -1) {
            browser = 'Microsoft Legacy Edge';
            version = nAgt.substring(verOffset + 5);
        }
        // Edge (Chromium)
        else if ((verOffset = nAgt.indexOf('Edg')) != -1) {
            browser = 'Microsoft Edge';
            version = nAgt.substring(verOffset + 4);
        }
        // MSIE
        else if ((verOffset = nAgt.indexOf('MSIE')) != -1) {
            browser = 'Microsoft Internet Explorer';
            version = nAgt.substring(verOffset + 5);
        }
        // Chrome
        else if ((verOffset = nAgt.indexOf('Chrome')) != -1) {
            browser = 'Chrome';
            version = nAgt.substring(verOffset + 7);
        }
        // Safari
        else if ((verOffset = nAgt.indexOf('Safari')) != -1) {
            browser = 'Safari';
            version = nAgt.substring(verOffset + 7);
            if ((verOffset = nAgt.indexOf('Version')) != -1) {
                version = nAgt.substring(verOffset + 8);
            }
        }
        // Firefox
        else if ((verOffset = nAgt.indexOf('Firefox')) != -1) {
            browser = 'Firefox';
            version = nAgt.substring(verOffset + 8);
        }
        // MSIE 11+
        else if (nAgt.indexOf('Trident/') != -1) {
            browser = 'Microsoft Internet Explorer';
            version = nAgt.substring(nAgt.indexOf('rv:') + 3);
        }
        // Other browsers
        else if ((nameOffset = nAgt.lastIndexOf(' ') + 1) < (verOffset = nAgt.lastIndexOf('/'))) {
            browser = nAgt.substring(nameOffset, verOffset);
            version = nAgt.substring(verOffset + 1);
            if (browser.toLowerCase() == browser.toUpperCase()) {
                browser = navigator.appName;
            }
        }
        // trim the version string
        if ((ix = version.indexOf(';')) != -1) version = version.substring(0, ix);
        if ((ix = version.indexOf(' ')) != -1) version = version.substring(0, ix);
        if ((ix = version.indexOf(')')) != -1) version = version.substring(0, ix);

        majorVersion = parseInt('' + version, 10);
        if (isNaN(majorVersion)) {
            version = '' + parseFloat(navigator.appVersion);
            majorVersion = parseInt(navigator.appVersion, 10);
        }

        // mobile version
        var mobile = /Mobile|mini|Fennec|Android|iP(ad|od|hone)/.test(nVer);

        // cookie
        var cookieEnabled = (navigator.cookieEnabled) ? true : false;

        if (typeof navigator.cookieEnabled == 'undefined' && !cookieEnabled) {
            document.cookie = 'testcookie';
            cookieEnabled = (document.cookie.indexOf('testcookie') != -1) ? true : false;
        }

        // system
        var os = unknown;
        var clientStrings = [
            {s:'Windows 10', r:/(Windows 10.0|Windows NT 10.0)/},
            {s:'Windows 8.1', r:/(Windows 8.1|Windows NT 6.3)/},
            {s:'Windows 8', r:/(Windows 8|Windows NT 6.2)/},
            {s:'Windows 7', r:/(Windows 7|Windows NT 6.1)/},
            {s:'Windows Vista', r:/Windows NT 6.0/},
            {s:'Windows Server 2003', r:/Windows NT 5.2/},
            {s:'Windows XP', r:/(Windows NT 5.1|Windows XP)/},
            {s:'Windows 2000', r:/(Windows NT 5.0|Windows 2000)/},
            {s:'Windows ME', r:/(Win 9x 4.90|Windows ME)/},
            {s:'Windows 98', r:/(Windows 98|Win98)/},
            {s:'Windows 95', r:/(Windows 95|Win95|Windows_95)/},
            {s:'Windows NT 4.0', r:/(Windows NT 4.0|WinNT4.0|WinNT|Windows NT)/},
            {s:'Windows CE', r:/Windows CE/},
            {s:'Windows 3.11', r:/Win16/},
            {s:'Android', r:/Android/},
            {s:'Open BSD', r:/OpenBSD/},
            {s:'Sun OS', r:/SunOS/},
            {s:'Chrome OS', r:/CrOS/},
            {s:'Linux', r:/(Linux|X11(?!.*CrOS))/},
            {s:'iOS', r:/(iPhone|iPad|iPod)/},
            {s:'Mac OS X', r:/Mac OS X/},
            {s:'Mac OS', r:/(Mac OS|MacPPC|MacIntel|Mac_PowerPC|Macintosh)/},
            {s:'QNX', r:/QNX/},
            {s:'UNIX', r:/UNIX/},
            {s:'BeOS', r:/BeOS/},
            {s:'OS/2', r:/OS\/2/},
            {s:'Search Bot', r:/(nuhk|Googlebot|Yammybot|Openbot|Slurp|MSNBot|Ask Jeeves\/Teoma|ia_archiver)/}
        ];
        for (var id in clientStrings) {
            var cs = clientStrings[id];
            if (cs.r.test(nAgt)) {
                os = cs.s;
                break;
            }
        }

        var osVersion = unknown;

        if (/Windows/.test(os)) {
            osVersion = /Windows (.*)/.exec(os)[1];
            os = 'Windows';
        }

        switch (os) {
            case 'Mac OS':
            case 'Mac OS X':
            case 'Android':
                osVersion = /(?:Android|Mac OS|Mac OS X|MacPPC|MacIntel|Mac_PowerPC|Macintosh) ([\.\_\d]+)/.exec(nAgt)[1];
                break;

            case 'iOS':
                osVersion = /OS (\d+)_(\d+)_?(\d+)?/.exec(nVer);
                osVersion = osVersion[1] + '.' + osVersion[2] + '.' + (osVersion[3] | 0);
                break;
        }

        // flash (you'll need to include swfobject)
        /* script src="//ajax.googleapis.com/ajax/libs/swfobject/2.2/swfobject.js" */
        var flashVersion = 'no check';
        if (typeof swfobject != 'undefined') {
            var fv = swfobject.getFlashPlayerVersion();
            if (fv.major > 0) {
                flashVersion = fv.major + '.' + fv.minor + ' r' + fv.release;
            }
            else  {
                flashVersion = unknown;
            }
        }
    }

    window.jscd = {
        screen: screenSize,
        browser: browser,
        browserVersion: version,
        browserMajorVersion: majorVersion,
        mobile: mobile,
        os: os,
        osVersion: osVersion,
        cookies: cookieEnabled,
        flashVersion: flashVersion
    };
}(this));

document.getElementById("sysinfo").innerHTML ='Navigator\n '+
'OS:                ' + jscd.os +' '+ jscd.osVersion + '\n ' +
'Engine name:       ' +  navigator.product + '\n ' +
'Browser platform:  ' +  navigator.platform + '\n ' +
'Browser:           ' + jscd.browser +' '+ jscd.browserMajorVersion +' (' + jscd.browserVersion + ')\n ' +
'Cookies:           ' + jscd.cookies + '\n ' +
'Flash:             ' + jscd.flashVersion + '\n ' +
'Full User Agent:   ' + navigator.userAgent + '\n ' +
'Java enabled:      ' +  navigator.javaEnabled() + '\n ' +
'Language:          ' +  navigator.language + '\n ' +
'Mobile:            ' + jscd.mobile + '\n ' +
'Screen Size:       ' + jscd.screen + '\n ' +
'Has local storage: ' + (typeof(Storage) !== "undefined")

navigator.geolocation.getCurrentPosition(showPosition);

function val(x) {
  return x == null ? '?' : x
}

function distance(pt1, pt2) {
  // from https://www.movable-type.co.uk/scripts/latlong.html
  const R = 10007540 * 2 / Math.PI  // meters; 6371e3;
  const phi1 = pt1.lati * Math.PI / 180; // phi, lamda in radians
  const phi2 = pt2.lati * Math.PI / 180;
  const delta_phi = (pt1.lati - pt2.lati) * Math.PI / 180;
  const delta_lamda = (pt1.long - pt2.long) * Math.PI / 180;
  const a = Math.sin(delta_phi / 2) * Math.sin(delta_phi / 2) +
    Math.cos(phi1) * Math.cos(phi2) *
    Math.sin(delta_lamda / 2) * Math.sin(delta_lamda / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  d = parseInt(R * c)
  return d
}

function showPosition(position) {
  coords = position.coords
  geo = {
    lati: coords.latitude,
    long: coords.longitude,
    accu: coords.accuracy,
    alti: coords.altitude,
    alti_accu: coords.altitudeAccuracy,
    head: coords.heading,
    ts:   position.timestamp,
    speed:  coords.speed
  }
  document.getElementById("position").innerHTML=
    'Geolocation'
        + '\n latitude:          ' + geo.lati
        + '\n latitude:          ' + geo.lati
        + '\n longitude:         ' + geo.long
        + '\n accuracy:          ' + geo.accu + ' m'
        + '\n altitude:          ' + val(geo.alti) + ' m'
        + '\n altitude accuracy: ' + val(geo.alti_accu)  + ' m'
        + '\n heading:           ' + val(geo.head)  + ' deg'
        + '\n                      clockwise from North'
        + '\n epoch timestamp:   ' + geo.ts.toLocaleString("en-US")  + ' ms'
        + '\n                      after 1970-1-1'
        + '\n                      ' + new Date(geo.ts).toISOString()
        + '\n speed:             ' + val(geo.speed) + ' m/sec'
        + '\n                      '+ (geo.speed * 2.24) +' MPH'
  if (typeof(Storage) !== "undefined" && localStorage.getItem("prev_geo") != null) {
    var prev_geo = JSON.parse(localStorage.getItem("prev_geo"));
    dis = distance (geo, prev_geo)
    document.getElementById("delta_position").innerHTML=
    ' Change since: '+ new Date(prev_geo.ts).toISOString()
        + '\n  ' + (geo.lati - prev_geo.lati) + '    (' + dis.toLocaleString("en-US") + ' m)'
        + '\n  ' + (geo.long - prev_geo.long)
        + '\n  ' + (geo.accu - prev_geo.accu)
        + '\n  ' + (geo.alti - prev_geo.alti)
        + '\n  ' + (geo.alti_accu - prev_geo.alti_accu)
        + '\n  ' +    (geo.head - prev_geo.head)
        + '\n'
        + '\n  ' + (geo.ts - prev_geo.ts).toLocaleString("en-US")
        + '\n'
        + '\n    ' + (parseInt((geo.ts - prev_geo.ts)/60000)) + ' min'
        + '\n  ' + (prev_geo.speed - prev_geo.speed)
        + '\n    ' + (prev_geo.speed * 2.24 - prev_geo.speed )
  }
  localStorage.setItem("prev_geo", JSON.stringify(geo));
}


function show_motion(event){
  document.getElementById("acceleration").innerHTML="Accelerometer/motion: "
    + '\n x-axis: ' + event.accelerationIncludingGravity.x
    + '\n y-axis: ' + event.accelerationIncludingGravity.y
    + '\n z-axis: ' + event.accelerationIncludingGravity.z;
}

function show_orientation(event){
  document.getElementById("orientation").innerHTML="Magnetometer/orientation: "
    + '\n is absolute:   ' + event.absolute
    + '\n alpha; z-axis: ' + event.alpha + ' (screen normal axis)'
    + '\n beta;  x-axis: ' + event.beta + ' (screen short axis)'
    + '\n gamma; y-axis: ' + event.gamma + ' (screen long axis)';
}

if(window.DeviceMotionEvent){
  window.addEventListener("devicemotion", show_motion, false);
}else{
  document.getElementById("acceleration").innerHTML="Acceleration/DeviceMotionEvent is not supported";
}

if(window.DeviceOrientationEvent){
  window.addEventListener("deviceorientation", show_orientation, false);
}else{
  document.getElementById("orientation").innerHTML="Magnetometer/DeviceOrientationEvent is not supported";
}

if (typeof(Gyroscope) !== "undefined") {
    let gyroscope = new Gyroscope({frequency: 60});

    gyroscope.addEventListener('reading', e => {
      document.getElementById("velocity").innerHTML =
          + "Angular velocity along:\n  X-axis " + gyroscope.x
          +"\n  Y-axis " + gyroscope.y
          +"\n  Z-axis " + gyroscope.z;
          console.log(", Z-axis " + gyroscope.z)
    });
    gyroscope.start();
    console.log('active')
} else {
    document.getElementById("velocity").innerHTML = "Cannot access gyroscope"
}
/*
let gyroscope = new Gyroscope({frequency: 60});

gyroscope.addEventListener('reading', e => {
  console.log("Angular velocity along the X-axis " + gyroscope.x);
  console.log("Angular velocity along the Y-axis " + gyroscope.y);
  console.log("Angular velocity along the Z-axis " + gyroscope.z);
});
gyroscope.start();
*/
