#!/bin/bash
##source /ibex/scratch/kafkass/semisup_disease/hface/bin/activate
#obo file,pubtoator, output
python get_ontology_dictionaries.py $1
python multi_lex_annot_conv_iob.py ./ifiles/all.dic $2 output/$3
#python replace.py $3
