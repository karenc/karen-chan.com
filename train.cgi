#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cgi
import cgitb; cgitb.enable()
import cookielib
import json
import random
import urllib
import urllib2
import urlparse

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
base_url = 'http://ojp.nationalrail.co.uk/'
url = 'http://ojp.nationalrail.co.uk/en/s/ldb/liveTrainsJson'
referer = 'http://ojp.nationalrail.co.uk/en/s/ldbboard/%s/%s'
user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0 Iceweasel/31.6.0'
json_train_fields = [
    '',
    'Due',
    'Dest',
    'Stat',
    'Platf',
    'X',
    ]


def get_train_times(at, departing=True, to=''):
    if not departing:
        json_train_fields[2] = 'Origin'
    data = {
        'departing': departing,
        'liveTrainsFrom': at,
        'liveTrainsTo': to,
        'serviceId': '',
        'f': '',
    }
    # Get cookies from ldb board
    ldb_url = urlparse.urljoin(base_url, '/service/ldbboard/{}/{}'.format(departing and 'dep' or 'arr', at))
    if to:
        ldb_url = '{}/{}/{}'.format(ldb_url, to, departing and 'To' or 'From')
    ldb_url = '{}?j=0'.format(ldb_url)
    content = opener.open(ldb_url).read()

    req = urllib2.Request('?'.join([url, urllib.urlencode(data)]))
    req.add_header('Referer', referer % (
        departing and 'dep' or 'arr', at))
    req.add_header('User-Agent', user_agent)
    content = opener.open(req).read()
    try:
        trains = [dict(zip(json_train_fields, train))
            for train in json.loads(content)['trains']]
    except ValueError:
        trains = []
    for train in trains:
        train['Due'] = '<a href="?details=%s&at=%s&departing=%s&to=%s">%s</a>' % (
            urllib.quote_plus(train['X']), at, departing, to, train['Due'])
    return trains

def construct_train_timestable(at, departing=True, to=''):
    train_times = get_train_times(at, departing, to)
    results = []
    for train_time in train_times:
        row = ['<td>%s</td>' % train_time[k].replace('&lt;', '<').replace(
                '&gt;', '>')
            for k in json_train_fields[1:-1]]
        css_class = ''
        if 'late' in row[-2] or 'Cancelled' in row[-2] or 'Delayed' in row[-2]:
            css_class = 'delayed'
        results.append(''.join('<tr class="%s">%s</tr>' % (
                        css_class, ''.join(row))))
    request = '''
        <table>
            <tr>
                %(headers)s
            </tr>
            %(time_table)s
        </table>
''' % {
        'headers': ''.join(['<th>%s</th>' % f for f in json_train_fields[1:-1]]),
        'time_table': ''.join(results),
    }
    return request

def construct_form(at, departing=True, to=''):
    form = '''
        <form class="clearfix" action="">
            <div class="clearfix field">
                <label for="at">Station:</label>
                <input id="at" name="at" type="text" value="%(at)s" />
            </div>
            <div class="clearfix field">
                <select name="departing">
                    <option %(select_depart)s value="true">Dep To</option>
                    <option %(select_arrive)s value="false">Arr From</option>
                </select>
                <input id="to" name="to" type="text" value="%(to)s" />
            </div>
            <div class="clearfix field">
                <input type="hidden" name="random" value="%(random)s" />
                <input class="right" type="submit" value="Submit" />
            </div>
        </form>
''' % {
        'at': at,
        'select_depart': departing and 'selected="selected"' or '',
        'select_arrive': not departing and 'selected="selected"' or '',
        'to': to,
        'random': random.randint(0, 10000),
    }
    return form

def get_train_detail(path):
    # get cookies
    get_train_times(at, departing, to)

    req = urllib2.Request(urlparse.urljoin(base_url, path))
    req.add_header('User-Agent', user_agent)
    req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    content = opener.open(req).read()
    # extract just the train time table
    start = content.find('<div id="live-departure-details"')
    if start == -1:
        return 'Unable to get information from nationalrail.co.uk'
    end = len(content)
    divs = 1
    current = start + 1
    while divs > 0:
        open_div = content.find('<div', current)
        close_div = content.find('</div>', current)
        if open_div == -1 and close_div == -1:
            break
        if open_div > close_div:
            divs -= 1
            current = close_div + 1
            end = close_div + 6
        else:
            divs += 1
            current = open_div + 1
    content = content[start:end]
    content = content.replace('Platform', 'Platf')
    content = content.replace('Status', 'Stat')
    content = content.replace('Departs', 'Dep')
    content = content.replace(
        'href="#"', 'href="?details=%s&at=%s&departing=%s&to=%s&random=%s"' % (
            urllib.quote_plus(path), at, departing, to, random.randint(0, 10000)))
    return content



fields = cgi.FieldStorage()

path = fields.getfirst('details', '')
departing = fields.getfirst('departing', 'true').lower() == 'true'
at = fields.getfirst('at', '')
to = fields.getfirst('to', '')

if path:
    body = get_train_detail(path)
    title = ''
    refresh = False

else:
    body = construct_form(at, departing, to)
    if at:
        body = ''.join([body, construct_train_timestable(at, departing, to)])
    title = at
    if to:
        title = '%s %s %s' % (title, departing and '->' or '<-',  to)
    refresh = True

print u'''Content-Type: text/html;charset=utf-8\r
\r
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=2.0, user-scalable=yes" />
    <title>%(title)s - Live Departure Board</title>
    %(refresh)s
    <style type="text/css">
        body {
            text-align: center;
            width: 300px;
            margin: auto;
        }
        table {
            border-collapse: collapse;
            margin: auto;
            font-size: 80%%;
            width: 100%%;
        }
        tr:nth-child(even) {
            background-color: #DDD;
        }
        table, th, td {
            border: 1px solid black;
        }
        label {
            font-size: 80%%;
            width: 100px;
            display: block;
            float: left;
        }
        input, select {
            width: 100px;
            display: block;
            float: left;
        }
        .right {
            float: right;
        }
        .field {
            margin: auto;
            width: 200px;
        }
        .clearfix:after, .clear:after {
            content: " ";
            display: block;
            height: 0;
            clear: both;
        }
        .delayed {
            color: red;
            font-weight: bold;
        }
        .departed {
            color: #888;
        }
        .departed.delayed {
            color: #f88;
        }
        .unbold {
            font-weight: normal;
        }
        .live-trains p,
        .live-trains span {
            text-align: left;
            margin: 0;
            display: block;
            font-size: 80%%;
        }
        .blue-lozenge {
            color: blue;
            font-weight: bold;
            text-align: left;
            margin: 0;
        }
        .blue-lozenge > span {
            font-size: 120%%;
        }
        #live-departure-details h2 {
            font-size: 100%%;
            margin: 0;
            margin-bottom: 5px;
            text-align: left;
        }
        .box-17 {
            display: none;
        }
        #live-departure-details ul {
            list-style-type: none;
        }
        #live-departure-details li {
            text-align: right;
        }
        .hidden {
            display: none;
        }
        .current:before {
            content: '[\\272a]';
            color: blue;
            font-size: 150%%;
            font-weight: normal;
        }
        .current * {
            display: none;
        }
        .disruptions {
            display: block;
            color: red;
        }
        .disruptions h3 {
            margin: 0;
            font-size: 100%%;
            text-decoration: underline;
            text-align: left;
        }
        .disruptions ul {
            padding: 0;
            margin: 0;
            font-size: 80%%;
        }
    </style>
</head>
<body>
    %(body)s
</body>
</html>''' % {
    'title': title,
    'body': body,
    'refresh': refresh and '<meta http-equiv="refresh" content="120" />' or '',
    }
