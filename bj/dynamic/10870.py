def solution(n):
    if n in [0, 1]:
        return n
    return solution(n - 1) + solution(n - 2)


while True:
    print((solution(int(input()))))
