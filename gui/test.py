def test(a):
    return a()

def go(x):
    return x + 1

ls = []

for i in range(10):
    ls.append(lambda: go(i))

for i in range(10):
    print(test(ls[i]))