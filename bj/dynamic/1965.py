
# n = 8
# li = [1, 6, 2, 5, 7, 3, 5, 6]

n = int(input())
li = list(map(int, input().split()))

"""
1 6 2 5 7 3 5 6
1 2 2 3 4 3 4 5
1 2 2 3 4 4 4 5

1 2 2 3 4 3 4 5   

"""

dp = [0 for _ in range(n)]
for i in range(n):
    max_x = 0
    for j in range(i):
        if li[j] < li[i]:
            max_x = max(max_x, dp[j])
    dp[i] = max_x + 1
print(max(dp))
