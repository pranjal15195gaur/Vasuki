from random import *
import sys
n = int(sys.argv[1])

W = 1000000000
t = randrange(W, 2*W)
print(f"{t}")
for i in range(n):
    print(f"{randrange(W//10, W//2)}")
