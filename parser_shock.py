import requests, bs4

#start of xml
def yml_begin(f):
    f.write('<yml_catalog>')
    f.write('<shop>')
    f.write('<currencies>')
    f.write('<currency id="UAH" rate="1"/>')
    f.write('</currencies>')
    f.write('<categories>')
    f.write('<category id="00000301">Новинки</category>')
    f.write('</categories>')
    f.write('<offers>')

#end of xml
def yml_end(f):
    f.write('</offers>')
    f.write('</shop>')
    f.write('</yml_catalog>')
    f.close()

#writing of the current offer
def new_offer(f):
    f.write('<offer id="'+code+'">')
    f.write('<categoryId>00000300</categoryId>')
    f.write('<currencyId>UAH</currencyId>')
    f.write('<name>'+name+'</name>')
    f.write('<price>'+str(price)+'</price>')
    f.write('<vendorCode>Ш-'+code+'</vendorCode>')
    f.write('<image>'+img+'</image>')
    f.write('<description>'+descr+'</description>')
    f.write('<available>true</available>')
    j=2
    while j<len(param):
        f.write('<param name="'+param[j]+'">'+param[j+1]+'</param>')
        j+=2
    f.write('</offer>')

#creating of xml
xmlfile=open('shock.xml', 'w', encoding="utf-8")
yml_begin(xmlfile)

fin=False
num=0
page=0

# base url for start of parsing
baseurl=input('Input URL: ')
while page<5 and not fin:
        url =baseurl + 'p-' + str(page) + '/'
        page += 1
        r=requests.get(url)
        r.encoding = 'UTF8'
        b=bs4.BeautifulSoup(r.text, 'html.parser')

        alinks=b.select('div.image a') #collect all links on the page
        apics=b.select('div.image img') #collect all pictures on the page

        links=[]
        pics=[]

        for a in alinks: #array of links
            links.append(a.get('href'))

        for p in apics: #array of pictures
            pics.append('https://yavshoke.ua'+p.get('src'))
        i = 0
        while i < len(links) and not fin: #for each link - go inside
            r = requests.get(links[i])
            b = bs4.BeautifulSoup(r.text, 'html.parser')
            avail = b.select('div.avail-text')
            avail = avail[0].getText()
            if avail == 'В наличии':   #if the offer is available
                num += 1
                name = b.select('div.def-product-data h1')
                name = name[0].getText()
                price = b.select('div.def-price-available span')
                price = float(price[0].getText())+60
                code = b.select('div.block-codes span')
                code = code[0].getText()
                img = pics[i]
                try: #maybe the offer hasn't description
                    descr = b.select('div.def-editor-content')
                    descr = descr[0].getText()
                except:
                    descr=' '
                try: #maybe the offer hasn't parameters
                    param = b.select('table.def-table')
                    param = param[0].getText()
                    paramtemp = param.split('\n')
                    param = []
                    for s in paramtemp:
                        if s != '':
                            param.append(s)
                except:
                    param = []
                    param.append('Свойство')
                    param.append('Характеристика')
                    param.append('Состояние')
                    param.append('Новое')
                new_offer(xmlfile)
            else:
                fin = True #end of parsing, no more available offers
            i += 1

yml_end(xmlfile)

print(num) #number of available offers in xml