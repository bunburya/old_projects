from html.parser import HTMLParser

class HTMLHandler(HTMLParser):
    
    def __init__(self):
        self.data = ''
        HTMLParser.__init__(self)
    
    def handle_data(self, data):
        self.data += data
    
    def handle_endtag(self, tag):
        if tag == 'p':
            self.data += '\n\n'
        if tag == 'img':
            self.data += '[IMAGE]'
    
    def get(self):
        return self.data
