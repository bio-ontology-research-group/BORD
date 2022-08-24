#!/bin/bash
#source /ibex/scratch/kafkass/semisup_disease/hface/bin/activate

##nltk=3.5
##spacy=3.0.1
#1 is the input original putator file
#2 is the output file
python tokenize.text.py $1

###step1:
###srun --time=00:30:00 --mem=90gb --gres=gpu:v100 --resv-ports=1 --pty /bin/bash -l
###step2:
###conda activate /ibex/scratch/kafkass/NER/conda-environment-examples/env

##deactivate


python predict_NER_iob.py $1.tok >$1.tmp
python replace.py $1.tmp

##source /ibex/scratch/kafkass/semisup_disease/hface/bin/activate

python postprocess4Abbr.py $1.tmp >output/NER_raw_predictions.iob
rm $1.tok
rm $1.tmp
###abbrlist.txt
less abbrlist.txt | sort | uniq >tmp.txt
mv tmp.txt output/abbrlist.txt
python normalize_ontology-based.py output/NER_raw_predictions.iob output/abbrlist.txt $1 output/$2 
