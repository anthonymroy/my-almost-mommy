import sqlite3
from db.name_lists import FIRST_NAMES, OLD_FIRST_NAMES, NICKNAMES, LAST_NAMES
connection = sqlite3.connect('./db/database.db')

with open('./db/schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

for name in FIRST_NAMES:
    cur.execute("INSERT INTO names (name, category) VALUES (?, ?)",(f'{name}', 'first_name'))

for name in OLD_FIRST_NAMES:
    cur.execute("INSERT INTO names (name, category) VALUES (?, ?)",(f'{name}', 'old_first_name'))

for name in NICKNAMES:
    cur.execute("INSERT INTO names (name, category) VALUES (?, ?)",(f'{name}', 'nickname'))

for name in LAST_NAMES:
    cur.execute("INSERT INTO names (name, category) VALUES (?, ?)",(f'{name}', 'last_name'))

connection.commit()
# Check
connection.row_factory = sqlite3.Row
names = connection.execute('SELECT * FROM names').fetchall()
print('Name Database')
for name in names:
    print(f"{name['name']} ({name['category']})")
connection.close()