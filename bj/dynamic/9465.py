for _ in range(int(input())):
    n = int(input())

    """case 1 """
    # input_li = [[0]*100000,[0]*100000]

    # for idx, var in enumerate(map(int,input().split())):
    #    input_li[0][idx] = var
    # for idx, var in enumerate(map(int,input().split())):
    #    input_li[1][idx] = var
    """case 1 end """

    """case 2 """
    input_li = []
    for _ in range(2):
        input_li.append([int(x) for x in input().split()])

    if n == 1:  # n == 1 인 경우 생각치 못해서 매우 고생
        print(max(input_li[0][0], input_li[1][0]))
        continue
    """case 2 end """

    a = input_li[0]
    b = input_li[1]

    result = [
        [a[0], b[0] + a[1]],
        [b[0], a[0] + b[1]]
    ]

    for i in range(2, len(a)):
        result[0].append(max(result[1][i - 2], result[1][i - 1]) + a[i])
        result[1].append(max(result[0][i - 2], result[0][i - 1]) + b[i])

    print(max(result[0][len(a) - 1], result[1][len(a) - 1]))
