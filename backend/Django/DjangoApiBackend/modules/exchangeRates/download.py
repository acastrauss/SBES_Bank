from urllib import request
import os

urlPath = "http://www.servisinfo.com/biz/menjacnica-online"
"""
    URL that should be used for exchange rates
"""

def DownloadFile()->str:
    htmlPath = os.path.join(
            os.getcwd(),        
            "modules",
            "exchangeRates",
            "exchanges.html"
    )

    request.urlretrieve(
        urlPath, htmlPath
    )

    return htmlPath
