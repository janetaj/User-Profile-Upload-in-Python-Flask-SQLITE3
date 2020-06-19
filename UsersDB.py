import sqlite3
connection = sqlite3.connect("users.db")
print("Database opened successfully")
cursor = connection.cursor()
connection.execute("create table users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT  NULL, email TEXT UNIQUE, gender TEXT, contact TEXT, dob TEXT, profile_pic BLOB)")
print("Table created successfully")
connection.close()   
