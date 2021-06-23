'''
作業 (利用 lambda)
id = 'A123456789'
第二碼 sex  = id[1] -> 1 (1: 男生, 2: 女生)
第三碼 area = id[2] -> 2 (0~5: 台灣, 6: 外國, 7: 無戶籍, 8: 港澳, 9: 大陸)
印出: 台灣男
'''

id = "A123456789"
sex = id[1]
area = id[2]

sex_info = {
    1: '男',
    2: '女'
}
area_info = {
    0: '台灣',
    1: '台灣',
    2: '台灣',
    3: '台灣',
    4: '台灣',
    5: '台灣',
    6: '外國',
    7: '無戶籍',
    8: '港澳',
    9: '大陸'
}

m1 = lambda sex, area: print(area_info.get(area), sex_info.get(sex))
m1(int(sex), int(area))
