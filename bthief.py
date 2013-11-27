import requests
from bs4 import BeautifulSoup
import pprint
import re
from PrestaAdder import PrestaAdder

pp = pprint.PrettyPrinter(indent=4)
debug=False
pa=PrestaAdder()

fvariationserr= open('varerr','w')
fmanuerr= open('manuerr','w')
#fetch page
def fetch_page(url):
    r = requests.get(url)
    if r.status_code != requests.codes.ok:
        print "Error fetching {0}".format(url)
        return None
    r.encoding = 'utf-8'

    return r.text.replace(u'\xa0',u' ')


def fetch_single_product(url,category_arr):
    print "Fetching {0}".format(url)
    page=fetch_page(url)
    if not page:
        print ">ERROR fetching product page"
        return
    pprodsoup=BeautifulSoup(page)
    prodsoup=pprodsoup.select('div.product-view')[0]
    
    product={'categories':category_arr}
    product['url']=url
    product['name']=prodsoup.select("div.product-name h1")[0].getText()
    try:
        product['manufacturer']=prodsoup.select("div#manufacturer_logo a")[0].get("title")
    except:
        if product['name'].find('Rock Shox'):
            product['manufacturer']='Rock Shox'    
        else:
            product['manufacturer']=None
            print "***Warning no manufacturer"
            fmanuerr.write('***Warning no manufacturer {0}\n'.format(url))

    prices=prodsoup.select('div.product-shop span.price')
    product['prices']=[]
    for pr in prices:
        nums=re.findall(r'\d+',pr.getText())
        product['prices'].append(float(nums[0])+float(nums[1])/100.0) #TODO substring dopo punto e virgola
    product['short_desc']=prodsoup.select('div.short-description div.std')[0].getText()
    product['desc']=prodsoup.select('div#product_tabs_description_tabbed_contents div.std')[0].getText()
    #codice prodotto
    product['code']=None
    entries=prodsoup.select('div#product_tabs_additional_tabbed_contents tr')
    for t in entries:
        if t.select('th')[0].getText()=="Codice Prodotto":
            product['code']=t.select('td')[0].getText()
        elif t.select('th')[0].getText()!="Nome":
            product['desc']+='</p><p>'+t.select('th')[0].getText()+' '
            product['desc']+=t.select('td')[0].getText()+'</p>'
    
    if not product['code']:
        print "**Error fetching product code for product {0}".format(url)
    product['imgurls']=[]
    product['imgurls'].append(prodsoup.select('p.product-image > img#image')[0].get('src'))
    #altre immagini
    moreviews=prodsoup.select('div.more-views ul li a')
    if len(moreviews)>1:
        for i in range(1,len(moreviews)):
            product['imgurls'].append(moreviews[i].get('href'))
    #variazioni
    optionsnames=prodsoup.select('div.product-options dt')
    optionschoices=prodsoup.select('div.product-options dd')
    product['variations']=[]
    for i in range(0,len(optionsnames)):
        v=optionsnames[i]
        name=v.select('label')[0].getText()
        opts=[]
        first=True
        for o in optionschoices[i].select('option'):
            if first:
                first=False
                continue
            opts.append(o.getText())
        vn={'name':name,'opts':opts}
        product['variations'].append(vn)
    if len(product['variations'])>0:
        fvariationserr.write('**Warning ignoring variations for {0}\n'.format(url))

    #DBG
    
    pa.add_product(product)


    return


#da pagina con prodotti di una categoria lancia fetching dei singoli prodotti
def fetch_products(url,category_arr):
    #print category_arr
    productspage=fetch_page(url)
    if not productspage:
        return
    pprods=BeautifulSoup(productspage)    
    prods=pprods.select("div.product-box")
    print "{0} products in this section".format(len(prods))
    for p in prods:
        fetch_single_product(p.select("a")[0].get("href"),category_arr)

    #vedo se ci sono altre pagine
    pager=pprods.select("div.pages > ol")
    #if pager:
     #   for mp in pager.select("li"):
      #      if "current" in li.get("class"):
       #         continue
        #    url=li.select("a")[0].get("href")
    if pager:
        nextl=pager[0].select("li a.next")
        if nextl:
            print "Has more"
            url=nextl[0].get("href")
            print url
            fetch_products(url,category_arr)

    return

#parsa una categoria in maniera ricorsiva, vede a che livello e agisce di conseguenza
def parse_category(li,category_arr):
    name=li.select("a span")[0].getText()
    new_arr=category_arr[:]
    new_arr.append(name)
    
    #link a pagina prodotto? (caso base)
    if not "parent" in li.get("class"):
        url=li.select("a")[0].get("href")
        fetch_products(url,new_arr)
    else:
        for subul in li.select("> ul"):
            for sub in subul.select("> li"):
                #print "SUB {0}".format(sub.select("a span")[0].getText())
                parse_category(sub,new_arr)


mainpage=fetch_page("http://www.gambacicli.com")
if not mainpage:
    exit()
mainsoup = BeautifulSoup(mainpage)
categories=mainsoup.select("ul#nav > li.level0")
if len(categories)<1:
    print "Error can't find nav menu"
    exit()
for li in categories:
    parse_category(li,[])

fvariationserr.close()
fmanuerr.close()

