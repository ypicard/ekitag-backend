alert('start script.js');

var playerStats = document.getElementById("stats").getElementsByTagName('tr');

// Remove useless rows
playerStats[0].remove();
playerStats[0].remove();
playerStats = [].slice.call(playerStats);

var final = {
  score: {
    red: 0,
    blue: 0,
  },
  players: [],
};

// Get each player's stats
playerStats.forEach(function(player) {
  var playerCells = [].slice.call(player.cells);
  var playerObj = {
    name: playerCells[0].getElementsByTagName('span')[1].innerHTML,
    team: playerCells[0].getElementsByTagName('span')[1].className.split(' ')[1].split('-')[1],
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
    powerups: playerCells[11].innerHTML,
  };

  final.score[playerObj.team] += parseInt(playerObj.captures);

  final.players.push(playerObj);

});

var msg = "Content scrapped :\n"
msg += 'SCORE :\n RED ' + final.score.red + ' - BLUE : ' + final.score.blue
msg += '\nPLAYERS :'
final.players.forEach(function(player) {
  msg += '\n' + player.name;
});
alert(msg);

var request = new XMLHttpRequest();
// Handle response 
request.onload = function() {
  var status = request.status;

  var data = request.responseText;
  console.log('Response status : ', status);
};

console.log('Sending request...');
request.open('POST', 'http://www.google.com/', true);
request.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
request.send(JSON.stringify(final));