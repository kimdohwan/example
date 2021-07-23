n = int(input())
li_input = [int(input()) for i in range(n)]

result = [1, 1, 1]
for i in range(3, max(li_input)):
    result.append(result[i - 2] + result[i - 3])
for j in li_input:
    print(result[j - 1])