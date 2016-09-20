#!/usr/bin/env python

import cgi
import cgitb; cgitb.enable()
import json
import os
import shutil

STORAGE = os.path.join(os.path.dirname(__file__), '../colors.txt')
PREPARE = os.path.join(os.path.dirname(__file__), '../colors.txt.1')

def initialize():
    colors = ['blue']
    for i in range(24):
        colors.append('red')
        colors.append('blue')
    store(colors)

def store(colors):
    open(PREPARE, 'w').write(','.join(colors))
    shutil.move(PREPARE, STORAGE)

def load():
    return open(STORAGE).readline().split(',')

def read(params):
    print 'Content-Type: application/json\r\n\r'
    colors = load()
    if len(colors) == 1:
        initialize()
        colors = load()
    result = []
    for i, c in enumerate(colors):
        result.append({
            'color': c,
            'position': i,
            'id': i,
            })
    print json.dumps(result)

def update(params):
    form = cgi.FieldStorage()
    color = form.getvalue('color')
    position = form.getvalue('position')
    colors = load()
    colors[int(position)] = color
    store(colors)

methods = [
        ('read', read),
        ('update', update),
        ]

def main():
    params = cgi.parse_qs(os.getenv('QUERY_STRING'))
    try:
        method = params.pop('method')[0]
    except:
        method = None
    if method:
        for m, handler in methods:
            if method == m:
                return handler(params)

    print 'Content-Type: text/plain\r\n\r'
    print 'Not implemented'

if __name__ == '__main__':
    main()
