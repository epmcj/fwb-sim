#N = 2^h - 1
n = 2048
f = open('topologyDegBalanced'+str(n)+"nodes", 'w')
L = range(0, n)

f.writelines("[(0,1), ")

i = 2
links = 0
for it in range(1,len(L)-1):
     if(links == n-2):
	break
     f.writelines("(" + str(it) + "," + str(i) + "),")
     if(links == n-4):
         f.writelines(" (" + str(it) + "," + str(i+1) + ")")
     else:
          f.writelines(" (" + str(it) + "," + str(i+1) + "), ")
     if(i == n or i == n-1):
     	break
     i = i + 2
     links = links + 2

f.writelines("]")
