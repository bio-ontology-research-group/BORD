from simpletransformers.ner import NERModel
from scipy.special import softmax
import pandas as pd
import numpy as np
import nltk
import logging
from sklearn.model_selection import train_test_split
import csv
import sys
import sklearn
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn.metrics import f1_score
import re
import numpy as np
from sklearn.metrics import accuracy_score
#Downlod NLTK requirements
nltk.download('punkt')
logging.basicConfig(level=logging.INFO)
transformers_logger = logging.getLogger("transformers")
transformers_logger.setLevel(logging.WARNING)

import torch

print( torch.version.cuda)
print (torch.backends.cudnn.enabled)
cuda_available = torch.cuda.is_available()
print ("Cuda available:")
print ( str(cuda_available))

columns = ['pmid', 'sentence_id', 'words','labels']
columns_eval=['sentence_id', 'words','labels']
train_df = pd.DataFrame(columns=columns)
eval_df = pd.DataFrame(columns=columns_eval)

custom_labels=custom_labels = list(train_df['labels'].unique())
print('unique:',custom_labels)


sent_id=1

train_data={}
train_data["pmid"]=[]
train_data["sentence_id"]=[]
train_data["words"]=[]
train_data["labels"]=[]

eval_data={}
#eval_data["pmid"]=[]
eval_data["sentence_id"]=[]
eval_data["words"]=[]
eval_data["labels"]=[]

pmid=""  
with open(sys.argv[1],'r') as f:
   for line in f:     
     if "PMID=" in line:
        pmid=line.strip().replace('PMID=','')     
     if ((line!="\n") and ("PMID=" not in line)):
       line=line.strip()
       res=re.split('\t',line)
       if len(res)==2:
         words=res[0]
         if res[1] =="-":
           res[1]="O"
         if pmid=="":
           pmid="0"
         labels=res[1]       
         train_data["pmid"].append(pmid)
         train_data["sentence_id"].append(sent_id)
         train_data["words"].append(words)
         train_data["labels"].append(labels)

     if (line=="\n"):
       sent_id=sent_id+1

train_df = pd.DataFrame.from_dict(train_data)
print(train_df['labels'])
#----------------------------------------------------------------------


#Drop column pmid
train_df.drop('pmid', axis='columns', inplace=True)

sent_id=1
with open(sys.argv[2],'r') as f:
   for line in f:
     if (line!="\n"):
       line=line.strip()
       res=re.split('\t',line)
       if len(res)==2:
         words=res[0]
         if res[1] =="-":
           res[1]="O"
         labels=res[1]
         eval_data["sentence_id"].append(sent_id)
         eval_data["words"].append(words)
         eval_data["labels"].append(labels)
     else:
       sent_id=sent_id+1
eval_df = pd.DataFrame.from_dict(eval_data)

outdir="./model"
model_args={'max_seq_length': 256,
'reprocess_input_data': True,
'overwrite_output_dir': True,
'num_train_epochs': 10,
'learning_rate': 1e-5,
'output_dir':outdir,
'save_eval_checkpoints': False,
'save_model_every_epoch': True,
'train_batch_size': 32,
'eval_batch_size': 32,
'fp16': True,
'save_steps': 10000,
'evaluate_during_training': False,
'process_count': 6,
'evaluate_during_training': False,
'use_early_stopping': True,
"early_stopping_metric_minimize": False,
'evaluate_during_training_verbose': True,
'evaluate_during_training_steps': 1000,
'early_stopping_patience': 5,
'early_stopping_delta': 0,
'early_stopping_metric': "eval_loss",
'early_stopping_metric_minimize': False,
'reprocess_input_data': True
}

custom_labels=['I','O','B']
##model = NERModel("bert", "bert-base-cased", args={"overwrite_output_dir": True, "reprocess_input_data": True}, use_cuda=cuda_available)
model = NERModel("bert", "dmis-lab/biobert-base-cased-v1.1", args=model_args, labels=custom_labels, use_cuda=cuda_available)


#Train the model
model.train_model(train_df, eval_df=eval_df)
#Performance on TEST
print ("PERFORMACE on DEVELOPMENT:")
result, model_outputs, predictions = model.eval_model(eval_df)
print (result)
# Evaluate the model
print ("PERFORMACE on TRAIN:")
result, model_outputs,predictions = model.eval_model(train_df)
print(result)


