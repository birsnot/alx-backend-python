import sqlite3


class ExecuteQuery:
    def __init__(self, query, params = ()):
        self.query = query
        self.params = params
        self.db_name = "../python-decorators-0x01/users.db"
        self.conn = None
        self.cursor = None
    
    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        result = self.cursor.fetchall()
        return result
    
    def __exit__(self, type, value, traceback):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()


with ExecuteQuery("SELECT * FROM users WHERE age > ?", (25,)) as results:
    print(results)