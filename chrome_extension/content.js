/* This injects the script.js into the active pageand gives it
access to global javascript objects */

var s = document.createElement('script');
s.src = chrome.extension.getURL('script.js');
s.onload = function() {
  this.remove();
};
(document.head || document.documentElement).appendChild(s);