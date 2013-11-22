import requests
from bs4 import BeautifulSoup



#fetch page
def fetch_page(url):
    r = requests.get(url)
    if r.status_code != requests.codes.ok:
        print "Error fetching {0}".format(url)
        return None
    return r.text


def fetch_single_product(url,category_arr):
    return


#da pagina con prodotti di una categoria lancia fetching dei singoli prodotti
def fetch_products(url,category_arr):
    print category_arr
    productspage=fetch_page(url)
    if not productspage:
        return
    pprods=BeautifulSoup(productspage)    
    prods=pprods.select("div.product-box")
    print "{0} products in this section".format(len(prods))
    for p in prods:
        fetch_single_product(p,category_arr)

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
        for subul in li.select("ul"):
            for sub in subul.select("li"):
                #print "SUB {0}".format(sub.select("a span")[0].getText())
                parse_category(sub,new_arr)


mainpage=fetch_page("http://www.gambacicli.com")
if not mainpage:
    exit()
mainsoup = BeautifulSoup(mainpage)
categories=mainsoup.select("ul#nav > li")
if len(categories)<1:
    print "Error can't find nav menu"
    exit()
for li in categories:
    parse_category(li,[])




