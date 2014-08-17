#   Author: Salil Agarwal (salil@dfordata.com)
#   Date:   18/08/2014

try:
    from bs4 import BeautifulSoup
    import requests
except ImportError:
    print 'You didn\'t have the required packages to run this script'


try:
    data = requests.get('http://www.soloboxeo.com/feed/')
    soup = BeautifulSoup(data.text, 'xml')
    items = soup.find_all('item')
    links = []
    title = []
    for i in items:
        links.append(i.link.text)
        title.append(i.title.text)

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
