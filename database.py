import sqlite3

conn = sqlite3.connect("database.db", check_same_thread=False)
c = conn.cursor()

def create_tables():

    c.execute("""
    CREATE TABLE IF NOT EXISTS users(
        username TEXT PRIMARY KEY,
        password TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS history(
        username TEXT,
        interest TEXT,
        recommended TEXT
    )
    """)

    conn.commit()

def register_user(username, password):
    try:
        c.execute("INSERT INTO users VALUES (?,?)",
                  (username, password))
        conn.commit()
        return True
    except:
        return False

def login_user(username, password):
    c.execute("SELECT * FROM users WHERE username=? AND password=?",
              (username, password))
    return c.fetchone()

def save_history(username, interest, recommended):
    c.execute("INSERT INTO history VALUES (?,?,?)",
              (username, interest, recommended))
    conn.commit()

def get_history(username):
    c.execute("SELECT recommended FROM history WHERE username=?",
              (username,))
    return c.fetchall()
