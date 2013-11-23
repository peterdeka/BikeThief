
from prestapyt import PrestaShopWebServiceError, PrestaShopWebService, PrestaShopWebServiceDict

#prestashop = PrestaShopWebService('http://localhost:8080/api', 'DXLK6ILU2P17PWT1GXYAWXIE79UWS8Z6')  # messages will be as xml
# or
prestashop = PrestaShopWebServiceDict('http://prestaimport.wannaup.com/api', 'DXLK6ILU2P17PWT1GXYAWXIE79UWS8Z6')  # messages will be as dict

# search / get all addresses
#prestashop.get('addresses') # will return the same xml message than
#prestashop.search('addresses')
# but when using PrestaShopWebServiceDict
print prestashop.search('products')
print prestashop.get('categories', options={'schema': 'blank'})

