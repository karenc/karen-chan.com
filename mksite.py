#!/usr/bin/env python

import ConfigParser
import os
import re
import sys

TMPL = 'site.tmpl'

def generate(filename, **kwargs):
    template_name = filename.rsplit('.', 1)[0]
    outfile = '{}.html'.format(template_name)
    print 'Generating %s' % outfile
    template = open(TMPL).read()
    names = re.findall('%\(([A-Za-z0-9_]+)\)', template)
    variables = dict([(v, '') for v in names])
    variables['page_name'] = template_name
    variables.update(kwargs)
    output = open(outfile, 'w')
    output.write(template % variables)
    output.close()

def read(filename):
    config = ConfigParser.ConfigParser({'header': ''})
    config.read(filename)
    page_vars = dict(config.items('page'))
    generate(os.path.basename(filename), **page_vars)

def main(files):
    for f in files:
        read(f)

if __name__ == '__main__':
    main(sys.argv[1:])
