import sqlite3
from models.Product import Product

class Db_Products:
    def __init__(self):
        self.connection = sqlite3.connect("storage/database/ShopDB.db", check_same_thread=False)

    def get_products(self) -> list[Product]:
        cur = self.connection.cursor()
        cur.execute("SELECT * FROM Products")
        products = []
        for row in cur:
            pro_obj = Product(*row)
            products.append(pro_obj)
        cur.close()
        return products