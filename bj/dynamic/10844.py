#     0 1 2 3 4 5 6 7 8 9
# 1   0 1 1 1 1 1 1 1 1 1
# 2   1 2 2 2 2 2 2 2 2 1
# 3   2 3 4 4 4 4 4 4 3 2

n = int(input())
dp = [[0, 1, 1, 1, 1, 1, 1, 1, 1, 1], ]
for i in range(n - 1):
    dp.append([])
    for j in range(10):
        if j == 0:
            dp[i + 1].append(dp[i][j + 1])
        elif j == 9:
            dp[i + 1].append(dp[i][j - 1])
        else:
            dp[i + 1].append(dp[i][j - 1] + dp[i][j + 1])
print(sum(dp[n - 1]) % 1000000000)
