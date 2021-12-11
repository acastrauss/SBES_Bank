from html import parser
from html.parser import HTMLParser
import os
import json

htmlPath = os.path.join(
    os.getcwd(),
    "modules",
    "paymentCodes",
    "Šifre plaćanja - Servisinfo.html"
)
"""
    This path should be used when it's executed from MAIN file in Django
"""


class MyHtmlParser(HTMLParser):
    def __init__(self, *, convert_charrefs: bool = ...) -> None:
        super().__init__(convert_charrefs=convert_charrefs)
        self.dataEncounter = False
        self.dataCnt = 0
        self.data0 = 0
        self.data1 = 0
        self.data2 = ''

        self.dataDict = {}

    def handle_starttag(self, tag: str, attrs) -> None:
        if (tag == 'td'):
            self.dataEncounter = True

    def handle_endtag(self, tag: str) -> None:
        if (tag == 'td'):
            self.dataEncounter = False

    def handle_data(self, data: str) -> None:
        if(self.dataEncounter):
            if (self.dataCnt == 0):
                self.data0 = data
            elif (self.dataCnt == 1):
                self.data1 = data
            elif (self.dataCnt == 2):
                self.data2 = data

                code = self.data0 + self.data1
                self.dataDict[int(code)] = self.data2

            self.dataCnt += 1
            self.dataCnt %= 3


def Parse()->dict:
    """
        Returns dict representation of payment codes
    """
    f = open(htmlPath, 'r', encoding='utf-8')
    htmlText = f.read()
    f.close()

    parser = MyHtmlParser()
    parser.feed(htmlText)

    # jsonCodes = json.dumps(
    #     parser.dataDict, ensure_ascii=False
    # )

    # fjson = open(
    #     os.path.join(os.getcwd(), 'jsonCodes.json'), 'w',
    #     encoding='utf-8'
    # )

    # fjson.write(jsonCodes)

    # fjson.close()

    return parser.dataDict