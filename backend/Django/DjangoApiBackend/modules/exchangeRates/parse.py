from .download import DownloadFile
import os
import json
import copy
from bs4 import BeautifulSoup


htmlPath = DownloadFile()

class MyParser():
    def __init__(self) -> None:
        self.dataDict = {}

    def Parse(self):
        with open(htmlPath, encoding='utf-8') as fp:
            soup = BeautifulSoup(fp, 'html.parser')
            tables = soup.find_all(
                'table'
            )

            for t in tables:
                rows = t.findChildren('tr', recursive=False)        
                for r in rows:
                    tds = r.findChildren('td', recursive=False)
                    if(len(tds) >= 5):
                        self.dataDict[tds[1].text] = float(tds[3].text)
                        