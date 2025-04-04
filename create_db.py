import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS activity_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        steps INTEGER,
        water_liters REAL,
        sleep_hours REAL
    )
''')

conn.commit()
conn.close()
print("Veritabanı oluşturuldu.")
