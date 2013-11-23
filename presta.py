
from prestapyt import PrestaShopWebServiceError, PrestaShopWebService, PrestaShopWebServiceDict
import pprint
#prestashop = PrestaShopWebService('http://localhost:8080/api', 'DXLK6ILU2P17PWT1GXYAWXIE79UWS8Z6')  # messages will be as xml
# or
prestashop = PrestaShopWebServiceDict('http://prestaimport.wannaup.com/api', 'DXLK6ILU2P17PWT1GXYAWXIE79UWS8Z6')  # messages will be as dict

# search / get all addresses
#prestashop.get('addresses') # will return the same xml message than
#prestashop.search('addresses')
# but when using PrestaShopWebServiceDict

category=prestashop.get('categories', options={'schema': 'blank'})
catego=category['category']
catego['id_parent']='2'
catego['active']='1'
catego['name']['language']['value']="Cateprova"
catego['link_rewrite']['language']['value']="cateprova"
catego['description']['language']['value']="mah un abella nuova categoria"
category['category']=catego
print category
r=prestashop.add('categories',category)
print r
