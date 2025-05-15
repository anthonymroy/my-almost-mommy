from db.name_lists import (COMMON_LAST_NAME, COMMON_FIRST_NAME, PREPPY_FIRST_NAME,
                           PREPPY_FIRST_OR_COMMON_LAST_NAME, PREPPY_LAST_NAME,
                           PREPPY_PREPPY_FIRST_NAME, WASPY_NICKNAME)
from pathlib import Path
import random
import sqlite3

CWD = Path(__file__).parent.resolve()
DATABASE_PATHFILE = CWD / './db/database.db'
SQL_PATHFILE = CWD / './db/schema.sql'

def one_in(num:int) -> bool:
	ans = False
	dice = range(num)
	if random.choice(dice) == 0:
		ans = True
	return ans

def print_almost_mommy_result(seed_name:str, mom_name:str, points:int|str=None):
    if points is None:
        print(f'{seed_name} -> {mom_name}')
        return
    if points == '':
        print(f'{seed_name} -> {mom_name}')
        return
    print(f'{seed_name} -> {mom_name} Points: {points}') 

def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DATABASE_PATHFILE)
    conn.row_factory = sqlite3.Row
    return conn

def get_mom_from_db(seed_name:str) -> str|None:
    conn = get_db_connection()
    mom_name = conn.execute('SELECT mom FROM names WHERE seed = ?', (seed_name,)).fetchone()
    conn.close()
    if mom_name is not None:
        return mom_name['mom']
    return mom_name

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
    if one_in(6):
        # Make hyphenated last name
        points += 1
        selected_key = random.choices(keys, weights=weights, k=1)[0]
        name2 = random.choice(vocabulary[selected_key]['names'])
        if name != name2:            
            name = name+'-'+name2
            points += vocabulary[selected_key]['points']
    return (name, points)

def acceptable_name(first_name:str, middle_name:str, last_name, preppy_points:str) -> bool:
    if (
        first_name == middle_name or 
        first_name in last_name or
        (middle_name in last_name and middle_name != '')
    ):        
        return False
    if preppy_points < 2:
        return False
    return True

def generate_random_mom(seed_name:any) -> tuple[str,int]:
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

    return mom, preppy_points

