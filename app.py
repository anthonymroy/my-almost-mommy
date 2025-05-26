from flask import Flask, render_template, request, url_for
from utils import (
    get_mom_from_db,
    generate_random_mom,
    get_db_connection,
    generate_random_strings,
    print_almost_mommy_result
)

app = Flask(__name__)

@app.route('/', methods=('GET', 'POST'))
def index():
    name = ''
    img_url = ''
    img_filename = ''
    if request.method == 'POST':        
        seed = request.form['name'].strip().lower()
        print(f'seed = {seed}')
        if len(seed) > 0:
            name, img_filename = get_mom_from_db(seed)
            if name is None:
                name,_,img_filename = generate_random_mom(seed)
                conn = get_db_connection()
                conn.execute('INSERT INTO moms (seed, name, image) VALUES (?, ?, ?)', (seed, name, img_filename))
                conn.commit()
                conn.close()
            img_url = url_for('static', filename=f'images/portraits/{img_filename}')
    print(f'name = {name}') 
    print(f'img_filename = {img_filename}') 
    print(f'img_url = {img_url}')        
    return render_template(
        'index1.html',
        my_almost_mommy_name=name,
        my_almost_mommy_img=img_url
    )

if __name__ == '__main__':
    names_to_generate = 100
    random_seeds = generate_random_strings(names_to_generate)
    print('\n')
    for seed in random_seeds:
        mom,points,image = generate_random_mom(seed)
        print_almost_mommy_result(seed, mom, points,image)