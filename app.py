from flask import Flask, render_template, request
from utils import (
    get_mom_from_db,
    generate_random_mom,
    get_db_connection,
    generate_random_strings,
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

if __name__ == '__main__':
    names_to_generate = 100
    random_seeds = generate_random_strings(names_to_generate)
    print('\n')
    for seed in random_seeds:
        mom,points = generate_random_mom(seed)
        print_almost_mommy_result(seed, mom, points)