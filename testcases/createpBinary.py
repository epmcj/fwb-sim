#Arvore bin completa cheia
#N = 2^h - 1
n = 8
f = open('topologyBalanced'+str(n)+"nodes", 'w')
L = range(0, n)

f.writelines("[")

i = 1
links = 0
for it in range(0,len(L)):
     if(links == n-1):
	break
     f.writelines("(" + str(it) + "," + str(i) + "),")
     if(links == n-3):
         f.writelines(" (" + str(it) + "," + str(i+1) + ")")
     else:
          f.writelines(" (" + str(it) + "," + str(i+1) + "), ")
     if(i == n or i == n-1):
     	break
     i = i + 2
     links = links + 2

f.writelines("]")
