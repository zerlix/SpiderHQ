import sqlite3
import config.config as cfg

class SQLiteDatabase:
    
    def __init__(self, db_name):
        self.db_name = cfg.database
        self.connection = None
        

    def connect(self):
        self.connection = sqlite3.connect(self.db_name)


    def disconnect(self):
        if self.connection:
            self.connection.close()


    def execute_query(self, query, params=None):
        cursor = self.connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        self.connection.commit()
        return cursor.fetchall()


    def create_table(self, table_name, columns):
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
        self.execute_query(query)


    def insert_data(self, table_name, data):
        placeholders = ', '.join(['?' for _ in range(len(data))])
        query = f"INSERT INTO {table_name} VALUES ({placeholders})"
        self.execute_query(query, data)

    def replace_data(self, table_name, data):
        placeholders = ', '.join(['?' for _ in range(len(data))])
        query = f"INSERT OR REPLACE INTO {table_name} VALUES ({placeholders})"
        self.execute_query(query, data)
    
    def select_data(self, table_name, condition=None):
        query = f"SELECT * FROM {table_name}"
        if condition:
            query += f" WHERE {condition}"
        return self.execute_query(query)


    def update_data(self, table_name, data, condition=None):
        set_values = ', '.join([f"{column} = ?" for column in data])
        query = f"UPDATE {table_name} SET {set_values}"
        if condition:
            query += f" WHERE {condition}"
        self.execute_query(query, list(data.values()))


    def delete_data(self, table_name, condition=None):
        query = f"DELETE FROM {table_name}"
        if condition:
            query += f" WHERE {condition}"
        self.execute_query(query)

    def commit(self):
        self.connection.commit()
