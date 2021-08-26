import psycopg2
from psycopg2.extras import DictCursor

conn = psycopg2.connect("postgres://cavtxnprgvurdg:a83e1b7bed2ee4f99a212bae203868d76ab14753fcf50bcdf05472a5d8b44c75@ec2-34-228-100-83.compute-1.amazonaws.com:5432/db6mfbge6uj3t3", 
                            cursor_factory=DictCursor)
cur = conn.cursor()

def create_user_tables():
    cur.execute(''' CREATE TABLE users (
        id  SERIAL  PRIMARY KEY     NOT NULL,
        email   TEXT    NOT NULL,
        phas   TEXT    NOT NULL,
        name    TEXT   NOT NULL); ''')
    print("Table created successfully")

    conn.commit()

def create_market_table():
    cur.execute(''' 
        CREATE TABLE products (
            id  SERIAL  PRIMARY KEY     NOT NULL,
            shop   TEXT    NOT NULL,
            category   TEXT    NOT NULL,
            product   TEXT    NOT NULL,
            description   TEXT    NOT NULL,
            price     INT, 
            image   TEXT  NOT NULL);
        ''')
    print("Table created successfully")

    conn.commit()

def insert_user(email, phash, name):
    cur.execute(f"INSERT INTO users (email, phas, name) \
      VALUES ('{email}', '{phash}', '{name}')")
    conn.commit()
    print("User created successfully")

def insert_product(shop, category, product, description, price, image):
    cur.execute(f"INSERT INTO products (shop, category, product, description, price, image) \
      VALUES ('{shop}', '{category}', '{product}', '{description}', '{price}', '{image}')")
    conn.commit()
    print("Product created successfully")

def get_user():
    try:
        cur.execute("SELECT * FROM users")
        rows = cur.fetchall()

        return rows

    except:
        print('No database')
        return -1

def get_product():
    try:
        cur.execute("SELECT * FROM products")
        rows = cur.fetchall()

        return rows

    except:
        print('No database')
        return -1

def get_helpdesk():
    try:
        cur.execute("SELECT * FROM helpdesk")
        rows = cur.fetchall()

        return rows

    except:
        print('No database')
        return -1

def find_user_email(email):
    cur.execute(f"SELECT * from users where Email = '{email}'")
    row = cur.fetchall()
    return row

def get_user_product(user):
    cur.execute(f"SELECT * FROM products where shop = '{user}'")
    rows = cur.fetchall()
    return rows

def delete_table_product():
    cur.execute("DROP TABLE products;")
    conn.commit()

    print("Delete")
def delete_table_user():
    cur.execute("DROP TABLE users;")
    conn.commit()

    print("Delete")

def create_tables2():
    cur.execute(''' CREATE TABLE helpdesk (
        FirstName  TEXT  NOT NULL,
        LastName   TEXT    NOT NULL,
        Email  TEXT    NOT NULL); ''')
    print("Table created successfully")
    conn.commit()

def insert_tables2(FirstName, LastName, email):
    
        cur.execute(f"INSERT INTO helpdesk(FirstName, LastName, Email) \
        VALUES ('{FirstName}', '{LastName}','{email}')")
        print("Table inserted successfully")
        conn.commit()
  
def read_tables2():
    try:
        cur.execute("SELECT * FROM helpdesk")
        rows = cur.fetchall()

        return rows

    except:
        print('None')
        return -1

def filter_email(email):
    cur.execute(f"SELECT * from helpdesk where Email = '{email}'")
    row = cur.fetchall()
    return row


if __name__ == '__main__':
    # insert_product('ShopA', 'Food', 'Bread_A', 'Nice', 10)
    # row = get_product()
    # delete_table_product()
    # create_market_table()
    # delete_table_user()
    # create_user_tables()
    print(get_product()[-1])
    # print(find_user_email("a"))
    # create_user_tables()
    # create_market_table()
    # print(get_user_product('ShopA'))