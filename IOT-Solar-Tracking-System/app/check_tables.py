import sqlite3

conn = sqlite3.connect("solar.db")
cursor = conn.cursor()

tables = cursor.execute(
    "SELECT name FROM sqlite_master WHERE type='table'"
).fetchall()

print("Tables in database:", tables)

conn.close()
