import os
from utils import (     
    get_db_connection, 
    get_mom_from_db, 
    generate_random_mom_name,
    generate_random_strings,
    print_almost_mommy_result,
    upsert_mom
)

def display_main_menu():
    print("--- MAIN MENU ---")
    print("A - Add entry")
    print("D - Delete entry")
    print("P - Print database")
    print("T - Test single name")
    print("Z - Test a list of names")

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
    print("--- ADD DIALOG ---")
    seed_name = input("Enter seed name: ").lower()
    db_mom_name, db_img_file = get_mom_from_db(seed_name)
    if db_mom_name is not None:
        print_almost_mommy_result(seed_name, db_mom_name, image_filename=db_img_file)
        if not confirmation_dialog("Overwrite?"):
            print("Add canceled")
            return
    mom_name = input("Enter new mom name: ")
    image_filename = ""
    if confirmation_dialog(f"Add image?"):
        image_filename = input("Enter image filename: ")
    if confirmation_dialog(f"Add {seed_name} -> {mom_name} @ {image_filename}?"):
        upsert_mom(seed_name, mom_name, image_filename)
    else:
        print("Add canceled")
        return
    
def delete_dialog():
    print("--- DELETE DIALOG ---")
    seed_name = input("Enter seed name to delete: ").lower()
    mom_name, mom_image = get_mom_from_db(seed_name)
    if mom_name is None:
        print(f"{seed_name} is not in database.")
        print("Delete canceled")
        return    
    if confirmation_dialog(f"Delete {seed_name} -> {mom_name} @ {mom_image}?"):
        conn = get_db_connection()
        cur = conn.cursor()        
        cur.execute("DELETE FROM moms WHERE seed = ?",(seed_name,))        
        conn.commit()
        conn.close()
    else:
        print("Delete canceled")
        return

def print_db():
    connection = get_db_connection()
    moms = connection.execute('SELECT * FROM moms').fetchall()
    print('My Almost Mommy Database')
    for mom in moms:
        print_almost_mommy_result(mom['seed'], mom['name'], image_filename=mom['image'])
    connection.close()

def test_single_dialog():
    while(True):
        print("--- TEST DIALOG ---")
        seed_name = input("Enter seed name (Leave blank to exit): ").lower()
        if seed_name == '':
            return
        method = 'Database'
        mom_name,_ = get_mom_from_db(seed_name)
        points = 'N/A'
        if mom_name is None:
            mom_name,points = generate_random_mom_name(seed_name)
            method = 'Generated'
        print(f'Method: {method}')
        print_almost_mommy_result(seed_name, mom_name, points)

def test_list_dialog():
    while(True):
        print("--- TEST DIALOG ---")
        text = input("How many random names to generate? (Leave blank to exit): ")
        if text == '':
            return
        try:
            number = int(text)
        except ValueError:
            print(f'Unable to parse "{text} as an int"')
            continue

        random_seeds = generate_random_strings(number)
        print('\n')
        for seed in random_seeds:
            mom,points = generate_random_mom_name(seed)
            print_almost_mommy_result('', mom, points)

def main():
    while True:
        display_main_menu()
        choice = input("Please choose an option (Leave blank to exit program): ")
        if choice == '': 
            break
        match choice.lower()[0]:
            case 'a':
                add_dialog()
            case 'd':
                delete_dialog()
            case 'p':
                print_db()
            case 't':
                test_single_dialog()
            case 'z':
                test_list_dialog()            
            case _:
                print(f'Unable to parse "{choice}".')    

if __name__ == '__main__':
    main()
    print(f'Program ended')