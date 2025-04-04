import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

try:
    cursor.execute('ALTER TABLE users ADD COLUMN first_name TEXT')
except:
    pass
try:
    cursor.execute('ALTER TABLE users ADD COLUMN last_name TEXT')
except:
    pass
try:
    cursor.execute('ALTER TABLE users ADD COLUMN email TEXT')
except:
    pass
try:
    cursor.execute('ALTER TABLE users ADD COLUMN birth_date TEXT')
except:
    pass
try:
    cursor.execute('ALTER TABLE users ADD COLUMN theme TEXT')
except:
    pass

conn.commit()
conn.close()

print("✅ Kullanıcı tablosu güncellendi.")
