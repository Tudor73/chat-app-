import sqlite3
from datetime import datetime


FILE = "messages.db"
NAME = "Messages"

class Database:

    def __init__(self):
        self.conn = None
        self.conn = sqlite3.connect(FILE)
        self.cursor = self.conn.cursor()
        self._create_table()

    def close_connection(self):
        self.conn.close()

    def _create_table(self):
        query = f'''CREATE TABLE IF NOT EXISTS {NAME} (id INTEGER PRIMARY KEY AUTOINCREMENT, name text, content text, time Date)'''
        self.cursor.execute(query)
        self.conn.commit()

    def insert_message(self, name, msg):
        query = "INSERT INTO ? VALUES(?,?,?,?)"
        self.cursor.execute(query, (NAME, None, name, msg, datetime.now()))
        self.cursor.commit()