import sqlite3
from utils import (
    DATABASE_PATHFILE, 
    get_db_connection, 
    get_mom_from_db, 
    generate_random_mom,
    print_almost_mommy_result
)

def display_main_menu():
    print("Available Options:")
    print("A - Add entry")
    print("D - Delete entry")
    print("P - Print database")
    print("T - Test names")
    print("Q - Quit")

def confirmation_dialog(message:str) -> bool:
    while True:
        choice = input(f"{message} (Y/N): ")
        match choice.lower():
            case 'y':
                return True
            case 'n':
                return False
            case _:
                print(f'Unable to parse "{choice}".')

def add_dialog():
    seed_name = input("Enter seed name: ").lower()
    db_mom_name = get_mom_from_db(seed_name)
    if db_mom_name is not None:
        print_almost_mommy_result(seed_name, db_mom_name)
        if not confirmation_dialog("Overwrite?"):
            print("Add canceled")
            return
    mom_name = input("Enter new mom name: ")
    if confirmation_dialog(f"Add {seed_name} -> {mom_name}?"):
        conn = get_db_connection()
        cur = conn.cursor()
        if db_mom_name is None:
            cur.execute("INSERT INTO names (seed, mom) VALUES (?, ?)",(seed_name, mom_name))
        else:
            cur.execute("UPDATE names SET mom = ? WHERE seed = ?",(mom_name,seed_name))
        conn.commit()
        conn.close()
    else:
        print("Add canceled")
        return
    
def delete_dialog():
    seed_name = input("Enter seed name to delete: ").lower()
    mom_name = get_mom_from_db(seed_name)
    if mom_name is None:
        print(f"{seed_name} is not in database.")
        print("Delete canceled")
        return    
    if confirmation_dialog(f"Delete {seed_name} -> {mom_name}?"):
        conn = get_db_connection()
        cur = conn.cursor()        
        cur.execute("DELETE FROM names WHERE seed = ?",(seed_name,))        
        conn.commit()
        conn.close()
    else:
        print("Delete canceled")
        return

def print_db():
    connection = sqlite3.connect(DATABASE_PATHFILE)
    connection.row_factory = sqlite3.Row
    names = connection.execute('SELECT * FROM names').fetchall()
    print('My Almost Mommy Database')
    for name in names:
        print_almost_mommy_result(name['seed'], name['mom'])
    connection.close()

def test_dialog():
    while(True):
        seed_name = input("Enter seed name (Leave blank to exit): ").lower()
        if seed_name == '':
            return
        method = 'Database'
        mom_name = get_mom_from_db(seed_name)
        points = 'N/A'
        if mom_name is None:
            mom_name, points = generate_random_mom(seed_name)
            method = 'Generated'
        print(f'Method: {method}')
        print_almost_mommy_result(seed_name, mom_name, points)

def main():
    while True:
        display_main_menu()
        choice = input("Choose option to edit database: ")
        match choice.lower():
            case 'a':
                add_dialog()
            case 'd':
                delete_dialog()
            case 'p':
                print_db()
            case 't':
                test_dialog()
            case 'q':
                break
            case _:
                print(f'Unable to parse "{choice}".')    

if __name__ == '__main__':
    main()
    print(f'Ending program')