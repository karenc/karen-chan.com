#!/usr/bin/perl

use CGI qw(:standard);
use strict;

print header();

print <<HTML;
<html>
    <body>
        <table>
HTML

#foreach my $k (keys %ENV) {
#    print "<tr><td>$k</td><td>$ENV{$k}</td></tr>\n";
#}

print <<HTML;
        </table>
        <script type="text/javascript">
            document.write('<table border="1">');
            document.write('<tr><td>screen height</td><td>' + window.screen.height + '</td></tr>');
            document.write('<tr><td>screen width</td><td>' + window.screen.width + '</td></tr>');
            for (var i in navigator) {
                var results = navigator[i];
                if (typeof navigator[i] == 'function') {
                    results = navigator[i]();
                }
                if (i == 'plugins') {
                    var a = '';
                    for (var j = 0; j < results.length; j++) {
                        for (var k in results[j]) {
                            a += results[j][k] + ',';
                        }
                    }
                    results = a;
                }
                document.write('<tr><td>' + i + '</td><td>' + results + '</td></tr>');
            }
            document.write('</table>');
        </script>
    </body>
</html>
HTML
