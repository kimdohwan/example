def solution():
    n = int(input())
    li = []
    for i in range(n):
        li.append([])
        for j in input().split():
            li[i].append(int(j))

    result = []
    for i in range(len(li)):
        result.append([])
        if i == 0:
            result[i].append(li[i][0])
            continue
        for j in range(len(li[i])):
            if j == 0:
                result[i].append(result[i - 1][j] + li[i][j])
            elif j == len(li[i]) - 1:
                result[i].append(result[i - 1][j - 1] + li[i][j])
            else:
                result[i].append(max(result[i - 1][j - 1], result[i - 1][j]) + li[i][j])
    return max(result[-1])


while True:
    print(solution())
