import sqlite3

sql = 'UPDATE Lotto SET n1 = %d, n2= %d WHERE id = %d ' \
      % (99, 98, 1)

print(sql)

conn = sqlite3.connect('demo.db')
cursor = conn.cursor()
cursor.execute(sql)
conn.commit()
conn.close()


print('Update ok, rowcount:', cursor.rowcount)
