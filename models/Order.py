class Order:
    def __init__(self, id, customer_id, product_id, order_date, payment_status, quantity):
        self.__id = id
        
        # The easiest solution is to just include the cid/pid for the order
        # There is an argument to be made for excluding the cid/pid
        # That would make the navigation properties below necessary instead of optional
        # It would also mean rewriting the db call to always include the Customer/Product
        self.__customer_id = customer_id
        self.__product_id = product_id
        self.order_date = order_date
        self.payment_status = payment_status
        self.quantity = quantity
        
        # Navigation properties
        self.customer = None
        self.product = None

    @property
    def id(self):
        return self.__id
    
    @property
    def customer_id(self):
        return self.__customer_id
    
    @property
    def product_id(self):
        return self.__product_id