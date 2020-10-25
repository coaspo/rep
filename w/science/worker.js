var i = 0;
var timeout

function timedCount() {
  i = i + 1; // not used
  postMessage(i);
  setTimeout("timedCount()",timeout);
}


self.addEventListener('message', function(e) {
  timeout = e.data.timeout
  timedCount()
}, false);
