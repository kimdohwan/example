def solution(n):
    A = [1, 2]
    for i in range(n - 2):
        A.append(A[-1] + A[-2])
    return A[n - 1] % 10007


# RuntimeError
# def solution(n):
#     if n == 1:
#         return 1
#     elif n == 2:
#         return 2
#
#     return solution(n - 1) + solution(n - 2)


while True:
    print(solution(int(input())))
