import sqlite3
from datetime import datetime


FILE = "messages.db" # file where database is stored
NAME = "Messages" # name of the table 


# the interface used to communicate to the database
class Database:

    def __init__(self):
        # creates connection to the database 
        self.conn = None
        self.conn = sqlite3.connect(FILE)
        self.cursor = self.conn.cursor()
        self._create_table()

    def close_connection(self):
        self.conn.close()

    def __create_table(self):
        # creates the table if the table doesn't already exists 
        # only used inside the class
        query = f'''CREATE TABLE IF NOT EXISTS {NAME} (id INTEGER PRIMARY KEY AUTOINCREMENT, name text, content text, time Date)'''
        self.cursor.execute(query)
        self.conn.commit()

    def get_messages_by_name(self, limit = 75, name=None):
        # executes a quey that returns all the messages from a specific user 
        # also used to return the last message send when limit = 1 
        query = f"SELECT * FROM {NAME} WHERE NAME = ? ORDER BY time DESC LIMIT {limit}"
        self.cursor.execute(query,(name,))
        messages = self.cursor.fetchall()

        results = [] 
        for msg in messages: # formats the data received from the database as json
            id, name, content, date = msg
            data = {"name": name, "message": content, "time":str(date)}
            if limit > 1:
                results.append(data)
            else:
                return data # return one json object if limit = 1

        return results # return a list of json 

    def get_all_messages(self, limit = 75):
        # returns all previous messages from database 
        query = f"SELECT * FROM {NAME}  ORDER BY time LIMIT {limit}"
        self.cursor.execute(query)
        messages = self.cursor.fetchall()
        results = []

        for msg in messages[:limit]:  # formats the data received from the database as json
            id, name, content, date = msg
            data = {"name": name, "message": content, "time":str(date)}
            results.append(data)
        return list(results)

    def insert_message(self, name, msg):
        # inserts message from a user in the database
        query = f"INSERT INTO {NAME} VALUES(?, ?, ?, ?)"
        self.cursor.execute(query, (None, name, msg, datetime.now()))
        self.conn.commit()

    def __delete_messages(self):
        #  deletes the table 
        # only used inside the class
        query = f"DROP TABLE IF EXISTS {NAME}"
        self.cursor.execute(query)
        self.conn.commit()