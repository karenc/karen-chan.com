#!/usr/bin/perl

use CGI qw(:standard);

print "Content-Type: text/html\n\n";
@words_list = split(/ /, param('l'));
$dict_file = '/usr/share/dict/words';
$UP_LIMIT = 20;
$DOWN_LIMIT = 3;

print <<HTML;
<html>
	<head>
		<title>Make-A-Word Result</title>
		<style type="text/css">
			#left {
				float : left;
				border : 1px solid black;
				background-color: #eea;
				height : 500px;
				overflow : auto;
			}
			#right {
				border : 1px solid black;
				height : 500px;
				overflow : auto;
				padding-left : 20px;
			}
			h3 {
				display : inline;
			}
			a {
				text-decoration : none;
			}
			a:hover {
				text-decoration : underline;
			}
		</style>
	</head>
	<body>
		<div id="left">
HTML

open(DICT, "$dict_file");
while (<DICT>) {
	chomp;
	if ((length($_) > $UP_LIMIT) || (length($_) < $DOWN_LIMIT) || (/'/) || /^[A-Z]/) {
		next;
	}
	$m = 1;
	for ($i = 0; $i <= length($_); $i++) {
		if (!&exist(substr($_, $i, 1))) {
			$m = 0;
			last;
		}
	}
	($m == 0) ? next : ($comp{$_} = 0);
}
close(DICT);

$total_words = keys %comp;

$score = 0;
printf "<h3>Words you found: (\%d)(\%d%%)</h3><br />\n", $#words_list, ($#words_list / $total_words * 100);
print "<table>";
foreach $word (@words_list) {
	if (exists($comp{$word})) {
		$tmp_score = 10;
		if (length($word) == 4) {
			$tmp_score += 2;
		} elsif (length($word) == 5) {
			$tmp_score += 5;
		} elsif (length($word) == 6) {
			$tmp_score += 10;
		} elsif (length($word) == 7) {
			$tmp_score += 20;
		} elsif (length($word) >= 8) {
			$tmp_score += 50;
		}
		delete($comp{$word});
	} else {
		$tmp_score = 0 - length($word);
	}
	$score += $tmp_score;
	print "<tr><td>$word</td><td>($tmp_score)</td></tr>\n";
}
print "</table>\n";
print "<br /><b>Score: $score</b><br /><br />\n";

open(SCORE, ">score.txt");
print SCORE "$score";
close(SCORE);

print <<HTML;
		<h3>Enter your name:</h3><br />
		<form action="submit_maw_hiscore.cgi" method="POST" />
			<input type="text" name="name" value="anonymous" size="10" />
			<input type="submit" value="submit" />
		</form>
HTML

print <<HTML;
		</div>
		<div id="right">
			<h3>Hi-Socre List</h3><br />
			<table border="1" width="50%">
HTML

open(HISCORE, "cat maw_hiscore.txt | sort -n -k 2 -r | head -20 |");
while (<HISCORE>) {
	my @score = split(/ /);
	print "\t\t\t\t<tr><td width=\"80%\">$score[0]</td><td>$score[1]</td></tr>\n";
}
close(HISCORE);
print "\t\t\t</table><br />\n";

@keys = keys %comp;
print "\n<h3>Words you missed: ($#keys)</h3><br />\n";
print "<table border=\"1\">\n";
$i = 0;
foreach $key (sort keys %comp) {
	if ($i % 5 == 0) {
		if ($i != 0) {
			print "</tr>";
		}
		print "<tr>";
	}
	$i++;
	print "<td width=\"20%\">$key</td>\n";
}

print <<HTML;
			</table>
		</div>
		<center>
			<h1><a href="maw.cgi">New Game</a></h1>
		</center>
	</body>
</html>
HTML

sub exist() {
	local $l = $_[0];
	local $i;
	local $w = param('w');
	for ($i = 0; $i <= length($w); $i++) {
		if (substr($w, $i, 1) =~ /$l/i) {
			return 1;
		}
	}
	return 0;
}
