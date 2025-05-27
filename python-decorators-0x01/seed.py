import sqlite3
import csv
import uuid
import os

DB_FILE = "users.db"

def connect_db():
    try:
        return sqlite3.connect(DB_FILE)
    except sqlite3.Error as err:
        print(f"Error: {err}")
        return None

def create_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            age REAL NOT NULL
        )
    """)
    connection.commit()
    print("Table users created successfully")
    cursor.close()

def insert_data(connection, filename):
    cursor = connection.cursor()
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            user_id = str(uuid.uuid4())
            name = row['name']
            email = row['email']
            age = float(row['age'])

            cursor.execute("""
                SELECT COUNT(*) FROM users WHERE name = ? AND email = ? AND age = ?
            """, (name, email, age))
            if cursor.fetchone()[0] == 0:
                cursor.execute("""
                    INSERT INTO users (user_id, name, email, age)
                    VALUES (?, ?, ?, ?)
                """, (user_id, name, email, age))
    connection.commit()
    cursor.close()

connection = connect_db()
create_table(connection)
insert_data(connection, "input/user_data.csv")