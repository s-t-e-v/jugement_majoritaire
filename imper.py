from turtle import end_fill


def fibonacci(n):

    if n == 1:
        return 0
    elif n == 2:
        return 1
    else:
        f0 = 0
        f1 = 1

        for i in range(n-2):
            f = f0 + f1
            f0 = f1
            f1 = f

        return f

for f in range(12):
    print(fibonacci(f+1), end=" ")
