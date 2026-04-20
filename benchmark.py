import numpy as np
import time

def original(img, data):
    for x, row in enumerate(img):
        for y, element in enumerate(row):
            if(element == 0):
                data[x][y] = int(0)
            else:
                data[x][y] = int(1)

def optimized(img, data):
    data[:] = np.where(img == 0, 0, 1)

# Generate a fake img of 28x28
img = np.random.randint(0, 256, size=(28, 28), dtype=np.uint8)
data_orig = np.zeros((28, 28), dtype=int)
data_opt = np.zeros((28, 28), dtype=int)

start = time.perf_counter()
for _ in range(10000):
    original(img, data_orig)
end_orig = time.perf_counter()

start_opt = time.perf_counter()
for _ in range(10000):
    optimized(img, data_opt)
end_opt = time.perf_counter()

print("Original time:", end_orig - start)
print("Optimized time:", end_opt - start_opt)
print("Are they equal:", np.array_equal(data_orig, data_opt))
