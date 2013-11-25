
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
import pprint
from copy import deepcopy

class PrestaAdder:

    def __init__(self):
        self.prestashop = PrestaShopWebServiceDict('http://prestaimport.wannaup.com/api', 'DXLK6ILU2P17PWT1GXYAWXIE79UWS8Z6')  # messages will be as dict
        self.categories={}
        self.manufacturers={}
        self.catschema=self.prestashop.get('categories', options={'schema': 'blank'})
        self.prodschema=self.prestashop.get('products', options={'schema': 'blank'})
        self.manuschema=self.prestashop.get('manufacturers', options={'schema': 'blank'})
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
            self.manufacturers[c['name']]=c['id']


    #inserisce le categorie se no esistono e ritorna l'id della categoria inserita (l'ultima sottocategoria)
    def add_categorytree(self,cats):
        #inserisco le categorie se non ci sono
        fathercat=2 #home
        for c in cats:
            if not self.catgories[c]:
                catego=self.catschema['category']
                catego['id_parent']=fathercat
                catego['active']='1'
                catego['name']['language']['value']=c
                catego['link_rewrite']['language']['value']=c.replace(' ','-')
                #catego['description']['language']['value']="mah un abella nuova categoria"
                category['category']=catego
                try:
                    r=prestashop.add('categories',self.catschema)
                except:
                    print "***Error while adding category {0}".format(c)
                    return None

                self.categories[c]=r['prestashop']['category']['id']
                fathercat=self.categories[c] #sara padre del prossimo

        return self.categories[c]


#inserisce e ritrna manufacturer
    def add_manufacturer(self,name):
        if not self.manufacturers[name]:
            m=self.manuschema['manufacturer']
            m['name']=name
            m['link_rewrite']=name.replace(' ','-')
            try:
                r=prestashop.add('manufacturers',self.manuschema)
            except:
                print "***Error while adding manufacturer {0}".format(name)
                return None
            self.manufacturers['name']=self.categories[c]=r['prestashop']['manufacturer']['id']
        
        return self.manufacturers[name]




    def reset_prodschema():
        p=self.prodschema
        p['wholesale_price']=None
        p['price']=None
        p['name']['language']['value']=None


#aggiunge un prodotto
    def add_product(self,prod):
        return True
        catid=add_categorytree(prod['categories'])
        manuid=add_manufacturer(prod['manufacturer'])

        if not catid or not manuid:
            print "***Error adding product related {0}".format(product['name'])
            return False

        p=self.prodschema['product']
        p['price']=prod['prices'][0]
        if len(prod['prices']>1):
            p['wholesale_price']=prod['prices'][1]
        p['link_rewrite']['language']['value']=prod['name'].replace(' ','-')
        p['name']['language']['value']=prod['name']
        p['id_category_default']=catid
        p['id_manufacturer']=manuid