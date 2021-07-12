# def solution(n):
#     cnt = 0
#     while n > 0:
#         if not n % 5:
#             return cnt + int(n // 5)
#         else:
#             n -= 3
#             cnt += 1
#     if n == 0:
#         return cnt
#     else:
#         return -1
#
# while True:
#     print(solution(int(input())))


# while True:
#     n = int(input())
#     print(-(n in [4, 7]) or n - 2 * n // 5 * 2)


while True:
    N = int(input())
    s = int("02413"[N % 5])
    T = N - 3 * s
    print(-1 if T < 0 else T // 5 + s)
