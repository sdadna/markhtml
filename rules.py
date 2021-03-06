#!/usr/bin/env python
# coding=utf-8

import pdb

class Rule:
    
    def action(self, block, handler):
        handler.start(self.type)
        handler.feed(block)
        handler.end(self.type)
        return True

class HeadingRule(Rule):
    type = []   
    def condition(self, block):
        if block[0:2] == "##" and block[2] != '#': 
            self.type = 'heading1'
        elif block[0:3] == '###' and block[3] != '#':
            self.type = 'heading2'
        elif block[0:4] == '####' and block[4] != '#':
            self.type = 'heading3'
        elif block[0:5] == '#####' and block[5] != '#':
            self.type = 'heading4'
        else:
            self.type = 'heading5:'

        return not '\n' in block and len(block) < 50 , self.type


class TitleRule(Rule):
    type = []
    def condition(self, block):
        self.type = 'title'
        if block[0] == '#' and block[1] != '#':

            return not '\n' in block and len(block) <= 50 and not block[-1] == ':', self.type
        
        return False, self.type
    
class ListItemRule(Rule):
    type = 'listitem'
    def condition(self, block):
        return block[0] == '-', self.type
    def action(self, block, handler):
        handler.start(self.type)
        handler.feed(block.strip('-'))
        handler.end(self.type)
        return True


class ListRule(ListItemRule):
    type = 'list'
    inside = False
    def condition(self, block):
        return True, self.type
    def action(self, block, handler):
        if not self.inside and ListItemRule.condition(self, block)[0]:
            handler.start(self.type)
            self.inside = True
        elif self.inside and not ListItemRule.condition(self, block)[0]:
            handler.end(self.type)
            self.inside = False
        return False

class MultiListRule(Rule):
    type = 'multilist'
    num = 0
    def compute_symbol(self, block):
        num = 0
        for x in block:
            if x == '-': 
                num += 1
            else:
                break
        return num

    def condition(self, block):
        self.num = self.compute_symbol(block)
        if self.num < 2:
            self.num = 0
            
        return self.num >= 2, self.type

    def action(self, block, handler):
        for i in range(self.num - 1):
            handler.start('list')
       
        ListItemRule().action(block, handler)

        for i in range(self.num - 1):
            handler.end('list')

        self.num = 0
        return True
    
class ParagraphRule(Rule):
    type = 'paragraph'
    def condition(self, block):        
        if block: return  True, self.type

class CommentRule(Rule):
    type = 'comment'
    def condition(self, block):
        if block[0:2] == '> ':
            return True, self.type
        return False, self.type

        
