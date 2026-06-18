from storage.db_customers import Db_Customers
from models.customer import Customer

class CustomerService:
    def __init__(self):
        self.__db_customers = Db_Customers()

    def get_customers(self):
        customers = self.__db_customers.get_all_customers()
        return customers        

    def get_all_customers(self):
        customers = self.__db_customers.get_all_customers()
        return customers
    
    def create_customers(self, name, mail, phone):
        new_customer = Customer(None, name, mail, phone)
        self.__db_customers.create_customer(new_customer)

    def get_customer_by_id(self, id):
        customer = self.__db_customers.get_customer_by_id(id)
        return customer
    
#-----------------------------------------------------------------------------------------
    def update_customer(self, updated_customer):
        self.__db_customer.update_customer(updated_customer)
        return self.get_customer_by_id(updated_customer.id)

    def delete_customer(self, id):
        self.__db_customer.delete_customer(id)
#----------------------------------------------------------------------------------------- 

    def get_all_customers_json(self):
        customers = self.get_all_customers()
        json_res = []
        for c in customers:
            json_res.append(c.to_json())
        return json_res    