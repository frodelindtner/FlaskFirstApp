import sqlite3

db = 'storage/VoresDB.db'
connection = sqlite3.connect(db)

def get_all_customers(conn:sqlite3.Connection):
    cur = conn.cursor()
    cur.execute("SELECT * FROM Customers")
    res_list = []
    for row in cur:
        res_list.append(row)
    return res_list

def create_customer(conn, name, email, phone):
    cur = conn.cursor()
    cur.execute("INSERT INTO Customers(Name, Email, Phone) VALUES(?, ?, ?)", (name, email, phone))
    conn.commit()

def update_customer_phone(conn, cid, new_phone):
    cur = conn.cursor()
    cur.execute("UPDATE Customers SET Phone = (?) WHERE Id = (?)", (new_phone, cid))
    conn.commit()

def delete_customer(conn, cid):
    cur = conn.cursor()
    cur.execute("DELETE FROM Customers WHERE Id = (?)", (cid,))
    conn.commit()

# create_customer(connection, 'Karrin', 'mm@cpd.dk', 12457865)
# update_customer_phone(connection, 8, 12125454)
# delete_customer(connection, 9)

customers = get_all_customers(connection)
print(customers)