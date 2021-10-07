# Retreived from: https://stackoverflow.com/questions/753052/strip-html-from-strings-in-python

from io import StringIO
from html.parser import HTMLParser

class StripHTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()

    def handle_data(self, data: str):
        self.text.write(data)

    def get_data(self) -> str:
        return self.text.getvalue()

def strip_tags(html) -> str:
    s = StripHTML()
    s.feed(html)
    return s.get_data()
