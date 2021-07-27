#   1 2 3 4 5 6 7 8 9 10
# 1 1 1 1 1 1 1 1 1 1 1
# 2 0 1 1 2 2 3 3 4 4 5
# 5 0 0 0 0 1 1 2 2 3 4
#   1 1 2 3 4 5 6 7 8 10

# 거꾸로 세어도 똑같네?
# 5 0 0 0 0 1 0 0 0 0 1
# 2 0 1 0 1 0 1 1 1 1 1
# 1 1 1 2 2 3 4 5 6 7 8
#   1 2 2 3 4 5 6 7 8 10

n, k = map(int, input().split())
result = [0] * (k + 1)
result[0] = 1
for _ in range(n):
    c = int(input())
    for i in range(c, k + 1):
        result[i] += result[i - c]
print(result[k])
