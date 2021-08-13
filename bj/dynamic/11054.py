# n = 10
# li = [1, 5, 2, 1, 4, 3, 4, 5, 2, 1]

n = int(input())
li = list(map(int, input().split()))

"""
10
1 5 2 1 4 3 4 5 2 1
1 2 2 1 3 3 4 5 2 1
1 5 2 1 4 3 3 3 2 1
"""

dp_1 = [0 for _ in range(n)]
dp_2 = [0 for _ in range(n)]
for i in range(n):
    max_x = 0
    for j in range(i):
        if li[j] < li[i]:
            max_x = max(max_x, dp_1[j])
    dp_1[i] = max_x + 1
    
    max_y = 0
    for k in range(n - 1, n - 1 - i, -1):
        if li[k] < li[n - 1 - i]:
            max_y = max(max_y, dp_2[k])
    dp_2[n - 1 - i] = max_y + 1

dp = [x + y - 1 for x, y in zip(dp_1, dp_2)]
print(max(dp))
            

