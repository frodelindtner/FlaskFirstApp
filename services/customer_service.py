from storage.db_customers import Db_Customers
from models.customer import Customer

class CustomerService:
    def __init__(self):
        self.__db_customers = Db_Customers()

    def get_all_customers(self):
        customers = self.__db_customers.get_all_customers()
        return customers
    
    def create_customer(self, name, mail, phone):
        new_customer = Customer(None, name, mail, phone)
        self.__db_customers.create_customer(new_customer)

    def get_customer_by_id(self, id):
        customer = self.__db_customers.get_customer_by_id(id)
        return customer