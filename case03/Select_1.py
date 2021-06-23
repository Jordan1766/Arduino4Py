import sqlite3

conn = sqlite3.connect('demo.db')
cursor = conn.cursor()
# 查詢資料列 META-INFO
cursor.execute('PRAGMA TABLE_INFO("Lotto")')
#print(cursor.fetchall())

names = [t[1] for t in cursor.fetchall()]
#print(names)
for name in names:
    print(name, end='\t')
print('\n-------------------------------------------------')

# 查詢資料列 sql
sql = 'SELECT id, n1, n2, n3, n4, n5, ts FROM Lotto'
cursor.execute(sql)
rows = cursor.fetchall()

conn.close()

for r in rows:
    print('{}\t{}\t{}\t{}\t{}\t{}\t{}\t'
        .format(r[0], r[1], r[2], r[3], r[4], r[5], r[6]))

print('完成')