console.log('Starting parsing...')
var playerStats = document.getElementById("stats").getElementsByTagName('tbody')[0].getElementsByTagName('tr');

var apiBaseUrl = 'https://ekitag-api.herokuapp.com/v1/';
// var apiBaseUrl = "http://localhost:5000/v1/";

// Remove useless rows
playerStats[0].remove();

playerStats = [].slice.call(playerStats);
var matchData = {
  "datetime": new Date().toISOString(),
  "r_score": 0,
  "b_score": 0,
  "duration": null,
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
playerStats.forEach(function (player) {

  var playerCells = [].slice.call(player.cells);
  // Build match object
  var pseudo = playerCells[0].getElementsByTagName('span')[1].innerHTML;
  var playerTeam = playerCells[0].getElementsByTagName('span')[1].className.split(' ')[1].split('-')[
    1]

  if (playerTeam == 'red') {
    redIndex += 1;
    matchData['r' + redIndex + '_pseudo'] = pseudo;
    matchData['r_score'] += Number(playerCells[7].innerHTML)
  } else if (playerTeam == 'blue') {
    blueIndex += 1;
    matchData['b' + blueIndex + '_pseudo'] = pseudo;
    matchData['b_score'] += Number(playerCells[7].innerHTML)
  }

  // Build player stats object
  var playerStats = {
    user_pseudo: pseudo,
    score: Number(playerCells[1].innerHTML),
    tags: Number(playerCells[2].innerHTML),
    popped: Number(playerCells[3].innerHTML),
    grabs: Number(playerCells[4].innerHTML),
    drops: Number(playerCells[5].innerHTML),
    hold: Number(playerCells[6].innerHTML.split(':')[0]) * 60 + Number(playerCells[6].innerHTML
      .split(':')[1]),
    captures: Number(playerCells[7].innerHTML),
    prevent: Number(playerCells[8].innerHTML.split(':')[0]) * 60 + Number(playerCells[8].innerHTML
      .split(':')[1]),
    returns: Number(playerCells[9].innerHTML),
    support: Number(playerCells[10].innerHTML),
    pups: Number(playerCells[11].innerHTML),
  };

  playersStats.push(playerStats);
});

// Approximation of match duration (min is to limit max length to 600 secs = 10 mins)
matchData['duration'] = Math.min(600, playersStats.reduce(function(sum, pl) {
  return sum + pl['hold'] + pl['prevent'];
}, 0) / 2);
if(matchData['duration'] >= 540 || (matchData['r_score'] < 5 && matchData['b_score'] < 5)) {
  matchData["duration"] = 600;
}

var msg = "Content scrapped :\n"
msg += 'SCORE :\n RED ' + matchData.r_score + ' - BLUE : ' + matchData.b_score
msg += '\nDURATION: ' + matchData.duration
msg += '\nPLAYERS :'
playersStats.forEach(function (player) {
  msg += '\n' + player.user_pseudo;
});
alert(msg);

// Convert matchData to FormData for post request
var matchFormData = new FormData();
for (var key in matchData) {
  matchFormData.append(key, matchData[key]);
}

// BUILD MATCH REQUEST
var matchDataRequest = new XMLHttpRequest();
console.log('Sending request...');
matchDataRequest.open('POST', apiBaseUrl + 'matches/pending', true);
matchDataRequest.onreadystatechange = function () {
  console.log("passed matchDataRequest.onreadystatechange");
  console.log(this.readyState);
  console.log(this.status);
  console.log(this);
  // TO Remove
  var response = JSON.parse(matchDataRequest.response)
  console.log(response);
  if (this.readyState == 4 && this.status == 200) {
    console.log("passed this.readyState=4");
    var response = JSON.parse(matchDataRequest.response)
    console.log(response);
    var matchId = response.value;
    console.log(matchId);

    // Send one request per player stats
    var confirmedPlayers = 0;
    playersStats.forEach(function (player) {
      console.log(player);

      var statsFormData = new FormData();
      for (var key in player) {
        statsFormData.append(key, player[key]);
      }

      var statRequest = new XMLHttpRequest();
      statRequest.open('POST', apiBaseUrl + 'matches/pending/' + matchId + '/stats', true);
      statRequest.onreadystatechange = function () {
        console.log("passed second state change");

        if (this.readyState == 4 && this.status == 200) {
          console.log("passed readyState");
          confirmedPlayers += 1;
          console.log(confirmedPlayers);
          if (confirmedPlayers == playerStats.length) {
            alert("Succesfully sent match !")
          }
        }
      }
      statRequest.send(statsFormData);
    })

  }
};
matchDataRequest.send(matchFormData);
