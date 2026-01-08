import sqlite3
import os



DB_PATH = os.path.join("data", "oiler_repairs.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    os.makedirs("data", exist_ok=True)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS repair_services (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT,
    service_name TEXT,
    price_raw TEXT,    
    currency TEXT DEFAULT 'UAH',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print(f"База данных готова по адресу: {DB_PATH}")