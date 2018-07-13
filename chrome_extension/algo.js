var apiBaseUrl = 'https://ekitag-api.herokuapp.com/v1/';
var htmlPlayerGroups = document.getElementsByClassName('player-group');
var players = [];
for (var i = 0; i < htmlPlayerGroups.length; i++) {
  var htmlPlayers = htmlPlayerGroups[i].getElementsByClassName('player-name');

  for (var j = 0; j < htmlPlayers.length; j++) {
    players.push(htmlPlayers[j].innerHTML);
  }
}

// BUILD ALGO REQUEST
var algoRequest = new XMLHttpRequest();
console.log('Sending request...');
var url = apiBaseUrl + 'algo/musigma_team/from_pseudos';
for (var i = 0; i < players.length; i++) {
  var ammend = i == 0 ? '?' : '&';
  url += ammend + 'pseudos=' + players[i];
}
url = encodeURI(url);

algoRequest.open('GET', url, true);
algoRequest.onreadystatechange = function() {
  if (this.readyState == 4 && this.status == 200) {
    var response = JSON.parse(algoRequest.response);
    var chatInput = document.getElementsByClassName('js-chat-input')[0];
    chatInput.value =
      'RED: ' + response.r_pseudos.join(' ') + '  BLUE: ' + response.b_pseudos.join(' ');
  }
};
algoRequest.send();
