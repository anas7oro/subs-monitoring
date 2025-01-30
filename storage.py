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

    insert_query = '''
        INSERT INTO subdomains (domain, subdomain)
        VALUES (%s, %s)
        ON CONFLICT (domain, subdomain) DO NOTHING
    '''

    for subdomain in subdomains:
        try:
            cursor.execute(insert_query, (domain, subdomain))
            if cursor.rowcount > 0:
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

def add_subdomain(domain, subdomain):
    """
    Manually adds a single subdomain under a specified domain.
    Returns True if inserted, False if it already existed or error.
    """
    conn = get_connection()
    cursor = conn.cursor()
    inserted = False

    query = '''
        INSERT INTO subdomains (domain, subdomain)
        VALUES (%s, %s)
        ON CONFLICT (domain, subdomain) DO NOTHING
    '''
    try:
        cursor.execute(query, (domain, subdomain))
        if cursor.rowcount > 0:
            inserted = True
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error adding subdomain {subdomain} to domain {domain}: {e}")
    finally:
        cursor.close()
        conn.close()

    return inserted

def remove_subdomain(domain, subdomain):
    """
    Removes a specific subdomain from the database.
    """
    conn = get_connection()
    cursor = conn.cursor()
    deleted = False
    try:
        cursor.execute('DELETE FROM subdomains WHERE domain = %s AND subdomain = %s', (domain, subdomain))
        if cursor.rowcount > 0:
            deleted = True
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error removing subdomain {subdomain} from domain {domain}: {e}")
    finally:
        cursor.close()
        conn.close()

    return deleted

def remove_subdomains_by_keyword(keyword):
    """
    Removes all subdomains containing the given keyword (case-sensitive) from the database.
    Returns the number of rows deleted.
    """
    conn = get_connection()
    cursor = conn.cursor()
    pattern = f'%{keyword}%'
    deleted_count = 0
    try:
        cursor.execute('DELETE FROM subdomains WHERE subdomain LIKE %s', (pattern,))
        deleted_count = cursor.rowcount
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error removing subdomains containing '{keyword}': {e}")
    finally:
        cursor.close()
        conn.close()

    return deleted_count
