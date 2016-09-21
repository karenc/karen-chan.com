#!/usr/bin/env python

import os
import sys
sys.path.append('/home/karen/src/to_pinyin')

import cgi
import cgitb
cgitb.enable()

import to_pinyin

title = 'Translate Chinese characters into pinyin'
form = '''
            <form action="" method="post">
                <div><label for="text">Enter text here:</label></div>
                <textarea name="text" id="text" cols="100" rows="20">%(value)s</textarea>
                <div class="form-footer">
                    <input type="submit" class="button" value="Submit" />
                </div>
            </form>
            '''

fields = cgi.FieldStorage()
text = fields.getfirst('text', '')

if text:
    remote_addr = os.getenv('REMOTE_ADDR')
    f = open(remote_addr, 'a')
    f.write(text + '\n\n')
    f.close()

def get_body(text):
    if not text:
        return ''

    try:
        text = unicode(text, 'utf-8')
    except UnicodeDecodeError:
        return ''

    def gen_body():
        yield '<pre>'
        for line in text.split('\n'):
            original = []
            for i, char in enumerate(line):
                if i % 30 == 0:
                    yield '\n'
#                    yield ''.join(original).encode('utf-8')
#                    yield '\n'
#                    original = []
                else:
                    yield ' '
                original.append(char)
                yield '<ruby><rb>%s</rb><rt>%s</rt></ruby>' % (
                        char.encode('utf-8'),
                        to_pinyin.get_pinyin(char).encode('utf-8'))
            to_pinyin.write_cache()
            yield '\n'
#            yield ''.join(original).encode('utf-8')
            yield '\n'
        yield '</pre>'

    return gen_body()

sys.stdout.write('''Content-Type: text/html;charset=utf-8\r
\r
<html>
    <head>
        <title>%(title)s</title>
        <style type="text/css">
            #content {
                margin: 0px auto;
                background-color: #eee;
                border: 1px dashed black;
                padding: 10px;
                font-size: 18px;
                font-family: arial,sans-serif;
                text-align: center;
            }
            h1 {
                font-size: 18px;
                margin: 0 0 10px 0;
            }
            textarea {
                font-size: 14px;
            }
            label {
                font-size: 14px;
            }
            .button {
                font-weight: bold;
                border: 1px solid black;
            }
            .form-footer {
                margin-top: 10px;
            }
        </style>
        <link rel="stylesheet" href="ruby.css" type="text/css" />
    </head>
    <body>
        <div id="content">
            <h1>%(title)s</h1>
''' % {
    'title': title,
    })

sys.stdout.write(form % {'value': text})

sys.stdout.write('<hr />')
for line in get_body(text):
    sys.stdout.write(line)
    sys.stdout.flush()

sys.stdout.write('''
        </div>
    </body>
</html>
''')
