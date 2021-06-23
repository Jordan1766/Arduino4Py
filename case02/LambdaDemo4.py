# 利用 lambda 設計一個 bmi 函數式宣告
# 並 "印出" 170, 60 的 "bmi 值"
# bmi <= 18 "過輕", bmi > 23 "過重", 其他 "正常"
# Ex: checkBMI(170, 60) 輸出 24.76 (正常)


def getBMIResult(bmi):
    if bmi > 23:
        return '過重'
    elif bmi > 18:
        return '正常'
    else:
        return '過輕'


# bmi = lambda h, w: w/((h/100.0)*(h/100.0))
# checkBMI = lambda num: print("%.2f 過重" % num) if num > 23 else print("%.2f 正常" % num) if num > 18 else print("%.2f 過輕" % num)
# checkBMI(bmi(170, 60))

bmi = lambda h, w: w / (h / 100) ** 2
checkBMI = lambda n: getBMIResult(n)
bmiValue = bmi(170, 60)
print('%.2f' % bmiValue, checkBMI(bmiValue))

