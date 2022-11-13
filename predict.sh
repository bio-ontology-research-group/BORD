#!/bin/bash
#1 is the input original putator file
#2 is the output file
python tokenize.text.py $1
python predict_NER_iob.py $1.tok >$1.tmp
python replace.py $1.tmp
python postprocess4Abbr.py $1.tmp >output/NER_raw_predictions.iob
rm $1.tok
rm $1.tmp
less abbrlist.txt | sort | uniq >tmp.txt
mv tmp.txt output/abbrlist.txt
python normalize_ontology-based.py output/NER_raw_predictions.iob output/abbrlist.txt $1 output/$2 
