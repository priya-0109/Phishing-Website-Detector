import sqlite3

conn = sqlite3.connect('phishing.db')

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS scan_history(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT,
    result TEXT,
    risk_score INTEGER
)
''')

conn.commit()
conn.close()

print("Database Created Successfully")