# storage.py

from db import get_connection

def save_subdomains(domain, subdomains):
    """
    Saves the given subdomains to the database with a unique constraint.
    Returns a set of subdomains that were newly inserted.
    """
    conn = get_connection()
    cursor = conn.cursor()
    new_subdomains = set()

    # We'll use PostgreSQL's ON CONFLICT DO NOTHING to avoid duplicates
    insert_query = '''
        INSERT INTO subdomains (domain, subdomain)
        VALUES (%s, %s)
        ON CONFLICT (domain, subdomain) DO NOTHING
    '''

    for subdomain in subdomains:
        try:
            cursor.execute(insert_query, (domain, subdomain))
            if cursor.rowcount > 0:
                # rowcount > 0 means new row was actually inserted
                new_subdomains.add(subdomain)
        except Exception as e:
            conn.rollback()
            print(f"Error inserting subdomain {subdomain}: {e}")

    conn.commit()
    cursor.close()
    conn.close()

    return new_subdomains

def get_subdomains(domain):
    """
    Retrieves all subdomains for a given domain from the database.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT subdomain FROM subdomains WHERE domain = %s', (domain,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return [r[0] for r in rows]

def search_subdomains(keyword):
    """
    Searches for subdomains containing the given keyword across all domains.
    """
    conn = get_connection()
    cursor = conn.cursor()
    pattern = f'%{keyword}%'
    cursor.execute('SELECT DISTINCT subdomain FROM subdomains WHERE subdomain LIKE %s', (pattern,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return [r[0] for r in rows]
