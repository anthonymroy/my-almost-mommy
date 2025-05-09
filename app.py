from db.sample_name_lists import (COMMON_LAST_NAME, COMMON_FIRST_NAME, PREPPY_FIRST_NAME,
                           PREPPY_FIRST_OR_COMMON_LAST_NAME, PREPPY_LAST_NAME,
                           PREPPY_PREPPY_FIRST_NAME, WASPY_NICKNAME)
from flask import Flask, render_template, request
import json
import random
import sqlite3

def one_in(num:int) -> bool:
	ans = False
	dice = range(num)
	if random.choice(dice) == 0:
		ans = True
	return ans

def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect('./db/database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_mom_from_db(seed_name:str) -> str:
    conn = get_db_connection()
    mommy_name = conn.execute('SELECT mom FROM names WHERE seed = ?', (seed_name,)).fetchone()
    conn.close()
    return mommy_name

def generate_vocabulary_odds(vocab:dict) -> None:
    vocab_size = 0
    for key in vocab.keys():
        vocab_size += len(vocab[key]['names'])
    
    for key in vocab.keys():
        vocab[key]['odds'] = float(len(vocab[key]['names'])) / vocab_size

def generate_first_name() -> tuple[str,int]:
    vocabulary = {
        'common_first_name': {'names':COMMON_FIRST_NAME,'points':0},
        'preppy_first_name': {'names':PREPPY_FIRST_NAME + PREPPY_FIRST_OR_COMMON_LAST_NAME,'points':1},
        'preppy_preppy_first_name': {'names':PREPPY_PREPPY_FIRST_NAME + WASPY_NICKNAME,'points':2}        
    }
    generate_vocabulary_odds(vocabulary)
    keys = list(vocabulary.keys())
    weights = [x['odds'] for x in list(vocabulary.values())]
    selected_key = random.choices(keys, weights=weights, k=1)[0]
    name = random.choice(vocabulary[selected_key]['names'])
    return (name, vocabulary[selected_key]['points'])
    
def generate_middle_name() -> tuple[str,int]:
    if one_in(2):
        # Half the time, return nothing
        return ('',0)
    vocabulary = {
        'preppy_last_name': {'names':PREPPY_FIRST_OR_COMMON_LAST_NAME,'points':1},
        'preppy_preppy_first_name': {'names':PREPPY_PREPPY_FIRST_NAME + WASPY_NICKNAME,'points':2}
    }
    generate_vocabulary_odds(vocabulary)
    keys = list(vocabulary.keys())
    weights = [x['odds'] for x in list(vocabulary.values())]
    selected_key = random.choices(keys, weights=weights, k=1)[0]
    name = random.choice(vocabulary[selected_key]['names'])
    return (name, vocabulary[selected_key]['points'])

def generate_last_name() -> tuple[str, int]:
    vocabulary = {
        'common_last_name': {'names':COMMON_LAST_NAME+PREPPY_FIRST_OR_COMMON_LAST_NAME,'points':0},        
        'preppy_last_name': {'names':PREPPY_LAST_NAME,'points':1}
    }
    generate_vocabulary_odds(vocabulary)
    keys = list(vocabulary.keys())
    weights = [x['odds'] for x in list(vocabulary.values())]
    selected_key = random.choices(keys, weights=weights, k=1)[0]
    name = random.choice(vocabulary[selected_key]['names'])
    points = vocabulary[selected_key]['points']
    if one_in(4):
        # Make hyphenated last name
        points += 1
        selected_key = random.choices(keys, weights=weights, k=1)[0]
        name2 = random.choice(vocabulary[selected_key]['names'])
        if name != name2:            
            name = name+'-'+name2
            points += vocabulary[selected_key]['points']
    return (name, points)

def acceptable_name(first_name:str, middle_name:str, last_name, preppy_points:str) -> bool:
    if first_name == middle_name or first_name in last_name or middle_name in last_name:
        return False
    if preppy_points < 2:
        return False
    if preppy_points == 4:
        return False
    return True

def generate_random_mom(seed_name:any) -> str:
    random.seed(seed_name)      
    while True:
        preppy_points = 0
        first_name, points = generate_first_name()
        preppy_points += points
        middle_name, points = generate_middle_name()
        preppy_points += points
        last_name, points = generate_last_name()
        preppy_points += points
        if acceptable_name(first_name, middle_name, last_name, preppy_points):
            break

    if len(middle_name) == 0 or ('"' in first_name and '"' in middle_name):
        first_name = first_name.replace('"','') 

    mom = first_name+' '+middle_name+' '+last_name
    mom = mom.replace('  ',' ')

    return mom

import os
app = Flask(__name__, template_folder='webpages')
current_working_directory = os.getcwd()
print(f"The current working directory is: {current_working_directory}")

with open('./secrets/sample.credentials.json') as f:
    credentials = json.load(f)
app.config['SECRET_KEY'] = credentials['sample_key']

@app.route('/', methods=('GET', 'POST'))
def index():
    mom = ''
    if request.method == 'POST':        
        seed_name = request.form['name'].strip().lower()
        print(f'seed_name = {seed_name}')
        mom = get_mom_from_db(seed_name)
        if mom is None:
            mom = generate_random_mom(seed_name)
            conn = get_db_connection()
            conn.execute('INSERT INTO names (seed, mom) VALUES (?, ?)', (seed_name, mom))
            conn.commit()
            conn.close()
    return render_template('index.html', my_almost_mommy=mom)

if __name__ == '__main__':
    seed_str = None
    generate_random_mom(seed_str)