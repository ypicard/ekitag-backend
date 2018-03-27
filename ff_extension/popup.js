document.addEventListener('DOMContentLoaded', function() {
  var addMatchButton = document.getElementById('add-match');

  addMatchButton.addEventListener('click', function() {
    chrome.tabs.getSelected(null, function(tab) {
      chrome.tabs.executeScript(tab.id, { code: "alert('test');" }, function(response) {

      });
    });
  })


});