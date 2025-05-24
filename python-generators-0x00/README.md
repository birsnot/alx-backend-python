## Task: Streaming Rows from an SQL Database Using a Generator

### Objective

Create a Python script that:

1. Connects to a MySQL server.
2. Creates a database called `ALX_prodev` if it doesn't exist.
3. Creates a table `user_data` with the following schema:

   * `user_id`: UUID (Primary Key, Indexed)
   * `name`: VARCHAR, NOT NULL
   * `email`: VARCHAR, NOT NULL
   * `age`: DECIMAL, NOT NULL
4. Seeds the table using data from `user_data.csv` (which contains only name, email, and age).
5. Generates and inserts UUIDs for each row in Python to ensure uniqueness.
6. Prints a few records to verify the insertion.

---

### Usage

Run the script using:

```bash
./0-main.py
```

You should see output similar to:

```
connection successful
Table user_data created successfully
Database ALX_prodev is present 
[('UUID1', 'Name1', 'Email1', Age1), ...]
```

---

### Functions

* `connect_db()`: Connects to MySQL server (not a specific DB).
* `create_database(connection)`: Creates `ALX_prodev` if it doesn't exist.
* `connect_to_prodev()`: Connects specifically to the `ALX_prodev` database.
* `create_table(connection)`: Creates the `user_data` table if it doesn’t already exist.
* `insert_data(connection, csv_file)`: Inserts data from `user_data.csv`, assigning a unique UUID for each user.

---

### Notes

* Since the CSV file does not contain `user_id`, UUIDs are generated in Python using `uuid.uuid4()`.
* All changes are committed using `connection.commit()` to persist them.
* Proper indexing is applied on `user_id` for efficiency.