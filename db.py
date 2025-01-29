# db.py

import psycopg2
import yaml

def get_db_config():
    """
    Reads database configuration from config.yaml and returns a dict.
    """
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    db_config = config.get('database', {})
    return db_config

def get_connection():
    """
    Returns a new psycopg2 connection using the config.yaml settings.
    """
    db_config = get_db_config()
    conn = psycopg2.connect(
        host=db_config.get('host', 'localhost'),
        port=db_config.get('port', 5432),
        dbname=db_config.get('dbname', 'subdomains_db'),
        user=db_config.get('user', 'mydbuser'),
        password=db_config.get('password', 'mypassword')
    )
    return conn

def init_db():
    """
    Creates the necessary tables (targets and subdomains) if they don't already exist.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Create targets table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS targets (
            id SERIAL PRIMARY KEY,
            domain TEXT UNIQUE NOT NULL
        )
    ''')

    # Create subdomains table with a unique constraint on (domain, subdomain)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subdomains (
            id SERIAL PRIMARY KEY,
            domain TEXT NOT NULL,
            subdomain TEXT NOT NULL,
            CONSTRAINT unique_domain_subdomain UNIQUE (domain, subdomain)
        )
    ''')

    conn.commit()
    cursor.close()
    conn.close()
