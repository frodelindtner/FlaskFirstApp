from services.customer_service import CustomerService
from services.product_service import ProductService
from storage.db_orders import Db_Orders
from models.Order import Order

class OrderService:
    def __init__(self):
        self.__db_order = Db_Orders()
        self.__customer_service = CustomerService()
        self.__product_service = ProductService()
    
    def get_orders(self):
        orders = self.__db_order.get_orders()
        for order in orders:
            # Connect the Customer and Product objects to every order
            # This makes navigation in the app way easier
            order.customer = self.__customer_service.get_customer_by_id(order.customer_id)
            order.product = self.__product_service.get_product_by_id(order.product_id)
        return orders
    
    def get_order_by_id(self, id):
        orders = self.get_orders()
        for order in orders:
            if order.id == id:
                return order
        else:
            return None
        
    # Note that both id and OrderDate are set to None - both are handled by the DB
    # (I don't want to deal with dates...)
    def create_order(self, customer_id, product_id, payment_status, quantity):
        new_order = Order(None, customer_id, product_id, None, payment_status, quantity)
        self.__db_order.create_order(new_order)