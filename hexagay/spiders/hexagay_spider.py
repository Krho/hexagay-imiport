# coding: utf-8
import re
import codecs
import json
import pywikibot
import bs4
import scrapy
import sys
from pywikibot import page
from bs4 import BeautifulSoup

class HexagaySpider(scrapy.Spider):
    name = "hexagay"
    #codec = sys.getfilesystemencoding()
    #codec = 'iso-8859-15'

    def start_requests(self):
        urls = [
            'http://www.hexagonegay.com/Gaypride2002.html',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'prides-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
        result = {}
        html_doc = response.body
        soup = BeautifulSoup(html_doc, 'html.parser')
        for c in soup.table.tbody.contents[3].contents[3].table.tbody.contents:
            if "tbody" in str(c) and c.tbody.contents is not None and c.tbody.contents[1].font is not None and "<" not in c.tbody.contents[1].font.contents[0].encode('utf8'):
                partialResult = {u"ville":unicode(c.tbody.contents[1].font.contents[0])}
                for i in range(((len(c.tbody.contents)-1)/4)):
                    partialResult[unicode(c.tbody.contents[3+4*i].font.contents[0])]=unicode(c.tbody.contents[5+4*i].font.contents[0])
                result[c.tbody.contents[1].font.contents[0]]=partialResult
        with codecs.open('dump.json', encoding='utf-8', mode='w+') as file:
            data = json.dumps(result, indent=2, encoding="utf-8")
            file.write(data)
        self.log('Extracted %s' % filename)
