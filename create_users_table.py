import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Kullanıcı tablosu oluştur
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
''')

# activity_log tablosuna user_id sütunu ekle
try:
    cursor.execute('ALTER TABLE activity_log ADD COLUMN user_id INTEGER DEFAULT 1')
except:
    pass  # Zaten varsa hata vermez

conn.commit()
conn.close()
print("✅ Kullanıcı tablosu ve user_id sütunu oluşturuldu.")
