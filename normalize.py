from tqdm import tqdm
import pickle, nltk, string, re, sys
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
from r_w import get_pred, write_pubtator
from rbm import rbm, candidates_dic, get_wordnet_pos
from copy import deepcopy
from multiprocessing import *
from nltk.stem import WordNetLemmatizer

global exact_dic, tmr, cmr
punct={}
for p in string.punctuation:
    punct[p]=' '

lemmatizer = WordNetLemmatizer()

#Please choose your thresholds for prediction here
tmr=0.8 #Token Matching Ratio
cmr=0.8 #Candidate Matching Ratio
exact_dic=pickle.load(open('ifiles/exact_dic.pkl','rb'))

def prediction_routine(p):
	if p[0].isupper() or len(p[0])<2:
		return []
	p[0]=re.sub(' +',' ',p[0].lower().replace("'s","").translate(str.maketrans(string.punctuation, ' '*len(string.punctuation)))).strip()
	global clf, exact_dic, tmr, cmr
	ppairs=[]
	predicted=[]
	candidates=candidates_dic(p[0])
	token_pos=nltk.pos_tag(p[0].split(' '))
	lemmas=' '.join([lemmatizer.lemmatize(token[0], get_wordnet_pos(token[1])) for token in token_pos])
	if p[0] in exact_dic:
		temp=[]
		for c in exact_dic[p[0].lower()]:
			temp.append(c)
		if len(temp)>0:
			predicted.append('||'.join(temp))
	elif lemmas in exact_dic:
		for c in exact_dic[lemmas]:
			predicted.append(c)
	else:
		for cand in candidates:
			ms, ds, os, os2,_ = rbm(deepcopy(p[0].strip().split(' ')),deepcopy(cand[1]))
			if os2<1:
				continue
			if ms/os>tmr and ms/os2>cmr:
				predicted.append(cand[0])
	if len(predicted)>0:
		newp=p
		newp[1]=predicted
		ppairs.append(newp)
	#else:
	#	newp=p
	#	newp[1]=['FP']
	#	ppairs.append(newp)
	return ppairs 


def predict_parallel( of, pred_f, abb_f, pub_f):
	pairs, abs_dic = get_pred(pred_f, abb_f, pub_f)
	everything,ppairs=[],[]
	with Pool() as p:
		everything=p.map(prediction_routine, pairs)
	if len(everything)>0:
		ppairs=everything[0]
		for i in everything[1:]:
			ppairs+=i
	write_pubtator(abs_dic, ppairs, of)
	
if __name__=="__main__":
	pred_f=sys.argv[1] #Prediction file
	abb_f=sys.argv[2] #Abbreviation file
	pub_f=sys.argv[3] #Original pubtator file
	of=sys.argv[4] #Output file
	lemmatizer = WordNetLemmatizer()
	predict_parallel(of,pred_f,abb_f,pub_f)
