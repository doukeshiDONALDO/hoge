import sqlite3

db_name = 'filename.db'

conn = sqlite3.connect(db_name)
c = conn.cursor()
sql = "select * from ndvi order by id desc limit 1"
c2 = c.execute(sql)
c3 = c2.fetchone()

conn.commit()
conn.close()
c4 = list(c3)
print(c4)
