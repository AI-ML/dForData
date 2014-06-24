#   Date: 21/06/2014
#   Name: Salil Agarwal

# scape ted.com with all of its talks.

import requests
from pattern import web


f = open( 'ted.txt', 'w' )
url = 'http://www.ted.com/talks/browse'

for number in range(1,51):
    params = {'page': number}
    print number
    webpage = requests.get(url, params=params)
    dom = web.Element( webpage.text )
    table = dom.by_tag( 'div.row row-sm-4up row-lg-6up row-skinny' )[0]
    for talk in table.by_tag('div.col'):
        speaker = talk.by_tag( 'h4.h12 talk-link__speaker' )[0].content.replace('\n', '').encode('ascii', 'ignore')
        talkname = talk.by_tag( 'h4.h9 m5' )[0].by_tag( 'a' )[0].content.replace('\n', '').encode('ascii', 'ignore')
        link = talk.by_tag( 'h4.h9 m5' )[0].by_tag( 'a' )[0].attributes.get('href').replace ('\n', '').encode('ascii', 'ignore')
        duration = talk.by_tag( 'span.thumb__duration' )[0].content.replace('\n','')
        metavalue = talk.by_tag( 'span.meta__val' )
        views = metavalue[0].content.replace('\n', '').encode('ascii', 'ignore')
        date = metavalue[1].content.replace('\n', '').encode('ascii', 'ignore')
        genres = metavalue[2].content.replace('\n', '').encode('ascii', 'ignore')
        f.write( '%s \t %s \t %s \t %s \t %s \t %s\n' % ( speaker, talkname, views, genres, date, duration ) )

f.close()

