#   Author: Salil Agarwal (salil@dfordata.com)
#   Date:   18/08/2014

try:
    from bs4 import BeautifulSoup
    import requests
    import xml.etree.ElementTree as ET
except ImportError:
    print 'You didn\'t have the required packages to run this script'


try:
    data = requests.get('http://www.soloboxeo.com/feed/')
    soup = ET.fromstring(data.text.encode('utf8'))
    items = soup.findall('.//item')
    links = []
    title = []
    for i in items:
        links.append(i.find('link').text)
        title.append(i.find('title').text)

    image = []
    text = []

    for url in links:
        article = requests.get(url)
        soup1 = BeautifulSoup(article.text)
        content = soup1.find('div',{'id':'postcontent'})
        if content.img != None:
            image.append(content.img['src'])
        else:
            image.append([])
        para = content.find_all('p')
        string = ''
        for i in para:
            string = string + i.text
        text.append(string)

    print image
    print title
    
    
except requests.ConnectionError:
    print 'No Internet. Please check your internet connection'
except NameError:
    pass
