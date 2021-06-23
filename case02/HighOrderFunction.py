
def add(x):
    return x + 1


def sub(x):
    return x - 1


def operator(func, x):
    if(x > 0):
        return func(x)
    else:
        return x


def multi(func1, func2, x):
    if(x > 0):
        return func1(x) * func2(x)
    else:
        return x


if __name__ == '__main__':
    x = 1
    x = add(x)
    print(x)
    x = sub(x)
    print(x)
# ---------------------------------------------------------
    y = 3
    y = operator(add, y)
    print(y)
# ---------------------------------------------------------
    y = -3
    y = operator(sub, y)
    print(y)
# ---------------------------------------------------------
    z = 5
    z = multi(add, sub, z)
    print(z)
