import json, math, pickle, sys
dic=json.load(open(sys.argv[1])) #direct children json file
maxi=0
full_dic={}
dic['owl:Nothing']=[]
from tqdm import tqdm 

def get_all_children(parent):
	children=list(set(dic[parent]))
	for c in children:
		children += get_all_children(c)
	return set(children)
		
			

for i, term in tqdm(enumerate(dic)):
	aterm=term[term.rfind('/')+1:].replace('_',':')
	children=get_all_children(term)
	full_dic[aterm]=[term[term.rfind('/')+1:].replace('_',':') for term in children]


f=open('ifiles/all_children.pkl','wb')
f.write(pickle.dumps(full_dic))
f.close()
