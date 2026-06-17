import sqlite3
from models.customer import Customer

class Db_Customers:
    def __init__(self):
        self.__connection = sqlite3.connect("storage/VoresDB.db", check_same_thread=False)

    def get_all_customers(self) -> list[Customer]:
        cur = self.__connection.cursor()
        cur.execute("SELECT * FROM Customers")
        customers = []
        for row in cur:
            cus_obj = Customer(*row)
            customers.append(cus_obj)
        cur.close()            
        return customers
    
    def create_customer(self, customer:Customer):
        cur = self.__connection.cursor()
        cur.execute("INSERT INTO Customers(Name, Email, Phone) VALUES(?, ?, ?)",(customer.name, customer.mail, customer.phone))
        self.__connection.commit()
        cur.close()

    def get_customer_by_id(self, id):
        cur = self.__connection.cursor()
        cur.execute("SELECT * FROM Customers WHERE Id = (?)",(id,))
        for row in cur:
            customer = Customer(*row)
        cur.close()
        return customer