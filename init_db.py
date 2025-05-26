from utils import get_db_connection, print_almost_mommy_result, SQL_PATHFILE

def initialize_db():
    connection = get_db_connection()
    with open(SQL_PATHFILE) as f:
        connection.executescript(f.read())

    cur = connection.cursor()
    cur.execute("INSERT INTO moms (seed, name, image) VALUES (?, ?, ?)",('lorelai gilmore', 'Pennilyn Lott','pennilyn-lott.jpg'))
    cur.execute("INSERT INTO moms (seed, name, image) VALUES (?, ?, ?)",('lorelei gilmore', 'Pennilyn Lott','pennilyn-lott.jpg'))
    cur.execute("INSERT INTO moms (seed, name, image) VALUES (?, ?, ?)",('rory gilmore', 'Sherry Tinsdale','sherry-tinsdale.jpg'))
    cur.execute("INSERT INTO moms (seed, name, image) VALUES (?, ?, ?)",('april nardini', 'Lorelai Gilmore','lorelai-gilmore.jpg'))
    cur.execute("INSERT INTO moms (seed, name, image) VALUES (?, ?, ?)",('lorelai', 'Pennilyn Lott','pennilyn-lott.jpg'))
    cur.execute("INSERT INTO moms (seed, name, image) VALUES (?, ?, ?)",('april', 'Lorelai Gilmore','lorelai-gilmore.jpg'))
    cur.execute("INSERT INTO moms (seed, name, image) VALUES (?, ?, ?)",('rory', 'Sherry Tinsdale','sherry-tinsdale.jpg'))

    connection.commit()
    connection.close()

def echo_db():
    connection = get_db_connection()
    moms = connection.execute('SELECT * FROM moms').fetchall()
    print('My Almost Mommy Database')
    for mom in moms:
        print_almost_mommy_result(mom['seed'], mom['name'], image_filename=mom['image'])
    connection.close()

if __name__ == '__main__':
    initialize_db()
    echo_db()