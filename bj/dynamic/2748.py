

def r(n):
    if n == 0 or n == 1:
        return n

    li = [0, 1]
    for i in range(2, n + 1):  # 0번째 수가 존재하므로 n + 1 이 포인트
        li.append(li[i - 1] + li[i - 2])

    return li[-1]


print(r(int(input())))
