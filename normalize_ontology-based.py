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
global clf, exact_dic, tmr, cmr
lemmatizer = WordNetLemmatizer()

#Please choose your thresholds for prediction here
#token_matching_ratio=0.8
#candidate_matching_ratio=0.8
mmr=0.7
cmr=0.8

exact_dic=pickle.load(open('ifiles/exact_dic.pkl','rb'))
children=pickle.load(open('ifiles/all_children.pkl','rb'))


def prediction_routine(p):
	if p[0].isupper() or len(p[0])<2:
		return []
	p[0]=re.sub(' +',' ',p[0].lower().replace("'s","").translate(str.maketrans(string.punctuation, ' '*len(string.punctuation)))).strip()
	global clf, exact_dic, mmr, cmr
	ppairs = []
	predicted=[]
	candidates=candidates_dic(p[0])
	token_pos=nltk.pos_tag(p[0].lower().split(' '))
	lemmas=' '.join([lemmatizer.lemmatize(token[0], get_wordnet_pos(token[1])) for token in token_pos])
	if p[0].lower() in exact_dic:
		for c in exact_dic[p[0].lower()]:
			predicted.append(c)
	elif lemmas in exact_dic:
		for c in exact_dic[lemmas]:
			predicted.append(c)
	else:
		scores, guides, pool=[], [], []
		for cand in candidates:
			ms, ds, os, os2, rem_words = rbm(deepcopy(p[0].split()),deepcopy(cand[1]))
			if os2<1 or os<1:
				continue
			if ms/os>mmr and ms/os2>cmr:
				pool.append([cand[0],ms/os,ms/os2])
			elif ms/os2 > 0.99 and ms/os<mmr and (cand[0] not in children or len(children[cand[0]])>1) :
				guides.append([cand[0], ' '.join(rem_words),ms,os,os2])
				
		if len(guides)>0 and len(pool)<1:
			max_score, max_class=0, ''
			tpool=[]
			for g in guides:
				valid_classes=set(children[g[0]])
				for cand in candidates:
					if cand[0] in valid_classes:
						ms, _, os, os2, _ = rbm(deepcopy(g[1].split()),deepcopy(cand[1]))
						if os<1 or os2<1:
							continue
						if (ms/os)<mmr or (ms/os2)<cmr:
							continue
						score=(ms/os)+(ms/os2)
						if score > max_score or score==max_score:
							pool.append([cand[0], ms/os,ms/os2])
							max_score=score
							max_class=cand[0]
		if len(pool)>0:
			predicted=[j[0] for j in pool]
		else:
			predicted=[]
			for g in guides:
				if g[-1]/g[-2]>0.5:
					predicted.append(g[0])
		
	if len(predicted)>0:
		newp=p
		newp[1]=predicted
		ppairs.append(newp)
	return ppairs
	

def predict_parallel( of, pred_f, abb_f, pub_f):
	pairs, abs_dic = get_pred(pred_f, abb_f, pub_f)
	everything, ppairs=[], []
	with Pool() as p:
		everything=p.map(prediction_routine, pairs)
	if len(everything)>0:
		ppairs=everything[0]
		for i in everything[1:]:
			ppairs+=i
	write_pubtator(abs_dic, ppairs, of)
	
	
if __name__=="__main__":
	pred_f=sys.argv[1]#Prediction file
	abb_f=sys.argv[2] #Abbreviation file
	pub_f=sys.argv[3] #Original unannotated pubtator file
	of=sys.argv[4] #Output file
	lemmatizer = WordNetLemmatizer()
	predict_parallel(of,pred_f,abb_f,pub_f)
