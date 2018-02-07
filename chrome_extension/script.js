alert('start script.js');

var playerStats = document.getElementById("stats").getElementsByTagName('tr');

// Remove useless rows
playerStats[0].remove();
playerStats[0].remove();
playerStats = [].slice.call(playerStats);

var matchData = {
  "r_score": 0,
  "b_score": 0,
  "b1_pseudo": null,
  "b2_pseudo": null,
  "b3_pseudo": null,
  "b4_pseudo": null,
  "b5_pseudo": null,
  "b6_pseudo": null,
  "r1_pseudo": null,
  "r2_pseudo": null,
  "r3_pseudo": null,
  "r4_pseudo": null,
  "r5_pseudo": null,
  "r6_pseudo": null,
}
var playersStats = [];



// Get each player's stats
var blueIndex = 0;
var redIndex = 0;
var redScore = 0;
var blueScore = 0;
playerStats.forEach(function(player) {

  var playerCells = [].slice.call(player.cells);

  // Build match object
  var pseudo = playerCells[0].getElementsByTagName('span')[1].innerHTML;
  var playerTeam = playerCells[0].getElementsByTagName('span')[1].className.split(' ')[1].split('-')[1]

  if (playerTeam == 'red') {
    redIndex += 1;
    matchData['r' + redIndex + '_pseudo'] = pseudo;
    matchData['r_score'] += playerCells[7].innerHTML
  } else if (playerTeam == 'blue') {
    blueIndex += 1;
    matchData['b' + redIndex + '_pseudo'] = pseudo;
    matchData['b_score'] += playerCells[7].innerHTML
  }

  // Build player stats object
  // match_id: null, // TODO
  var playerStats = {
    user_pseudo: pseudo,
    score: playerCells[1].innerHTML,
    tags: playerCells[2].innerHTML,
    popped: playerCells[3].innerHTML,
    grabs: playerCells[4].innerHTML,
    drops: playerCells[5].innerHTML,
    hold: playerCells[6].innerHTML,
    captures: playerCells[7].innerHTML,
    prevent: playerCells[8].innerHTML,
    returns: playerCells[9].innerHTML,
    support: playerCells[10].innerHTML,
    pups: playerCells[11].innerHTML,
  };

  playersStats.push(playerStats);
});

var msg = "Content scrapped :\n"
msg += 'SCORE :\n RED ' + matchData.r_score + ' - BLUE : ' + matchData.b_score
msg += '\nPLAYERS :'
playersStats.forEach(function(player) {
  msg += '\n' + player.pseudo;
});
alert(msg);

// Convert matchData to FormData for post request
var matchFormData = new FormData();
for (var key in matchData) {
  matchFormData.append(key, matchData[key]);
}

// BUILD MATCH REQUEST
var matchDataRequest = new XMLHttpRequest();
matchDataRequest.onreadystatechange = function() {
  if (this.readyState == 4 && this.status == 200) {
    console.log(this);
    // Now send players stats
    // Same for playersStats
    var statsRequest = new XMLHttpRequest();

    var statsFormData = new FormData();
    statsFormData.append('match_id', 1); // TODO : TAKE MATCH ID FROM PREV RESPONSE
    for (var key in playersStats) {
      statsFormData.append(key, playersStats[key]);
    }

    // Stats request callback
    statsFormData.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        alert('I SUPPOSE SUCCESS');
        console.log(this);
      }
    };

    // Send second request
    // TODO : ADD ID BELOW
    statsRequest.open('POST', 'https://ekitag-api.herokuapp.com/v1/matches/' + 1 + '/pending/', true);
    statsRequest.send(statsFormData);
  }
};

console.log('Sending request...');
matchDataRequest.open('POST', 'https://ekitag-api.herokuapp.com/v1/matches/pending/', true);
// matchDataRequest.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
matchDataRequest.send(matchFormData);