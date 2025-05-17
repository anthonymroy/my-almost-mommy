from db.name_lists import (COMMON_LAST_NAME, COMMON_FIRST_NAME, PREPPY_FIRST_NAME,
                           PREPPY_FIRST_OR_COMMON_LAST_NAME, PREPPY_LAST_NAME,
                           PREPPY_PREPPY_FIRST_NAME, WASPY_NICKNAME)
from Levenshtein import distance as lev_dist
from pathlib import Path
import random
import string
import sqlite3

CWD = Path(__file__).parent.resolve()
DATABASE_PATHFILE = CWD / './db/database.db'
SQL_PATHFILE = CWD / './db/schema.sql'

def one_in(num:int, return_value:bool=True) -> bool:
    """
    Has a 1:num chance of returning a specified boolean value. 

    Args:
    num: An integer representing the denominator of the probability (1/num).
            It defines the upper bound (exclusive) of the range from which a
            random number is chosen.
    return_value: A boolean value to return when the random choice is 0.
                    Defaults to True.

    Returns:
        True with a probability of 1/num (if return_value is True),
        or False with a probability of 1/num (if return_value is False).
        Returns the opposite of 'return_value' with a probability of (num-1)/num.
    """
    ans = not return_value
    dice = range(num)
    if random.choice(dice) == 0:
        ans = return_value
    return ans

def print_almost_mommy_result(seed_name:str, mom_name:str, points:int|str=None) -> None:
    """
    Prints a formatted string indicating a relationship between two names,
    optionally including a point value.

    Args:
        seed_name: The name of the 'seed'.
        mom_name: The name of the 'mom'.
        points: An optional integer or string representing points associated with the relationship.
                If None or an empty string (''), the points are not included in the output.
                Defaults to None.

    Returns:
        None.
    """
    if points is None:
        print(f'{seed_name} -> {mom_name}')
        return
    if points == '':
        print(f'{seed_name} -> {mom_name}')
        return
    print(f'{seed_name} -> {mom_name} ({points} points)') 

def get_db_connection() -> sqlite3.Connection:
    """
    Establishes and returns a connection to an SQLite database.
    """
    conn = sqlite3.connect(DATABASE_PATHFILE)
    conn.row_factory = sqlite3.Row
    return conn

def get_mom_from_db(seed_name:str) -> str|None:
    """
    Retrieves the 'mom' name associated with a given 'seed' name from the database.

    Args:
        seed_name: The 'seed' name to search for in the database.

    Returns:
        The 'mom' name (as a string) if a matching 'seed' is found, otherwise None.
    """

    conn = get_db_connection()
    mom_name = conn.execute('SELECT mom FROM names WHERE seed = ?', (seed_name,)).fetchone()
    conn.close()
    if mom_name is not None:
        return mom_name['mom']
    return mom_name

def generate_vocabulary_odds(vocab:dict) -> None:
    """
    Calculates and adds the probability of each category in the vocabulary dictionary.

    Args:
        vocab: A dictionary where keys represent categories and values are
               dictionaries containing a list of 'names'. For example:
               {
                   'category1': {'names': ['name_a', 'name_b']},
                   'category2': {'names': ['name_c']}
               }

    Returns:
        None. This function modifies the input dictionary directly.
    """
    vocab_size = 0
    for key in vocab.keys():
        vocab_size += len(vocab[key]['names'])
    
    for key in vocab.keys():
        vocab[key]['odds'] = float(len(vocab[key]['names'])) / vocab_size

def generate_first_name() -> tuple[str,int]:
    """
    Generates a name and its associated point value based on a weighted vocabulary.

    Returns:
        A tuple containing the randomly selected first name (str) and its
        corresponding point value (int).
    """
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
    """
    Generates a name and its associated point value based on a weighted vocabulary.

    Returns:
        A tuple containing the randomly selected first name (str) and its
        corresponding point value (int).
    """
    if one_in(8, False):
        return ('',0) #No middle name
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
    """
    Generates a name and its associated point value based on a weighted vocabulary.

    Returns:
        A tuple containing the randomly selected first name (str) and its
        corresponding point value (int).
    """
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
    if one_in(8, True):
        # Make hyphenated last name
        points += 1
        selected_key = random.choices(keys, weights=weights, k=1)[0]
        name2 = random.choice(vocabulary[selected_key]['names'])
        if name != name2:            
            name = name+'-'+name2
            points += vocabulary[selected_key]['points']
    return (name, points)

def levenshtein_difference(string1:str, string2:str) -> float:
    """
    Determines the Levenshtein distance of two strings normalized by the length of the longest
    string.

    Returns:
        Float between [0,1] inclusive where 0 means the strings are identical ans 1 means the
        strings are as different as they can be
    """
    if (string1 is None) ^ (string2 is None): #XOR
        return 1.0
    if (string1 is None) and (string2 is None):
        return 0.0
    distance = lev_dist(string1, string2)
    norm = max(len(string1),len(string2))
    return float(distance)/ norm

def acceptable_name(first_name:str, middle_name:str, last_name:str, preppy_points:str) -> bool:
    """
    Determines if a generated full name is considered "acceptable" based on certain criteria.

    The criteria include checking for similarity between the first, middle, and last names,
    and a minimum required 'preppy_points' value.

    Args:
        first_name: The generated first name (string).
        middle_name: The generated middle name (string).
        last_name: The generated last name (string).
        preppy_points: An integer representing the accumulated "preppy points"
                       associated with the generated names.

    Returns:
        True if the name meets all the acceptability criteria, False otherwise.
    """
    if preppy_points < 2:
        return False
    if levenshtein_difference(first_name, middle_name) < 0.5:
        return False
    last_names = last_name.split('-')
    for name in last_names:        
        if (levenshtein_difference(first_name, name) < 0.5 or 
            levenshtein_difference(middle_name, name) < 0.5):
            return False
    return True

def generate_random_mom(seed_name:any) -> tuple[str,int]:
    """
    Generates a random "mom" name (first, middle, last) and its associated
    total "preppy points" based on a given seed.

    Args:
        seed_name: An arbitrary value used to seed the random number generator.
                   This ensures that the same seed will produce the same sequence
                   of generated names.

    Returns:
        A tuple containing the generated full "mom" name (string) and the
        total accumulated "preppy points" (integer) for that name.
    """
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

def generate_random_strings(count:int,min_length:int=5, max_length:int=32) -> list[str]:
    """
    Generates a list of random strings 

    Args:
        count: The number of random strings to generate.
        min_length: The minimum length of each generated string (default: 5).
        max_length: The maximum length of each generated string (default: 32).

    Returns:
        A list containing the random generated strings.
    """
    random.seed(None)
    viable_characters = string.ascii_letters + ' ' +'-'+'.'
    random_strings = []
    for _ in range(count):
        string_length = random.randint(min_length, max_length)
        new_string = ''.join(random.choice(viable_characters) for _ in range(string_length))
        random_strings.append(new_string)   
    return random_strings