#!/usr/bin/env python
# coding=utf-8
import re,sys
from util import *

print '<html><head><meta charset="utf-8"><title>即时标记 script</title><body>'

title = True
for block in blocks(sys.stdin):
    block = re.sub(r'\*(.+?)\*',r'<em>\1</em>',block)
    if title:
        print '<h1>'
        print block
        print '</h1>'
        title = False

    else:
        print '<p>'
        print block
        print '</p>'
      #  title = True

print '</body></html>'

