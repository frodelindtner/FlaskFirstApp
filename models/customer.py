class Customer:
    def __init__(self, id, name, mail, phone):
        self.__id = id
        self.__name = name
        self.__mail = mail
        self.__phone = phone

    @property
    def id(self):
        return self.__id
    
    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, new_name):
        self.__name = new_name

    @property
    def mail(self):
        return self.__mail
    
    @mail.setter
    def mail(self, new_mail):
        self.__mail = new_mail
    
    @property
    def phone(self):
        return self.__phone
    
    @phone.setter
    def phone(self, new_phone):
        self.__phone = new_phone