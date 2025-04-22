import random

inf = open("x.in", "w")
ouf = open("x.out", "w")

for i in range(100):
    x = 0
    for j in range(10, 50):
        s = random.choice("abcdefghijklmnopqrstuvwxyz")
        inf.write(f"{s}")
        x += s in "aeiou"
    inf.write("\n")
    ouf.write(f"{x}\n")

inf.close()
ouf.close()
