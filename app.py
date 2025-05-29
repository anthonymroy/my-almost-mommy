from flask import Flask, render_template, request
import os
from utils import (
    get_verified_image_directory,
    generate_random_mom_name,
    get_or_generate_name,
    get_or_generate_image_filename,
    get_portraits,
    generate_random_strings,
    print_mom_result,
    upsert_mom
)

app = Flask(__name__)

@app.route('/', methods=('GET', 'POST'))
def index():
    name = ''
    img_filepath = ''
    portraits = get_portraits()
    portraits = [os.path.join(get_verified_image_directory(p),p).replace("\\","/") for p in portraits]
    if request.method == 'POST':        
        seed = request.form['name'].strip().lower()
        name = get_or_generate_name(seed)
        if name is None:
            name = ''
        img_filename = get_or_generate_image_filename(seed)
        img_directory = get_verified_image_directory(img_filename)
        try:
            img_filepath = os.path.join(img_directory,img_filename).replace("\\","/")
        except TypeError:
            img_filepath = ''
        if len(name) > 0:
            upsert_mom(seed, name, img_filename)

    # # Useful for debugging
    # print(f'name = {name}') 
    # print(f'img_filepath = {img_filepath}')  
    # print(f'portraits = {portraits}')       
    
    return render_template(
        'index.html',
        portrait_1=portraits[0],
        portrait_2=portraits[1],
        portrait_3=portraits[2],
        portrait_4=portraits[3],
        portrait_5=portraits[4],
        portrait_6=portraits[5],
        almost_mommy_name=name,
        almost_mommy_img=img_filepath
    )

@app.route('/about')
def about():     
    return render_template('about.html')

@app.route('/contact')
def contact():     
    return render_template('contact.html')

if __name__ == '__main__':
    names_to_generate = 100
    random_seeds = generate_random_strings(names_to_generate)
    print('\n')
    for seed in random_seeds:
        mom,points = generate_random_mom_name(seed)
        print_mom_result(seed, mom, points)