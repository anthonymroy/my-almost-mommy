import sqlite3
from pathlib import Path

CWD = Path(__file__).parent.resolve()
DATABASE_PATHFILE = CWD / './db/database.db'

def initialize():
    connection = sqlite3.connect(DATABASE_PATHFILE)

    with open('./db/schema.sql') as f:
        connection.executescript(f.read())

    cur = connection.cursor()
    cur.execute("INSERT INTO names (seed, mom) VALUES (?, ?)",('lorelai gilmore', 'Pennilyn Lott'))
    cur.execute("INSERT INTO names (seed, mom) VALUES (?, ?)",('lorelei gilmore', 'Pennilyn Lott'))
    cur.execute("INSERT INTO names (seed, mom) VALUES (?, ?)",('rory gilmore', 'Sherry Tinsdale'))
    cur.execute("INSERT INTO names (seed, mom) VALUES (?, ?)",('april nardini', 'Lorelai Gilmore'))

    connection.commit()
    connection.close()

def print():
    connection = sqlite3.connect(DATABASE_PATHFILE)
    connection.row_factory = sqlite3.Row
    names = connection.execute('SELECT * FROM names').fetchall()
    print('My Almost Mommy Database')
    for name in names:
        print(f"{name['seed']} ({name['mom']})")
    connection.close()

if __name__ == '__main__':
    initialize()
    print()