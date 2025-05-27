import sqlite3


class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        return self.conn
        
    def __exit__(self, type, value, traceback):
        if self.conn:
            self.conn.close()

with DatabaseConnection("../python-decorators-0x01/users.db") as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    result = cursor.fetchall()
    print(result)
