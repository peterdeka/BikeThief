
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

class PrestaAdder:

    def __init__(self):
        self.prestashop = PrestaShopWebServiceDict('http://prestaimport.wannaup.com/api', 'DXLK6ILU2P17PWT1GXYAWXIE79UWS8Z6')  # messages will be as dict
        self.categories={}
        self.catschema=self.prestashop.get('categories', options={'schema': 'blank'})
        self.prodschema=self.prestashop.get('products', options={'schema': 'blank'})
        print "PrestaAdder is ACTIVE"


    #prendo tutte le categorie presenti sul server di destinazione
    def fetch_categories(self):
        cats=self.prestashop.get('categories?display=[name,id]')
        for c in cats['categories']['category']:
            self.categories[c['name']['language']['value']]=c['id']


    #inserisce le categorie se no esistono e ritorna l'id della categoria inserita (l'ultima sottocategoria)
    def add_categorytree(self,cats):
        #inserisco le categorie se non ci sono
        fathercat=2 #home
        for c in cats:
            if not self.catgories[c]:
                catego=category['category']
                catego['id_parent']=fathercat
                catego['active']='1'
                catego['name']['language']['value']=c
                catego['link_rewrite']['language']['value']=c.replace(' ','-')
                #catego['description']['language']['value']="mah un abella nuova categoria"
                category['category']=catego
                try:
                    r=prestashop.add('categories',category)
                except:
                    print "***Error while adding category {0}".format(c)
                    return None

                self.categories[c]=r['prestashop']['category']['id']
                fathercat=self.categories[c] #sara padre del prossimo

        return self.categories[c]


    def add_product(self,prod):
        return True
        catid=add_categorytree(prod['categories'])
        if not catid:
            print "***Error adding product {0}".format(product['name'])
            return False

        #TODO fill in prod info in schema using catid
        prodo=None