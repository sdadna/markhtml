#!/usr/bin/env python
# coding=utf-8

import sys
import re
from handlers import *
from util import *
from rules import *

class Parser:
    def __init__(self, handler):
        self.handler = handler
        self.rules = []
        self.filters = []

    def addRule(self, rule):
        self.rules.append(rule)

    def addFilter(self, pattern, name):
        def filter(block, handler):
            return re.sub(pattern, handler.sub(name), block)
        self.filters.append(filter)

    def parse_type(self, block, type):
        if type == 'title':
            block = block[1:].upper()
        elif type == 'heading1':
            block = block[2:]
        elif type == 'heading2':
            block = block[3:]
        elif type == 'heading3':
            block = block[4:]
        elif type == 'heading4':
            block = block[5:]

        if type == 'comment':
            block = block[2:]

        return block

    def parse(self, file):
        self.handler.start('document')
        for block in blocks(file):
            for filter in self.filters:
                block = filter(block, self.handler)

            for rule in self.rules:
                condition,btype = rule.condition(block)
                if condition:
                    bblock = self.parse_type(block, btype)
                    last = rule.action(bblock, self.handler)
                    if last:break
                 
        self.handler.end('document')

class BasicTestPaser(Parser):
    def __init__(self, handler,):
        Parser.__init__(self, handler)
        self.addRule(CommentRule())
        self.addRule(ListRule())
        self.addRule(ListItemRule())
        self.addRule(TitleRule())
        self.addRule(HeadingRule())
        self.addRule(ParagraphRule())
        

        self.addFilter(r'\*{2}([^*]+)\*{2}', 'blod')
        self.addFilter(r'[\s]\*([^*]+)\*[\s]', 'emphasis')
        self.addFilter(r'(http://[\.a-zA-Z/]+)','url')
        self.addFilter(r'([\.a-zA-Z\d]+@[\.\da-zA-Z]+[a-zA-Z]+)','email')
        self.addFilter(r'[\\]([^a-zA-A0-9])', 'transform')

handler = HTMLHandler()
parser = BasicTestPaser(handler)
#with  open('test_input.txt','r+') as file:
#   print file.read()
parser.parse(sys.stdin)


