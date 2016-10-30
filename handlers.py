#!/usr/bin/env python
# coding=utf-8

class Handler:
    
    def callback(self, prefix, name, *args):
        method = getattr(self, prefix+name, None)
        if callable(method): 
            return method(*args)

    def start(self, name):
        self.callback("start_", name)

    def end(self, name):
        self.callback("end_", name)

    def sub(self, name):#改成直接调用会怎么样
        def substitution(match):
            result = self.callback("sub_", name, match)
            if result is None: match.group(0)
            return result
        return substitution

class HTMLHandler(Handler):

    def start_document(self):
        print "<html><head><meta charset='gb2312'><title>...</title></head><body>"

    def end_document(self):
        print "<body><html>"
    
    def start_title(self):
        print "<h1>"

    def end_title(self):
        print "</h1>"

    def start_heading1(self):
        print "<h2>"

    def end_heading1(self):
        print "</h2>"
    
    def start_heading2(self):
        print "<h3>"
    
    def end_heading2(self):
        print "</h3>"

    def start_heading3(self):
        print "<h4>"
    
    def end_heading3(self):
        print "</h4>"

    def start_heading4(self):
        print "<h5>"

    def end_heading4(self):
        print "</h5>"

    def start_heading5(self):
        print "<h6>"

    def end_heading5(self):
        print "</h6>"

    def start_list(self):
        print "<ul>"

    def start_paragraph(self):
        print "<p>"

    def end_paragraph(self):
        print "</p>"
    
    def start_comment(self):
        print "<blockquot>"

    def end_comment(self):
        print "</blockquot>"

    def end_list(self):
        print "</ul>"

    def start_listitem(self):
        print "<li>"

    def end_listitem(self):
        print "</li>"

    
    def sub_emphasis(self, match):
        return "<em>%s</em>" % match.group(1)
    
    def sub_blod(self, match):
        return "<B>%s</B>" % match.group(1)
    
    def sub_url(self, match):
        return '<a href="%s"> %s </a>' %(match.group(1), match.group(1))

    def sub_email(self, match):
        return '<a href="mailto:%s">%s</a>' %(match.group(1), match.group(1))

    def sub_transform(self, match):
        return '%s' %match.group(1)

    def feed(self, data):
        print data

