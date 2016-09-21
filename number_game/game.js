var scr = document.getElementById('screen');
var score = 0;
var myTimeInt;
var total = 0;
var key;
var nNum = 0;
var curNNum = 0;
var startTime = new Date().getTime();

function start() {
	clearInterval(myTimeInt);
	score = 0;
	total = 0;
	scr.value = '';
	document.getElementById('score').innerHTML = 0;
	document.getElementById('keypressed').innerHTML = '';
	myTimeInt = setInterval(outNum, document.getElementById('speed').value);
}

function increaseSpeed() {
	clearInterval(myTimeInt);
	document.getElementById('speed').value -= 100;
	myTimeInt = setInterval(outNum, document.getElementById('speed').value);
}

function outNum() {
	if (scr.value.length == 10) {
		alert('you lost\n\nScore: ' + score);
	}
	scr.value += Math.floor(Math.random() * 9) + 1;
}

function keyEventHandler(e) {
	if (!e) {
		e = window.event;
	}
	key = e.which;
	if (!key) {
		key = e.keyCode;
	}
	key = key - 48;
	if (key >= 0 && key <= 9) {
		var re = new RegExp(key);
		if (scr.value.match(re)) {
			scr.value = scr.value.replace(re, '');
			checkScore();
		}
	}
}

function clear() {
	document.getElementById('bonus').innerHTML = '';
}

function checkScore() {
	total += key;
	nNum++;
	curNNum++;
	if (total % 10 == 0) {
		//score += Math.pow(10, total / 10);
		score += 10;
		if (score % 50 == 0) {
			increaseSpeed();
		}
		document.getElementById('efficiency').innerHTML = (nNum / (score / 10)).toFixed(2) + ' numbers per hit';
		document.getElementById('time_efficiency').innerHTML = ((new Date().getTime() - startTime) / (score / 10) / 1000).toFixed(2) + ' seconds per hit';
		total = 0;
		var grade;
		if (curNNum == 2) {
			grade = 'Incredible';
		} else if (curNNum == 3) {
			grade = 'Excellent';
		} else if (curNNum <= 5) {
			grade = 'Good';
		} else if (curNNum <= 8) {
			grade = 'Fine';
		} else if (curNNum <= 12) {
			grade = 'Poor';
		} else {
			grade = 'Booched';
		}
		document.getElementById('bonus').innerHTML = grade + ' hit!';
		curNNum = 0;
		setTimeout(clear, 1000);
	}
	if (document.getElementById('show_num_stack').checked) {
		document.getElementById('keypressed').innerHTML = total;
	} else {
		document.getElementById('keypressed').innerHTML = '';
	}
	document.getElementById('score').innerHTML = score;
}

document.onkeypress = keyEventHandler;
