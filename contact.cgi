#!/usr/bin/env python

import cgi
#import cgitb; cgitb.enable()
import datetime

fields = cgi.FieldStorage()
f = open('/home/karen/karen-chan-contact.txt', 'a')
f.write('Sent at %s\nName: %s\nEmail: %s\nMessage: %s\n\n' % (
    datetime.datetime.now().strftime('%Y-%m-%d %H:%S'),
    fields.getfirst('name'), fields.getfirst('email'),
    fields.getfirst('message')))
f.close()

print 'Location: /contact.html\r\n\r\n'
