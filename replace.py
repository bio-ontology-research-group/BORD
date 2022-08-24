import sys
f=open(sys.argv[1])
data=f.read()
data=data.replace('\n\n','\n')
f.close()
f=open(sys.argv[1],'w+')
f.write(data)
f.close()
