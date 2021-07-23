t = int(input())
input_li = [list(map(lambda x: int(x), input().split())) for _ in range(t)]

while input_li:
    n, m = input_li.pop(0)

    li = [[0 for _ in range(n)] for _ in range(m)]
    assert len(li) == m

    for i in range(m):
        for j in range(n):
            if j == 0:
                li[i][j] = i + 1
            elif i == 0:
                li[i][j] = 1
            elif i == j:
                li[i][j] = 1
            else:
                li[i][j] = li[i - 1][j] + li[i - 1][j - 1]

    print(li[m - 1][n - 1])



