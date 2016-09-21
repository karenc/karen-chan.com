#!/usr/bin/perl

use CGI qw(:standard);

sub new_grid() {
	@char = ('a'..'z');
	$v = 0;
	while ($v < 3) {
		%grid = ();
		$v = 0;
		for ($i = 0; $i < 9; $i++) {
			$r = int(rand() * $#char);
			if (exists($grid{$char[$r]})) {
				$i--; 
				next;
			} else {
				($grid{$char[$r]} = 0);
				if ($char[$r] =~ /[aeiou]/) {
					$v++;
				}
			}
		}
	}
}

print header;
print <<HTML;
<html>
	<head>
		<title>Make-A-Word</title>
		<style type="text/css">
		 	body {
				font-family: arial;
			}
			#top {
				background-color : black;
				color : red;
				font-weight : bold;
				position : absolute;
				left : 20px;
				top : 10px;
				width : 510px;
			}
			#left {
				position : absolute;
				left : 20px;
				top : 40px;
				width : 200px;
			}
			#right {
				border : 1px solid black;
				margin-top : 40px;
				margin-left : 220px;
				background-color : #eea;
				height : 135px;
				width : 300px;
				overflow : auto;
			}
			#word {
				border : 1px solid black;
				background-color : #eea;
				font-family : fixed-width;
				width : 200px;
			}
			#bottom {
				position : absolute;
				background-color : black;
				color : red;
				left : 20px;
				margin-top : 10px;
				margin-bottom : 10px;
				width : 510px;
				font-weight : bold;
			}
			#instructions {
				position : absolute;
				border : 1px solid black;
				left : 20px;
				top : 210px;
				width : 508px;
			}
		</style>
		<script type="text/javascript">
			var list = new Array();
			function onwordchange(e) {
				e.preventDefault();
				var word = document.getElementById("word").value;
				document.getElementById("word").value = "";
				if (isInList(word)) {
					document.getElementById("bottom").innerHTML = "Word is already in List";
					return false;
				}
				if (!isInGrid(word)) {
					document.getElementById("bottom").innerHTML = "Word contains characters not in the grid";
					return false;
				}
				if (word.length < 3) {
					document.getElementById("bottom").innerHTML = "Word cannot contain less than 3 characters";
					return false;
				}
				list[list.length] = word;
				document.getElementById("right").innerHTML += word + "\\n";
				document.getElementById("right").scrollTop = document.getElementById("right").scrollHeight;
				document.getElementById("bottom").innerHTML = "&nbsp;";
				return false;
			}
			function isInList(word) {
				for (i = 0; i < list.length; i++) {
					if (list[i] == word) {
						return true;
					}
				}
				return false;
			}
			var grid;
			function isInGrid(word) {
HTML

&new_grid();
@key = (keys %grid);
print "\t\t\t\tgrid = \"".join('', @key)."\";\n";
print "\t\t\t\tif (word.match(/[^".join('', @key)."]/)) {;\n";
print <<HTML;
					return false;
				} else {
					return true;
				}
			}
			function timer() {
				var time = document.getElementById("top").innerHTML.substring(11);
				if (time == 0) {
					submit();
					return;
				}
				document.getElementById("top").innerHTML = "Time Left: " + (time - 1);
				setTimeout('timer()', 1000);
			}
			function submit() {
				alert("time's up!");
				var param = list.join("+");
				document.location.href = "make_a_word.cgi?l=" + param + "&w=" + grid;
			}
		</script>
        <script type="text/javascript">

          var _gaq = _gaq || [];
          _gaq.push(['_setAccount', 'UA-34774368-1']);
          _gaq.push(['_setDomainName', 'karen-chan.com']);
          _gaq.push(['_trackPageview']);

          (function() {
            var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
            ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
            var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
          })();

        </script>
	</head>
	<body>
		<div id="top">Time Left: 120</div>
		<div id="left">
		<table style="font-size: 15pt; " border="1" align="center">
HTML

$i = 0;
for $key (keys %grid) {
	if ($i % 3 == 0) {
		if ($i != 0) {
			print "\t\t\t</tr>\n\t\t\t<tr>\n";
		} else {
			print "\t\t\t<tr>\n";
		}
	}
	print "\t\t\t\t<td align=\"center\" width=\"20\">$key</td>\n";
	$i++;
}
print <<HTML;
			</tr>
		</table>
		<br />
		<form id="game">
		<input type="text" id="word" />
		<input type="submit" style="display : none;" />
		</form>
		</div>
		<div id="right">
		</div>
		<div id="bottom">
			&nbsp;
		</div>
		<div id="instructions">
			<b>Browser Requirements:<br /></b>
			<a href="http://www.getfirefox.com/">Firefox</a><br /><br />
			<b>Instructions:<br /></b>
			You will be given 9 letters.  From these letters, make as many words as possible within 2 minutes using any combination of the letters.  Letters may be used as many times as necessary, or not at all.  Words must be longer than 3 letters, and must be real words.<br /><br />
			<b>Scoring:<br /></b>
			<table>
				<tr>
					<td>10 points</td>
					<td>for each real word in the list</td>
				</tr>
				<tr>
					<td>2 point bonus</td>
					<td>for 4-letter real words</td>
				</tr>
				<tr>
					<td>5 point bonus</td>
					<td>for 5-letter real words</td>
				</tr>
				<tr>
					<td>10 point bonus</td>
					<td>for 6-letter real words</td>
				</tr>
				<tr>
					<td>20 point bonus</td>
					<td>for 7-letter real words</td>
				</tr>
				<tr>
					<td>50 point bonus</td>
					<td>for 8-letter or more real words</td>
				</tr>
				<tr>
					<td><font color="red">1 point deduction</font></td>
					<td>for each letter in a non-real word</td>
				</tr>
			</table>
			<br /><font size="1"><i>Written in <a href="http://www.vim.org/">VIM</a> for Firefox</i></font><br />
		</div>
		<script type="text/javascript">
			setTimeout('timer()', 1000);
			document.getElementById("word").focus();
			document.getElementById('game').onsubmit = onwordchange;
		</script>
	</body>
</html>
HTML
