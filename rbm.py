import math, pickle, nltk
from tqdm import tqdm
from copy import deepcopy
from scipy import spatial
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.corpus import stopwords

stop_words={x:True for x in stopwords.words('english')}
stop_words["'"]=True
stop_words[","]=True
stop_words['-']=True
stop_words['(']=True
stop_words[')']=True
stop_words['"']=True
del(stop_words['as'])
letters=[x for x in stop_words if len(x)<2]
for l in letters:
    del(stop_words[l])

lemmatizer = WordNetLemmatizer()
wdic=pickle.load(open('ifiles/words_dic.pkl','rb'))
tdic=pickle.load(open('ifiles/tokens_dic.pkl','rb'))

def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R') or treebank_tag=='IN':
        return wordnet.ADV
    else:
        return wordnet.NOUN


def rbm(set1,set2,threshold=0.3):
	#threshold=0.3 #Threshold for allowed difference in edit distance, the lower the stricter, you can set this for yourself
	matching_score=0
	diff_score=0
	set1=[x for x in set1 if x not in stop_words]
	set2=[x for x in set2 if x not in stop_words]
	original_size=len(set1)
	original_size2=len(set2)
	if original_size==0 or original_size2==9:
		return 0,0,1,1,[]
	rem_words=[]
	for token1 in set1:
		best_match=""
		best_score=math.inf
		for token2 in set2:
			score=edit_distance(token1,token2)
			if score<threshold and score<best_score:
				best_score=score
				best_match=token2
		if best_score<math.inf:
			set2.remove(best_match)
			matching_score+=1
			diff_score+=best_score
		else:
			rem_words.append(token1)
	return matching_score, diff_score, original_size, original_size2, rem_words
			

def edit_distance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1
    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]/len(s2)

def candidates_dic(mention):
	ranks={}
	candidates=[]
	nmention=mention.lower().split(' ')
	try:
		token_pos=nltk.pos_tag(nmention)
		lemmas=[lemmatizer.lemmatize(token[0], get_wordnet_pos(token[1])) for token in token_pos]
	except:
		print('Could not lemmatize: ',repr(mention), nmention)
		lemmas=[]

	for w in nmention+lemmas:
		if w not in wdic:
			continue
		for gclass in wdic[w]:
			if gclass not in ranks:
				ranks[gclass]={}
			for index in wdic[w][gclass]:
				if index not in ranks[gclass]:
					ranks[gclass][index]=0
				ranks[gclass][index]+=1
	for gclass in ranks:
		maxi=0
		maxv=-10
		for index in ranks[gclass]:
			if ranks[gclass][index]>maxv:
				maxi=index
				maxv=ranks[gclass][index]
		candidates.append([gclass,tdic[gclass][maxi],maxi])
	return candidates


if __name__=='__main__':
	lemmatizer = WordNetLemmatizer()
