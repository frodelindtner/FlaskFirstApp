import sqlite3
from models.Order import Order

class Db_Orders:
    def __init__(self):
        self.connection = sqlite3.connect("storage/database/ShopDB.db", check_same_thread=False)

    def get_orders(self) -> list[Order]:
        cur = self.connection.cursor()
        cur.execute("SELECT * FROM Orders")
        orders = []
        for row in cur:
            order_obj = Order(*row)
            orders.append(order_obj)
        cur.close()
        return orders
    
    def create_order(self, new_order:Order):
        cur = self.connection.cursor()
        cur.execute("INSERT INTO Orders(CId, PId, PaymentStatus, Quantity) VALUES(?,?,?,?)", (new_order.customer_id, new_order.product_id, new_order.payment_status, new_order.quantity))
        self.connection.commit()