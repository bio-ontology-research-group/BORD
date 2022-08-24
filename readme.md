# BORD
***
## Preparation
1. First create a virtual environment in your working directory called venv
2. Activate the virtual env
3. Install requirements with
```
pip3 install -r requirements.txt
```
4. Install apex as follows:
```
git clone https://github.com/NVIDIA/apex
cd apex
pip install -v --disable-pip-version-check --no-cache-dir ./
```
5. Download the spacy english model
```
python3 -m spacy download en_core_web_sm
```

## Lexical annotation for distant supervision
1. To create the training dataset by lexically annotating a corpus provided in pubtator format, run lexical_annot.sh 
 
 it requires the following arguments in order:
 - The ontology in obo format
 - The corpus that you want to annotate in pubtator format to create the weakly labeled dataset for training
 - The output file name

Example:
```
./lexical_annot.sh ont.obo sample.input.txt weak_output.txt
```
2. Run the same command on a different corpus to create the development set
3. You will need to extract children and parents to use the ontology-based normalization, please refer to the following script for reference:
https://github.com/smalghamdi/groovyScripts/blob/master/direct_parent_direct_child.groovy
the output should be two files in json format
4. For ontology-based normalization you will also need to run the following script:
```
get_IC_allchildren.py direct_children.json
```
where the input is the direct_children json file

## Training
1. Run the train.sh script

it requires the output from the previous step which can be run twice: The first one to create training set and another one to create the development set

For the sake of the example we use the same file twice:
```
./train.sh weak_output.txt weak_output.txt 
```
Alternatively, you can use our sample files as follows:
```
./train.sh ../sample.input.4train.iob ../sample.dev.iob
```

## Prediction
1. Run the predict.sh script
where the input is as follows in order:
- The pubtator file for which you want to predict
- The output file which will be stored under the output directory

To run the ontology-based normalization:

Replace the script name 'normalize.py' in the last line in predict.sh to 'normalize_ontology-based.py' 

Example: 
```
./predict.sh sample.input.txt final_output.txt
```

***
## Trained models
To use our trained model, download it from:
AND unzip it in the model/ directory

AND download the intermediate files from:
AND unzip it in the ifiles/ directory

