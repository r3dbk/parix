import sqlite3

conn = sqlite3.connect('parix.db')
cur = conn.cursor()

# cur.execute('UPDATE appointments_db SET status = ? WHERE appointment_id = ?;', (str(0), str(0),))
cur.execute('DROP TABLE appointments_db')

print(cur.execute('SELECT * FROM appointments_db;').fetchall())