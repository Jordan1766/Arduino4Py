# 哪個數字出現最多

import sqlite3

conn = sqlite3.connect('demo.db')
cursor = conn.cursor()

sql = 'SELECT n1, n2, n3, n4, n5 FROM Lotto '
cursor.execute(sql)
rows = cursor.fetchall()

conn.close()

nums_list = []

for i in range(39):
    print(i)
    nums_list.append(0)

for r in rows:
    for i in range(5):
        for j in range(39):
            if j + 1 == r[i]:
                nums_list[j] += 1

print(nums_list)

maxNum = max(nums_list)
index = 0
for i in range(39):
    if maxNum == nums_list[i]:
        index = i + 1

print('max :', maxNum)
print('num: ', index)
