import sys
#import nltk
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
import multiprocessing
from multiprocessing import Pool

data={}
toklist=[]
sentlist=[]


def readfile(fname):
  with open(fname,'r') as f:
   for line in f:
     line = line.rstrip("\n")
     if "|t|" in line:
       fin="" 
       pmid1,text=line.split('|t|')
       fin=text
     if "|a|" in line:
       pmid2,text=line.split('|a|')
       if pmid1==pmid2:
         fin=fin+"\n"+text
     data[pmid1]=fin
     

def tokenize_text(cn,pmid):
   res="PMID:"+pmid
   #print (res + "  from function")
   cnt=0    
   sentlist=sent_tokenize(data[pmid])
   for s in sentlist:
     #if (cnt>0):
     res=res+"\n"
     toklist=word_tokenize(s)
     cnt=cnt+1
     for t in toklist:
       res=res+t+"\n"
   return res


lst=[]
result=[]
readfile(sys.argv[1])
s=1
for key in data:
#  print (key+"\t"+data[key])
   lst.append((s,key))
   s=s+1
 #result=tokenize_text(key)      

size=multiprocessing.cpu_count()-1
#print ("Nof cpus="+str(size))
process_pool = multiprocessing.Pool(size)

result = process_pool.starmap(tokenize_text,lst)

ofile = open(sys.argv[1]+".tok", "w") 
for i in result:
  ofile.write(i)
ofile.close()
