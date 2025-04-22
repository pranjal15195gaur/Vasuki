from random import *

import sys

N = int(sys.argv[1])
n = randrange(N, 5 * N)

for i in range(n):
    print(f"{randrange(N//2, 2*N)}")
