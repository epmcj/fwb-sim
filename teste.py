import time

startTime = time.time()
for k in range(2000):
    a = set()
    for j in range(3):
        for i in range(2000):
            a.add(i)
    b = list(a)
endTime = time.time()
print(" set time: {}".format(endTime - startTime))

startTime = time.time()
for k in range(2000):
    a = []
    for j in range(3):
        for i in range(2000):
            a.append(i)
    c = list(set(a))
endTime = time.time()
print("list time: {}".format(endTime - startTime))

print("b len = {}, c len = {}".format(len(b), len(c)))