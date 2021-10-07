# Retreived from: https://stackoverflow.com/questions/753052/strip-html-from-strings-in-python

from io import StringIO
from html.parser import HTMLParser
from newspaper import Article as NewspaperArticle

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

def fetch_article_url(article_url: str) -> int:
    news_article = NewspaperArticle(article_url, keep_article_html=True)
    news_article.download()
    news_article.parse()
    striped_article = strip_tags(news_article.article_html)
    return len(striped_article.strip().split(" "))
