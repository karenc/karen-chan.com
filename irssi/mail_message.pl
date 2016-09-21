use strict;
use vars qw($VERSION %IRSSI);
use POSIX;

use Irssi;
$VERSION = '0.0.3';
%IRSSI = (
    authors     => 'karen chan',
    contact     => 'karen@karen-chan.com',
    name        => 'mail_message',
    description => 'Sends you an email when you get a message',
    url         => '',
    license     => '',
    changed     => '',
);

my $my_email_address = 'karen@karen-chan.com';
my $my_nick = 'karen';
my %from_addresses = (
    'karen' => 'karen@karen-chan.com',
    'example' => 'example@example.com',
);

my $cmd = "echo \"%s\" | mail %s -s 'irc message' $my_email_address";

sub receive_message {
    my ($server, $msg, $nick, $address, $target) = @_;
    chomp($msg);

    if (!$server->{usermode_away}) {
        return;
    }

    if ($target && $msg !~ /$my_nick/) {
        return;
    }

    my $reply_to = '';
    if (exists $from_addresses{$nick}) {
        $reply_to = "-a 'From: $nick <$from_addresses{$nick}>'";
    }
    if ($target) {
        $msg = "<$nick, $target> $msg";
    } else {
        $msg = "<$nick> $msg";
    }
    $msg =~ s/"/"'"'"/g;
    chomp($msg);
    my $mail = sprintf($cmd, $msg, $reply_to);
    `$mail`;
}

Irssi::signal_add({
        'message public' => \&receive_message,
        'message private' => \&receive_message,
    });
