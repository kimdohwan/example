# example
n = 6
input_li = [6, 10, 13, 9, 8, 1, ]

# submit
# n = int(input())
# input_li = [int(input()) for _ in range(n)]


def s(li):
    if len(li) < 3:
        return sum(li)

    max_li = [
        li[0],
        li[0] + li[1],
        max(
            li[0] + li[1],
            li[0] + li[2],
            li[1] + li[2],
        )
    ]

    for i in range(3, len(li)):
        max_li.append(
            max(
                li[i] + max_li[i - 2],
                li[i] + li[i - 1] + max_li[i - 3],
                max_li[i - 1],
            )
        )

    return max_li[-1]


print(s(input_li))
