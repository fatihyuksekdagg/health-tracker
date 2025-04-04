import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS goals (
        user_id INTEGER PRIMARY KEY,
        step_goal INTEGER DEFAULT 10000,
        water_goal REAL DEFAULT 2.0,
        sleep_goal REAL DEFAULT 8.0
    )
''')

conn.commit()
conn.close()

print("✅ Hedefler tablosu başarıyla oluşturuldu.")
