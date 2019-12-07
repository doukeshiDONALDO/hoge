
import sqlite3


db_name = './../fileupload/filename.db'
conn = sqlite3.connect(db_name)
c = conn.cursor()
sql = "select * from ndvi order by id desc limit 1"
c2 = c.execute(sql)
c3 = c2.fetchone()
conn.commit()
conn.close()
idkey = c3[0]
ndvi = 999
conn = sqlite3.connect(db_name)
c = conn.cursor()
sql = "update ndvi  set value = {} where  id = {}".format(ndvi,idkey)
c2 = c.execute(sql)
conn.commit()
conn.close()







