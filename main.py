import datasets
import time


total = 0
start = time.time()

for k, v in datasets.loader.load_data().items():
    total += len(v)
    print(k, len(v))
    print()

print(total)

print(time.time() - start)


