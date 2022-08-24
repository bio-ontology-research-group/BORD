from simpletransformers.ner import NERModel
from scipy.special import softmax
import torch
import re
import numpy as np
import pandas as pd
import sys

cuda_available = torch.cuda.is_available()

columns = ['sentence_id', 'words','labels']
test_df = pd.DataFrame(columns=columns)

model= NERModel('bert', './model/')

sent_id=1
sent=""
sentences=[]

string=sys.argv[1]

with open(string,'r') as f:
   for line in f:
     if (line!="\n"):
       line=line.strip()
       words=line
       test_df = test_df.append({'sentence_id': sent_id, 'words': words}, ignore_index=True)
       sent=sent + words + " "
     else:
       sent_id=sent_id+1
       sent=sent.rstrip()
       sentences.append(sent)
       sent=""
#Getting the last sentence from the file
sent=sent.rstrip()
sentences.append(sent)

predictions, raw_outputs = model.predict(sentences, split_on_space=True)

for n, (preds, outs) in enumerate(zip(predictions, raw_outputs)):
    #print("\n")
    for pred, out in zip(preds, outs):
        key = list(pred.keys())[0]
        new_out = out[key]
        preds = list(softmax(np.mean(new_out, axis=0)))
        #print(key, pred[key], preds[np.argmax(preds)], preds)
        print (key +"\t"+pred[key])
    print ("\n")    
