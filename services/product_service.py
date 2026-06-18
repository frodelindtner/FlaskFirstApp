from storage.db_products import Db_Products
from models.Product import Product

class ProductService:
    def __init__(self):
        self.__db_products = Db_Products()
    
    def get_products(self):
        products = self.__db_products.get_products()
        return products
    
    def get_product_by_id(self, id):
        products = self.get_products()
        for product in products:
            if product.id == id:
                return product
        else:
            return None