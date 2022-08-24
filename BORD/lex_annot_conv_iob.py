import sys
import re
import json
import nltk
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
import spacy
from spacy.tokens import Doc
from spacy.lang.en import English 
from spacy.training import offsets_to_biluo_tags
from spacy.matcher import PhraseMatcher
from scispacy.abbreviation import AbbreviationDetector

nlp = spacy.load('en_core_web_sm')
class NltkTokenizer:
    def __init__(self, vocab):
        self.vocab = vocab

    def __call__(self, text):
        words = nltk.word_tokenize(text)
        return Doc(self.vocab, words=words)


nlp.add_pipe("abbreviation_detector")


mysent=[] #empty for each abstract
myAbbr=[]
disease_list={}
abst_list={}

disfile=sys.argv[1]
with open(disfile,'r') as f:
   for line in f:
     line = line.rstrip("\n")
     label,dis_id=line.split('\t')
     disease_list[label]=dis_id

testfile=sys.argv[2]
#9949209|t|Genetic mapping of the copper toxicosis locus in Bedlington terriers to dog chromosome 10, in a region syntenic to human chromosome region 2p13-p16.
with open(testfile,'r') as f:
   for line in f:
     line = line.rstrip("\n")
     if "|t|" in line:
       pmid,text=line.split('|t|')
       abstract=text
     if "|a|" in line:
       pmid,text=line.split('|a|')
       abstract=abstract + " " + text
     abst_list[pmid]=text
for abs_item in abst_list:
 myAbbr=[]
 print("PMID="+abs_item+"\tO")
 doc=nlp(abst_list[abs_item])
 for abrv in doc._.abbreviations:
   myAbbr.append(str(abrv).lower())
 all_sent = sent_tokenize(abstract)
 for sent in all_sent:
   black_list=set() #empty for each sentence
   found_start=[] #empty for each sentence
   found_end=[] #empty for each sentence
   entities=[] #empty for each sentence
   found_list=[]
   found_hp=[]
   mysent=[]
   final=[]
   for disease in disease_list:
      regex = re.compile(r'\b(' + disease + r')\b')
      res = [(ele.start(), ele.end()) for ele in regex.finditer(sent.lower())]
      if len(res)>0:
        for r in res:
             #annot_list.append("ANNOT\t"+str(cnt)+"\t"+key +"\t"+str(r[0]) + "\t" +str(r[1]) +"\t"+ disease +"\t" +disease_list[disease])      
           if disease not in myAbbr:
             found_start.append(r[0])
             found_end.append(r[1])
             found_list.append(disease)
             found_hp.append(disease_list[disease])
   for i in range(0,len(found_start)):
     for j in range (0, len(found_start)):
       if (i!=j):
           if((found_start[i] <= found_start[j]) and (found_end[i]>=found_end[j])):
                black_list.add(str(found_start[j])+"__"+str(found_end[j]))
           if ((found_start[i] <= found_end[j]) and (found_end[j]<=found_end[i])):
                black_list.add(str(found_start[j])+"__"+str(found_end[j]))
           if ((found_start[i] <= found_end[j]) and (found_start[j]<=found_end[i])):
                black_list.add(str(found_start[j])+"__"+str(found_end[j]))
  
   for i in range(0,len(found_start)):  
     ind=str(found_start[i])+"__"+str(found_end[i])
     if ind not in black_list:
       #print(found_list[i]+"\t"+ str(found_start[i]) + "\t"+ str(found_end[i])) 
       entities.append((found_start[i],found_end[i],found_hp[i]))
     #else:
       #print (found_list[i]+"\t"+ str(found_start[i]) + "\t"+ str(found_end[i]) +"\tblack_list")
   mysent.append(sent)
   final.append({"entities":list(entities)})
   TRAIN_DATA=list(zip(mysent,final))

  # print (TRAIN_DATA)
   docs = []
   tokens=[]
   for text, annot in TRAIN_DATA:
      nlp.tokenizer = NltkTokenizer(nlp.vocab)
      doc = nlp(text)
      for token in doc:
        tokens.append(token)

      tags = offsets_to_biluo_tags(doc, annot['entities'])
##tags = offsets_to_biluo_tags(doc, entities)
## then convert L->I and U->B to have IOB tags for the tokens in the doc
     
      for i in range (0,len(tokens)):
        tags[i]=tags[i].replace("L", "I")
        tags[i]=tags[i].replace("U","B")
        tags[i]=tags[i].replace("-DISEASE","")
        print (str(tokens[i])+"\t"+str(tags[i]))
   print ("\n")
