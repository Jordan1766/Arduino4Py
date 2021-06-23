def check_score(score):
    if score >= 60:
        return "pass"
    else:
        return "Fail"


if __name__ == '__main__':
    score = 70
    result = check_score(score)
    print(result, check_score(score))
# -------------------------------------------------
    result = "Pass" if score >= 60 else "Fail"
    print(result)
# -------------------------------------------------
    result = lambda score: "Pass" if score >= 60 else "Fail"
    print(result(score), result(50))
# -------------------------------------------------
    temp = lambda : print("24.5度")
    print(temp)
    temp()
