import sqlite3


conn = sqlite3.connect('../case03/demo.db')
cursor = conn.cursor()
cursor.execute("INSERT INTO Employee(ID, NAME, AGE, ADDRESS, SALARY) VALUES (1, 'Paul', 32, 'Taipei', 45000.0)")
cursor.execute("INSERT INTO Employee(ID, NAME, AGE, ADDRESS, SALARY) VALUES (2, 'Allen', 28, 'Taipei', 42000.0)")
cursor.execute("INSERT INTO Employee(ID, NAME, AGE, ADDRESS, SALARY) VALUES (3, 'Teddy', 41, 'Taoyuan', 55000.0)")
cursor.execute("INSERT INTO Employee(ID, NAME, AGE, ADDRESS, SALARY) VALUES (4, 'Mark', 29, 'New-Taipei', 35000.0)")
cursor.execute("INSERT INTO Employee(ID, NAME, AGE, ADDRESS, SALARY) VALUES (5, 'John', 36, 'New-Taipei', 51000.0)")
cursor.execute("INSERT INTO Employee(ID, NAME, AGE, ADDRESS, SALARY) VALUES (6, 'Mary', 21, 'Taoyuan', 28000.0)")
conn.commit()
conn.close()
