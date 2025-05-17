from utils import get_db_connection, print_almost_mommy_result, SQL_PATHFILE

def initialize_db():
    connection = get_db_connection()
    with open(SQL_PATHFILE) as f:
        connection.executescript(f.read())

    cur = connection.cursor()
    cur.execute("INSERT INTO names (seed, mom) VALUES (?, ?)",('lorelai gilmore', 'Pennilyn Lott'))
    cur.execute("INSERT INTO names (seed, mom) VALUES (?, ?)",('lorelei gilmore', 'Pennilyn Lott'))
    cur.execute("INSERT INTO names (seed, mom) VALUES (?, ?)",('rory gilmore', 'Sherry Tinsdale'))
    cur.execute("INSERT INTO names (seed, mom) VALUES (?, ?)",('april nardini', 'Lorelai Gilmore'))
    cur.execute("INSERT INTO names (seed, mom) VALUES (?, ?)",('lorelai', 'Pennilyn Lott'))
    cur.execute("INSERT INTO names (seed, mom) VALUES (?, ?)",('april', 'Lorelai Gilmore'))
    cur.execute("INSERT INTO names (seed, mom) VALUES (?, ?)",('rory', 'Sherry Tinsdale'))

    connection.commit()
    connection.close()

def echo_db():
    connection = get_db_connection()
    names = connection.execute('SELECT * FROM names').fetchall()
    print('My Almost Mommy Database')
    for name in names:
        print_almost_mommy_result(name['seed'], name['mom'])
    connection.close()

if __name__ == '__main__':
    initialize_db()
    echo_db()