use lib "/home/karen/.irssi/scripts/libwww-perl-5.826/lib/";
use strict;
use vars qw($VERSION %IRSSI);
use POSIX;

use Irssi;
$VERSION = '0.0.3';
%IRSSI = (
    authors        => 'karen chan',
    contact        => 'karen@karen-chan.com',
    name           => 'linktitle',
    description    => 'priv msg the title of the urls',
    url            => '',
    license        => '',
);

my %pipe_tag = ();

sub linktitle {
    my ($server, $msg, $nick, $address, $target) = @_;
    chomp($msg);

    if ($msg !~ /(http[^ ]*)/) {
        return;
    }
    if ($nick eq $server->{'nick'}) {
        return;
    }

    my $url = $1;
    my ($rh, $wh);
    pipe $rh, $wh;
    my $pid = fork();
    unless (defined $pid) {
        close($rh);
        close($wh);
        return;
    } elsif ($pid) {
        close($wh);
        Irssi::pidwait_add($pid);
        $pipe_tag{$rh} = Irssi::input_add(fileno($rh), INPUT_READ, \&respond, [$server, $rh]);
        return;
    }
    close($rh);
    get_title($wh, $url, $server->{'nick'}, $nick, $target);
    POSIX::_exit(1);
}

sub respond {
    my ($server, $readhandle) = @{@_[0]};
    my $line = '';
    $line .= $_ while (<$readhandle>);
    Irssi::print($line);
    Irssi::input_remove($pipe_tag{$readhandle});
    close($readhandle);
}

sub get_title {
    my ($wh, $url, $my_nick, $nick, $target) = @_;
    use LWP::UserAgent;
    my $ua = LWP::UserAgent->new;
    $ua->agent('Mozilla/5.0 (X11; U; Linux i686; en-GB; rv:1.9.0.10) Gecko/2009042513 Ubuntu/8.04 (hardy) Firefox/3.0.10');
    my $response = $ua->get($url);
    my $content = $response->content;
    if ($content =~ /<title>([^<]*)<\/title>/i) {;
        my $title = $1;
        print $wh "<$nick> " . $response->title . " $url";
    } else {
        print $wh "<$nick> " . $response->base . " $url";
    }
    close($wh);
}

Irssi::signal_add({
        'message public' => \&linktitle,
        'message private' => \&linktitle,
    });
