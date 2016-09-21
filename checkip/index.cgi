#!/usr/bin/env python

import cgitb; cgitb.enable()

import cgi
import os
import socket
import sys

sys.path.append('/home/karen/.local/lib/python2.7/site-packages')

from geoip import geolite2

form = cgi.FieldStorage()

remote_addr = form.getfirst('ip', os.getenv('REMOTE_ADDR'))
try:
    hostname = remote_addr and socket.gethostbyaddr(remote_addr)[0]
    hostname = '({})'.format(hostname)
except (IndexError, socket.herror, socket.gaierror):
    hostname = ''

match = geolite2.lookup(remote_addr)

print('Context-Type: text/plain\r\n\r')
print('Current IP Address: {} {}'.format(remote_addr, hostname))
print('Country: {} Timezone: {}'.format(match.country, match.timezone))
