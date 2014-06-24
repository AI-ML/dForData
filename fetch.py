#   Date: 24/06/2014
#   Name: Salil Agarwal


import requests
from pattern import web

def dom( url, params ):
    #Fetch the page from url and return Document Object Model(DOM).
    return web.Element( requests.get(url, params=params).text )
