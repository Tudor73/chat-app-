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

    def get_all_messages(self, limit = 100, name =None):
        if not name:
            query = f"SELECT * FROM {NAME} ORDER BY time"
            self.cursor.execute(query)
        else:
            query = f"SELECT * FROM {NAME} WHERE NAME = ? ORDER BY time"
            self.cursor.execute(query, (name,))
        
        messages = self.cursor.fetchall()
        results = []

        for msg in messages[:limit]:
            id, name, content, date = msg
            data = {"name": name, "message": content, "time":str(date)}
            results.append(data)
        return list(results)

    def insert_message(self, name, msg):
        query = f"INSERT INTO {NAME} VALUES(?, ?, ?, ?)"
        self.cursor.execute(query, (None, name, msg, datetime.now()))
        self.conn.commit()