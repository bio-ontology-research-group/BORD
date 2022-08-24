#nltk=3.5
#spacy=3.0.1

How to run BORD on local GPU?

first create a virtual environment in your working directory

pip3 install -r requirements.txt
git clone https://github.com/NVIDIA/apex
cd apex
pip install -v --disable-pip-version-check --no-cache-dir ./

python3 -m spacy download en_core_web_sm
----------------------------------------------


How to run predict.sh script on IBEX ?

step1:
srun --time=00:30:00 --mem=90gb --gres=gpu:v100 --resv-ports=1 --pty /bin/bash -l

step2:
conda activate /ibex/scratch/kafkass/NER/conda-environment-examples/env

inputfile must be in PubTator format.
step 3: 
./predict.sh inputfile outputfile


how to run train.sh script on IBEX?
step1:
srun --time=00:30:00 --mem=90gb --gres=gpu:v100 --resv-ports=1 --pty /bin/bash -l

step2:
conda activate /ibex/scratch/kafkass/NER/conda-environment-examples/env

inputfile and devfile must be in the IOB format

./train.sh inputfile devfile outputfile


how to lexically annotate an input text? (input data preparation)

./lexical_annot.sh dicfile inputfile outputfile
