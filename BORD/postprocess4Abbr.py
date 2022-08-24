import sys
import re
#import json
#from nltk.tokenize import sent_tokenize
import spacy
from spacy.lang.en import English
from spacy.training import offsets_to_biluo_tags
from spacy.matcher import PhraseMatcher
from scispacy.abbreviation import AbbreviationDetector

nlp = spacy.load('en_core_web_sm')

nlp.add_pipe("abbreviation_detector")

#READ FROM FILE

def read_file(infile):
 sent=""
 sentences=[]
 pmids=[]
 with open(infile,'r') as f:
   for line in f:
     if (line!="\n") and "PMID" not in line:
       line=line.strip()
       res=line.split('\t')
       if len(res)==2:
         sent=sent+str(res[0])+" "
    # else:
     if "PMID" in line:
          pmids.append(line)
          sent=sent.rstrip()
          if (sent!=""):
            sentences.append(sent)
            sent=""
#Getting the last sentence from the file
 sent=sent.rstrip()
 sentences.append(sent)
 return sentences, pmids

#-----------------------------------------------------------------------------

fw = open("abbrlist.txt", "w")
hpo_dic={}
tt=[]
infile="./ifiles/all.dic"
with open (infile, 'r') as f:
  for line in f:
    hid,label=line.strip().split("\t")
    hpo_dic[label]=1
    if "," in label:
     tt=label.split(",")
     hpo_dic[tt[0]]=1

#infile="sample.txt"
infile=sys.argv[1]

biobert_sentences, pmids_list=read_file(infile)

myabbrList={}


for s in range (len(biobert_sentences)):
    
    tmpList=[]
    mysent=biobert_sentences[s]
    mypmid=pmids_list[s]
    tmpList=mypmid.split("\t")
    mypmid=tmpList[0]
    tmpList=[]

    if (len(mysent)>0):
      #print (mysent)
      doc=nlp(mysent)
      for abrv in doc._.abbreviations:
        lf=str(abrv._.long_form)
        lf=lf.replace(" '","'").replace(" - ","-").lower()
        if " . " in lf:
          tmpList=lf.split(" . ")
          lf=tmpList[1]
          tmpList=[]

        #print (lf)
        test=lf.endswith("nemia")
        if (lf in hpo_dic or "tumour" in lf or "tumor" in lf or "symptom" in lf or "disease" in lf or "disorder" in lf or "syndrome" in lf or "abnormality" in lf or "abnormalities" in lf or test or "cancer" in lf) and "virus" not in lf:
           tmpList.append(str(abrv))
           fw.write(mypmid+"\t"+str(abrv)+"\t"+lf+"\n")
           #print(f"{abrv} \t ({abrv.start}, {abrv.end}) {abrv._.long_form}")
      myabbrList[mypmid]=list(set(tmpList))

#REWRITE
#infile="sample.txt"
i=-1
tags=[]
tokens=[]

with open(infile,'r') as f:
   for line in f:
     if "PMID" in line:
       mypmid=line
       tmpList=mypmid.split("\t")
       mypmid=tmpList[0]
       addabbrList=myabbrList[mypmid]
       print(line.strip())
     if (line!="\n") and "PMID" not in line:
       line=line.strip()
       i=i+1
       res=re.split('\t',line) 
       if len(res)<2:
           print (line)
           sys.exit(0)

       tags.append(res[1])
       res[0]=res[0].replace(";","").replace(",","")
       tokens.append(res[0])
       if len(tags)>2 and tags[i-1]=="O" and (tags[i-2]=="B" or tags[i-2]=="I") and tokens[i-1]=="(" and len(tokens[i])>1 and tokens[i].isupper():
           #addabbrList.append(res[0])

           ttmp=[]
           ttmp2=[]
           for t in range (i-1,0,-1):
             if tags[t]=="I":
               ttmp.append(tokens[t])
             if tags[t]=="B":
               ttmp.append(tokens[t])
               break
           ttmp2=ttmp[::-1]
           lf=" ".join(ttmp2)
           firstletter=lf[0].upper()
           if (lf in hpo_dic or "tumour" in lf or "tumor" in lf or "symptom" in lf or "disease" in lf or "disorder" in lf or "syndrome" in lf or "abnormality" in lf or "abnormalities" in lf or test) and "virus" not in lf and (firstletter in res[0]):
             fw.write(mypmid +"\t"+res[0] +"\t"+" ".join(ttmp2)+"\n")
             addabbrList.append(res[0])
       
       if res[0] in addabbrList:
         print (res[0]+"\tB")
       else:
         print (line)
     if (line=="\n"):
       print (line.strip())

