import sqlite3
import uuid

from serializer.product_serializer import ProductSerializer


class DatabaseHandler:
    def __init__(self):
        self.database_connection = sqlite3.Connection("database.db")

    def create_user_database(self):
        database_cursor = self.database_connection.cursor()
        database_cursor.execute(
            "CREATE TABLE user (user_id INTEGER PRIMARY KEY, username VARCHAR(255) NOT NULL,password TEXT,active BOOLEAN);"
        )

    def create_product_database(self):
        database_cursor = self.database_connection.cursor()
        database_cursor.execute(
            "CREATE TABLE product (product_id INTEGER PRIMARY KEY, name VARCHAR(255) NOT NULL,description TEXT,price DECIMAL(10, 2) NOT NULL,stock_quantity INT NOT NULL,category VARCHAR(100),brand VARCHAR(100),created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);"
        )

    def create_product_entry(self, database_entry_kwargs):
        database_cursor = self.database_connection.cursor()
        id = uuid.uuid4()
        query = "INSERT INTO product VALUES(?, ?, ?, ?, ?, ?, ?)"
        values = (id, database_entry_kwargs['product_name'], database_entry_kwargs['product_description'],
                  database_entry_kwargs['product_price'], database_entry_kwargs['inventory_quantity'],
                  database_entry_kwargs['category'], database_entry_kwargs['brand'])
        database_cursor.execute(query, values)
        self.database_connection.commit()

    def create_user_entry(self, database_entry_kwargs):
        database_cursor = self.database_connection.cursor()
        id = uuid.uuid4()
        query = "INSERT INTO user (username, password, active) VALUES (?, ?, ?)"
        values = (id, database_entry_kwargs['username'], database_entry_kwargs['password'], database_entry_kwargs['active'])
        database_cursor.execute(query, values)
        self.database_connection.commit()

    def list_products(self, page_number, entry_limit):
        database_cursor = self.database_connection.cursor()
        query = "SELECT * from product LIMIT ? OFFSET ?"
        values = (entry_limit, page_number)
        product_list = database_cursor.execute(query, values)
        query_response = product_list.fetchall()
        product_serializer = ProductSerializer(query_response)
        return product_serializer.list_api_serializer()

    def update_product(self, product_id, update_parameters):
        database_cursor = self.database_connection.cursor()
        update_string = ""
        for key in list(update_parameters.keys()):
            update_string = update_string + f"{key}={update_parameters[key]}, "
        database_cursor.execute(f"UPDATE product SET {update_string} WHERE id = {product_id}")
        self.database_connection.commit()

    def delete_product(self, product_id):
        database_cursor = self.database_connection.cursor()
        query = "SELECT * FROM product WHERE id= ?"
        values = (product_id,)
        product = database_cursor.execute(query, values)
        query_response = product.fetchone()
        if query_response is None:
            raise Exception("No Product Found For this Product ID.")
        database_cursor.execute(f"DELETE FROM product WHERE id = {product_id}")
        self.database_connection.commit()

    def get_product(self, product_id):
        database_cursor = self.database_connection.cursor()
        query = "SELECT * FROM product WHERE id= ?"
        values = (product_id,)
        product = database_cursor.execute(query, values)
        query_response = product.fetchall()
        if query_response is None:
            raise Exception("No Product Found For this Product ID.")
        product_serializer = ProductSerializer(query_response)
        return product_serializer.list_api_serializer()

    def get_customer(self, username):
        database_cursor = self.database_connection.cursor()
        query = "SELECT * FROM user WHERE username = ?"
        values = (username,)
        product = database_cursor.execute(query, values)
        query_response = product.fetchone()
        return query_response
