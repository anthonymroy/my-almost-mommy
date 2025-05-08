import sqlite3
connection = sqlite3.connect('./db/database.db')
connection.row_factory = sqlite3.Row
names = connection.execute('SELECT * FROM names').fetchall()
print('My Almost Mommy Database')
for name in names:
    print(f"{name['seed']} ({name['mom']})")
connection.close()