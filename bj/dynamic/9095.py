# me
def solution(n):
    li = [1, 2, 4]

    if n < len(li):
        return li[n - 1]

    while len(li) < n:
        li.append(li[-1] + li[-2] + li[-3])

    return li[-1]


# them
def solution(n):
    if n == 1:
        return 1
    if n == 2:
        return 2
    if n == 3:
        return 4

    return solution(n - 1) + solution(n - 2) + solution(n - 3)


aa = input()
for i in range(int(aa)):
    print(solution(int(input())))
