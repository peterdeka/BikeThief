import requests
from bs4 import BeautifulSoup



#fetch page
def fetch_page(url):
    r = requests.get(url)
    if r.status_code != requests.codes.ok:
        print "Error fetching {0}".format(url)
        return None
    return r.text


#da pagina con prodotti di una categoria lancia fetching dei singoli prodotti
def fetch_products(url,category_arr):
    print category_arr
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




