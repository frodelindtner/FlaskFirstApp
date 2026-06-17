import unittest
from customer import Customer

class Testing(unittest.TestCase):
    def test_customer_properties(self):
        # Arrange
        customer_name = 'Test Customer'
        customer_mail = 'test@test.dk'
        customer_phone = 12345678
        # Act
        c = Customer(1, customer_name, customer_mail, customer_phone)
        result_name = c.name
        result_mail = c.mail
        result_phone = c.phone
        # Assert
        self.assertEqual(result_name, customer_name)
        self.assertEqual(result_mail, customer_mail)
        self.assertEqual(result_phone, customer_phone)

    def test_customer_id_property(self):
        # Arrange
        customer_id = 10001
        # Act
        c = Customer(customer_id, 'test', 'c@c.dk', 1)
        result = c.id
        # Assert
        self.assertEqual(result, customer_id)

unittest.main()