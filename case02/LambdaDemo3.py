# lambda lab:
# 請利用lambda 做出能夠判斷 odd 基數, even 偶數的函式
# result(4) 得到 "even"
# result(3) 得到 "odd"

result = lambda x: print("odd") if x % 2 > 0 else print("even")
result(4)
result(3)

result1 = lambda n: "Even" if n % 2 == 0 else "Odd"

