import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute('SELECT * FROM activity_log')
data = cursor.fetchall()

if data:
    for row in data:
        print(row)
else:
    print("Hiç veri bulunamadı.")

conn.close()
