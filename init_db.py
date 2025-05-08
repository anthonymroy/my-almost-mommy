import sqlite3

def initialize():
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

def print():
    connection = sqlite3.connect('./db/database.db')
    connection.row_factory = sqlite3.Row
    names = connection.execute('SELECT * FROM names').fetchall()
    print('My Almost Mommy Database')
    for name in names:
        print(f"{name['seed']} ({name['mom']})")
    connection.close()

if __name__ == '__main__':
    initialize()
    print()