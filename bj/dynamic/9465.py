
# error->?
# T = int(input())
#
# T_li = []
# for _ in range(T):
#     n = int(input())
#     input_li = [[int(i) for i in input().split()] for _ in range(2)]
#     T_li.append(input_li)
#
#
# for a, b in T_li:
#
#     result = [
#         [a[0], b[0] + a[1]],
#         [b[0], a[0] + b[1]]
#     ]
#
#     for i in range(2, len(a)):
#         result[0].append(max(result[1][i - 2], result[1][i - 1]) + a[i])
#         result[1].append(max(result[0][i - 2], result[0][i - 1]) + b[i])
#
#     print(max(result[0][len(a) - 1], result[1][len(a) - 1]))


# no error
for _ in range(int(input())):
    input_li = [[], []]
    n = int(input())
    for i in range(len(input_li)):
        for j in map(int, input().split()):
            input_li[i].append(j)

    input_li[0][1] += input_li[1][0]
    input_li[1][1] += input_li[0][0]

    for i in range(2, n):
        input_li[0][i] += max(input_li[1][i - 2], input_li[1][i - 1])
        input_li[1][i] += max(input_li[0][i - 2], input_li[0][i - 1])

    print(max(input_li[0][n - 1], input_li[1][n - 1]))


