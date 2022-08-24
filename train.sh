#!/bin/bash
#First run lexical_annot script then provide its outputs here
#1 IOB input
#2 IOB dev 
mkdir model
python train_cuda_biobert.py output/$1 output/$2 >./model/eval_on_dev.txt
