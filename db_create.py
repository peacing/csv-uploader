import sqlite3
from _config import DATABASE_PATH

with sqlite3.connect('csv.db') as connection:

    c = connection.cursor()

    c.execute("""CREATE TABLE data(customer_id INTEGER,
                first_name TEXT, last_name TEXT, address TEXT, state TEXT, zip_code INTEGER,
                status_change TEXT, product_id INTEGER, product_name TEXT, purchase_amount REAL,
              date TEXT)""")


