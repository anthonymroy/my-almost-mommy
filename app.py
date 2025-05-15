from flask import Flask, render_template, request
import random
import string
from utils import (
    get_mom_from_db,
    generate_random_mom,
    get_db_connection,
    print_almost_mommy_result
)

app = Flask(__name__, template_folder='webpages')

@app.route('/', methods=('GET', 'POST'))
def index():
    mom = ''
    if request.method == 'POST':        
        seed_name = request.form['name'].strip().lower()
        mom = get_mom_from_db(seed_name)
        if mom is None:
            mom,_ = generate_random_mom(seed_name)
            conn = get_db_connection()
            conn.execute('INSERT INTO names (seed, mom) VALUES (?, ?)', (seed_name, mom))
            conn.commit()
            conn.close()
            
    return render_template('index.html', my_almost_mommy=mom)

def generate_random_strings(count:int,min_length:int=5, max_length:int=32) -> list[str]:
    viable_characters = string.ascii_letters + ' ' +'-'+'.'
    random_strings = []
    for _ in range(count):
        string_length = random.randint(min_length, max_length)
        new_string = ''.join(random.choice(viable_characters) for _ in range(string_length))
        random_strings.append(new_string)   
    return random_strings

if __name__ == '__main__':
    names_to_generate = 100
    random_seeds = generate_random_strings(names_to_generate)
    print('\n')
    for seed in random_seeds:
        mom,points = generate_random_mom(seed)
        print_almost_mommy_result(seed, mom, points)