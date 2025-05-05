from db import 
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

def GenerateRandomFemaleName(seed_str):
    random.seed(seed_str)
    conn = get_db_connection()
    first_names = [x['name'] for x in conn.execute('SELECT name FROM names WHERE category = "first_name"').fetchall()]
    nicknames = [x['name'] for x in conn.execute('SELECT name FROM names WHERE category = "nickname"').fetchall()]
    last_names = [x['name'] for x in conn.execute('SELECT name FROM names WHERE category = "last_name"').fetchall()]
    ##Formats
    # first "nickname" last
    # first "nickname" last_long
    # nickname last
    # nickname last_long  
    # first_old last  
    # first_old last_long 
    # first_old "nickname" last
    name = random.choice(first_names)+' "'+random.choice(nicknames)+'" '+random.choice(last_names)
    return name

def generate_name(first:str, last:str) -> str:
    #remove whitespace and lower
    seed_string = (first.strip() + last.strip()).lower()
    if seed_string == 'lorelaigilmore':
        return 'Pennilyn Lott'
    if len(seed_string) == 0:
         return ''   
    return GenerateRandomFemaleName(seed_string)

app = Flask(__name__, template_folder='webpages')
with open('./secrets/sample.credentials.json') as f:
    credentials = json.load(f)
app.config['SECRET_KEY'] = credentials['sample_key']

@app.route('/', methods=('GET', 'POST'))
def index():
    mommy_name = ''
    if request.method == 'POST':
        mommy_name = generate_name(request.form['first_name'],request.form['last_name'])
    return render_template('index.html', name=mommy_name)

if __name__ == '__main__':
    print(GenerateRandomFemaleName("teststring"))