import psycopg2 as p

# reading config file for database name, username and password
def read_config(file_path):
    config = {}
    with open(file_path, 'r') as file:
        for line in file:
            key, value = line.strip().split('=')
            config[key.strip()] = value.strip()
    return config

# please update the config.txt file with the databases' name username password
config = read_config('src/config.txt')
database = config.get('database')
username = config.get('username')
password = config.get('password')

def query(query):
    conn = p.connect(dbname=database, user=username, password=password, host='localhost', port=5432)
    cursor = conn.cursor()
    cursor.execute(query)
    
    try:
        fetch = cursor.fetchall()
    except p.ProgrammingError:
        fetch = []

    cursor.close()
    conn.commit()
    conn.close()

    return fetch
