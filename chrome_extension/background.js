chrome.browserAction.onClicked.addListener(function(tab) {
  // No tabs or host permissions needed!

  if (tab.url.search('tagpro-chord.koalabeast.com/groups/') !== -1) {
    console.log("YAP")
    chrome.tabs.executeScript({
      file: 'algo.js'
    });
  } else {
    chrome.tabs.executeScript({
      file: 'scrap.js'
    });
  }
});
