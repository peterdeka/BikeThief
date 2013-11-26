
  #REFERENCE TEST
    # category=prestashop.get('categories', options={'schema': 'blank'})
    # catego=category['category']
    # catego['id_parent']='2'
    # catego['active']='1'
    # catego['name']['language']['value']="Cateprova"
    # catego['link_rewrite']['language']['value']="cateprova"
    # catego['description']['language']['value']="mah un abella nuova categoria"
    # category['category']=catego
    # #print category
    # r=prestashop.add('categories',category)
    # print r['prestashop']['category']['id']
    #END TEST
from prestapyt import PrestaShopWebServiceError, PrestaShopWebService, PrestaShopWebServiceDict
import requests
from requests.auth import HTTPBasicAuth
import pprint
import io

class PrestaAdder:
    
    def __init__(self):
        self.prestashop = PrestaShopWebServiceDict('http://prestaimport.wannaup.com/api', 'DXLK6ILU2P17PWT1GXYAWXIE79UWS8Z6')  # messages will be as dict
        self.categories={}
        self.manufacturers={}
        self.catschema=self.prestashop.get('categories', options={'schema': 'blank'})
        self.prodschema=self.prestashop.get('products', options={'schema': 'blank'})
        self.manuschema=self.prestashop.get('manufacturers', options={'schema': 'blank'})
        self.skipcats={}
        self.fetch_categories()
        self.fetch_manufacturers()
        self.pp = pprint.PrettyPrinter(indent=4)
        print "PrestaAdder is ACTIVE, schemas loaded"


    #prendo tutte le categorie presenti sul server di destinazione
    def fetch_categories(self):
        cats=self.prestashop.get('categories?display=[name,id]')
        for c in cats['categories']['category']:
            self.categories[c['name']['language']['value']]=c['id']
       

    #prendo tutte le categorie presenti sul server di destinazione
    def fetch_manufacturers(self):
        manu=self.prestashop.get('manufacturers?display=[name,id]')
        for m in manu['manufacturers']['manufacturer']:
            self.manufacturers[m['name']]=m['id']
        
    def safeescape(self,s):
        s=s.replace('"',' pollici')
        s=s.replace('/',' ')
        s=s.replace('   ',' ')
        return s

    #inserisce le categorie se no esistono e ritorna l'id della categoria inserita (l'ultima sottocategoria)
    def add_categorytree(self,cats):
        #inserisco le categorie se non ci sono
        wholestring=""
        fathercat=2 #home
        for c in cats:
            wholestring=wholestring+c
            if not wholestring in self.categories:
                catego=self.catschema['category']
                catego['id_parent']='{0}'.format(fathercat)
                catego['active']='1'
                c=self.safeescape(c)
                catego['name']['language']['value']=c
                catego['link_rewrite']['language']['value']=c.replace(' ','-')
                #catego['description']['language']['value']=c
                #catego['description']['language']['value']="mah un abella nuova categoria"
                self.catschema['category']=catego
                #print self.catschema
                try:
                    r=self.prestashop.add('categories',self.catschema)
                except:
                    print "***Error while adding category {0}".format(c)
                    return None

                self.categories[wholestring]=r['prestashop']['category']['id']
                fathercat=self.categories[wholestring] #sara padre del prossimo

        return self.categories[wholestring]


#inserisce e ritrna manufacturer
    def add_manufacturer(self,name):
        if not name:
            return None
        if not name in self.manufacturers:
            m=self.manuschema['manufacturer']
            m['name']=name
            m['active']='1'
            #m['link_rewrite']=name.replace(' ','-')
            try:
                r=self.prestashop.add('manufacturers',self.manuschema)
            except:
                print "***Error while adding manufacturer {0}".format(name)
                return None
            self.manufacturers[name]=r['prestashop']['manufacturer']['id']
        
        return self.manufacturers[name]




    def reset_prodschema(self):
        p=self.prodschema['product']
        p['wholesale_price']=None
        p['price']=None
        p['name']['language']['value']=None


#carica immagine prodotto
    def add_prod_img(self,prodid,imgurl,idx):
        f = open('tmp','wb')
        f.write(requests.get(imgurl).content)
        f.close()
        fd        = io.open("tmp", "rb")
        content   = fd.read()
        fd.close()
        #self.prestashop.add('images/products/{0}'.format(prodid), files=[('image',  content)])
        files = {'image': ('image.png', open('tmp', 'rb'))}
        r=requests.post('http://prestaimport.wannaup.com/api/images/products/{0}'.format(prodid),files=files, auth=HTTPBasicAuth('DXLK6ILU2P17PWT1GXYAWXIE79UWS8Z6', ''))
        if r.status_code==200:
            print "image added"
        else:
            print "ERROROROROROROOR adding image {0}".format(r.status_code)
            print r.text

#aggiunge un prodotto
    def add_product(self,prod):
        self.reset_prodschema()
        catid=self.add_categorytree(prod['categories'])
        manuid=self.add_manufacturer(prod['manufacturer'])

        if not catid or not manuid:
            print "***Error adding product related"# {0}".format(prod['name'])
            return False

        prod['name']=self.safeescape(prod['name'])
        prod['desc']=self.safeescape(prod['desc'])
        prod['short_desc']=self.safeescape(prod['short_desc'])
        
        p=self.prodschema['product']
        p['price']='{0}'.format(prod['prices'][0])
        if len(prod['prices'])>1:
            p['wholesale_price']='{0}'.format(prod['prices'][1])
        p['link_rewrite']['language']['value']=prod['name'].replace(' ','-')
        p['name']['language']['value']=prod['name']
        p['id_category_default']=catid
        p['associations']['categories']['category']['id']=catid
        if manuid:
            p['id_manufacturer']=manuid
        p['description']['language']['value']=prod['desc']
        p['description_short']['language']['value']=prod['short_desc']
        p['active']='1'
        p['available_for_order']='1'
        p['show_price']='1'
        n=len(prod['code'])
        if n>31:
            n=31
        p['reference']=prod['code'][:n]

        try:
            r=self.prestashop.add("products",self.prodschema)
        except:
            print "Error addding product"
            self.pp.pprint(self.prodschema)
            return False
        
        print "prod added id "+r['prestashop']['product']['id']
        #TODO images
        i=0
        for img in prod['imgurls']:
            self.add_prod_img(r['prestashop']['product']['id'],img,i)
            i+=1
        