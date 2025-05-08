import sqlite3
connection = sqlite3.connect('./db/database.db')

with open('./db/schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()
cur.execute("INSERT INTO names (seed, mom) VALUES (?, ?)",('lorelai gilmore', 'Pennilyn Lott'))
cur.execute("INSERT INTO names (seed, mom) VALUES (?, ?)",('lorelei gilmore', 'Pennilyn Lott'))
cur.execute("INSERT INTO names (seed, mom) VALUES (?, ?)",('rory gilmore', 'Sherry Tinsdale'))
cur.execute("INSERT INTO names (seed, mom) VALUES (?, ?)",('april nardini', 'Lorelai Gilmore'))

connection.commit()
connection.close()