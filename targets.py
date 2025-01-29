# targets.py

from db import get_connection

def add_target(domain):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO targets (domain) VALUES (%s)', (domain,))
        conn.commit()
        print(f"Added {domain} to monitoring list.")
    except Exception as e:
        conn.rollback()
        if "duplicate key value" in str(e):
            print(f"{domain} is already in the monitoring list.")
        else:
            print(f"Error adding domain {domain}: {e}")
    finally:
        cursor.close()
        conn.close()

def remove_target(domain):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM targets WHERE domain = %s', (domain,))
        conn.commit()
        print(f"Removed {domain} from monitoring list.")
    except Exception as e:
        conn.rollback()
        print(f"Error removing domain {domain}: {e}")
    finally:
        cursor.close()
        conn.close()

def list_targets():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT domain FROM targets')
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return [row[0] for row in rows]
