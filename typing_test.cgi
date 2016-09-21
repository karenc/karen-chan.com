#!/usr/bin/perl

use CGI qw(:standard);

%textmap = ('great_expectation' => 'great_expectation');

print <<HTML;
Content-Type: text/html

<html>
	<head>
		<title>Typing Test</title>
		<style type="text/css">
			body {
				font-family : sans-serif;
				margin-left : 10%;
				margin-right : 10%;
			}
			.text {
				height : 250px;
				overflow : auto;
			}
			h1 {
				background-color : black;
				color : white;
				padding : 10px;
				margin-bottom : 0px;
			}
			#main {
				border : 1px solid black;
				text-align : center;
				padding : 10px;
			}
			#top {
				background-color : #eea;
			}
			#bottom {
				background-color : #bbf;
			}
			table {
				border-collapse: collapse;
			}
			td {
				border: 1px solid black;
			}
		</style>
		<script type="text/javascript">
			document.onkeypress = keypressed;
			if (navigator.userAgent.match(/Chrome/)) {
				document.onkeydown = keydown;
			}
			function keydown(e) {
				e = e ? e : window.event;
				var key = e.keyCode ? e.keyCode : e.which;
				// backspace character
				if (key == 8) {
					var body = document.getElementById('bottom').innerHTML;
					var lastChar = body.substring(body.length - 1);
					if (lastChar == ' ' || lastChar == '\\n') {
						return false;
					}
					body = body.substring(0, body.length - 1);
					typed_word = typed_word.substring(0, typed_word.length - 1);
					document.getElementById('bottom').innerHTML = body;
					return false;
				}
			}
			var total_words = 0;
			var typed_word = '';
			function keypressed(e) {
				e = e ? e : window.event;
				var key = e.keyCode ? e.keyCode : e.which;
				document.getElementById('bottom').scrollTop = document.getElementById('bottom').scrollHeight;
				// backspace character
				if (key == 8) {
					var body = document.getElementById('bottom').innerHTML;
					var lastChar = body.substring(body.length - 1);
					if (lastChar == ' ' || lastChar == '\\n') {
						return false;
					}
					body = body.substring(0, body.length - 1);
					typed_word = typed_word.substring(0, typed_word.length - 1);
					document.getElementById('bottom').innerHTML = body;
					return false;
				}
				// return character
				if (key == 13) {
					highlight();
					document.getElementById('bottom').innerHTML += '<br />\\n';
					return false;
				}
				// space character
				if (key == 32) {
					highlight();
					document.getElementById('bottom').innerHTML += ' ';
					return false;
				}
				// & character
				if (key == 38) {
					document.getElementById('bottom').innerHTML += '&amp;';
					typed_word += '&amp;';
					return false;
				}
				// < character
				if (key == 60) {
					document.getElementById('bottom').innerHTML += '&lt;';
					typed_word += '&lt;';
					return false;
				}
				// > character
				if (key == 62) {
					document.getElementById('bottom').innerHTML += '&gt;';
					typed_word += '&gt;';
					return false;
				}
				key = String.fromCharCode(key);
				document.getElementById('bottom').innerHTML += key;
				typed_word += key;
				return false;
			}
			var index = -1;
			var lines = 0;
			var expected_word = '';
			function highlight() {
				total_words++;
				match();
				var body = document.getElementById('top').innerHTML;
				body = body.replace('<font color="red"><b>', '');
				body = body.replace('</b></font>', '');
				var space = body.indexOf(' ', index);
				var newline = body.indexOf('\\n', index);
				var oldIndex = index;
				var which = '';
				if (space == -1 && newline == -1) {
					return;
				} else if (space == -1) {
					index = newline;
					which = 'newline';
				} else if (newline == -1) {
					index = space;
					which = 'space';
				} else {
					index = (space < newline) ? space : newline;
					which = (space < newline) ? 'space' : 'newline';
				}
				if (which == 'newline') {
					lines++;
					if (lines == 10) {
						document.getElementById('top').scrollTop += 150;
						lines = -1;
					}
				}
				expected_word = body.substring(oldIndex, index);
				expected_word = expected_word.replace('<br>', '');
				body = body.substring(0, oldIndex) + '<font color="red"><b>' + body.substring(oldIndex, index) + '</b></font>' + body.substring(index);
				index++;
				document.getElementById('top').innerHTML = body;
			}
			var correct_words = 0;
			function match() {
				if (expected_word != typed_word) {
					var body = document.getElementById('bottom').innerHTML;
					var space = body.lastIndexOf(' ');
					var newline = body.lastIndexOf('\\n');
					var match_index = 0;
					if (space == -1 && newline == -1) {
						match_index = 0;
					} else if (space == -1) {
						match_index = newline;
					} else if (newline == -1) {
						match_index = space;
					} else {
						match_index = (space > newline) ? space : newline;
					}
					body = body.substring(0, match_index) + '<font color="red">' + body.substring(match_index) + '</font>\\n';
					document.getElementById('bottom').innerHTML = body;
				} else {
					correct_words++;
				}
				typed_word = '';
			}
			function time() {
				var time = document.getElementById('time').innerHTML;
				time--;
				document.getElementById('time').innerHTML = time;
				if (time == 0) {
					alert("test finished!");
					var string = "<center>Gross speed: " + (total_words / total_time * 60) + " words per minute<br />" +
							"Accuracy: " + (correct_words / total_words * 100) + "%<br />" + "Net speed: " + 
							(correct_words / total_time * 60) + " words per minute<br /></center>\\n";
					document.body.innerHTML += string;
					return;
				}
				setTimeout('time()', 1000);
			}
		</script>
	</head>
	<body>
HTML

$length = param('length');
if (!exists $textmap{param('text')}) {
	print "\t\t\t<h1>Invalid choice of text</h1>\n";
} else {
	$choice = $textmap{param('text')};
	print "\t\t\t<h1>Typing Test</h1>\n";
	print "\t\t\t<div id=\"main\">\n";
	print '<table width="80%" align="center"><tr><td><div class="text" id="top">';
	$lines = `cat $choice | wc -l`;
	chomp($lines);
	$words = $length * 100;
	$head = int(rand() * ($lines - $words)) + $words;
	open(TEXT, "head -$head $choice | tail -$words | ");
	while (<TEXT>) {
		chomp;
		s/&/&amp;/g;
		s/</&lt;/g;
		s/>/&gt;/g;
		print "$_<br>\n";
	}
	close(TEXT);
	print '</td>';
	print '<td rowspan="2" width="20%">Time Left:<br /><div id="time">'.
			(param('length') * 60).'</div><br /><br /><a href="typing_test.html">Back to typing test</a></td>';
	print '</tr><tr><td><div id="bottom" class="text"></div></td></tr>';
	print '</table>';
}

print <<HTML;
		</div>
		<script type="text/javascript">
			var total_time = document.getElementById('time').innerHTML;
			time();
			highlight();
		</script>
	</body>
</html>
HTML
