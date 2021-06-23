import sqlite3

# sql = " SELECT NAME FROM Employee ORDER BY SALARY DESC"
sql = "SELECT 'MAX' as TYPE, NAME , max(SALARY) FROM Employee " \
      "UNION ALL " \
      "SELECT 'MIN' as TYPE, NAME , min(SALARY) FROM Employee"


conn = sqlite3.connect('../case03/demo.db')
cursor = conn.cursor()
cursor.execute(sql)

rows = cursor.fetchall()

conn.commit()
conn.close()

print(rows)

