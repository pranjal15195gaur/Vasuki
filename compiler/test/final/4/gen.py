import random

n = random.randrange(1000000, 2000000)
m = random.randrange(1500000, 3000000)

f = open("large.in", "w")
f.write(f"{n} {m}\n")
for i in range(n+m):
    f.write(f"{random.randrange(1, 250000)}\n")
